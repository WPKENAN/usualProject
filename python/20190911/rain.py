answer=input("Is it currently raining? ")
if answer.upper()=="YES":
    print("You should take the bus.")
elif answer.upper()=="NO":
    distance=input("How far in km do you need to travel? ")
    distance=float(distance)
    if distance>=10:
        print("You should ride your bus.")
    elif distance <10 and distance>=4:
        print("You should ride your bike.")
    else:
        print("You should walk.")
