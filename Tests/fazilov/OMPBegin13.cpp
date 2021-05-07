#include <iostream>
#include <math.h>
#include <time.h>
#include <sstream>
#include "pt4.h"
#include "omp.h"
using namespace std;

int n;
double x, sum, sumj;

int optimalMiddle(int n) {
	return sqrt(n * (n + 1) / 2);
}
double sumReducer(int start, int end)
{
	double threadSum, tempSum;
	threadSum = tempSum = sumj = sum = 0.0;
	for (int i = start; i <= end; i++)
	{
		tempSum = 0.0;
		for (int j = 1; j <= i; j++)
			tempSum += (j + pow(x + j, 1.0 / 4.0)) / (2 * i * j - 1);
		threadSum += 1 / tempSum;
	}
	return threadSum;
}
int* setRange(int n) {
	int kVals[100000];
	int limit = ((((n - 1) * n) / 2) + (n * n)) / 4;
	int c = 0;
	int kI = 0;
	for (int i = 1; i <= n; i++)
	{
		for (int j = i; j <= 2 * n; j++)
			c++;
		if (c >= limit)
		{
			c = 0;
			kVals[kI] = i;
			kI++;
		}
	}
	kVals[3] = n;
	return kVals;
}

void Solve()
{
	Task("OMPBegin13");

	pt >> x >> n;
	clock_t start = clock();
	pt << sumReducer(1, n);
	clock_t end = clock();
	ShowLine("None parallel time: "+(end - start));

	pt >> x >> n;
	start = clock();
	double threadSum = 0.0;
	int* K = setRange(n);
#pragma omp parallel sections reduction(+: threadSum)
	{
#pragma omp section 
		{
			auto startThread = clock();
			threadSum = sumReducer(1, K[0]);
			auto endThread = clock();
			ShowLine("Thread time: " + (endThread - startThread));
		}
#pragma omp section
		{
			auto startThread = clock();
			threadSum = sumReducer(K[0] + 1, K[1]);
			auto endThread = clock();
			ShowLine("Thread time: " + (endThread - startThread));
		}
#pragma omp section
		{
			auto startThread = clock();
			threadSum = sumReducer(K[1] + 1, K[2]);
			auto endThread = clock();
			ShowLine("Thread time: " + (endThread - startThread));
		}
#pragma omp section
		{
			auto startThread = clock();
			threadSum = sumReducer(K[2] + 1, K[3]);
			auto endThread = clock();
			ShowLine("Thread time: "+(endThread - startThread));
		}
	}
	end = clock();

	ShowLine("Total multithreading time: " + (end - start));
	pt << threadSum;
}