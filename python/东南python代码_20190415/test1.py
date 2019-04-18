cal={}
    for ft in fts:
        cal[ft] = {}
        for man in bestie_dict[unknown_user]:
            if ft in feat_dict[man]:
                if feat_dict[man][ft] not in cal[ft]:
                    cal[ft][feat_dict[man][ft]] = 1;
                else:
                    cal[ft][feat_dict[man][ft]] = cal[ft][feat_dict[man][ft]] + 1

        count = 0
        for item in cal[ft]:
            count = cal[ft][item] + count

        if count==0:
            for man in friend_second_besties(unknown_user, bestie_dict):
                if ft in feat_dict[man]:
                    if feat_dict[man][ft] not in cal[ft]:
                        cal[ft][feat_dict[man][ft]] = 1;
                    else:
                        cal[ft][feat_dict[man][ft]] = cal[ft][feat_dict[man][ft]] + 1

    result={}
    for ft in fts:
        result[ft]=[]
        count = 0
        temp=[]
        for item in cal[ft]:
            count = cal[ft][item] + count
        if count==0:
            temp=[]
            continue

        max_num=0;
        for item in cal[ft]:
            if cal[ft][item] > max_num:
                max_num = cal[ft][item];

        for item in cal[ft]:
            if cal[ft][item] == max_num:
                temp.append(item)

        temp.sort()
        result[ft]=temp
    print(result)
    return result