def x_base(x):
    return int(x*(x+1)/2)

def y_scale(x,y):
    b = x + y - 2
    return int((x+b)*(b-x+1)/2)

def solution(x,y):
    return str(x_base(x) + y_scale(x,y))

test_1 = (3,2)
test_2 = (5,10)

result = solution(*test_1)
