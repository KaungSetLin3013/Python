def AgeVerification(age =int(input("Please input your age. => "))):
    if age>=18:
        print("You are old enough")
        return True
    else:
        print("You are too young")
        return False

print(AgeVerification())