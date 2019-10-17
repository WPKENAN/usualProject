import sys
if __name__=="__main__":
    if len(sys.argv)<3:
        print("Too few arguments.")
    elif len(sys.argv)>3:
        print("Too many arguments.")
    else:
        try:
            w = int(sys.argv[1])
            h = int(sys.argv[2])
        except:
            print("Invalid argument.")

        if w<0 and h<0:
            print("Negative dimensions.")
        elif w<0:
            print("Negative width.")
        elif h<0:
            print("Negative height")
        else:
            for i in range(int(h)):
                print("*"*w)

