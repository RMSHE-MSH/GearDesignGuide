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

//��һ�����в���һ���������ֵ(����, ��Բ��ֵ, ���鳤��)
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

//[��P208/10-13]ȷ������ǿ�ȼ���ĳ����غɷֲ�ϵ��KFbeta(�����غɷֲ�ϵ��KHbeta, �ݿ�b, �ݸ�h)
GEARMATH_API double AutoGetKFbeta(double KHbeta, double b, double h) {
	return pow(KHbeta, (pow(b / h, 2) / (1 + (b / h) + pow(b / h, 2))));
}

//[��P206/10-8]ȷ������ϵ��KFV(���־��ȵȼ�C,�ֶ�Բ���ٶ�V)
GEARMATH_API double AutoGetKV(int C, double V) {
	//int C = round((-0.5048 * log(z) - 1.144 * log(m) + 2.852 * log(0.012) + 3.32));
	double B = 0.25 * pow((C - 5.0), 0.667);
	double A = 50 + 56 * (1.0 - B);

	// ����ϵ��KV���ɿ�����
	double V_max = pow(A + (14 - C), 2) / 200;
	if (V > V_max) cout << "[����]./����ϵ��KV/���ֽ�Բ���ٶ� (V = " << V << " > " << "V_max = " << V_max << ") �⽫���¶���ϵ��KV���ɿ�." << endl;
	if (!(6 <= C <= 12)) cout << "[����]./����ϵ��KV/���־���ϵ�� (C = " << C << " ����[6, 12]������) �⽫���¶���ϵ��KV���ɿ�." << endl;

	return pow(A / (A + sqrt(200 * V)), -B);
}

//��ȡDLL����·��;
string GetCurrentModule() {
	HMODULE hModule = NULL;
	char DLLPATH[MAX_PATH + 1] = { 0 };
	GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS, (LPCTSTR)GetCurrentModule, &hModule);

	::GetModuleFileName(hModule, DLLPATH, MAX_PATH);
	return string(DLLPATH);
}

//��ʼ��ͼ�δ���;
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

//��ʾͼƬ;
GEARMATH_API void c_ShowIMGDATA(char *name) {
	string DllPATH = GetCurrentModule();
	string EXEPATH = DllPATH.substr(0, DllPATH.length() - 19);
	string IMGPATH = EXEPATH + "Resource\\" + string(name) + ".png";

	////���ļ��ж���ͼ��
	//Mat img = imread(IMGPATH, 1);

	////�������ͼ��ʧ��
	//if (img.empty()) {
	//	fprintf(stderr, "Can not load image %s\n", IMGPATH);
	//	system("pause");
	//}
	////��ʾͼ��
	//imshow(name, img);

	////�˺����ȴ�������������������ͷ���
	//waitKey();

	LPCTSTR _IMGPATH = IMGPATH.c_str();

	::SetWindowText(c_initgraph(400, 400, RGB(40, 44, 52)), name);
	loadimage(NULL, _IMGPATH, 0, 0, true);
}

//���Բ�ֵ(���ֵ��x����,���˻�������)�����x��Ӧ��y����
GEARMATH_API double c_Linear_interpolation(double x, double x0, double y0, double x1, double y1) {
	return (y0 + ((((x - x0) * y1) - ((x - x0) * y0)) / (x1 - x0)));
}

//����б��������ϵ��ZH
GEARMATH_API double c_ZH_helical(double alpha_n, double beta) {
	double alpha_t = atan(tan(alpha_n * pi / 180) / cos(beta * pi / 180));
	double beta_b = atan(tan(beta * pi / 180) * cos(alpha_t * pi / 180));
	double ZH = sqrt((2 * cos(beta_b)) / (cos(alpha_t) * sin(alpha_t)));

	return ZH;
}

//����б���ֽӴ�ƣ��ǿ���غ϶�ϵ��Z_epsilon
GEARMATH_API double c_Zepsilon_helical(double z1, double z2, double alpha_n, double beta, double PHI_d, double h_an = 1) {
	double alpha_t = atan(tan(alpha_n * pi / 180) / cos(beta * pi / 180));
	double alpha_at1 = acos((z1 * cos(alpha_t)) / (z1 + 2 * h_an * cos(beta * pi / 180)));
	double alpha_at2 = acos((z2 * cos(alpha_t)) / (z2 + 2 * h_an * cos(beta * pi / 180)));
	double epsilon_alpha = (z1 * (tan(alpha_at1) - tan(alpha_t)) + z2 * (tan(alpha_at2) - tan(alpha_t))) / (2 * pi);
	double epsilon_beta = (PHI_d * z1 * tan(beta * pi / 180)) / pi;
	double Z_epsilon = sqrt(((4 - epsilon_alpha) / 3) * (1 - epsilon_beta) + (epsilon_beta / epsilon_alpha));

	return Z_epsilon;
}

//����Сб���ֶַ�Բֱ��;
GEARMATH_API double c_d1_test_helical(double KH_t, double T1, double PHI_d, double u, double ZH, double ZE, double Zepsilon, double Zbeta, double sigmaH) {
	double A = (2 * KH_t * T1) / PHI_d;
	double B = (u + 1) / u;
	double C = pow(((ZH * ZE * Zepsilon * Zbeta) / sigmaH), 2);
	double d1_test = pow(A * B * C, (1.0 / 3.0));

	return d1_test;
}

//��������ƣ��ǿ�ȵ��غ϶�ϵ��Y_epsilon
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

//����б��������ƣ��ǿ�ȵ�������ϵ��Y_beta
GEARMATH_API double c_Y_beta_helical(double beta, double z1, double PHI_d) {
	double epsilon_beta = (PHI_d * z1 * tan(beta * pi / 180)) / pi;
	double Y_beta = 1 - epsilon_beta * (beta / 120);

	return Y_beta;
}

//����б���ֵ�������Zv
GEARMATH_API double c_Zv_helical(double beta, double z) {
	double Zv = z / pow(cos(beta * pi / 180), 3);

	return Zv;
}

//��������ƣ�ͼ���ĳ���ģ��m_nt
GEARMATH_API double c_mF_helical(double KFt, double T1, double Y_epsilon, double Y_beta, double beta, double PHI_d, double z1, double NYLL2) {
	double A = (2 * KFt * T1 * Y_epsilon * Y_beta * pow(cos(beta * pi / 180), 2)) / (PHI_d * pow(z1, 2));
	double m_nt = pow(A * NYLL2, (1.0 / 3.0));

	return m_nt;
}