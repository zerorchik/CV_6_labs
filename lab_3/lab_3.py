from graphics import *
import numpy as np
import math as mt
import scipy

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

    print('\nВхідна матриця')
    print(prlpd)

    return prlpd

# # Масштабування та зміщення за допомогою "Лінійної інтерполяції"
# def scale_and_shift(prlpd, st, dx, dy, dz):
#     # Створення пустої матриці для зберігання результату
#     pr_xy = np.zeros_like(prlpd)
#
#     for i in range(len(prlpd)):
#         # Масштабування кожної точки
#         pr_xy[i][0] = prlpd[i][0] * st + dx
#         pr_xy[i][1] = prlpd[i][1] * st + dy
#         pr_xy[i][2] = prlpd[i][2] * st + dz
#         pr_xy[i][3] = prlpd[i][3]  # Зберігаємо останній елемент без змін
#
#     print('\nМастабування та зміщення')
#     print(pr_xy)
#
#     return pr_xy

# Клас кривих Безьє
class BezierCurve:
    def __init__(self, control_points):
        self.control_points = control_points

    def evaluate(self, t):
        n = len(self.control_points) - 1
        result = np.zeros_like(self.control_points[0])
        for i in range(n + 1):
            result += self.control_points[i] * self.bernstein(n, i, t)
        return result

    def scale(self, factor):
        scaled_control_points = [self.control_points * factor]
        return BezierCurve(scaled_control_points)

    def translate(self, translation):
        translated_control_points = [point + translation for point in self.control_points]
        return BezierCurve(translated_control_points)

    @staticmethod
    def bernstein(n, i, t):
        return scipy.special.comb(n, i) * (1 - t) ** (n - i) * t ** i

# Масштабування та зміщення за допомогою "кривих Безьє"
def scale_and_shift(prlpd, st, dx, dy, dz):
    # Створення пустої матриці для зберігання результату
    pr_xy = np.zeros_like(prlpd)

    for i in range(len(prlpd)):
        # Масштабування кожної точки
        bezier_x = BezierCurve(prlpd[i][0]).scale(st).translate(dx)
        bezier_y = BezierCurve(prlpd[i][1]).scale(st).translate(dy)
        bezier_z = BezierCurve(prlpd[i][2]).scale(st).translate(dz)

        # Отримання нових координат
        pr_xy[i][0] = bezier_x.evaluate(0.5)  # Вибір середньої точки
        pr_xy[i][1] = bezier_y.evaluate(0.5)  # Вибір середньої точки
        pr_xy[i][2] = bezier_z.evaluate(0.5)  # Вибір середньої точки
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
def prlpd_visualisation(win, pr_xy, color, color_mode):
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

    if not color_mode:
        obj_6 = Polygon(Point(Bx, By), Point(Cx, Cy), Point(Fx, Fy), Point(Ix, Iy))
        # obj_6.setFill(color)
        obj_6.draw(win)

    obj_5 = Polygon(Point(Mx, My), Point(Ax, Ay), Point(Dx, Dy), Point(Ex, Ey))
    if color_mode:
        obj_5.setFill(color[0])
    obj_5.draw(win)

    if not color_mode:
        obj_4 = Polygon(Point(Mx, My), Point(Ix, Iy), Point(Fx, Fy), Point(Ex, Ey))
        # obj_4.setFill(color)
        obj_4.draw(win)

    obj_3 = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy))
    if color_mode:
        obj_3.setFill(color[1])
    obj_3.draw(win)

    if not color_mode:
        obj_2 = Polygon(Point(Dx, Dy), Point(Cx, Cy), Point(Fx, Fy), Point(Ex, Ey))
        # obj_2.setFill(color)
        obj_2.draw(win)

    obj_1 = Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ix, Iy), Point(Mx, My))
    if color_mode:
        obj_1.setFill(color[2])
    obj_1.draw(win)

    return [obj_1, obj_3, obj_5]

