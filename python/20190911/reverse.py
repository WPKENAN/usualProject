while(1):
    try:
        ip = input()
        print(ip[::-1])
    except EOFError:
        # print("over")
        exit(0)
