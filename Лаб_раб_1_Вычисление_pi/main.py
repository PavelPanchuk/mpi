import subprocess
import numpy as np
import matplotlib.pyplot as plt

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
        
        output = result.stdout
        # Поиск строки с "wall clock time"
        found_time = False
        for line in output.splitlines():
            if "wall clock time" in line:
                try:
                    time = float(line.split("=")[1].strip())
                    times.append(time)
                    found_time = True
                    break
                except ValueError:
                    found_time = False
        
        if not found_time:
            print(f"Время выполнения не найдено для попытки {attempt + 1} (np={num_procs}, intervals={num_intervals})")

    if len(times) == 0:
        print(f"Ошибка: не удалось извлечь время выполнения для np={num_procs}, intervals={num_intervals}")
        return None
    
    return np.mean(times)

# Внешний цикл по количеству процессов
procs_list = [1, 2, 4, 8]
# Внутренний цикл по количеству интервалов
intervals_list = [1, 200, 1000, 10000]
# Глубокий цикл по количеству попыток
attempts_list = [1, 3, 5,10]

# Словарь для сохранения времени выполнения
results = {}

# Запускаем внешние циклы и сохраняем результаты
for num_intervals in intervals_list:
    results[num_intervals] = []
    for num_procs in procs_list:
        avg_time = run_mpi(num_procs, num_intervals, max(attempts_list))  # Используем максимальное количество попыток
        if avg_time is not None:
            results[num_intervals].append((num_procs, avg_time))

# Построение графиков
plt.figure(figsize=(10, 6))
for num_intervals, data in results.items():
    procs = [item[0] for item in data]  # Количество процессов
    times = [item[1] for item in data]  # Время выполнения
    plt.plot(procs, times, marker='o', label=f"Intervals = {num_intervals}")

plt.title("Зависимость времени выполнения от количества потоков")
plt.xlabel("Количество потоков")
plt.ylabel("Среднее время выполнения (секунды)")
plt.grid(True)
plt.legend()
plt.show()
plt.savefig('graph.png')
print("all")