
def parse_scenario(filename):
    # TODO implement this function
    lines=open(filename).readlines();
    for i in range(len(lines)):#循环处理文件的每一行
        lines[i]=lines[i].strip('\n').split(',')
        for j in range(len(lines[i])):#遍历每一行的每一个数字
            try:
                lines[i][j]=eval(lines[i][j])
            except:
                pass

    M=lines[0][0];
    if M <=0:
        return None

    f_grid=[[0]*M for i in range(M)]
    for i in range(1,1+M):#读取这些行存到f_grid里面
        for j in range(M):
            f_grid[i-1][j]=lines[i][j]

    h_grid = [[0] * M for i in range(M)]
    for i in range(M+1,M+1+M):#读取这些行存大h_grid里面
        for j in range(M):
            h_grid[i-M-1][j]=lines[i][j]

    i_threshold=lines[2*M+1][0]
    w_direction=lines[2*M+2][0]
    burn_seeds=lines[2*M+3]

    Dir=['NW','N','NE','W','E','SW','S','SE','None',''];
    if i_threshold > 8 or i_threshold <= 0 or w_direction not in Dir :
        return None

    if burn_seeds[0] not in range(M) or burn_seeds[1] not in range(M):
        return None

    if f_grid[burn_seeds[0]][burn_seeds[1]]<=0:
        return None

    result={};
    result['f_grid']=f_grid
    result['h_grid']=h_grid
    result['i_threshold']=i_threshold
    result['w_direction']=w_direction
    result['burn_seeds']=[tuple(burn_seeds)]
    return result
def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    # TODO implement this function
    x=i;
    y=j;

    # 邻居是周围的八个方格，这八个邻居相对中心的坐标存到矩阵中，[1,1]代表右下角角的邻居
    # 点point[x][y]邻居的真实坐标就是point[x+i][j+j]
    normal_neighbor=[];
    for i in range(-1,2):
        for j in range(-1,2):
            if i==0 and j==0:
                continue
            normal_neighbor.append([i,j])

    if w_direction=='N':
        normal_neighbor.append([2,-1])
        normal_neighbor.append([2, 0])
        normal_neighbor.append([2, 1])
    elif w_direction=='S':
        normal_neighbor.append([-2, -1])
        normal_neighbor.append([-2, 0])
        normal_neighbor.append([-2, 1])
    elif w_direction=='W':
        normal_neighbor.append([-1, 2])
        normal_neighbor.append([0, 2])
        normal_neighbor.append([1, 2])
    elif w_direction=='E':
        normal_neighbor.append([-1, -2])
        normal_neighbor.append([0, -2])
        normal_neighbor.append([1, -2])
    elif w_direction=='NW':
        normal_neighbor.append([1, 2])
        normal_neighbor.append([2, 1])
        normal_neighbor.append([2, 2])
    elif w_direction=='NE':
        normal_neighbor.append([1, -2])
        normal_neighbor.append([2, -1])
        normal_neighbor.append([2, -2])
    elif w_direction=='SW':
        normal_neighbor.append([-1, 2])
        normal_neighbor.append([-2, 1])
        normal_neighbor.append([-2, 2])
    elif w_direction=='SE':
        normal_neighbor.append([-1, -2])
        normal_neighbor.append([-2, -1])
        normal_neighbor.append([-2, -2])

    # print(normal_neighbor)
    M=len(f_grid)
    ignition_factor=[[0]*M for i in range(M)]#用来存储当前的着火因子
    for i in range(M):#循环遍历每一个方格
        for j in range(M):
            if b_grid[i][j]:#如果当前方格在着火状态，就访问他的邻居
                f_grid[i][j]=f_grid[i][j]-1;#燃料-1
                for neighbor in normal_neighbor:#访问每一个邻居
                    if i+neighbor[0] in range(M) and j+neighbor[1] in range(M):#如果邻居的坐标点合法
                        if h_grid[i+neighbor[0]][j+neighbor[1]] > h_grid[i][j]:#邻居高度，大于自己
                            factor=2;
                        elif h_grid[i+neighbor[0]][j+neighbor[1]] < h_grid[i][j]:#邻居高度<自己
                            factor=0.5;
                        else:
                            factor=1
                        ignition_factor[i+neighbor[0]][j+neighbor[1]]=1*factor+ignition_factor[i+neighbor[0]][j+neighbor[1]];#计算当前邻居的累计着火因子
    # print(ignition_factor)
    for i in range(M):
        for j in range(M):
            if ignition_factor[i][j]>=i_threshold and f_grid[i][j]>0:#如果着火因子大于阈值并且燃料不是0
                b_grid[i][j]=True
            if f_grid[i][j] == 0:#如果燃料是0
                b_grid[i][j] = False

    print(b_grid)
    print(ignition_factor)
    # return b_grid[x][y]


