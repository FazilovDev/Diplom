#include <iostream>
#include <math.h>
#include <time.h>
#include <sstream>
#include "pt4.h"
#include "omp.h"
using namespace std;

string get_string_from_data(const char* info, double number) {
    basic_ostringstream<char> out;
    out << info << fixed << number << endl;
    return out.str();
}

double FNoParallel(double x, int n) {
    double result = 0;
    for (long int i = 1; i <= n; ++i) {
        double sum = 0;
        for (long int j = 1; j <= i; ++j)
            sum += (j + sin(x + j)) / (2.0 * i * j - 1.0);
        result = result + 1 / sum;
    }
    return result;
}

double FParallel(double x, int n) {
    double result = 0;
    double sum = 0;
    long int i, j;
    clock_t start;
    clock_t end;
    omp_set_num_threads(4);
    start = clock();
    #pragma omp parallel private(i,j,start,end) firstprivate(sum) reduction (+: result)
    {
        int id_thread = omp_get_thread_num();
        clock_t begin_thread = clock();
        for (i = id_thread + 1; i <= n; i += 8) {
            sum = 0;
            for (j = 1; j <= i; ++j)
                sum += (j + sin(x + j)) / (2.0 * i * j - 1.0);
            result += 1 / sum;
        }
        for (i = 8 - id_thread; i <= n; i += 8) {
            sum = 0;
            for (j = 1; j <= i; ++j)
                sum += (j + sin(x + j)) / (2.0 * i * j - 1.0);
            result += 1 / sum;
        }
        clock_t time_th = clock() - begin_thread;
        Show(get_string_from_data("Thread time: ", (clock()- begin_thread)));
    }
    end = clock();

    clock_t time_thread = end - start;
    Show(get_string_from_data("Total multithreading time: ", time_thread));
    return result;
}


void Solve()
{
    Task("OMPBegin5");
    double x;
    int n;
    pt >> x >> n;

    clock_t start = clock();
    pt << FNoParallel(x, n);
    clock_t end = clock();
    clock_t difNoneParallel = end - start;

    Show(get_string_from_data("None-parallel time: ", difNoneParallel));
    Show(get_string_from_data("num_proc: ", omp_get_num_procs()));
    Show(get_string_from_data("num_threads: ", 4));

    pt >> x >> n;
    start = clock();
    pt << FParallel(x, n);
    end = clock();
    clock_t difParallel = end - start;
    Show(get_string_from_data("Total parallel time: ", difParallel));
    double res = difNoneParallel / difParallel;
    Show("Rate: ", res);
}
