#include "iostream"
using namespace std;

int main(){
	// double t=(1<<sizeof(char)*8);
	// cout << (1<<sizeof(char)) << endl;
	// cout << t << endl;
	double a=11.1;
	int b=0;
	cout << a << " " << (unsigned short)a << endl;

	if (a>255) b=255;
	else if(a<0) b=0;
	else{
		b=(int)a;
	}
	cout << sizeof(char) << endl;
	unsigned char c=97;
	cout << c << endl; 
	cout << (int)c << endl;
	return 0;
}