#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int fac(int n)
{
    if(n < 2)
    return 1;
    else
    return n*fac(n-1);
}

char* reverse(char* s)
{
    register char t;
    char *p = s;     //p point to s begin
    char *q = s + (strlen(s)-1);   //q point to s end

    while(p < q)
    {
       t = *p;
       *p = *q;
       *q = t;
       p++;
       q--;
    }
    return s;
}

int test()
{
    char s[BUFSIZ];
    printf("4! = %d\n",fac(4));
    printf("8! = %d\n",fac(8));

    strcpy(s,"abcdef");
    printf("reverse abcdef ,we get %s\n",reverse(s));

    strcpy(s,"madam");
    printf("reverse madam,we get %s\n",reverse(s));

    return 0;
}

#include "Python.h"

static PyObject*
Extest_fac(PyObject *self,PyObject *args)
{
    int num;
    if(!PyArg_ParseTuple(args,"i",&num))
        return NULL;
    return (PyObject *)Py_BuildValue("i",fac(num));
}

static PyObject*
Extest_doppel(PyObject *self,PyObject *args)
{
    char *orig_str;
    char *dupe_str;
    PyObject *retval;

    if(!PyArg_ParseTuple(args,"s",orig_str))
        return NULL;
    retval = (PyObject*)Py_BuildValue("ss",orig_str,dupe_str = reverse(strdup(orig_str)));
    free(dupe_str);
    return retval;
}

static PyObject *
Extest_test()
{
    test();
    return (PyObject*)Py_BuildValue("");
}

static PyMethodDef
ExtestMethods[] =
{
    {"fac",Extest_fac,METH_VARARGS},
    {"doppel",Extest_doppel,METH_VARARGS},
    {"test",Extest_test,METH_VARARGS},
    {NULL,NULL},
};

void initExtest()
{
    Py_InitModule("Extest",ExtestMethods);
}


