import sys


if __name__=="__main__":
    if len(sys.argv)<2:
        print("Not enough arguments.")
    elif len(sys.argv)>2:
        print("Too many arguments.")
    else:
        n=sys.argv[1]
        if n.isdigit():
            n=int(n)
            graph=[[0]*(i+1) for i in range(n+1)]
            # print(graph)
            graph[0][0]=1
            for i in range(1,len(graph)):
                graph[i][0]=1
                graph[i][len(graph[i])-1] = 1
                for j in range(1,len(graph[i])-1):
                    graph[i][j]=graph[i-1][j-1]+graph[i-1][j]

            for line in graph:
                for dit in line:
                    print(dit,end=' ')
                print()

        else:
            print("Invalid argument.")
