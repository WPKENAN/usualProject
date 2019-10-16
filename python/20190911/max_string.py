print("Input 3 strings and find what string is the longest")
a=input()
b=input()
c=input()

if len(a)==len(b)==len(c)==0:
    print("All strings are empty")
elif len(a)==len(b)==len(c):
    print("All strings are the same length")
else:
    if len(a)>=len(b) and len(a)>len(c):
        print("\"{}\" is the longest string".format(a))
    elif len(b)>=len(a) and len(b)>len(c):
        print("\"{}\". is the longest string".format(b))
    else:
        print("\"{}\" is the longest string".format(c))

