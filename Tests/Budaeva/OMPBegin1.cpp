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
			sum = sum + (j + pow((x + j), 1.0 / 3.0)) / (2.0 * i * j - 1.0);
		result = result + 1 / sum;
	}
	return result;
}

double FParallel(double x, int n) {
	double result = 0;
	double sum = 0;
	long int i, j;
	long int count = 0;
	clock_t start;
	clock_t end;
	start = clock();
#pragma omp parallel private(i,j,start,end) firstprivate(count,sum) reduction (+: result)

#pragma omp for
	for (i = 1; i <= n; ++i) {
		sum = 0;
		for (j = 1; j <= i; ++j)
			sum += (j + pow((x + j),1.0/3.0)) / (2.0 * i * j - 1.0);
		result += 1 / sum;
		count++;

	}
	end = clock();

	clock_t time_thread = end - start;
	Show(get_string_from_data("Thread time: ", time_thread));
	return result;
}

void Solve()
{
    Task("OMPBegin1");
	double x;
	int n;
	pt >> x >> n;

	clock_t start = clock();
	pt << FNoParallel(x, n);
	clock_t end = clock();
	clock_t difNoneParallel = end - start;

	Show(get_string_from_data("None-parallel time: ", difNoneParallel));
	Show(get_string_from_data("num_proc: ", omp_get_num_procs()));
	Show(get_string_from_data("num_threads: ", omp_get_num_threads()));

	pt >> x >> n;
	start = clock();
	pt << FParallel(x, n);
	end = clock();
	clock_t difParallel = end - start;
	Show(get_string_from_data("Total parallel time: ", difParallel));
	double res = difNoneParallel / difParallel;
	Show("Rate: ", res);
}
