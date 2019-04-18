#include "bits/stdc++.h"
// #include "test.h"
using namespace std;
class A
{
//...
public:
    void func1() {
    	cout << "int" << endl;
    }
    void func2(){

    }
};
int main(){

	 A a1;
    const A a2;
    a1.func1();
    //等价于a1.func1(&a1);//ok

    a1.func2();
    //等价于a1.func2(&a1);//ok

    // a2.func1();
    //等价于a2.func1(&a2);//ok

    // a2.func2();
    //等价于a2.func2(&a2);//error

}

