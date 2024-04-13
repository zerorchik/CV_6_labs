from PIL import Image, ImageDraw
from pylab import *

# Виділення векторного контуру
def vector_circuit(image, title_1, title_2):
    figure()
    contour(image, origin='image')
    axis('equal')
    title(title_1)
    show()
    contour(image, levels=[170], colors='black', origin='image')
    axis('equal')
    title(title_2)
    show()

    return

# Перетворення зображення з відтінків сірого в ЧБ
def mono(img, title):
    draw = ImageDraw.Draw(img)  # Інструмент для малювання
    width = img.size[0]         # Ширина картинки
    height = img.size[1]        # Висота картинки
    pix = img.load()            # Значення пікселів картинки

    print('Уведіть коефіцієнт розрізнення для ЧБ')
    factor = int(input('factor:'))
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            s = a + b + c
            # Рішення, до якого з 2 кольорів поточне значення кольору ближче
            if s > (((255 + factor) // 2) * 3):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw.point((i, j), (a, b, c))

    plt.imshow(img)
    plt.title(title)
    plt.show()
    img = img.convert('RGB')
    img.save("image_result.jpg", "JPEG")
    del draw

    return

if __name__ == '__main__':
    file_name = 'image.jpg'

    img = array(Image.open('image.jpg').convert('L'))
    image = Image.open("image.jpg")
    vector_circuit(img, 'Виділення контурів у відтінках сірого (до)', 'Контури (до)')

    mono(image, 'Перетворення в ЧБ')
    img = array(Image.open('image_result.jpg').convert('L'))
    vector_circuit(img, 'Виділення контурів у відтінках сірого (після)', 'Контури (після)')
