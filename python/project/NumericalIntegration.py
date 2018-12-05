def fun(x):
    return x ** 0.5
#梯形公式
def trapezium_formula(a, b):
    return 1 / 2.0 * (b - a) * (fun(a) + fun(b))
#中矩形公式
def rectangel_formula(a, b):
    return (b - a) * fun((a + b) / 2.0)
#辛普森公式
def simpose_formula(a, b):
    return 1 / 6 * (b - a) * (fun(a) + 4 * fun((a + b) / 2) + fun(b))

def composite_integration(a, b, N):
    sum = 0
    s = 0
    step = (b - a) / N
    i = a
    while i < b:
        s = trapezium_formula(i, i + step)
        # s = rectangel_formula(i, i+step)
        # s = simpose_formula(i, i+step)
        sum = sum + s
        i = i + step
        print(i)
    print(sum)
    return sum

composite_integration(0.5, 1, 1000)
