/*
 * sample.c
 *
 *  Created on: 2016年11月28日
 *      Author: hawrk
 *      Desc: a sample function for python call
 */
#include "sample.h"

int gcd(int x,int y)
{
	int g = y;
	while(x > 0)
	{
		g = x;
		x = y%x;
		y = g;
	}
	return g;
}

int in_mandel(double x,double y,int n)
{
	double lx = 0.00,ly = 0.00,temp;
	while(n > 0)
	{
		temp = lx*lx - ly*ly + x;
		ly = 2*lx*ly + y;
		lx = temp;
		n -= 1;
		if(lx*lx + ly*ly > 4)
		{
			return 0;
		}
	}
	return 1;
}

int devide(int a,int b,int* remainder)
{
	int quot = a/b;
	*remainder = a%b;
	return quot;
}

double avg(double* a,int n)
{
	int i;
	double total = 0.0;
	for(i = 0;i< n;i++)
	{
		total += a[i];
	}
	return total/n;
}

double distince(Point* p1,Point* p2)
{
	return hypot(p1->x - p2->x,p1->y - p2->y);
}
