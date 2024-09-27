#include "mpi.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>  // Для использования функции atoi
//mpirun.mpich -n 8 -f host-file-by-ip /home/user/workspace/Panchuk/Лаб_раб_1_Вычисление_pi/a.out 1000000000
double f(double);

double f(double a)
{
    return (4.0 / (1.0 + a * a));
}

int main(int argc, char *argv[])
{
    int n, myid, numprocs, i;
    double PI25DT = 3.141592653589793238462643;
    double mypi, pi, h, sum, x;
    double startwtime = 0.0, endwtime;
    int namelen;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    // Инициализация MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);
    MPI_Get_processor_name(processor_name, &namelen);

    if (argc != 2) {  // Проверяем, что передан аргумент с количеством интервалов
        if (myid == 0) {
            printf("Usage: %s <number_of_intervals>\n", argv[0]);
        }
        MPI_Finalize();
        return 1;
    }

    // Преобразуем аргумент командной строки в целое число
    n = atoi(argv[1]);

    if (n <= 0) {
        if (myid == 0) {
            printf("The number of intervals must be a positive integer.\n");
        }
        MPI_Finalize();
        return 1;
    }

    // Начало вычислений
    if (myid == 0) {
        startwtime = MPI_Wtime();
    }

    h = 1.0 / (double)n;
    sum = 0.0;
    for (i = myid + 1; i <= n; i += numprocs) {
        x = h * ((double)i - 0.5);
        sum += f(x);
    }
    mypi = h * sum;

    // Суммируем все результаты
    MPI_Reduce(&mypi, &pi, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (myid == 0) {
        //printf("pi is approximately %.16f, Error is %.16f\n",pi, fabs(pi - PI25DT));
        endwtime = MPI_Wtime();
        printf("wall clock time = %f\n", endwtime - startwtime);
        //printf("%f\n", endwtime - startwtime);
    }

    MPI_Finalize();
    return 0;
}
