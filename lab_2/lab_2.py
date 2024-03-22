from PIL import Image, ImageDraw
from matplotlib import pyplot as plt


# Зчитування файлу зображення
def image_read(file_name: str) -> None:
    # Відкриття файлу зображення
    image = Image.open(file_name)
    # Створення інструменту для малювання
    draw = ImageDraw.Draw(image)
    # Визначення ширини картинки
    width = image.size[0]
    # Визначення висоти картинки
    height = image.size[1]
    # Отримання значень пікселей для картинки
    pix = image.load()
    print('\nПочаткове зображення')
    print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
    plt.imshow(image)
    plt.show()
    image_info = {"image_file": image, "image_draw": draw, "image_width": width, "image_height": height,
                  "image_pix": pix}

    return image_info


# # Зміна яскравості
# def brightness_change(file_name_start: str, file_name_stop: str) -> None:
#     image_info = image_read(file_name_start)
#     image = image_info["image_file"]
#     draw = image_info["image_draw"]
#     width = image_info["image_width"]
#     height = image_info["image_height"]
#     pix = image_info["image_pix"]
#
#     print('\nУведіть діапазон зміни яскравості')
#     factor = int(input('factor:'))
#     for i in range(width):
#         for j in range(height):
#             # Додавання яскравості
#             a = pix[i, j][0] + factor
#             b = pix[i, j][1] + factor
#             c = pix[i, j][2] + factor
#             if a < 0:
#                 a = 0
#             if b < 0:
#                 b = 0
#             if c < 0:
#                 c = 0
#             if a > 255:
#                 a = 255
#             if b > 255:
#                 b = 255
#             if c > 255:
#                 c = 255
#             draw.point((i, j), (a, b, c))
#
#     plt.imshow(image)
#     plt.show()
#     print('\nКінцеве зображення')
#     print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
#     image.save(file_name_stop, "JPEG")
#     del draw
#
#     return


# Зміна яскравості з використанням алгоритму Брезенхема
def brightness_change_with_gradient(file_name_start: str, file_name_stop: str) -> None:
    image_info = image_read(file_name_start)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    # Задайте початкові та кінцеві точки для лінії зміни яскравості
    start_point = (0, 0)  # Лівий верхній кут
    end_point = (width - 1, height - 1)  # Правий нижній кут

    # Розрахуйте коефіцієнт зміни яскравості за градієнтом
    print('\nУведіть діапазон зміни яскравості')
    max_brightness_change = int(input('factor:'))
    brightness_gradient = max_brightness_change / (width + height)  # Градієнт зміни яскравості

    # Прокладання лінії від початкової до кінцевої точки з використанням алгоритму Брезенхема по діагоналі
    x1, y1 = start_point
    x2, y2 = end_point
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    x = x1
    y = y1
    while x != x2 or y != y2:
        # Зміна яскравості кожного пікселя на діагоналі відповідно до його розташування вздовж лінії
        factor = brightness_gradient * (x - x1 + y - y1)  # Збільшення яскравості
        for j in range(height):
            # Додавання яскравості до кожного пікселя на діагоналі
            if 0 <= x < width and 0 <= j < height:  # Перевірка меж зображення
                a = int(min(max(pix[x, j][0] + factor, 0), 255))
                b = int(min(max(pix[x, j][1] + factor, 0), 255))
                c = int(min(max(pix[x, j][2] + factor, 0), 255))
                draw.point((x, j), (a, b, c))

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    plt.imshow(image)
    plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='green', label='Line')   # Відображення лінії між точками start_point та end_point
    plt.scatter(*start_point, color='red', label='Start Point', s=100, zorder=3)  # Відображення точки start_point
    plt.scatter(*end_point, color='blue', label='End Point', s=100, zorder=3)  # Відображення точки end_point
    plt.legend()  # Відображення легенди з поясненням кольорів точок
    plt.show()
    print('\nКінцеве зображення')
    print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
    image.save(file_name_stop, "JPEG")
    del draw

    return


# # Відтінкі сірого
# def shades_of_gray(file_name_start: str, file_name_stop: str) -> None:
#     image_info = image_read(file_name_start)
#     image = image_info["image_file"]
#     draw = image_info["image_draw"]
#     width = image_info["image_width"]
#     height = image_info["image_height"]
#     pix = image_info["image_pix"]
#
#     for i in range(width):
#         for j in range(height):
#             a = pix[i, j][0]
#             b = pix[i, j][1]
#             c = pix[i, j][2]
#             S = (a + b + c) // 3  # усередненя пікселів
#             draw.point((i, j), (S, S, S))
#
#     plt.imshow(image)
#     plt.show()
#     print('\nКінцеве зображення')
#     print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
#     image.save(file_name_stop, "JPEG")
#     del draw
#
#     return


