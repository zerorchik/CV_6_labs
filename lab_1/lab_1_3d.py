from graphics import *
import numpy as np
import math as mt

import imageio
from PIL import ImageGrab

# Ініціалізація вікна
def init_window(xw, yw):
    win = GraphWin('Паралелепіпед', xw, yw)
    win.setBackground('white')

    return win

# Ініціалізація паралелепіпеда
def init_figure():
    # Вхідна матриця фігури
    prlpd = np.array([[0, 0, 0, 1],
                      [2, 0, 0, 1],
                      [2, 1, 0, 1],
                      [0, 1, 0, 1],
                      [0, 0, 2, 1],
                      [2, 0, 2, 1],
                      [2, 1, 2, 1],
                      [0, 1, 2, 1]])

    print('Вхідна матриця')
    print(prlpd)

    return prlpd

# Масштабування та зміщення
def scale_and_shift(prlpd, st, dx, dy, dz):
    # Створення пустої матриці для зберігання результату
    pr_xy = np.zeros_like(prlpd)

    for i in range(len(prlpd)):
        # Масштабування кожної точки
        pr_xy[i][0] = prlpd[i][0] * st + dx
        pr_xy[i][1] = prlpd[i][1] * st + dy
        pr_xy[i][2] = prlpd[i][2] * st + dz
        pr_xy[i][3] = prlpd[i][3]  # Зберігаємо останній елемент без змін

    print('\nМастабування та зміщення')
    print(pr_xy)

    return pr_xy

# Проекція на XY (Z=0)
def project_xy(figure):
   f = np.array(
       [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]])
   ft = f.T
   pr_xy = figure.dot(ft)

   print('\nПроекція на XY')
   print(pr_xy)

   return pr_xy

# Аксонометрія
def dimetri(figure, teta_x, teta_y):
    teta_rx = (3 / 14 * teta_x) / 180
    teta_ry = (3 / 14 * teta_y) / 180

    f_1 = np.array(
        [[mt.cos(teta_rx),  0,  -mt.sin(teta_rx),   0],
         [0,                1,  0,                  0],
         [mt.sin(teta_rx),  0,  mt.cos(teta_rx),    1],
         [0,                0,  0,                  0]])
    ft_1 = f_1.T
    pr_xy_1 = figure.dot(ft_1)

    f_2 = np.array(
        [[1,    0,                  0,                  0],
         [0,    mt.cos(teta_ry),    mt.sin(teta_ry),    0],
         [0,    -mt.sin(teta_ry),   mt.cos(teta_ry),    0],
         [0,    0,                  0,                  1]])
    ft_2 = f_2.T
    pr_xy_2 = pr_xy_1.dot(ft_2)

    print('\nДиметрія')
    print(pr_xy_2)

    return pr_xy_2

# Обертання навколо X
def rotate_x (figure, teta_x):
    teta_rx = (3 / 14 * teta_x) / 180

    f = np.array(
        [[1,    0,                  0,                  0],
         [0,    mt.cos(teta_rx),    mt.sin(teta_rx),    0],
         [0,    -mt.sin(teta_rx),   mt.cos(teta_rx),    0],
         [0,    0,                  0,                  1]])
    ft = f.T
    pr_xy = figure.dot(ft)

    print('\nОбертання навколо Х')
    print(pr_xy)

    return pr_xy

