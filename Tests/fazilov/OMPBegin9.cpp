#include <iostream>
#include <math.h>
#include <time.h>
#include <sstream>
#include "pt4.h"
#include "omp.h"
using namespace std;

int n;
double x, sum;

string get_string_from_data(const char* info, double number) {
    basic_ostringstream<char> out;
    out << info << fixed << number << endl;
    return out.str();
}

int optimalMiddle(int n) {
    return sqrt(n * (n + 1) / 2);
}

double sumReducer(int start, int end)
{
    double threadSum = 0;
    double tempSum = 0;
    for (int i = start; i <= end; i++)
    {
        tempSum = 0.0;
        for (int j = 1; j <= i; j++)
            tempSum += (j + log(1.0 + x + j)) / (2.0 * i * j - 1.0);
        threadSum += 1 / tempSum;
    }
    return threadSum;
}

void Solve()
{
	Task("OMPBegin9");
    pt >> x >> n;
    clock_t start = clock();
    pt << sumReducer(1, n);
    clock_t end = clock();
    clock_t difNoneParallel = end - start;
    Show(get_string_from_data("None-parallel time: ", difNoneParallel));
    Show(get_string_from_data("num_proc: ", omp_get_num_procs()));
    Show(get_string_from_data("num_threads: ", 4));

	pt >> x >> n;
    clock_t begin = clock();
	double threadSum = 0.0;
#pragma omp parallel sections reduction(+: threadSum)
	{
#pragma omp section 
		{
            clock_t startThread = clock();
			threadSum = sumReducer(1, n - optimalMiddle(n) - 1);
            clock_t endThread = clock();
            Show(get_string_from_data("Thread time ", endThread - startThread));
		}
#pragma omp section
		{
            clock_t startThread = clock();
            threadSum = sumReducer(n - optimalMiddle(n), n);
            clock_t endThread = clock();
            Show(get_string_from_data("Thread time ", endThread - startThread));
		}
	}
    end = clock();
    pt << threadSum;
    clock_t difParallel = end - start;
    Show(get_string_from_data("Total parallel time: ", difParallel));
    double res = difNoneParallel / difParallel;
    Show("Rate: ", res);
}