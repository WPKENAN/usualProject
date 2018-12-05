def createDatabase(filePath):
    L=[]
    f=open(filePath);
    content=f.readlines();
    for row in content:
        temp=row.strip('\n').split(',');
        temp[3]=float(temp[3]);
        L.append(temp)

    return L;

def DisplayMenu():
    print("Here are some options for you: ")
    print("1. Print List of CDs");
    print("2. Sort CDs by Title");
    print("3. Sort CDs by Artist");
    print("4. Sort CDs by Genre");
    print("5. Sort CDs by Price");
    print("6. Find All CDs by Title")
    print("7. Find All CDs by Artist")
    print("8. Find All CDs by Genre")
    print("9. Find All CDs with Price at Most X")
    print("10. Quit")

def PrintList(L):
    for i in range(len(L)):
        print("%d: %s,%s,%s,%f"%(i+1,L[i][0],L[i][1],L[i][2],L[i][3]));

def SortByTitle(L):
    Ltemp=L.copy();#把L 复制给 Ltemp 防止原始L被更改
    for i in range(len(Ltemp)):
        for j in range(i,len(Ltemp)):
            if Ltemp[i][0].lower()>Ltemp[j][0].lower():
                temp=Ltemp[i];
                Ltemp[i]=Ltemp[j];
                Ltemp[j]=temp;

    return Ltemp;

def SortByArtist(L):
    Ltemp = L.copy();  # 把L 复制给 Ltemp 防止原始L被更改
    for i in range(len(Ltemp)):
        for j in range(i, len(Ltemp)):
            if Ltemp[i][1].lower() > Ltemp[j][1].lower():
                temp = Ltemp[i];
                Ltemp[i] = Ltemp[j];
                Ltemp[j] = temp;

    return Ltemp;

def SortByGenre(L):
    Ltemp = L.copy();  # 把L 复制给 Ltemp 防止原始L被更改
    for i in range(len(Ltemp)):
        for j in range(i, len(Ltemp)):
            if Ltemp[i][2].lower() > Ltemp[j][2].lower():
                temp = Ltemp[i];
                Ltemp[i] = Ltemp[j];
                Ltemp[j] = temp;

    return Ltemp;

def SortByPrice(L):
    Ltemp = L.copy();  # 把L 复制给 Ltemp 防止原始L被更改
    for i in range(len(Ltemp)):
        for j in range(i, len(Ltemp)):
            if Ltemp[i][3] > Ltemp[j][3]:
                temp = Ltemp[i];
                Ltemp[i] = Ltemp[j];
                Ltemp[j] = temp;

    return Ltemp;

def FindByTitle(L,str):
    Ltemp=[];
    for row in L:
        if row[0]==str:
            Ltemp.append(row);
    return Ltemp;

def FindByArtist(L,str):
    Ltemp=[];
    for row in L:
        if row[1]==str:
            Ltemp.append(row);
    return Ltemp;

def FindByGenre(L,str):
    Ltemp=[];
    for row in L:
        if row[2]==str:
            Ltemp.append(row);
    return Ltemp;

def FindByPrice(L,price):
    Ltemp=[];
    for row in L:
        if row[3]<=price:
            Ltemp.append(row);
    return Ltemp;

def test(L):
    Ltemp=L.copy()
    Ltemp[99]=['dada','dad','da','dw']

if __name__=="__main__":
    filePath = 'C:/Users/Anzhi/Desktop/file.txt';
    L=createDatabase(filePath);
    while(1):
        DisplayMenu();
        option=float(input("Please input your option(1-10): "));
        if option>10 or option<1:
            print("Input error")
            continue;

        if option==1:
            PrintList(L);
        elif option==2:
            PrintList(SortByTitle(L));
        elif option==3:
            PrintList(SortByArtist(L));
        elif option==4:
            PrintList(SortByGenre(L));
        elif option==5:
            PrintList(SortByPrice(L));
        elif option==6:
            str=input("Please input the Title you search: ");
            PrintList(FindByTitle(L,str));
        elif option==7:
            str = input("Please input the Artist you search: ");
            PrintList(FindByArtist(L, str));
        elif option==8:
            str = input("Please input the Genre you search: ");
            PrintList(FindByGenre(L, str));
        elif option==9:
            price = float(input("Please input the Price you search: "));
            PrintList(FindByPrice(L, price));
        elif option==10:
            break;
        else:
            continue;
        print("********************************************************************")


    # PrintList(SortByTitle(L))
    # PrintList(FindByPrice(L,50))
    # test(L)
    # PrintList(L)