# Видалення невидимих граней за алгоритмом "Плаваючого обрію"
def removing_faces(pr_dim, pr_xy, x_max, y_max, z_max, win):
    # Матриця без проекції
    aa_x = pr_dim[0, 0]
    aa_y = pr_dim[0, 1]
    aa_z = pr_dim[0, 2]
    
    bb_x = pr_dim[1, 0]
    bb_y = pr_dim[1, 1]
    bb_z = pr_dim[1, 2]
    
    ii_x = pr_dim[2, 0]
    ii_y = pr_dim[2, 1]
    ii_z = pr_dim[2, 2]
    
    mm_x = pr_dim[3, 0]
    mm_y = pr_dim[3, 1]
    mm_z = pr_dim[3, 2]
    
    #
    dd_x = pr_dim[4, 0]
    dd_y = pr_dim[4, 1]
    dd_z = pr_dim[4, 2]
    
    cc_x = pr_dim[5, 0]
    cc_y = pr_dim[5, 1]
    cc_z = pr_dim[5, 2]
    
    ff_x = pr_dim[6, 0]
    ff_y = pr_dim[6, 1]
    ff_z = pr_dim[6, 2]
    
    ee_x = pr_dim[7, 0]
    ee_y = pr_dim[7, 1]
    ee_z = pr_dim[7, 2]

    # Перевірка чи знаходяться грані в зоні видимості

    # Фронтальна та Верхня грані
    if (abs(aa_z-z_max) > abs(dd_z-z_max)) and (abs(bb_z-z_max) > abs(cc_z-z_max))  \
            and (abs(ii_z-z_max) > abs(ff_z-z_max)) and (abs(mm_z-z_max) > abs(ee_z-z_max)):
        flag_f = 1
    else:
        flag_f = 2
    print('flag_f =', flag_f)
    # Ліва та Права грані
    if (abs(dd_x - x_max) > abs(cc_x - x_max)) and (abs(aa_x - x_max) > abs(bb_x - x_max)) \
            and (abs(mm_x - x_max) > abs(ii_x - x_max)) and (abs(ee_x - x_max) > abs(ff_x - x_max)):
        flag_r = 1
    else:
        flag_r = 2
    print('flag_r =', flag_r)
    # Задня та Нижня грані
    if (abs(aa_y - y_max) > abs(mm_y - y_max)) and (abs(bb_y - y_max) > abs(ii_y - y_max)) \
            and (abs(cc_y - y_max) > abs(ff_y - y_max)) and (abs(dd_y - y_max) > abs(ee_y - y_max)):
        flag_p = 1
    else:
        flag_p = 2
    print('flag_p =', flag_p)

    # Проекція
    a_x = pr_xy[0, 0]
    a_y = pr_xy[0, 1]

    b_x = pr_xy[1, 0]
    b_y = pr_xy[1, 1]

    i_x = pr_xy[2, 0]
    i_y = pr_xy[2, 1]

    m_x = pr_xy[3, 0]
    m_y = pr_xy[3, 1]

    #
    d_x = pr_xy[4, 0]
    d_y = pr_xy[4, 1]

    c_x = pr_xy[5, 0]
    c_y = pr_xy[5, 1]

    f_x = pr_xy[6, 0]
    f_y = pr_xy[6, 1]

    e_x = pr_xy[7, 0]
    e_y = pr_xy[7, 1]

    # Ліва грань
    obj = Polygon(Point(a_x, a_y), Point(m_x, m_y), Point(e_x, e_y), Point(d_x, d_y))
    if flag_r == 2:
        obj.setFill('blue')
        obj.draw(win)
    # Права грань
    obj = Polygon(Point(b_x, b_y), Point(i_x, i_y), Point(f_x, f_y), Point(c_x, c_y))
    if flag_r == 1:
        obj.setFill('magenta')
        obj.draw(win)
    # Верхня грань
    obj = Polygon(Point(a_x, a_y), Point(b_x, b_y), Point(c_x, c_y), Point(d_x, d_y))
    if flag_p == 1:
        obj.setFill('indigo')
        obj.draw(win)
    # Нижня грань
    obj = Polygon(Point(m_x, m_y), Point(i_x, i_y), Point(f_x, f_y), Point(e_x, e_y))
    if flag_p == 2:
        obj.setFill('gray')
        obj.draw(win)
    # Тильна грань
    obj = Polygon(Point(a_x, a_y), Point(b_x, b_y), Point(i_x, i_y), Point(m_x, m_y))
    if flag_f == 2:
        obj.setFill('cyan')
        obj.draw(win)
    # Фронтальна грань
    obj = Polygon(Point(d_x, d_y), Point(c_x, c_y), Point(f_x, f_y), Point(e_x, e_y))
    if flag_f == 1:
        obj.setFill('purple')
        obj.draw(win)

    return

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

    teta_x = 160
    teta_y = 80

    color = ['blue', 'purple', 'indigo']

    # Головні виклики

    '''Монохром'''
    win = init_window(xw, yw)
    prlpd = init_figure()
    # Диметрія
    prlpd_2 = dimetri(prlpd, teta_x, teta_y)
    # Проекція на XY
    pr_xy_3 = project_xy(prlpd_2)
    # Масштабування та зміщення фігури
    pr_xy_3_scaled_center = scale_and_shift(pr_xy_3, st, dx, dy, dz)
    # Візуалізація МОНОХРОМУ фігури
    objs = prlpd_visualisation(win, pr_xy_3_scaled_center, color, color_mode=False)
    win.getMouse()
    win.close()

    '''Видалення граней'''
    win = init_window(xw, yw)
    prlpd = init_figure()
    # Диметрія
    prlpd_2 = dimetri(prlpd, teta_x, teta_y)
    # Проекція на XY
    pr_xy_3 = project_xy(prlpd_2)
    # Масштабування та зміщення фігури
    pr_xy_3_scaled_center = scale_and_shift(pr_xy_3, st, dx, dy, dz)
    # Візуалізація КОЛОР фігури З ВИДАЛЕНИМИ ГРАНЯМИ
    removing_faces(prlpd_2, pr_xy_3_scaled_center, (xw * 2), (yw * 2), (yw * 2), win)
    win.getMouse()
    win.close()

    '''Видалення граней + поворот'''
    # Кути повороту
    teta_x = 180
    teta_y = -90

    win = init_window(xw, yw)
    prlpd = init_figure()
    # Диметрія
    prlpd_2 = dimetri(prlpd, teta_x, teta_y)
    # Проекція на XY
    pr_xy_3 = project_xy(prlpd_2)
    # Масштабування та зміщення фігури
    pr_xy_3_scaled_center = scale_and_shift(pr_xy_3, st, dx, dy, dz)
    # Візуалізація повернутої КОЛОР фігури З ВИДАЛЕНИМИ ГРАНЯМИ
    removing_faces(prlpd_2, pr_xy_3_scaled_center, (xw * 2), (yw * 2), (yw * 2), win)
    win.getMouse()
    win.close()
