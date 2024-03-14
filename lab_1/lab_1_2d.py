from graphics import *
import math as mt
import time

import imageio
from PIL import ImageGrab

# Ініціалізація вікна і фігури
def init_window(text, xw, yw, size_x, size_y, center_x, center_y):
    # Ініціалізація вікна
    win = GraphWin(text, xw, yw)
    win.setBackground('white')

    # Координати вершин ромба в центрі вікна
    x1 = center_x - size_x / 2
    y1 = center_y
    x2 = center_x
    y2 = center_y + size_y / 2
    x3 = center_x + size_x / 2
    y3 = center_y
    x4 = center_x
    y4 = center_y - size_y / 2

    # Малювання ромба перед обертанням
    diamond = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
    diamond.setOutline("gray")
    diamond.setFill("gray")
    diamond.draw(win)

    return win, x1, y1, x2, y2, x3, y3, x4, y4

# Поворот фігури на кут тета
def rotation(win, x1, y1, x2, y2, x3, y3, x4, y4):
    # Вибір кута тета
    print('Оберіть кут обертання фігури (0-360):')
    rotation_angle = int(input('angle:'))
    if rotation_angle in range(0, 361):
        # Перетворення кута обертання в радіани
        theta = mt.radians(rotation_angle)

        # Обчислення центра ромба
        center_x = (x1 + x2 + x3 + x4) / 4
        center_y = (y1 + y2 + y3 + y4) / 4

        # Обчислення нових координат ромба після обертання
        x1_rotated = center_x + (x1 - center_x) * mt.cos(theta) - (y1 - center_y) * mt.sin(theta)
        y1_rotated = center_y + (x1 - center_x) * mt.sin(theta) + (y1 - center_y) * mt.cos(theta)

        x2_rotated = center_x + (x2 - center_x) * mt.cos(theta) - (y2 - center_y) * mt.sin(theta)
        y2_rotated = center_y + (x2 - center_x) * mt.sin(theta) + (y2 - center_y) * mt.cos(theta)

        x3_rotated = center_x + (x3 - center_x) * mt.cos(theta) - (y3 - center_y) * mt.sin(theta)
        y3_rotated = center_y + (x3 - center_x) * mt.sin(theta) + (y3 - center_y) * mt.cos(theta)

        x4_rotated = center_x + (x4 - center_x) * mt.cos(theta) - (y4 - center_y) * mt.sin(theta)
        y4_rotated = center_y + (x4 - center_x) * mt.sin(theta) + (y4 - center_y) * mt.cos(theta)

        # Малювання ромба після обертання
        rotated_diamond = Polygon(Point(x1_rotated, y1_rotated), Point(x2_rotated, y2_rotated),
                                  Point(x3_rotated, y3_rotated), Point(x4_rotated, y4_rotated))
        rotated_diamond.setOutline("orange")
        rotated_diamond.setFill("orange")
        rotated_diamond.draw(win)

        win.getMouse()
        win.close()

    return

# Перенос фігури в напрямку direction на len одиниць
def move(win, x1, y1, x2, y2, x3, y3, x4, y4):
    # Карта напрямків переносу
    def directions():
        names = ['Пн', 'пн-зх', 'пн-сх', 'Зх', 'Сх', 'пд-зх', 'пд-сх', 'Пд']
        print(f'\n\t\t  {names[0]}\t\t')
        print(f'\t{names[1]}\t {names[2]}\t')
        print(f'{names[3]}\t\t\t\t\t{names[4]}')
        print(f'\t{names[5]}\t {names[6]}\t')
        print(f'\t\t  {names[7]}\t\t\n')

        return names

    # Вибір напрямку та довжини переносу
    print('\nОберіть напрямок переносу:')
    names = directions()
    for i in range(0, 8):
        print(i + 1, '-', names[i])
    direction = int(input('\ndirection:'))
    if direction in range(1, 9):
        print('\nОберіть довжину переносу (0-100):')
        len = int(input('len:'))
        if len in range(0, 101):
            # Пн
            if direction == 1:
                dx = 0
                dy = len
            # пн-зх
            elif direction == 2:
                dx = -len
                dy = len
            # пн-сх
            elif direction == 3:
                dx = len
                dy = len
            # Зх
            elif direction == 4:
                dx = -len
                dy = 0
            # Сх
            elif direction == 5:
                dx = len
                dy = 0
            # пд-зх
            elif direction == 6:
                dx = -len
                dy = -len
            # пд-сх
            elif direction == 7:
                dx = len
                dy = -len
            # Пн
            else:
                dx = 0
                dy = -len

            # Обчислення нових координат ромба після переносу
            x1_moved = x1 + dx
            y1_moved = y1 - dy
            x2_moved = x2 + dx
            y2_moved = y2 - dy
            x3_moved = x3 + dx
            y3_moved = y3 - dy
            x4_moved = x4 + dx
            y4_moved = y4 - dy

            # Малювання ромба після переносу
            moved_diamond = Polygon(Point(x1_moved, y1_moved), Point(x2_moved, y2_moved),
                                   Point(x3_moved, y3_moved), Point(x4_moved, y4_moved))
            moved_diamond.setOutline("orange")
            moved_diamond.setFill("orange")
            moved_diamond.draw(win)

            win.getMouse()
            win.close()

    return

