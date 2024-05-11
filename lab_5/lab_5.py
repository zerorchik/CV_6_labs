import cv2
import numpy as np
import imutils

# Перетворення зображення в HSV
def img_to_hsv(image_name):
    image = cv2.imread(image_name)
    image = imutils.resize(image, width=600)
    # Перетворення в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    return image, hsv

# Кольорова кластеризація по HSV гістограмі яскравості
def color_clasterising(image, hsv):
    '''
    HSV (відтінок, насиченість, яскравість)

        відтінок (0-360) - 0 червоний, 120 зелений, 240 синій
        насиченість (0-255)
        яскравість (0-255)
    '''

    # Визначення об'єктів міської забудови в HSV
    lower_city = np.array([0, 10, 0])
    upper_city = np.array([25, 170, 120])
    # Створення маски
    mask = cv2.inRange(hsv, lower_city, upper_city)

    # Побітове порівняння кольорового образу - "маски" із поточними кадрами
    img_bitwise_and = cv2.bitwise_and(image, image, mask=mask)
    # Median blurring
    img_median_blurred = cv2.medianBlur(img_bitwise_and, 5)

    return mask, img_median_blurred

# Сегментація і виділення контурів
def contours(image, mask):
    # Виявлення контурів
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Малювання контурів на вхідному зображенні
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    return contour_image

# Ідентифікація великих поселень
def identification(image, mask):
    # Розширення маски
    kernel = np.ones((5, 5), np.uint8)
    mask_dilated = cv2.dilate(mask, kernel, iterations=2)
    # Виявлення контурів
    contours_identification, _ = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Обчислення площ контурів
    areas = [cv2.contourArea(contour) for contour in contours_identification]
    # Визначення порогової площі за квантилем 0.95
    threshold_area = np.quantile(areas, 0.95)

    # Малювання всіх контурів
    img_identification = image.copy()
    i = 0
    for contour in contours_identification:
        # Ідентифікація об'єкта, якщо його площа більша за 95%
        if cv2.contourArea(contour) > threshold_area:
            i += 1
            cv2.drawContours(img_identification, [contour], -1, (0, 255, 0), 2)
            # Обчислення моменту контуру
            M = cv2.moments(contour)
            # Ценрт масс контуру
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                # Отримання розмірів тексту
                text = f'City {i}'
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                thickness = 1
                text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                # Зміщення позиції тексту, щоб його центр співпадав з центром об'єкту
                text_offset_x = cX - text_size[0] // 2
                text_offset_y = cY + text_size[1] // 2
                cv2.putText(img_identification, text, (text_offset_x, text_offset_y), font, font_scale, (255, 255, 255), thickness)

    return img_identification

# Візуалізація результатів
def print_result(image, contour_image, img_median_blurred, img_identification):
    # Відображення вхідного зображення, зображення з контурами та обробленого зображення
    cv2.imshow('Input Image', image)
    cv2.imshow('Contours', contour_image)
    cv2.imshow('Segment Image', img_median_blurred)
    cv2.imshow('Identification', img_identification)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Блок головних викликів
if __name__ == "__main__":
    image_name = 'Sentinel-2_L2A_True_Color.jpg'

    # Перетворення зображення в HSV
    image, hsv = img_to_hsv(image_name)

    # Кольорова кластеризація
    mask, img_median_blurred = color_clasterising(image, hsv)
    # Сегментація і виділення контурів
    contour_image = contours(image, mask)
    # Ідентифікація
    img_identification = identification(image, mask)

    # Результати
    print_result(image, contour_image, img_median_blurred, img_identification)
