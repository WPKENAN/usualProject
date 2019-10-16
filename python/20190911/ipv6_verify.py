ip=input("Please enter an IP address:")
ip=ip.split(':')

def valid(character):
    if character <= 'F' and character>='A' or character <= 'f' and character>='a' or character <= '9' and character>='0':
        return True
    return False
if len(ip)!=8:
    print("It is not a valid IPv6 address.")

flag_=True
for i in range(8):
    if len(ip[i])==1 and valid(ip[i]):
        continue
    elif len(ip[i]) == 1 and valid(ip[i]):
        flag_ = False
        break;
    elif len(ip[i])>4:
        flag_=False
        break;
    else:
        for j in ip[i]:
            if not valid(j):
                flag_=False
                break;
    if not flag_:
        break;

if flag_:
    print("It is a valid IPv6 address.")
else:
    print("It is not a valid IPv6 address.")
