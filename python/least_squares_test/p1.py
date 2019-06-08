import os

class People:
    def __init__(self,name,tel,address):
        self.name=name;
        self.tel=tel
        self.address=address


def option(path):
    file = open(path)
    contents = file.readlines();
    file.close()

    address = {}
    for item in contents:
        item = item.strip('\n').split(',')
        address[item[0]] = [item[1], item[2]]
    print(address)

    while 1:
        print("0 显示信息\n1 添加信息\n2 退出系统\n")
        op = input("请输入要执行的操作:")
        if not op in ['0', '1', '2']:
            print("error")
            continue
        op = int(op)
        if op == 0:
            print(address)
        elif op == 1:
            name = input("input name: ")
            tel = input("input tel: ")
            addr = input("input address: ")
            address[name] = [tel, addr]
        elif op == 2:
            print("exit system")
            file = open(path, 'w')
            for key in address.keys():
                file.write("{},{},{}\n".format(key, address[key][0], address[key][1]))
            file.close()
            exit(0)
        else:
            continue
if __name__=="__main__":
    path='./address.csv'
    if not os.path.exists(path):
        tmp=open(path,'w')
        tmp.close()

    option(path)






