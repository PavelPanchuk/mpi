import subprocess
import numpy as np

def run_mpi(num_procs, num_intervals, num_attempts):
    """
    Запускает программу с MPI, используя заданное количество процессов, интервалов и попыток,
    возвращает среднее время выполнения.
    """
    times = []
    for attempt in range(num_attempts):
        result = subprocess.run(
            ["mpirun", "-np", str(num_procs), "./mypiout", str(num_intervals)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Извлекаем время выполнения из вывода программы
        output = result.stdout.splitlines()
        for line in output:
            if "wall clock time" in line:
                time = float(line.split("=")[1].strip())
                times.append(time)
                break
    
    if len(times) == 0:
        print(f"Ошибка: не удалось извлечь время выполнения для np={num_procs}, intervals={num_intervals}")
        return None
    return np.mean(times)

# Внешний цикл по количеству процессов
procs_list = [1, 2, 4, 10]
# Внутренний цикл по количеству интервалов
intervals_list = [10, 200, 100000]
# Глубокий цикл по количеству попыток
attempts_list = [1, 3, 8]

# Запускаем внешние циклы
for num_procs in procs_list:
    for num_intervals in intervals_list:
        for num_attempts in attempts_list:
            avg_time = run_mpi(num_procs, num_intervals, num_attempts)
            if avg_time is not None:
                print(f"Среднее время для np={num_procs}, интервалов={num_intervals}, попыток={num_attempts}: {avg_time:.6f} сек")
