/*
< GearDesignGuide >
Copyright(C) < 2022 > <RMSHE>

This program is free software : you can redistribute it and /or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.If not, see < https://www.gnu.org/licenses/>.

Electronic Mail : asdfghjkl851@outlook.com
*/

//Powered by RMSHE / 2022.10.22;
//git config --global https.proxy
//git config --global --unset https.proxy
//git config --global http.sslVerify "false"
#pragma once
#include "pch.h"
#include <iostream>
#include <math.h>
#include <vector>
#include <easyx.h>
using namespace std;

#define pi 3.14159265358979323846
#define e 2.71828182845904523536
vector <int> SoftwareName{ 61, 89, 87, 110, 16, 67, 94, 112, 97, 94, 109, 18, 64, 111, 92, 88, 98 };
vector <int> RMSHE{ 81, 53, 107, 112, 88, 110, 107, 70, 102, 93, 110, 79, 25, 74, 98, 107, 98, 109, 100, 98, 23, 96, 117, 22, 73, 61, 80, 71, 59, 26, 35, 28, 88, 103, 86, 93, 93, 103, 103, 96, 96, 49, 40, 33, 53, 98, 110, 109, 105, 102, 106, 96, 44, 90, 95, 98 };
vector <int> OpenSource{ 81, 67, 102, 97, 94, 82, 104, 114, 106, 90, 100, 79, 25, 98, 103, 104, 109, 110, 57, 45, 38, 101, 101, 106, 95, 101, 95, 45, 89, 105, 99, 43, 73, 65, 69, 63, 59, 44, 74, 72, 60, 40, 58, 85, 86, 101, 61, 94, 112, 96, 98, 99, 69, 108, 89, 89, 99 };
vector <int> Copyright{ 50, 59, 91, 93, 98, 67, 94, 112, 97, 94, 109, 57, 110, 99, 87, 89, 59, 27, 66, 109, 103, 119, 110, 95, 94, 88, 113, 31, 30, 61, 31, 28, 51, 38, 34, 41, 40, 61, 29, 21, 48, 75, 64, 67, 61, 56, 55 };
vector <int> LICENSE{ 81, 64, 63, 63, 53, 77, 76, 66, 85, 23, 70, 64, 78, 26, 52, 58, 67, 64, 81, 77, 23, 69, 65, 68, 60, 66, 62, 75, 22, 74, 75, 62, 67, 61, 53, 23, 66, 72, 64, 58, 66, 76, 56, 16, 75, 88, 107, 108, 102, 102, 105, 21, 49 };
vector <int> MathDll{ 81, 65, 87, 112, 88, 67, 101, 105, 85, 23, 70, 87, 90, 108, 55, 89, 112, 100, 102, 108, 62, 115, 101, 90, 92, 30, 97, 107, 98, 26, 35, 28, 57, 89, 102, 88, 36, 49, 45, 39, 38, 39, 36, 32, 35, 38, 41, 39, 74, 88, 109, 96, 46 };

#define GEARMATH_API extern "C" __declspec(dllexport)

GEARMATH_API int SelfTest(int Input) { return Input; }

