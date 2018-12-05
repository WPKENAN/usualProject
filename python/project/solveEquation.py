import sympy

x=sympy.symbols('x');
delt=9.17e9;
sita=0.1;
vc=3;
y=sympy.solve(4*(2*x)**vc*sympy.exp(-1/8*sita**2*x)-delt,x);
print(y)
