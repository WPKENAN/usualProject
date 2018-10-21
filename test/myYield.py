def f(text):
    print("1");
    line=(yield);
    print("dad")
    print("dasdsa")


m=f("wp");

count=0;
for i in m:
    print("i: ",count)
    count+=1;
    print(i)
