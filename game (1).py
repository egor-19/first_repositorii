import ctypes
pole = [ 0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,1,1,1,0,0,0,
         0,0,0,0,0,0,0,0,0,0 ] 

r = 6
c = 10

object = ctypes.CDLL('./game2.so')
object.rules.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_int * (r*c),ctypes.c_int,ctypes.c_int]
object.rules.restype = ctypes.c_int




def print_field( field):
    for y in range(r):
        for x in range(c):
            print(field[y*c+x], end=' ')
        print()






#    в пустой (мёртвой) клетке, с которой соседствуют три живые клетки, зарождается жизнь;
#    если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
#   в противном случае (если живых соседей меньше двух или больше трёх) клетка умирает 
#(«от одиночества» или «от перенаселённости»).





def do_rules(pole):
    pole2 = (ctypes.c_int * (r*c))()
    for y in range(r):
        for x in range(c):
            pole2[y*c+x]=object.rules(x,y,pole,r,c)
    return pole2


def copy_py_to_c (pole):
    my_array = (ctypes.c_int * (r*c))()
    for y in range(r):
        for x in range(c):
            my_array[y*c+x] = pole[y*c+x]
    return my_array


#int   <- type
#int()  <- 0



'''(y,x)
101
01+    <- 1, 2
001

...
10101+001
     ^
012345

y*ROWS+x'''

pole_c = copy_py_to_c(pole)
print("Исходное поле:")
print_field(pole_c)


print()
new_pole = do_rules(pole_c)
print("Поле после применения правил:")
print_field(new_pole)
