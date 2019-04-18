def get_friendly_dict(friend_list):
    bestie_dict={};
    for item in friend_list:
        if item[0] not in bestie_dict:
            bestie_dict[item[0]]=set();
        if item[1] not in bestie_dict:
            bestie_dict[item[1]] = set();
        bestie_dict[item[0]].add(item[1]);
        bestie_dict[item[1]].add(item[0]);

    print(bestie_dict)
    return bestie_dict

def friend_besties(individual,bestie_dict):
    f_best = []
    if individual not in bestie_dict:
        print("[]")
        return []
    for item in bestie_dict[individual]:
        f_best.append(item);
    f_best.sort()
    # print(f_best)
    return f_best

def friend_second_besties(individual,bestie_dict):
    if individual not in bestie_dict:
        return []

    all_second=set();
    for best_friend in bestie_dict[individual]:
        for second_friend in bestie_dict[best_friend]:
            all_second.add(second_friend)


    only_second = []
    for item in all_second:
        if item in bestie_dict[individual] or item == individual:
            continue
        only_second.append(item)

    return only_second


def besties_coverage(individuals, bestie_dict, relationship_list):
    # TODO write function
    all_people = set()
    for item in bestie_dict:
        all_people.add(item)
        for item_sub in bestie_dict[item]:
            all_people.add(item_sub)

    allcount = len(all_people)

    if len(individuals) == 0:
        print(0)
        return 0.0

    if individuals[0] not in bestie_dict:
        print(0)
        return 0.0

    num = len(bestie_dict[individuals[0]])

    if relationship_list == []:
        print(num/allcount)
        return num / allcount

    for i in range(len(relationship_list)):
        num = num + len(relationship_list[i](individuals[0], bestie_dict))

    print(num/allcount)
    return num / allcount


def friendly_prediction(unknown_user, features, bestie_dict, feat_dict):
    # TODO implement this function

    cal = {} #作为特征字典的字典
    for ft in features: #遍历每一种特征学校，作者等等
        cal[ft] = {} #对每一类特征建立一个字典，比如cal['school']:因为学校有很多种，统计不同学校的数量
        if unknown_user in bestie_dict: #如果best_dic中有这个人的信息，即bestie_dict['unknown_user']存在
            for man in bestie_dict[unknown_user]: #遍历他的最好的朋友
                if man in feat_dict: #如果他的当前最好的朋友，在feat_dict中找得到
                    if ft in feat_dict[man]: #feat_dict[man]指的是man这个人的一些特征，如果这个人含有tf这个特征，比如含有school这个特征
                        if feat_dict[man][ft] not in cal[ft]:#看一下cal[ft]中有没有这个特征的信息，比如这个tf是学校，但是看一下他的学校有没有存在cal[ft],不存在的化，初始化,计数为1，第一次出现
                            cal[ft][feat_dict[man][ft]] = 1
                        else:#else说明，存在这个学校，增加计数就行了比如，前面已经出现了清华大学，再次出现计数增加1就行了
                            gg = feat_dict[man][ft]
                            cal[ft][gg] = cal[ft][gg] + 1

            count = 0 #这个计数主要是为了看最好的朋友如果当前特征都是0，就需要看第二好的朋友了，题目要求，比如大家的学校信息都不存在
            for item in cal[ft]:
                count = cal[ft][item] + count

            if count == 0:#如果计数是0，需要在第二好的朋友中查找
                for man in friend_second_besties(unknown_user, bestie_dict):#在第二好的朋友中重复，在第一好的朋友中所做的事情
                    if ft in feat_dict[man]:
                        if feat_dict[man][ft] not in cal[ft]:
                            cal[ft][feat_dict[man][ft]] = 1
                        else:
                            gg = feat_dict[man][ft]
                            cal[ft][gg] = cal[ft][gg] + 1

    print(cal)
    result = {}#存出结果
    for ft in features: #遍历所有需要输出的特征ft
        result[ft] = []#初始化
        count = 0
        temp = []
        for item in cal[ft]:
            count = cal[ft][item] + count
        if count == 0:
            temp = []
            continue

        max_num = 0
        for item in cal[ft]:
            if cal[ft][item] > max_num:
                max_num = cal[ft][item]#记录出现次数最多的，特征值，比如清华有两个，北大有两个，中科大一个，那么max_num=2

        for item in cal[ft]:
            if cal[ft][item] == max_num:#把并列第一个加入结果中，在这个例子中，学校应该加入，清华和北大，出现次数并列第一
                temp.append(item)

        temp.sort() #题目要求排序输出
        result[ft] = temp

    # print(result)
    return result