# # Масштабування фігури на коефіцієнт k
# def scale(win, x1, y1, x2, y2, x3, y3, x4, y4):
#     # Обчислення центра ромба
#     center_x = (x1 + x2 + x3 + x4) / 4
#     center_y = (y1 + y2 + y3 + y4) / 4
#
#     # Обчислення відстаней від центра ромба до його вершин
#     x1_dist = x1 - center_x
#     y1_dist = y1 - center_y
#     x2_dist = x2 - center_x
#     y2_dist = y2 - center_y
#     x3_dist = x3 - center_x
#     y3_dist = y3 - center_y
#     x4_dist = x4 - center_x
#     y4_dist = y4 - center_y
#
#     # Вибір режиму масштабування
#     print('\nОберіть режим масштабування:')
#     print('1 - Збільшення')
#     print('2 - Зменшення')
#     scale_mode = int(input('mode:'))
#     # Якщо режим існує
#     if scale_mode in range(1, 3):
#         # Вибір коефіцієнту масштабування
#         print('\nОберіть коефіцієнт масштабування:')
#         scale_koef = float(input('k:'))
#         if (scale_mode == 1 and scale_koef > 1) or (scale_mode == 2 and scale_koef < 1):
#             # Обчислення нових координат ромба після масштабування
#             x1_scaled = x1_dist * scale_koef + center_x
#             y1_scaled = y1_dist * scale_koef + center_y
#
#             x2_scaled = x2_dist * scale_koef + center_x
#             y2_scaled = y2_dist * scale_koef + center_y
#
#             x3_scaled = x3_dist * scale_koef + center_x
#             y3_scaled = y3_dist * scale_koef + center_y
#
#             x4_scaled = x4_dist * scale_koef + center_x
#             y4_scaled = y4_dist * scale_koef + center_y
#
#             # Зменшення
#             # Малювання ромба після масштабування
#             scaled_diamond = Polygon(Point(x1_scaled, y1_scaled), Point(x2_scaled, y2_scaled),
#                                      Point(x3_scaled, y3_scaled), Point(x4_scaled, y4_scaled))
#             scaled_diamond.setOutline("orange")
#             scaled_diamond.setFill("orange")
#             scaled_diamond.draw(win)
#
#             # Збільшення
#             if scale_mode == 1:
#                 # Додатове зображення ромба перед обертанням
#                 diamond = Polygon(Point(x1, y1), Point(x2, y2), Point(x3, y3), Point(x4, y4))
#                 diamond.setOutline("gray")
#                 diamond.setFill("gray")
#                 diamond.draw(win)
#
#             win.getMouse()
#             win.close()
#
#     return

