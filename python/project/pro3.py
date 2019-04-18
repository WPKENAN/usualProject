


def dfs(homework,m,n):
    myQueue=[0]*m;

    homework.sort();
    for i in range(n):
        myQueue[0]=myQueue[0]+homework[i]
        myQueue.sort()
    return myQueue[-1]




if __name__=="__main__":
    mylist=input()
    mylist=mylist.strip('\n')
    mylist=mylist.split(' ')
    m=int(mylist[0])
    n=int(mylist[1])

    mylist2=input()
    mylist2=mylist2.strip('\n')
    mylist2=mylist2.split(' ')
    for i in range(len(mylist2)):
        mylist2[i] = int(mylist2[i])

    print(dfs(mylist2,m,n))