#{'kim': {'glenn', 'sandy', 'alex'}, 'sandy': {'kim', 'alex'}, 'alex': {'sandy', 'kim'}, 'glenn': {'kim'}}
if __name__=="__main__":
    # get_bestie_dict([('kim', 'sandy'), ('sandy', 'alex'), ('alex', 'glenn'), ('glenn', 'kim')])

    # friend_list=[('kim', 'sandy'), ('alex', 'sandy'), ('kim', 'alex'), ('kim', 'glenn')];
    # bestie_dict=get_friendly_dict(friend_list)
    # #
    # # friend_besties('kim', bestie_dict)
    # # friend_besties('ali',bestie_dict)
    # #
    # # friend_second_besties('kim',bestie_dict)
    # # friend_second_besties('glenn',bestie_dict)
    #
    # friend_besties('kim', {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},'glenn': {'kim'}})
    # friend_besties('ali', {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},'glenn': {'kim'}})
    # besties_coverage(['glenn'], {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'}, 'glenn': {'kim'}}, [friend_besties])

    # besties_coverage(['glenn'], {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},'glenn': {'kim'}}, [])
    # besties_coverage(['glenn'], {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},
    #                              'glenn': {'kim'}}, [friend_besties])
    #
    # besties_coverage(['glenn'], {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},
    #                              'glenn': {'kim'}}, [friend_second_besties])
    #
    # besties_coverage(['glenn'], {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},
    #                              'glenn': {'kim'}}, [friend_besties,friend_second_besties])

    friendly_prediction('glenn', {'favourite author', 'university'}, {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'}, 'glenn': {'kim'}},
                        {'glenn': {'university': ''},
                         'kim': {'favourite author': 'AA Milne'},
                         'sandy': {'favourite author': 'JRR Tolkien', "university": "University of Melbourne"},
                         'alex': {'favourite author': 'AA Milne', 'university': 'Monash University'}})

    friendly_prediction('kim', {'birthplace'},
                        {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},
                         'glenn': {'kim'}}, {'glenn': {'university': ''}, 'kim': {'favourite author': 'AA Milne'},
                                             'sandy': {'favourite author': 'JRR Tolkien',
                                                       "university": "University of Melbourne"},
                                             'alex': {'favourite author': 'AA Milne',
                                                      'university': 'Monash University'}})
    friendly_prediction('kim', {'university'},
                        {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},'glenn': {'kim'}},
                        {'glenn': {'university': ''},
                         'kim': {'favourite author': 'AA Milne'},
                         'sandy': {'favourite author': 'JRR Tolkien', "university": "University of Melbourne"},
                         'alex': {'favourite author': 'AA Milne','university': 'Monash University'}})
    #
    friendly_prediction('', {'university'},
                        {'kim': {'sandy', 'alex', 'glenn'}, 'sandy': {'kim', 'alex'}, 'alex': {'kim', 'sandy'},
                         'glenn': {'kim'}},
                        {'glenn': {'university': ''},
                         'kim': {'favourite author': 'AA Milne'},
                         'sandy': {'favourite author': 'JRR Tolkien', "university": "University of Melbourne"},
                         'alex': {'favourite author': 'AA Milne', 'university': 'Monash University'}})