# Циклічне масштабування фігури на коефіцієнт k
def scale(win, x1, y1, x2, y2, x3, y3, x4, y4):
    # Обчислення центра ромба
    center_x = (x1 + x2 + x3 + x4) / 4
    center_y = (y1 + y2 + y3 + y4) / 4

    # Обчислення відстаней від центра ромба до його вершин
    x1_dist = x1 - center_x
    y1_dist = y1 - center_y
    x2_dist = x2 - center_x
    y2_dist = y2 - center_y
    x3_dist = x3 - center_x
    y3_dist = y3 - center_y
    x4_dist = x4 - center_x
    y4_dist = y4 - center_y

    # Вибір режиму масштабування
    print('\nОберіть режиму масштабування:')
    print('1 - Збільшення')
    print('2 - Зменшення')
    scale_mode = int(input('mode:'))
    # Якщо режим існує
    if scale_mode in range(1, 3):
        # Збільшення
        if scale_mode == 1:
            scale_koef = 1.05
        else:
            scale_koef = 0.9

    # Змінні для перевірки виходу за межі вікна або повного зменшення фігури
    within_window = True
    fully_scaled = False

    # Створення списку для зберігання зображень
    frames = []

    # Початок циклу масштабування
    while within_window and not fully_scaled:

        # Збереження зображення з вікна
        frame = get_image(win)
        frames.append(frame)

        x1_scaled = x1_dist * scale_koef + center_x
        y1_scaled = y1_dist * scale_koef + center_y

        x2_scaled = x2_dist * scale_koef + center_x
        y2_scaled = y2_dist * scale_koef + center_y

        x3_scaled = x3_dist * scale_koef + center_x
        y3_scaled = y3_dist * scale_koef + center_y

        x4_scaled = x4_dist * scale_koef + center_x
        y4_scaled = y4_dist * scale_koef + center_y

        # Перевірка, чи ромб залишається в межах вікна
        if all(0 <= coord <= win.getWidth() and 0 <= coord <= win.getHeight() for coord in
               [x1_scaled, x2_scaled, x3_scaled, x4_scaled]):
            # Затримка перед наступною ітерацією
            time.sleep(0.1)

            # Малювання ромба після масштабування
            scaled_diamond = Polygon(Point(x1_scaled, y1_scaled), Point(x2_scaled, y2_scaled),
                                     Point(x3_scaled, y3_scaled), Point(x4_scaled, y4_scaled))
            scaled_diamond.setOutline("orange")
            scaled_diamond.draw(win)

            # Перевірка, чи ромб повністю зменшився
            threshold = 0.1 # Значення, яке ми вважаємо досить малим для зупинки циклу
            if max(abs(x1_scaled - center_x), abs(y1_scaled - center_y)) <= threshold:
                fully_scaled = True

        else:
            within_window = False  # Ромб вийшов за межі вікна, завершення циклу масштабування

        # Оновлення відстаней до вершин ромба для наступного кроку масштабування
        x1_dist = x1_scaled - center_x
        y1_dist = y1_scaled - center_y
        x2_dist = x2_scaled - center_x
        y2_dist = y2_scaled - center_y
        x3_dist = x3_scaled - center_x
        y3_dist = y3_scaled - center_y
        x4_dist = x4_scaled - center_x
        y4_dist = y4_scaled - center_y

    # Зберігаємо анімацію у форматі GIF
    imageio.mimsave("animation_2d.gif", frames)

    if not within_window:
        print('\nРомб вийшов за межі вікна')
    else:
        print('\nРомб повністю зменшився')

    win.getMouse()
    win.close()

    return

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
    xw = 600    # ширина вікна
    yw = 600    # висота вікна

    size_x = 200    # ширина ромба
    size_y = 400    # висота ромба

    center_x = xw / 2   # зміщення висоти ромба
    center_y = yw / 2   # зміщення ширини ромба

    # Обертання
    win, x1, y1, x2, y2, x3, y3, x4, y4 = init_window('Обертання ромба', xw, yw, size_x, size_y, center_x, center_y)
    rotation(win, x1, y1, x2, y2, x3, y3, x4, y4)
    # Перенос
    win, x1, y1, x2, y2, x3, y3, x4, y4 = init_window('Перенос ромба', xw, yw, size_x, size_y, center_x, center_y)
    move(win, x1, y1, x2, y2, x3, y3, x4, y4)
    # Масштабування
    win, x1, y1, x2, y2, x3, y3, x4, y4 = init_window('Масштабування ромба', xw, yw, size_x, size_y, center_x, center_y)
    scale(win, x1, y1, x2, y2, x3, y3, x4, y4)