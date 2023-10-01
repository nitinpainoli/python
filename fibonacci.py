range =  int(input("enter the range"))

n1 , n2 = 0,1
count = 0

while count < range:
    print(n1)
    temp = n1 + n2
    n1 = n2
    n2 = temp
    count += 1