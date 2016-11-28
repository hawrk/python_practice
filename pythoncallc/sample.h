/*
 * sample.h
 *
 *  Created on: 2016年11月28日
 *      Author: hawrk
 *      Desc: a sample c function for python3 call
 */

#ifndef SAMPLE_H_
#define SAMPLE_H_

#include <math.h>

//返回最大公约数
int gcd(int x,int y);

//复数集吧
int in_mandel(double x,double y,int n);

//除数，返回商和余数 （指针返回)
int devide(int a,int b,int* remainder);

//计算数组的平均数
double avg(double* a,int n);

//c structure
typedef struct Point
{
	double x,y;
}Point;

//test c data structure
double distince(Point* p1,Point* p2);






#endif /* SAMPLE_H_ */
