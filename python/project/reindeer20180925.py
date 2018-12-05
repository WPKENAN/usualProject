def printPascal(n):
    rows=[1]*(n+1);
    if n==0:
        return rows;
    for i in range(1,n):
        rows[i]=printPascal(n-1)[i-1]+printPascal(n-1)[i];

    return rows;

while 1:
    n=int(input("Number n: "));

    for i in range(0,n+1):
        # print("第%d行"%(i))
        test=printPascal(i)
        print(test)
