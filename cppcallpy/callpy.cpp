/*
 * callpy.cpp
 *
 *  Created on: 2016-7-28
 *      Author: hawrk
 */

#include <python2.7/Python.h>
#include <iostream>

using namespace std;

int main(int argc,char* argv[])
{
	Py_Initialize();
	if(!Py_IsInitialized())
	{
		cout<<"init fail"<<endl;
		return -1;
	}

	PyRun_SimpleString("import sys");
	PyRun_SimpleString("print '----import sys----'");
	PyRun_SimpleString("sys.path.append('./')");
	PyObject *pName,*pModule,*pDict,*pFunc,*pArgs;

	pName = PyString_FromString("pytest");
	pModule = PyImport_Import(pName);
	if(!pModule)
	{
		cout<<"error to import module"<<endl;
		return -1;
	}
	pDict = PyModule_GetDict(pModule);
	if(!pDict)
	{
		cout<<"error to get dict"<<endl;
		return -1;
	}

	//add fun
	cout<<"call func begin...."<<endl;
	pFunc = PyDict_GetItemString(pDict,"add");
	if(!pFunc ||!PyCallable_Check(pFunc))
	{
		cout<<"call fun add error"<<endl;
		return -1;
	}

	cout<<"add args"<<endl;
	pArgs = PyTuple_New(2);
	PyTuple_SetItem(pArgs,0,Py_BuildValue("i",3));    //BuildValue "i" 表示创建int 类型变量
	PyTuple_SetItem(pArgs,1,Py_BuildValue("i",4));

	PyObject_CallObject(pFunc,pArgs);

	Py_DECREF(pName);
	Py_DECREF(pArgs);
	Py_DECREF(pModule);

	Py_Finalize();
	return 0;


}


