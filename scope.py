a  = 15

def scope():
    global a
    a = 10
    print(a)

scope()
print(a)