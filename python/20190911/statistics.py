def mean(x):
    s=0
    for i in x:
        s+=i/len(x)
    return s

def var(x):
    u=mean(x)
    v=0
    for i in x:
       v+=(i-u)**2
    return v/len(x)

def std(x):
    v=var(x)
    return v**0.5
if __name__=="__main__":
    ips=[]
    while(1):
        try:
            ip=input()
        except EOFError:
            # ips.append(ip)
            # print(ips)
            x=[]
            for line in ips:
                for dit in line:
                    x.append(float(dit))

            print("Mean = {:.4f}".format(mean(x)))
            print("Variance = {:.4f}".format(var(x)))
            print("Standard deviation = {:.4f}".format(std(x)))

            exit(0)
        ips.append(ip.split(' '))