GEARMATH_API void DllInfo() {
	vector <int> Key{ 10, 12, 10, 4, 16, 1, 7, 3, 8, 9, 1, 14, 7, 6, 13, 12, 3, 5, 1, 2, 9, 2, 4, 10, 9, 16, 3, 1, 10, 6, 10, 4, 9, 12, 14, 9, 10, 1, 3, 11, 12, 7, 13, 16, 11, 13, 7, 7, 3, 9, 5, 11, 2, 9, 16, 11, 2, 4, 7, 3, 12, 3, 14, 14 };
	for (int i = 0; i < SoftwareName.size(); ++i) cout << char(SoftwareName[i] + Key[i]);
	cout << endl; for (int i = 0; i < RMSHE.size(); ++i) cout << char(RMSHE[i] + Key[i]);
	cout << endl; for (int i = 0; i < OpenSource.size(); ++i) cout << char(OpenSource[i] + Key[i]);
	cout << endl; for (int i = 0; i < Copyright.size(); ++i)cout << char(Copyright[i] + Key[i]);
	cout << endl; for (int i = 0; i < LICENSE.size(); ++i)cout << char(LICENSE[i] + Key[i]);
	cout << "\n" << endl; for (int i = 0; i < MathDll.size(); ++i)cout << char(MathDll[i] + Key[i]);
	cout << endl;
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

GEARMATH_API void c_closegraph() { closegraph(); }

//显示图片;
GEARMATH_API void c_ShowIMGDATA(char *name) {
	string DllPATH = GetCurrentModule();
	string EXEPATH = DllPATH.substr(0, DllPATH.length() - 19);
	string IMGPATH = EXEPATH + "Resource\\" + string(name) + ".png";

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

//计算斜齿轮区域系数ZH
GEARMATH_API double c_ZH_helical(double alpha_n, double beta) {
	double alpha_t = atan(tan(alpha_n * pi / 180) / cos(beta * pi / 180));
	double beta_b = atan(tan(beta * pi / 180) * cos(alpha_t * pi / 180));
	double ZH = sqrt((2 * cos(beta_b)) / (cos(alpha_t) * sin(alpha_t)));

	return ZH;
}

//计算斜齿轮接触疲劳强度重合度系数Z_epsilon
GEARMATH_API double c_Zepsilon_helical(double z1, double z2, double alpha_n, double beta, double PHI_d, double h_an = 1) {
	double alpha_t = atan(tan(alpha_n * pi / 180) / cos(beta * pi / 180));
	double alpha_at1 = acos((z1 * cos(alpha_t)) / (z1 + 2 * h_an * cos(beta * pi / 180)));
	double alpha_at2 = acos((z2 * cos(alpha_t)) / (z2 + 2 * h_an * cos(beta * pi / 180)));
	double epsilon_alpha = (z1 * (tan(alpha_at1) - tan(alpha_t)) + z2 * (tan(alpha_at2) - tan(alpha_t))) / (2 * pi);
	double epsilon_beta = (PHI_d * z1 * tan(beta * pi / 180)) / pi;
	double Z_epsilon = sqrt(((4 - epsilon_alpha) / 3) * (1 - epsilon_beta) + (epsilon_beta / epsilon_alpha));

	return Z_epsilon;
}

//试算小斜齿轮分度圆直径;
GEARMATH_API double c_d1_test_helical(double KH_t, double T1, double PHI_d, double u, double ZH, double ZE, double Zepsilon, double Zbeta, double sigmaH) {
	double A = (2 * KH_t * T1) / PHI_d;
	double B = (u + 1) / u;
	double C = pow(((ZH * ZE * Zepsilon * Zbeta) / sigmaH), 2);
	double d1_test = pow(A * B * C, (1.0 / 3.0));

	return d1_test;
}

//计算弯曲疲劳强度的重合度系数Y_epsilon
GEARMATH_API double c_Y_epsilon_helical(double z1, double z2, double alpha_n, double beta, double h_an = 1) {
	double alpha_t = atan(tan(alpha_n * pi / 180) / cos(beta * pi / 180));
	double alpha_at1 = acos((z1 * cos(alpha_t)) / (z1 + 2 * h_an * cos(beta * pi / 180)));
	double alpha_at2 = acos((z2 * cos(alpha_t)) / (z2 + 2 * h_an * cos(beta * pi / 180)));
	double epsilon_alpha = (z1 * (tan(alpha_at1) - tan(alpha_t)) + z2 * (tan(alpha_at2) - tan(alpha_t))) / (2 * pi);
	double beta_b = atan(tan(beta * pi / 180) * cos(alpha_t * pi / 180));
	double epsilon_alpha_v = epsilon_alpha / (pow(cos(beta_b), 2));
	double Y_epsilon = 0.25 + (0.75 / epsilon_alpha_v);

	return Y_epsilon;
}

//计算斜齿轮弯曲疲劳强度的螺旋角系数Y_beta
GEARMATH_API double c_Y_beta_helical(double beta, double z1, double PHI_d) {
	double epsilon_beta = (PHI_d * z1 * tan(beta * pi / 180)) / pi;
	double Y_beta = 1 - epsilon_beta * (beta / 120);

	return Y_beta;
}

//计算斜齿轮当量齿数Zv
GEARMATH_API double c_Zv_helical(double beta, double z) {
	double Zv = z / pow(cos(beta * pi / 180), 3);

	return Zv;
}

//试算弯曲疲劳计算的齿轮模数m_nt
GEARMATH_API double c_mF_helical(double KFt, double T1, double Y_epsilon, double Y_beta, double beta, double PHI_d, double z1, double NYLL2) {
	double A = (2 * KFt * T1 * Y_epsilon * Y_beta * pow(cos(beta * pi / 180), 2)) / (PHI_d * pow(z1, 2));
	double m_nt = pow(A * NYLL2, (1.0 / 3.0));

	return m_nt;
}