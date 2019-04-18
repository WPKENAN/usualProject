# def dfs(cost_profit,vis,money):
#     for i in range(len(cost_profit)):
#         if i not in vis and cost_profit[i][0] <=money:
#             money=money+cost_profit[i][1]
#             vis.add(i)
#             dfs(cost_profit,vis,money)
def dfs(cost_profit,vis,money):
    i=0;
    while i < len(cost_profit) and money>=cost_profit[i][0]:
        money=money+cost_profit[i][1]
        i=i+1
    return money

if __name__ == '__main__':
    mylist=input()
    mylist = mylist.strip('\n')
    mylist = mylist.split(',')
    for i in range(len(mylist)):
        mylist[i] = int(mylist[i])

    mylist2 = input()
    mylist2 = mylist2.strip('\n')
    mylist2 = mylist2.split(',')
    for i in range(len(mylist2)):
        mylist2[i] = int(mylist2[i])

    money=int(input())
    cost_profit=[]
    for i in range(len(mylist)):
        if mylist2[i]-mylist[i] < 0:
            continue
        cost_profit.append([mylist[i],mylist2[i]-mylist[i]])

    cost_profit.sort()
    vis=set();
    isRight=0;
    print(dfs(cost_profit,vis,money))

    # print(cost_profit)

