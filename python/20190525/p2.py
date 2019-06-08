import itertools
def comp10001go_valid_groups(strlists):

    if len(strlists)==0:#如果是空的就合法
        return True

    for strlist in strlists:#遍历所有的序列
        # print(comp10001go_score_group(strlist))
        if len(strlist)<=1:#如果本次列表是单个卡牌或者是空直接下一次循环
            continue
        if comp10001go_score_group(strlist)<0:#如果返回的值是正数肯定是合法的，不合法的都是负数
            return False

    return True


def comp10001go_score_group(strlist):
    valdict = {'0': 10, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'J': 11, 'Q': 12,
               'K': 13, 'A': 20};
    colordict = {'H': 0, 'D': 0, 'S': 1, 'C': 1}


    cardColor = []
    for item in strlist:
        if not item[0].upper() in valdict:
            return -1
        if not item[1].upper() in colordict:
            return -1;
        cardColor.append([valdict[item[0].upper()], item[1].upper()])
    # print(cardColor)

    # case1 If the group is a valid  N-of-a-kind
    if len(cardColor) > 1:
        result = 1;
        first = cardColor[0][0]
        flag = 0;
        for i in range(1, len(cardColor)):
            result = result * (i + 1);
            if cardColor[i][0] != first or cardColor[i][0]==20:
                flag = 1;
                break;
        if not flag:
            # print(result*first)
            return result * first

    # case2 If the group is a valid run
    if len(cardColor) > 2:
        result = 0;
        isAcolor = []
        isnAcolor = []
        for item in cardColor:
            if item[0] == 20:
                isAcolor.append(item)
            else:
                isnAcolor.append(item)
        isnAcolor.sort()

        # case2.1
        if len(isAcolor) != 0:
            for itemlist in itertools.permutations(isAcolor):
                newlist = [isnAcolor[0]];
                i = 1;
                j = 0;
                while i < len(isnAcolor):
                    if newlist[-1][0] != isnAcolor[i][0] - 1 and j < len(itemlist):
                        newlist.append([newlist[-1][0] + 1, itemlist[j][1]]);
                        j = j + 1;
                    else:
                        newlist.append(isnAcolor[i])
                        i = i + 1
                # print(newlist)
                if len(newlist) == len(cardColor):
                    flag = 0;
                    result = newlist[0][0];
                    for i in range(1, len(newlist)):
                        if newlist[i][0] == newlist[i - 1][0] + 1 and colordict[newlist[i][1]] != colordict[
                            newlist[i - 1][1]]:
                            result = result + newlist[i][0]
                            continue
                        else:
                            flag = 1
                            break;
                    if not flag:
                        # print(result)
                        return result
        else:  # case2.2
            flag = 0;
            result = isnAcolor[0][0];
            for i in range(1, len(isnAcolor)):
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

if __name__ == "__main__":
    print(comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C']]))
    print(comp10001go_valid_groups([['KC', 'KH', 'KS', 'AD'], ['2C']]))
    print(comp10001go_valid_groups([['KC', 'KH', 'KS', 'KD'], ['2C', '3H']]))
