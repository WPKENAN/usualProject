import re

def getWord(line):
    line2=''
    for i in line:
        if i<="Z" and i>="A" or i<="z" and i>="a":
            line2+=i

    return line2.lower()
while(1):
    flag_=True
    count_line={}
    count_anagram={}
    line=input("Enter line:")
    anagram=input("Enter anagram:")

    line=getWord(line)
    anagram=getWord(anagram)

    for word in line:
        if word not in count_line:
            count_line[word]=1
        else:
            count_line[word]+=1

    for word in anagram:
        if word not in count_anagram:
            count_anagram[word]=1
        else:
            count_anagram[word]+=1

    for word in count_line:
        if word not in count_anagram:
            flag_=False
            break;
        elif count_anagram[word]!=count_line[word]:
            flag_=False
            break;
    if flag_:
        print("Anagram!")
    else:
        print("Not an anagram.")