# Зміна відтінків сірого з використанням алгоритму Брезенхема
def shades_of_gray_with_gradient(file_name_start: str, file_name_stop: str) -> None:
    image_info = image_read(file_name_start)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    # Задайте початкові та кінцеві точки для лінії градієнта
    start_point = (0, 0)  # Лівий верхній кут
    end_point = (width - 1, height - 1)  # Правий нижній кут

    # Розрахунок коефіцієнта зміни відтінків сірого за градієнтом
    max_gray_change = 255  # Максимальний відтінок сірого
    print('\nУведіть фактор сили градієнту (0-1)')
    gradient_factor = float(input('factor:'))
    gray_gradient = gradient_factor * max_gray_change / (width + height)  # Градієнт зміни відтінків сірого

    # Прокладання лінії від початкової до кінцевої точки з використанням алгоритму Брезенхема
    x1, y1 = start_point
    x2, y2 = end_point
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    x = x1
    y = y1
    while x != x2 or y != y2:
        # Зміна відтінку сірого кожного пікселя вздовж лінії градієнта
        factor = gray_gradient * (x - x1 + y - y1)  # Зміна відтінку сірого
        for j in range(height):
            # Застосування градієнту відтінків сірого до кожного пікселя на діагоналі
            if 0 <= x < width and 0 <= j < height:  # Перевірка меж зображення
                r, g, b = pix[x, j]
                gray = int((r + g + b) / 3)  # Відтінок сірого
                new_gray = int(min(max(gray + factor, 0), 255))  # Новий відтінок сірого з градієнтом
                draw.point((x, j), (new_gray, new_gray, new_gray))

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    plt.imshow(image)
    plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='green', label='Line')
    plt.scatter(*start_point, color='red', label='Start Point', s=100, zorder=3)
    plt.scatter(*end_point, color='blue', label='End Point', s=100, zorder=3)
    plt.legend()
    plt.show()
    print('\nКінцеве зображення')
    print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
    image.save(file_name_stop, "JPEG")
    del draw

    return


# # Негатив
# def negative(file_name_start: str, file_name_stop: str) -> None:
#     image_info = image_read(file_name_start)
#     image = image_info["image_file"]
#     draw = image_info["image_draw"]
#     width = image_info["image_width"]
#     height = image_info["image_height"]
#     pix = image_info["image_pix"]
#
#     for i in range(width):
#         for j in range(height):
#             a = pix[i, j][0]
#             b = pix[i, j][1]
#             c = pix[i, j][2]
#             # Від кожного пікселя віднімається 256 - макс. значення для кольору
#             draw.point((i, j), (255 - a, 255 - b, 255 - c))
#
#     plt.imshow(image)
#     plt.show()
#     print('\nКінцеве зображення')
#     print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
#     image.save(file_name_stop, "JPEG")
#     del draw
#
#     return


# Зміна негативу з використанням алгоритму Брезенхема
def negative_with_gradient(file_name_start: str, file_name_stop: str) -> None:
    image_info = image_read(file_name_start)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    # Задайте початкове та кінцеве значення глибини негативу
    start_depth = 0  # Початкова глибина негативу
    end_depth = 255  # Кінцева глибина негативу (повний негатив)

    # Задайте початкову та кінцеву точки для лінії градієнту
    start_point = (0, 0)  # Лівий верхній кут
    end_point = (width - 1, height - 1)  # Правий нижній кут

    # Прокладання лінії від початкової до кінцевої точки з використанням алгоритму Брезенхема
    x1, y1 = start_point
    x2, y2 = end_point
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    x = x1
    y = y1
    while x != x2 or y != y2:
        # Обчислення глибини негативу для поточного пікселя вздовж лінії
        current_depth = start_depth + (end_depth - start_depth) * (x - x1 + y - y1) / (width + height)
        for j in range(height):
            # Застосування глибини негативу до кожного пікселя на діагоналі
            if 0 <= x < width and 0 <= j < height:  # Перевірка меж зображення
                r, g, b = pix[x, j]
                new_r = min(255 - r * (current_depth / 255), 255)
                new_g = min(255 - g * (current_depth / 255), 255)
                new_b = min(255 - b * (current_depth / 255), 255)
                draw.point((x, j), (int(new_r), int(new_g), int(new_b)))

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    plt.imshow(image)
    plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='green', label='Line')
    plt.scatter(*start_point, color='red', label='Start Point', s=100, zorder=3)
    plt.scatter(*end_point, color='blue', label='End Point', s=100, zorder=3)
    plt.legend()
    plt.show()

    print('\nКінцеве зображення')
    print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
    image.save(file_name_stop, "JPEG")
    del draw

    return


