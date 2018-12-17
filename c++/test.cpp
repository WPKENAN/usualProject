#include "iostream"
#include <fstream>
using namespace std;

int main(){
	// double t=(1<<sizeof(char)*8);
	// cout << (1<<sizeof(char)) << endl;
	// cout << t << endl;
	// double a=11.1;
	// int b=0;
	// cout << a << " " << (unsigned short)a << endl;

	// if (a>255) b=255;
	// else if(a<0) b=0;
	// else{
	// 	b=(int)a;
	// }
	// cout << sizeof(char) << endl;
	// unsigned char c=97;
	// cout << c << endl; 
	// cout << (int)c << endl;
	// return 0;
	// int m=2;
	// int n=4;
	// int **p=new int*[m];
	// for(int i=0; i<m; i++) 
 //   		p[i]=new int[n];
 //   	for(int i=0;i<m;i++){
 //   		for(int j=0;j<n;j++){
 //   			cout << p[i][j] << endl;
 //   		}
 //   		cout << " ======" << endl;
 //   	}

	ifstream ifile; 
	ifile.open( "C:\\Users\\Anzhi\\Desktop\\18.txt" );
	float a;
	float b;
	float c;
	while(ifile >> a >> b >> c){
	
		cout << a << " " << b << " " << c << endl;	
		// cout << dot << endl;
	}
	cout << "stop" << endl;
	ifile.close();
	// return 0;
	return 0;

}