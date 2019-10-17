while(1):
    p = "* "
    n = int(input())

    if n>20 or n<2:
        print("Invalid height.")
        continue
    else:
        for i in range(2*n):
            print('{:^{width}}'.format(p*(i+1), width=4*n)*(i<n),'{:^{width}}'.format(p*(i-n+1), width=2*n)*(i>=n),'{:^{width}}'.format(p*(i-n+1), width=2*n)*(i>=n), sep="")