# # Сепія
# def sepia(file_name_start: str, file_name_stop: str) -> None:
#     image_info = image_read(file_name_start)
#     image = image_info["image_file"]
#     draw = image_info["image_draw"]
#     width = image_info["image_width"]
#     height = image_info["image_height"]
#     pix = image_info["image_pix"]
#
#     print('\nУведіть коефіцієнт сепії')
#     depth = int(input('depth:'))
#     for i in range(width):
#         # Підрахунок середнього значення кольорової гами - перетворення з коефіціентом
#         for j in range(height):
#             a = pix[i, j][0]
#             b = pix[i, j][1]
#             c = pix[i, j][2]
#             S = (a + b + c) // 3
#             a = S + depth * 2
#             b = S + depth
#             c = S
#             if a > 255:
#                 a = 255
#             if b > 255:
#                 b = 255
#             if c > 255:
#                 c = 255
#             draw.point((i, j), (a, b, c))
#
#     plt.imshow(image)
#     plt.show()
#     print('\nКінцеве зображення')
#     print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
#     image.save(file_name_stop, "JPEG")
#     del draw
#
#     return


# Зміна глибини сепії з використанням алгоритму Брезенхема
def sepia_with_gradient(file_name_start: str, file_name_stop: str) -> None:
    # Зчитування зображення та необхідних параметрів
    image_info = image_read(file_name_start)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    # Задання початкової та кінцевої глибини сепії
    start_depth = 0  # Початкова глибина сепії
    print('\nУведіть діапазон зміни сепії')
    end_depth = int(input('depth:'))  # Кінцева глибина сепії

    # Задання початкової та кінцевої точок для лінії градієнту
    start_point = (0, 0)  # Лівий верхній кут
    end_point = (width - 1, height - 1)  # Правий нижній кут

    # Розрахунок коефіцієнта градієнту сепії
    gradient = (end_depth - start_depth) / (width + height)

    # Прокладання лінії від початкової до кінцевої точки за допомогою алгоритму Брезенхема
    x1, y1 = start_point
    x2, y2 = end_point
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    x = x1
    y = y1
    while x != x2 or y != y2:
        # Обчислення глибини сепії для поточного пікселя вздовж лінії
        current_depth = start_depth + (end_depth - start_depth) * (x - x1 + y - y1) / (width + height)

        # Застосування глибини сепії до кожного пікселя на діагоналі
        for j in range(height):
            if 0 <= x < width and 0 <= j < height:  # Перевірка меж зображення
                r, g, b = pix[x, j]
                gray = (r + g + b) // 3  # усереднення кольорів
                sepia_r = min(gray + current_depth * 2, 255)
                sepia_g = min(gray + current_depth, 255)
                sepia_b = min(gray, 255)
                draw.point((x, j), (int(sepia_r), int(sepia_g), int(sepia_b)))

        # Оновлення значення помилки та координат
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    # Відображення зображення та лінії градієнту
    plt.imshow(image)
    plt.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='green', label='Line')
    plt.scatter(*start_point, color='red', label='Start Point', s=100, zorder=3)
    plt.scatter(*end_point, color='blue', label='End Point', s=100, zorder=3)
    plt.legend()
    plt.show()

    # Виведення інформації про кінцеве зображення та збереження його
    print('\nКінцеве зображення')
    print(f'red = {pix[1, 1][0]}\tgreen = {pix[1, 1][1]}\tblue = {pix[1, 1][2]}')
    image.save(file_name_stop, "JPEG")
    del draw

    return


# Блок головних викликів
if __name__ == "__main__":

    file_name_start = 'image.png'
    file_name_stop = "stop.png"

    print('Оберіть тип перетворення:')
    print('0 - зміна яскравості')
    print('1 - відтінки сірого')
    print('2 - негатив')
    print('3 - сепія')
    mode = int(input('mode:'))
    if mode == 0:
        # brightness_change(file_name_start, file_name_stop)
        brightness_change_with_gradient(file_name_start, file_name_stop)
    if mode == 1:
        # shades_of_gray(file_name_start, file_name_stop)
        shades_of_gray_with_gradient(file_name_start, file_name_stop)
    if mode == 2:
        # negative(file_name_start, file_name_stop)
        negative_with_gradient(file_name_start, file_name_stop)
    if mode == 3:
        # sepia(file_name_start, file_name_stop)
        sepia_with_gradient(file_name_start, file_name_stop)
