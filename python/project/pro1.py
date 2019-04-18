isRight=0
def dfs(mylist,result,vis):
    global isRight

    if isRight:
        return
    if len(result)==6:
        if mylist[result[0]]*10+mylist[result[1]] < 24 and mylist[result[2]]*10+mylist[result[3]] < 60 and mylist[result[4]]*10+mylist[result[5]] < 60:
            print("{}{}:{}{}:{}{}".format(mylist[result[0]],mylist[result[1]],mylist[result[2]],mylist[result[3]],mylist[result[4]],mylist[result[5]]))
            isRight=1

    for i in range(6):
        if i not in vis:
            vis.add(i);
            result.append(i)
            dfs(mylist,result,vis)
            vis.remove(i)
            result.remove(i)

if __name__=="__main__":
    mylist=input()
    mylist = mylist.strip('\n')
    mylist = mylist[1:len(mylist) - 1]
    mylist = mylist.split(',')
    for i in range(len(mylist)):
        mylist[i] = int(mylist[i])
    mylist.sort(reverse=1)

    result=[];
    vis=set()
    dfs(mylist,result,vis)
    if not isRight:
        print("invalid")