def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    # TODO implement this function
    # pass
    w_direction=w_direction.upper()
    M = len(f_grid)
    result=[[False] * M for i in range(M)];

    for i in range(M):
        for j in range(M):
            result[i][j]=f_grid[i][j]

    b_grid=[[False] * M for i in range(M)];
    b_grid[burn_seeds[0][0]][burn_seeds[0][1]]=True;


    normal_neighbor = [];
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            normal_neighbor.append([i, j])

    if w_direction == 'N':
        normal_neighbor.append([2, -1])
        normal_neighbor.append([2, 0])
        normal_neighbor.append([2, 1])
    elif w_direction == 'S':
        normal_neighbor.append([-2, -1])
        normal_neighbor.append([-2, 0])
        normal_neighbor.append([-2, 1])
    elif w_direction == 'W':
        normal_neighbor.append([-1, 2])
        normal_neighbor.append([0, 2])
        normal_neighbor.append([1, 2])
    elif w_direction == 'E':
        normal_neighbor.append([-1, -2])
        normal_neighbor.append([0, -2])
        normal_neighbor.append([1, -2])
    elif w_direction == 'NW':
        normal_neighbor.append([1, 2])
        normal_neighbor.append([2, 1])
        normal_neighbor.append([2, 2])
    elif w_direction == 'NE':
        normal_neighbor.append([1, -2])
        normal_neighbor.append([2, -1])
        normal_neighbor.append([2, -2])
    elif w_direction == 'SW':
        normal_neighbor.append([-1, 2])
        normal_neighbor.append([-2, 1])
        normal_neighbor.append([-2, 2])
    elif w_direction == 'SE':
        normal_neighbor.append([-1, -2])
        normal_neighbor.append([-2, -1])
        normal_neighbor.append([-2, -2])

    # print(normal_neighbor)
    t=1;
    oneList_b_grid=[]
    for i in range(M):
        for j in range(M):#把b_grid一维化
            oneList_b_grid.append(b_grid[i][j])
    while True in oneList_b_grid:#如果oneList_b_grid有正在燃烧的则继续循环，循环里面的就跟第二个project一模一样
        ignition_factor = [[0] * M for i in range(M)]
        for i in range(M):
            for j in range(M):
                if b_grid[i][j]:
                    f_grid[i][j] = f_grid[i][j] - 1;
                    for neighbor in normal_neighbor:
                        if i + neighbor[0] in range(M) and j + neighbor[1] in range(M):
                            if h_grid[i + neighbor[0]][j + neighbor[1]] > h_grid[i][j]:
                                factor = 2;
                            elif h_grid[i + neighbor[0]][j + neighbor[1]] < h_grid[i][j]:
                                factor = 0.5;
                            else:
                                factor = 1
                            ignition_factor[i + neighbor[0]][j + neighbor[1]] = factor + ignition_factor[i + neighbor[0]][j + neighbor[1]];

        for i in range(M):
            for j in range(M):
                if ignition_factor[i][j] >= i_threshold and f_grid[i][j] > 0:
                    b_grid[i][j] = True
                if f_grid[i][j] == 0:
                    b_grid[i][j] = False
        oneList_b_grid = []
        for i in range(M):
            for j in range(M):
                oneList_b_grid.append(b_grid[i][j])
        t=t+1

    count=0;
    for i in range(M):
        for j in range(M):#对比下然后之后的景观和燃烧之前的，如果不一样说明当前方格燃烧过，计算下燃烧的数量
            if result[i][j]!=f_grid[i][j]:
                count=count+1;

    return (f_grid,count)


if __name__=="__main__":
    # check_ignition([[True, False], [False, False]], [[2, 2], [2, 2]], [[1, 1], [1, 1]], 1, 'N', 0, 1);
#     # check_ignition([[True, True, False], [False, False, False], [False, False, False]],
#     #                [[1, 1, 1], [1, 1, 1], [1, 0, 0]], [[2, 2, 1], [2, 3, 1], [1, 1, 1]], 2, None, 1, 1);
    run_model([[2, 2], [2, 2]], [[1, 1], [1, 1]], 1, 'N', [(0, 0)])
    run_model([[2, 0], [0, 2]], [[1, 1], [1, 1]], 2, 'S', [(0, 0)])