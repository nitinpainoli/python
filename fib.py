# def fib(n):
#     a = 0
#     b = 1
    
#     if (n == 1):
#         print(a)
#     elif (n <=0 ):
#          print("enter wrong output")
#     else:
#         print(a)
#         print(b)
#         for i in range(2,n):
#             c = a + b
#             a = b
#             b = c
#             print(c)

def fibchecker(n):
    a = 0
    b = 1
    
    if (n == 1):
        print(a)
    elif (n <=0 ):
         print("enter wrong output")
    else:
        print(a)
        print(b)
        for i in range(2,n):
            c = a + b
            a = b
            b = c
            if (c >= n):
                break
            else:
                print(c)

    
    
if __name__ ==  '__main__':
    #fib(0)
    fibchecker(100)