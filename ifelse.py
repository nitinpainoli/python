num1 = int(input("enter the first number"))
num2 = int(input("enter the secont number"))
num3 = int(input("enter the third number"))

if num1 > num2 and num1 > num3:
    print(num1, "is grater")
elif num2 > num1 and num2 > num3:
    print(num2, "is grater")
else:
     print(num3, "is grater")