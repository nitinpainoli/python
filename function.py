#variable length argument in function

def sum(*b):
    
    c = 0 
    for i  in b:
        c = c + i
    print(c)
    
sum(12,1,3,4)


## keyword variable length argument
def person(name, **data):
    print(name)
    print(data)

person('nitin', city = 'dehradun', age = 28, mobile_no = '7895420767' )