#include "iostream"
using namespace std;

int main(){
	double t=(1<<sizeof(char)*8);
	cout << (1<<sizeof(char)) << endl;
	cout << t << endl;
	return 0;
}