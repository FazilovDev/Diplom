#include <cmath> 
#include <chrono>
#include <string>
#include "pt4.h"
#include "omp.h"
using namespace std;

void Solve()
{
	Task("OMPBegin22");
	int n;
	double x, sum, sumj;
	pt >> x >> n;
	sum = 0.0;
	clock_t start = clock();
	for (int i = 1; i <= n; i++)
	{
		sumj = 0.0;
		for (int j = 1; j <= i+n; j++)
			sumj += (j + pow(x + j, 1.0 / 5.0)) / (2 * i * j - 1);
		sum += 1 / sumj;
	}
	clock_t end = clock();
	ShowLine("None parallel time: " + to_string(end - start));
	ShowLine("num_proc: ", omp_get_num_procs());
	ShowLine("num_threads: ", 4);
	double difNoneParallel = end - start;
	pt << sum;
	sum = 0;

	pt >> x >> n;
	start = clock();
#pragma omp parallel for num_threads(4) reduction(+:sum) private(sumj) schedule(dynamic)
	for (int i = 1; i <= n; i++)
	{
		sumj = 0.0;
		for (int j = 1; j <= i + n; j++)
			sumj += (j + pow(x + j, 1.0 / 5.0)) / (2 * i * j - 1);
		sum += 1 / sumj;
	}
	end = clock();
	double rate = difNoneParallel/ (end - start);
	ShowLine("Total parallel time: " + to_string(end - start));
	ShowLine("Rate: " + to_string(rate));
	pt << sum;
}

