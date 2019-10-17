ip=input()
count={}

for i in range(10):
    count[i]=0

for i in ip:
    count[int(i)]+=1

for key in count.keys():
    print("{}:{}".format(key,count[key]))