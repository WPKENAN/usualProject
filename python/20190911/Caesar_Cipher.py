while(1):
    key=input("Enter key:")
    line=input("Enter line:")

    key=int(key)
    line=list(line)
    if key<0 or key>26:
        print("Invalid key!")
        continue
    for i in range(len(line)):
        if line[i]<="Z" and line[i]>="A":
            line[i]=chr((ord(line[i])-ord("A")+key)%26+ord("A"))
        elif line[i]<="z" and line[i]>="a":
            line[i] = chr((ord(line[i]) - ord("a") + key) % 26 + ord("a"))

    print("".join(str(i) for i in line))
