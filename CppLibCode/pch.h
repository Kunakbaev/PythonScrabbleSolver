#ifndef _MY_LIB_H
#define _MY_LIB_H

//#ifndef MY_LIB_EXPORTS
//	
//	// we are building DLL
//	#ifdef BUILD_DLL
//		#define MY_LIB_EXPORTS __declspec(dllexport)
//	#else
//		// we are consuming DLL
//		// #pragma comment(lib, "my_lib.lib")
//		#define MY_LIB_EXPORTS __declspec(dllexport)
//	#endif
//
//#endif

#define MY_LIB_EXPORTS __declspec(dllexport)
#define _CRT_SECURE_NO_WARNINGS

#include <string>
#include <map>
#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

#ifdef __cplusplus
	extern "C" {
#endif

		MY_LIB_EXPORTS void __stdcall loadWords(const char* dictPath);
		MY_LIB_EXPORTS int __stdcall solve(char** matrix,
			const char* l, const char* path, int wordsInSolution);

#ifdef __cplusplus
	}
#endif

#endif
