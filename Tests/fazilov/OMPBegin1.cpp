#include "pt4.h"
#include "omp.h"
#include <iostream>
using namespace std;

void Solve()
{
    //Task("OMPBegin1");

#pragma omp parallel
    for (int i = 0; i < 2; ++i)
        cout << omp_get_thread_num() << endl;

}
