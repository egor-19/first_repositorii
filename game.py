from tkinter import *
import ctypes

window = Tk()
window.title("ИГРА ЖИЗНИ")
window.geometry("500x350")
window.resizable(width=False, height=False)


pole = [0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,1,1,1,0,0,0,
        0,0,0,0,0,0,0,0,0,1]

r = 6
c = 10


object = ctypes.CDLL('./game2.so')
object.rules.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int * (r*c), ctypes.c_int, ctypes.c_int]
object.rules.restype = ctypes.c_int

# Создание интерфейса
cell_size = 50  # размер клетки
canvas = Canvas(window, width=c*cell_size, height=r*cell_size, bg='red')
canvas.pack()



def draw_field():
    canvas.delete("all")
    # рисую клетку
    for i in range(r + 1):
        canvas.create_line(0, i*cell_size,c *cell_size, i*cell_size)
    for j in range(c + 1):
        canvas.create_line(j*cell_size, 0, j*cell_size, r*cell_size)
    # закрасить клеточку
    for y in range(r):
        for x in range(c):
            if pole[y*c+x] == 1:
                canvas.create_rectangle(x*cell_size, y*cell_size,(x+1)*cell_size, (y+1)*cell_size,fill='white')

# основная часть
button_frame = Frame(window)
button_frame.pack()

def do_rules(pole):
    pole2 = (ctypes.c_int * (r*c))()
    for y in range(r):
        for x in range(c):
            pole2[y*c+x] = object.rules(x,y, pole,r,c)
    return pole2

def next_step():
    global pole
    pole_c = (ctypes.c_int * (r*c))(*pole)
    new_pole = do_rules(pole_c)
    pole = list(new_pole)
    draw_field()

running = False

def start_stop():
    global running
    running = not running
    if running:
        auto_step()

def auto_step():
    if running:
        next_step()
        window.after(900, auto_step)


start_button = Button(button_frame, text="Старт/Стоп", command=start_stop)
start_button.pack(side=RIGHT)

# чтобы задавать начальную фигуру нажатием
def toggle_cell(event):
    x = event.x // cell_size
    y = event.y // cell_size
    if 0 <= x < c and 0 <= y < r:
        index = y * c + x
        pole[index] = 1 - pole[index]
        draw_field()

canvas.bind("<Button-1>", toggle_cell)



draw_field()
window.mainloop()