# Побудова паралелепіпеда
def prlpd_visualisation(win, pr_xy, color):
    Ax = pr_xy[0, 0]
    Ay = pr_xy[0, 1]
    Bx = pr_xy[1, 0]
    By = pr_xy[1, 1]
    Ix = pr_xy[2, 0]
    Iy = pr_xy[2, 1]
    Mx = pr_xy[3, 0]
    My = pr_xy[3, 1]

    Dx = pr_xy[4, 0]
    Dy = pr_xy[4, 1]
    Cx = pr_xy[5, 0]
    Cy = pr_xy[5, 1]
    Fx = pr_xy[6, 0]
    Fy = pr_xy[6, 1]
    Ex = pr_xy[7, 0]
    Ey = pr_xy[7, 1]

    # print(f'A ({Ax}, {Ay})'); print(f'B ({Bx}, {By})'); print(f'I ({Ix}, {Iy})');  print(f'M ({Mx}, {My})');
    # print(f'D ({Dx}, {Dy})'); print(f'C ({Cx}, {Cy})'); print(f'F ({Fx}, {Fy})'); print(f'E ({Ex}, {Ey})');

    obj_6 = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Fx, Fy), Point(Ix, Iy))
    obj_6.setFill(color)
    obj_6.draw(win)

    obj_5 = Polygon(Point(Mx, My), Point(Ax, Ay), Point(Dx, Dy), Point(Ex, Ey))
    obj_5.setFill(color)
    obj_5.draw(win)

    # obj_4 = Polygon(Point(Mx, My), Point(Ix, Iy), Point(Fx, Fy), Point(Ex, Ey))
    # obj_4.setFill(color)
    # obj_4.draw(win)

    obj_3 = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    obj_3.setFill(color)
    obj_3.draw(win)

    # obj_2 = Polygon(Point(Dx, Dy), Point(Cx, Cy), Point(Fx, Fy), Point(Ex, Ey))
    # obj_2.setFill(color)
    # obj_2.draw(win)

    obj_1 = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ix, Iy), Point(Mx, My))
    obj_1.setFill(color)
    obj_1.draw(win)

    return [obj_1, obj_3, obj_5, obj_6]

# Отримання зображень з вікна
def get_image(win):
    # Отримуємо зображення з вікна
    img = ImageGrab.grab(bbox=(win.master.winfo_x(), win.master.winfo_y(),
                               win.master.winfo_x() + win.master.winfo_width(),
                               win.master.winfo_y() + win.master.winfo_height()))
    img = img.convert('RGB')  # Перетворюємо у RGB формат

    return img

# Блок головних викликів
if __name__ == '__main__':

    # Константи
    xw = 600  # ширина вікна
    yw = 600  # висота вікна
    st = 100  # розмір сторони фігури

    # Обчислення зсуву для центру вікна
    dx = (xw - st) / 2
    dy = (yw - st) / 2
    dz = dy

    teta_x = 180
    teta_y = -90

    # Змінні для зберігання кольорів
    colors = ['gray', 'orange']

    # Створення списку для зберігання зображень
    frames = []

    # Головні виклики
    win = init_window(xw, yw)
    prlpd = init_figure()

    angle = 0
    i = 0
    while not win.isClosed():

        # Збереження зображення з вікна
        frame = get_image(win)
        frames.append(frame)

        win.delete("all")  # Очищаємо вікно

        # Обертання фігури
        prlpd_rotated = rotate_x(prlpd, angle)
        # Диметрія
        prlpd_2 = dimetri(prlpd_rotated, teta_x, teta_y)
        # Проекція на XY
        pr_xy_3 = project_xy(prlpd_2)
        # Масштабування та зміщення фігури
        pr_xy_3_scaled_center = scale_and_shift(pr_xy_3, st, dx, dy, dz)
        # Візуалізація фігури
        objs = prlpd_visualisation(win, pr_xy_3_scaled_center, colors[i])

        win.update()  # Оновлюємо вікно

        # Збереження зображення з вікна
        frame = get_image(win)
        frames.append(frame)

        i += 1
        if i >= len(colors):
            i = 0
        angle += 60
        time.sleep(0.1)  # Затримка для анімації

        for obj in objs:  # Закриваємо об'єкти
            obj.undraw()
        time.sleep(0.2)  # Затримка для анімації

        # Збереження зображення з вікна
        frame = get_image(win)
        frames.append(frame)

        if win.checkMouse():
            win.close()

    # Зберігаємо анімацію у форматі GIF
    imageio.mimsave("animation.gif", frames)