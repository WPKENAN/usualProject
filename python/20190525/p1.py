import itertools

import itertools


def comp10001go_score_group(strlist):
    # 建立字典，字符跟数字对应
    valdict = {'0': 10, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'J': 11, 'Q': 12,
               'K': 13, 'A': 20};
    #建立字典，颜色对应，红色0，黑色1
    colordict = {'H': 0, 'D': 0, 'S': 1, 'C': 1}

    #循环第一列是数字，第二列是颜色
    cardColor = []
    for item in strlist:
        cardColor.append([valdict[item[0].upper()], item[1].upper()])
    # print(cardColor)

    # case1 If the group is a valid  N-of-a-kind
    if len(cardColor) > 1:#如果牌的数量大于1
        result = 1;
        first = cardColor[0][0]
        flag = 0;#标记牌是否相同
        for i in range(1, len(cardColor)):
            result = result * (i + 1);
            if cardColor[i][0] != first:#如果牌的数值不全部相等
                flag = 1;
                break;
        if not flag:#如果牌的数字完全相同
            # print(result*first)
            return result * first

    # case2 If the group is a valid run
    if len(cardColor) > 2:#判断牌的数量是否大于2
        result = 0;
        isAcolor = []#临时存储A的所有牌
        isnAcolor = []#临时存储不是A的所有牌
        for item in cardColor:
            if item[0] == 20:#如果是A
                isAcolor.append(item)
            else:#不是A
                isnAcolor.append(item)
        isnAcolor.sort()#对不是A的那个序列进行从小到大的排序

        # case2.1
        if len(isAcolor) != 0:#如果整个序列中有A，即isAcolor不为空

            for itemlist in itertools.permutations(isAcolor):#对isAcolor进行全排列
                newlist = [isnAcolor[0]];#newlist用来存储isAcolor，isnAcolor合并之后的新的列表
                i = 1;
                j = 0;
                while i < len(isnAcolor):#如果i小与isnAcolor的长度
                    # 如果isnAcolor[i][0]-1不等于newlist最后一个值的，即不连续，则要插入A来尝试使列表连续
                    if newlist[-1][0] != isnAcolor[i][0] - 1 and j < len(itemlist):
                        newlist.append([newlist[-1][0] + 1, itemlist[j][1]]);
                        j = j + 1;
                    else:#如果isnAcolor[i][0]-1等于newlist最后一个值的，则直接插入isnAcolor[i]即可
                        newlist.append(isnAcolor[i])
                        i = i + 1
                # print(newlist)
                if len(newlist) == len(cardColor):#如果合并的长度与原长度相等
                    flag = 0;
                    result = newlist[0][0];
                    for i in range(1, len(newlist)):#这里就是判断合并之后的序列是否符合连续，且颜色不相等这两个要求
                        if newlist[i][0] == newlist[i - 1][0] + 1 and colordict[newlist[i][1]] != colordict[
                            newlist[i - 1][1]]:
                            result = result + newlist[i][0]
                            continue
                        else:#如果不合格就跳出进行下一次
                            flag = 1
                            break;
                    if not flag:#如果合格直接输出
                        # print(result)
                        return result
        else:  # case2.2 如果整个序列中没有A，即isAcolor为空
            flag = 0;
            result = isnAcolor[0][0];
            for i in range(1, len(isnAcolor)):#这里就是判断序列是否符合连续，且颜色不相等这两个要求
                result = result + isnAcolor[i][0]
                if colordict[isnAcolor[i][1]] == colordict[isnAcolor[i - 1][1]] or isnAcolor[i][0] == isnAcolor[i - 1][
                    0]:
                    flag = 1;
                    break;

            if not flag:
                return result
                # print(result)

    result = 0;
    for i in range(len(cardColor)):
        result = result + cardColor[i][0]
    # print(-result)
    return -result


if __name__=="__main__":
    print(comp10001go_score_group(['4S', '2C', '3D']))
    print(comp10001go_score_group(['4C', '4H', '4S']))
    print(comp10001go_score_group(['KC', 'KH', 'KS', 'KD']))
    print(comp10001go_score_group(['5H', '4S', '2C', 'AD']))
    print(comp10001go_score_group(['2C', 'AD', '4S']))
    print(comp10001go_score_group(['3C', '4H', 'AS']))
    print(comp10001go_score_group(['4H', '0H', 'JC', '2H', '7H']))
    print(comp10001go_score_group(['2C', '3D']))
    print(comp10001go_score_group(['4C', '4H', '3S']))
    print(comp10001go_score_group(['2C', '3D', '4H']))