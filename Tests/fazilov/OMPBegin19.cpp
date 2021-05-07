#include <cmath> 
#include <chrono>
#include <string>
#include "pt4.h"
#include "omp.h"
using namespace std;

void Solve()
{
	Task("OMPBegin19");
	int n;
	double x, sum, sumj;
	pt >> x >> n;
	sum = 0.0;
	clock_t start = clock();
	for (int i = 1; i <= n; i++)
	{
		sumj = 0.0;
		for (int j = i; j <= n; j++)
			sumj += (j + cos(x + j)) / (2 * i * j - 1);
		sum += 1 / sumj;
	}
	clock_t end = clock();
	ShowLine("Total single thread time: " + to_string(end-start));
	pt << sum;
	sum = 0;

	pt >> x >> n;
	start = clock();
#pragma omp parallel for num_threads(2) reduction(+:sum) private(sumj) schedule(static, 1)
	for (int i = 1; i <= n; i++)
	{
		sumj = 0.0;
		for (int j = i; j <= n; j++)
			sumj += (j + cos(x + j)) / (2 * i * j - 1);
		sum += 1 / sumj;
	}
	end = clock();
	ShowLine("Total multithreading time: " + to_string(end-start));
	pt << sum;
}
