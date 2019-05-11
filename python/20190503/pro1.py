def parse_scenario(filename):
    # TODO implement this function
    lines=open(filename).readlines();
    for i in range(len(lines)):
        lines[i]=lines[i].strip('\n').split(',')
        for j in range(len(lines[i])):
            try:
                lines[i][j]=eval(lines[i][j])
            except:
                pass

    M=lines[0][0];
    if M <=0:
        return None

    f_grid=[[0]*M for i in range(M)]
    for i in range(1,1+M):
        for j in range(M):
            f_grid[i-1][j]=lines[i][j]

    h_grid = [[0] * M for i in range(M)]
    for i in range(M+1,M+1+M):
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
    result['burn_seeds']=tuple(burn_seeds)
    # print(f_grid)
    # print(h_grid)
    # print(i_threshold)
    # print(w_direction)
    # print(burn_seeds)
    # print(lines)
    # print(result)
    return tuple


def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    # TODO implement this function
    x = i;
    y = j;
    # pass
    # neighbor is the surrounding eight squares, the coordinates of the eight
    # neighbors relative to the center are stored in the matrix, [1,1]
    # represents the neighbor in the lower right corner
    normal_neighbor = [];
    # Point[x][y] The real coordinates of the neighbor are point[x+i][j+j]
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
    M = len(f_grid)
    # Used to store the current ignition factor
    ignition_factor = [[0] * M for i in range(M)]
    # loop through each cell
    for i in range(M):
        for j in range(M):
            # If the current square is on fire, visit his neighbor
            if b_grid[i][j]:
                # Fuel-1
                f_grid[i][j] = f_grid[i][j] - 1;
                # Access every neighbor
                for neighbor in normal_neighbor:
                    # If the neighbor's coordinate point is legal
                    if i + neighbor[0] in range(M) and j + neighbor[1] in range(M):
                        # neighbor height, greater than yourself
                        if h_grid[i + neighbor[0]][j + neighbor[1]] > h_grid[i][j]:
                            factor = 2;
                            # neighbor height <self
                        elif h_grid[i + neighbor[0]][j + neighbor[1]] < h_grid[i][j]:
                            factor = 0.5;
                        else:
                            factor = 1
                            # Calculate the cumulative ignition factor of the
                            # current neighbor
                        ignition_factor[i + neighbor[0]][j + neighbor[1]] = 1 * factor + \
                                                                            ignition_factor[i + neighbor[0]][
                                                                                j + neighbor[1]];

    for i in range(M):
        for j in range(M):
            # If the ignition factor is greater than the threshold and the fuel
            # is not 0
            if ignition_factor[i][j] >= i_threshold and f_grid[i][j] > 0:
                b_grid[i][j] = True
                # if fuel is 0
            if f_grid[i][j] == 0:
                b_grid[i][j] = False
    return b_grid[x][y]

def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    # TODO implement this function
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
    t=1;
    oneList_b_grid=[]
    for i in range(M):
        for j in range(M):
            oneList_b_grid.append(b_grid[i][j])
            #If oneList_b_grid is burning, continue to loop, the loop is
            #exactly the same as the second project
    while True in oneList_b_grid:
        ignition_factor = [[0] * M for i in range(M)]
        for i in range(M):
            for j in range(M):
                if b_grid[i][j] and f_grid[i][j]>=1:
                    f_grid[i][j] = f_grid[i][j] - 1;
                    for neighbor in normal_neighbor:
                        if i + neighbor[0] in range(M) and j + neighbor[1] in range(M):
                            if h_grid[i + neighbor[0]][j + neighbor[1]] > h_grid[i][j]:
                                factor = 2;
                            elif h_grid[i + neighbor[0]][j + neighbor[1]] < h_grid[i][j]:
                                factor = 0.5;
                            else:
                                factor = 1
                            ignition_factor[i + neighbor[0]][j + neighbor[1]] = 1 * factor + \
                                                                                ignition_factor[i + neighbor[0]][
                                                                                    j + neighbor[1]];
        # print(ignition_factor)
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
        # Contrast and then the landscape and before the burning, if not the
        # same as the current square burning, calculate the number of burning
        for j in range(M):
            if result[i][j]!=f_grid[i][j] :
                count=count+1;
    return (f_grid,count)


def plan_burn(f_grid, h_grid, i_threshold, town_cell):
    # TODO implement this function
    # pass

    M = len(f_grid)
    result = [[False] * M for i in range(M)];
    for i in range(M):
        for j in range(M):
            result[i][j] = f_grid[i][j]

    seeds = []
    for i in range(M):
        for j in range(M):
            seeds.append((i,j))

    safeSeeds=set()
    for seed in [(0,1)]:
        if seed == town_cell:
            continue
        print(seed)
        for w_direction in ['NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE', 'None']:
            for i in range(M):
                for j in range(M):
                    f_grid[i][j] = result[i][j];

            b_grid = [[False] * M for i in range(M)];
            b_grid[seed[0]][seed[1]] = True;

            normal_neighbor = [];
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    normal_neighbor.append([i, j])

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
            oneList_b_grid=[]
            for i in range(M):
                for j in range(M):
                    oneList_b_grid.append(b_grid[i][j])

            while True in oneList_b_grid:
                ignition_factor = [[0] * M for i in range(M)]
                for i in range(M):
                    for j in range(M):
                        if b_grid[i][j]:
                            f_grid[i][j] = f_grid[i][j] - 1;
                            for neighbor in normal_neighbor:
                                if i + neighbor[0] in range(M) and j + neighbor[1] in range(M):
                                    if h_grid[i + neighbor[0]][j + neighbor[1]] > h_grid[i][j]:
                                        factor = 1;
                                    elif h_grid[i + neighbor[0]][j + neighbor[1]] < h_grid[i][j]:
                                        factor = 0.25;
                                    else:
                                        factor = 0.5
                                    ignition_factor[i + neighbor[0]][j + neighbor[1]] = 1 * factor + ignition_factor[i + neighbor[0]][j + neighbor[1]];
                # print(ignition_factor)
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

            print(f_grid)
            if f_grid[town_cell[0]][town_cell[1]]!=result[town_cell[0]][town_cell[1]]:
                safeSeeds.add(seed);

    print(safeSeeds)

if __name__=="__main__":
    # filename="data.txt"
    # parse_scenario(filename=filename)
    plan_burn([[2, 2], [1, 2]], [[1, 2], [1, 2]], 2, (1, 1))