//Powered by RMSHE / 2022.10.22;
#pragma once
#include "pch.h"
#include <iostream>
#include <math.h>
#include <vector>
#include <easyx.h>
using namespace std;

#define e 2.71828182845904523536
vector <int> RMSHE{ 83, 159, 87, 106, 97, 112, 183, 145, 143, 132, 58, 122, 126, 91, 134, 57, 59, 63, 101, 115, 145, 106, 169, 109, 151, 58, 153, 162, 22, 146, 108, 128, 101, 77, 71, 74, 41, 79, 49, 29, 30, 27, 123, 73, 94, 46, 80 };

#define GEARMATH_API extern "C" __declspec(dllexport)

GEARMATH_API int Info(int INPUT) {
	cout << endl;
	vector <int> info0 = { 15, 7, 1, 4, 11, 3, 14, 16, 3, 1, 4, 11, 2, 8, 12, 7, 1, 1, 6, 12, 8, 13, 16, 15, 6, 1, 15, 4, 6, 10, 14, 5, 4, 4, 5, 1, 12, 5, 4, 7, 6, 11, 15, 12, 16, 8, 5 };
	vector <int> info1 = { 11, 4, 15, 19, 10, 14, 9, 8, 4, 20, 28, 25, 8, 22, 9, 10, 27, 13, 17, 18, 13, 26, 4, 15, 15, 16, 14, 12, 27, 7, 15, 19, 2, 17, 11, 22, 14, 31, 5, 29, 28, 31, 2, 2, 8, 28, 22 };
	vector <int> info2 = { 8, 55, 4, 7, 28, 22, 63, 32, 41, 41, 11, 19, 27, 5, 30, 28, 40, 43, 32, 10, 31, 18, 43, 8, 60, 41, 54, 49, 11, 61, 32, 59, 27, 21, 45, 50, 11, 55, 2, 1, 2, 1, 61, 15, 40, 16, 47 };

	for (int i = 0; i < RMSHE.size(); ++i) {
		cout << char(RMSHE[i] - info2[i] + info1[i] - info0[i]);
	}cout << "\n" << endl;

	return INPUT;
}

double GetNearest(double x, double y, double target) { if (target - x >= y - target)return y; else return x; }

//在一数组中查找一个数的最近值(数组, 待圆整值, 数组长度)
GEARMATH_API double GetNearestElement(double arr[], double target, int Num) {
	if (target <= arr[0])return arr[0];
	if (target >= arr[Num - 1])return arr[Num - 1];
	int left = 0, right = Num, mid = 0;
	while (left < right) {
		mid = (left + right) / 2;
		if (arr[mid] == target)return arr[mid];
		if (target < arr[mid]) {
			if (mid > 0 && target > arr[mid - 1])return GetNearest(arr[mid - 1], arr[mid], target);
			right = mid;
		} else {
			if (mid < Num - 1 && target < arr[mid + 1])return GetNearest(arr[mid], arr[mid + 1], target);
			left = mid + 1;
		}
	}
	return arr[mid];
}

//[查P208/10-13]确定弯曲强度计算的齿向载荷分布系数KFbeta(齿向载荷分布系数KHbeta, 齿宽b, 齿高h)
GEARMATH_API double AutoGetKFbeta(double KHbeta, double b, double h) {
	return pow(KHbeta, (pow(b / h, 2) / (1 + (b / h) + pow(b / h, 2))));
}

//[查P206/10-8]确定动载系数KFV(齿轮精度等级C,分度圆线速度V)
GEARMATH_API double AutoGetKV(int C, double V) {
	//int C = round((-0.5048 * log(z) - 1.144 * log(m) + 2.852 * log(0.012) + 3.32));
	double B = 0.25 * pow((C - 5.0), 0.667);
	double A = 50 + 56 * (1.0 - B);

	// 动载系数KV不可靠警告
	double V_max = pow(A + (14 - C), 2) / 200;
	if (V > V_max) cout << "[警告]./动载系数KV/齿轮节圆线速度 (V = " << V << " > " << "V_max = " << V_max << ") 这将导致动载系数KV不可靠." << endl;
	if (!(6 <= C <= 12)) cout << "[警告]./动载系数KV/齿轮精度系数 (C = " << C << " 不在[6, 12]区间内) 这将导致动载系数KV不可靠." << endl;

	return pow(A / (A + sqrt(200 * V)), -B);
}

//获取DLL自身路径;
string GetCurrentModule() {
	HMODULE hModule = NULL;
	char DLLPATH[MAX_PATH + 1] = { 0 };
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS, (LPCTSTR)GetCurrentModule, &hModule);

	::GetModuleFileName(hModule, DLLPATH, MAX_PATH);
	return string(DLLPATH);
}

//初始化图形窗口;
GEARMATH_API HWND c_initgraph(int width, int height, COLORREF color) {
	HWND hWnd = initgraph(width, height, EW_SHOWCONSOLE);
	setorigin(0, 0);
	setbkcolor(color);

	if (color < RGB(128, 128, 128)) {
		setlinecolor(RGB(239, 239, 239));
		setfillcolor(RGB(97, 175, 239));
	} else {
		setlinecolor(RGB(45, 45, 45));
		setfillcolor(RGB(47, 84, 115));
	}

	cleardevice();
	setaspectratio(1, 1);
	::setbkmode(TRANSPARENT);

	::MoveWindow(hWnd, 10, 10, ::getwidth(), ::getheight(), 0);

	return hWnd;
}

//显示图片;
GEARMATH_API void c_ShowIMGDATA(char *name) {
	string DllPATH = GetCurrentModule();
	string EXEPATH = DllPATH.substr(0, DllPATH.length() - 19);
	string IMGPATH = EXEPATH + "IMGDATA\\" + string(name) + ".png";

	////从文件中读入图像
	//Mat img = imread(IMGPATH, 1);

	////如果读入图像失败
	//if (img.empty()) {
	//	fprintf(stderr, "Can not load image %s\n", IMGPATH);
	//	system("pause");
	//}
	////显示图像
	//imshow(name, img);

	////此函数等待按键，按键盘任意键就返回
	//waitKey();

	LPCTSTR _IMGPATH = IMGPATH.c_str();

	::SetWindowText(c_initgraph(400, 400, RGB(40, 44, 52)), name);
	loadimage(NULL, _IMGPATH, 0, 0, true);
}

//线性插值(需插值的x坐标,两端基点坐标)将输出x对应的y坐标
GEARMATH_API double c_Linear_interpolation(double x, double x0, double y0, double x1, double y1) {
	return (y0 + ((((x - x0) * y1) - ((x - x0) * y0)) / (x1 - x0)));
}