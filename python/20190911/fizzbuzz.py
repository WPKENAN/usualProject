while(1):
    ip=input()
    ip=int(ip)

    if ip%3==0 and ip%5==0:
        print("FizzBuzz")
    elif ip%3==0:
        print("Fizz")
    elif ip%5==0:
        print("Buzz")
    else:
        print(ip)