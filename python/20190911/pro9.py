esp=1e-3
while(1):
    a_b=input()
    try:
        a=float(a_b.split(' ')[0])
        b=float(a_b.split(' ')[1])
    except:
        print("Invalid input.")
        exit(0)

    # print((a+b)/a-a/b)
    # print((b+a)/b-b/a)
    if (abs((a+b)/a-a/b)<esp or abs((b+a)/b-b/a)<esp) and a!=0 and b!=0:
        print("Golden ratio!")
    else:
        print("Maybe next time.")

