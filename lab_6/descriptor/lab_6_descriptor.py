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

# Детектор кутів Харріса
def harris_corner_detector(image):
    img = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # Розширений результат для розмітки кутів
    dst = cv2.dilate(dst, None)

    # Порогове значення для оптимального значення - може відрізнятися залежно від зображення
    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    return img

# Дескриптор SIFT для заданих функцій на основі виявлення кутів Харріса
def sift_descriptors_on_harris(image):

    def harris(img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img = np.float32(gray_img)
        dst = cv2.cornerHarris(gray_img, 2, 3, 0.04)
        result_img = img.copy()

        # Порогове значення для оптимального значення - може відрізнятися залежно від зображення
        # Малює ключові точки кута Харріса на зображенні (RGB [0, 0, 255] -> синій)
        result_img[dst > 0.01 * dst.max()] = [0, 0, 255]
        # dst, більше за порогове значення = ключова точка
        keypoints = np.argwhere(dst > 0.01 * dst.max())
        keypoints = [cv2.KeyPoint(float(x[1]), float(x[0]), 13) for x in keypoints]

        return (keypoints, result_img)

    img = image.copy()
    # Обчислюємо features кута Харріса та перетворюємо їх на ключові точки
    kp, img = harris(img)
    # Обчислюємо дескриптори SIFT з ключових точок Harris Corner
    sift = cv2.SIFT_create()
    sift.compute(img, kp)
    img = cv2.drawKeypoints(img, kp, img)

    return img

# Порівняння двох зображень
def sift_feature_matching(image_1, image_2):
    img1 = image_1.copy()
    img2 = image_2.copy()

    # Запуск детектора SIFT
    sift = cv2.SIFT_create()
    # Знаходження ключових точок та дескрипторів за допомогою SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # Параметри FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Підрахунок кількості ідентифікованих дескрипторів для кожного зображення
    total_descriptors_img1 = len(des1)
    total_descriptors_img2 = len(des2)

    # Підрахунок кількості співпадінь
    matching_descriptors = 0
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            matching_descriptors += 1

    # Виведення кількості ідентифікованих дескрипторів для кожного зображення
    print(f'Усього дескрипторів на image 1:\t\t{total_descriptors_img1}')
    print(f'Усього дескрипторів на image 2:\t\t{total_descriptors_img2}')
    print(f'\nКількість співпадінь:\t\t\t\t{matching_descriptors}')

    # Вибір меншої кількості дескрипторів для розрахунку відсотка ідентичності
    min_total_descriptors = min(total_descriptors_img1, total_descriptors_img2)

    # Розрахунок відсотка ідентичності, з урахуванням маштабування
    similarity_percentage = round(min(100 * (matching_descriptors / min_total_descriptors), 100), 3)
    print(f'Відсоток ідентичності:\t\t\t\t{similarity_percentage}%')
    belive_interval = round(min(100 * (matching_descriptors / min_total_descriptors) / 0.15, 100), 3)
    print(f'Відсоток довіри:\t\t\t\t\t{belive_interval}%')

    # Створення маски для відображення зіставлених точок на зображенні
    matchesMask = [[0, 0] for i in range(len(matches))]
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv2.DrawMatchesFlags_DEFAULT)

    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
    # Розмір зображення для створення білої лінії
    height, width, _ = img3.shape
    # Додавання білої лінії між зображеннями
    img_with_line = cv2.line(img3, (width // 2, 0), (width // 2, height), (255, 255, 255), 2)
    cv2.imshow('sift_feature_matching', img_with_line)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Візуалізація результатів
def print_result(image, contour_image, img_median_blurred, img_identification, img_harris, img_sift):
    # Відображення вхідного зображення, зображення з контурами та обробленого зображення
    cv2.imshow('Input Image', image)
    cv2.imshow('Contours', contour_image)
    cv2.imshow('Segment Image', img_median_blurred)
    cv2.imshow('Identification', img_identification)
    cv2.imshow('Harris Detector', img_harris)
    cv2.imshow('SIFT Descriptor', img_sift)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Блок головних викликів
if __name__ == "__main__":
    image_name = ['Sentinel-1.jpg', 'Sentinel-2.jpg']

    # Перетворення зображення в HSV
    image_1, hsv = img_to_hsv(image_name[0])
    # Кольорова кластеризація
    mask, img_median_blurred_1 = color_clasterising(image_1, hsv)
    # Сегментація і виділення контурів
    contour_image = contours(image_1, mask)
    # Ідентифікація
    img_identification = identification(image_1, mask)

    # Детектор кутів Харріса
    img_harris = harris_corner_detector(img_median_blurred_1)
    # Дескриптори SIFT для кутів Харріса
    img_sift = sift_descriptors_on_harris(img_median_blurred_1)
    print_result(image_1, contour_image, img_median_blurred_1, img_identification, img_harris, img_sift)


    # Перетворення зображення в HSV
    image_2, hsv = img_to_hsv(image_name[1])
    # Кольорова кластеризація
    mask, img_median_blurred_2 = color_clasterising(image_2, hsv)
    # Сегментація і виділення контурів
    contour_image = contours(image_2, mask)
    # Ідентифікація
    img_identification = identification(image_2, mask)

    # Детектор кутів Харріса
    img_harris = harris_corner_detector(img_median_blurred_2)
    # Дескриптори SIFT для кутів Харріса
    img_sift = sift_descriptors_on_harris(img_median_blurred_2)
    print_result(image_2, contour_image, img_median_blurred_2, img_identification, img_harris, img_sift)

    # Співставлення ознак
    sift_feature_matching(img_median_blurred_1, img_median_blurred_2)