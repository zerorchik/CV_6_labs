import cv2
import numpy as np
from matplotlib import pyplot as plt

# Гістограма яскравості вхідного зображення
def input_image(img_name):
    # Зображення
    img = cv2.imread(img_name)
    imS = cv2.resize(img, (600, 500))
    cv2.imshow("img", imS)

    # Гістограма яскравості
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img

# Накладання маски на вхідне зображення
def mask(img):
    # Створення маски
    mask = np.zeros(img.shape[:2], np.uint8)
    # Розміри маски (висота, ширина)
    mask[0:1200, 4000:5000] = 255
    # Зображення під маскою
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    # Гістограми яскравості
    hist_full = cv2.calcHist([img], [0], None, [256], [0, 256]) # Вхідного зображення
    hist_mask = cv2.calcHist([img], [0], mask, [256], [0, 256]) # Зображення під маскою

    # Графік
    plt.subplot(221), plt.imshow(img, 'gray') # Вхідне зображення
    plt.subplot(222), plt.imshow(mask, 'gray') # Маска
    plt.subplot(223), plt.imshow(masked_img, 'gray') # Зображення під маскою
    plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask) # Гістограми: вхідного зображення та зображення під маскою
    plt.xlim([0, 256])
    plt.show()

# Розтягнення гістограми
def hist_normalise(image_name, result_image_name):
    # ЧБ вхідне зображення
    img = cv2.imread(image_name, 0)

    # Відокремлення діапазону яскравості
    normalized_img = cv2.normalize(img, None, 70, 72, cv2.NORM_MINMAX)
    # Розтягнення обраного діапазону на весь діапазон 0-255
    equ = cv2.equalizeHist(normalized_img)
    # Зклеювання зображень
    res = np.hstack((img, equ))

    # Гістограми яскравості
    hist_full = cv2.calcHist([img], [0], None, [256], [0, 256]) # Вхідного зображення
    hist_equ = cv2.calcHist([equ], [0], None, [256], [0, 256]) # Обраного розтягнутого діапазону

    # Графік
    plt.subplot(221), plt.imshow(img) # Вхідне зображення
    plt.subplot(222), plt.plot(hist_full) # Гістограма
    plt.subplot(223), plt.imshow(equ) # Обраний розтягнутий діапазон
    plt.subplot(224), plt.plot(hist_equ) # Гістограма
    plt.xlim([0, 256])
    plt.show()

    # Відображення результатів (зклеєний кадр)
    imS = cv2.resize(res, (800, 300))
    plt.imshow(imS)
    plt.show()

    cv2.imwrite(result_image_name, res)

    return imS

# Блок головних викликів
if __name__ == "__main__":
    image_name = 'Sentinel-2_L2A_True_Color'
    image = image_name + '.jpg'
    result_image = image_name + '_Result.jpg'

    # Гістограма яскравості вхідного зображення
    img = input_image(image)
    # Накладання маски на вхідне зображення
    mask(img)
    # Розтягнення гістограми
    result = hist_normalise(image, result_image)