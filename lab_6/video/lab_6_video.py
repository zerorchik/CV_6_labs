import cv2
import numpy as np

# Захоплення кадра
def get_frame(cap, scaling_factor):
    # Прочитати поточний кадр з об'єкту захоплення відео
    _, frame = cap.read()
    # Змінити розмір зображення
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame

if __name__ == '__main__':
    i = 3
    # Визначення об'єкту захоплення відео
    cap = cv2.VideoCapture(f'Video_{i}.mp4')

    # Опис відео і параметри
    # videos = ['Video_1', 'Video_2', 'Video_3', 'Video_4']
    # descriptions = ['пара', 'поїзд', 'люди', 'жінка']
    scale = [0.5, 0.5, 0.75, 1.05]

    # Визначення масштабного коефіцієнта для зображень
    scaling_factor = scale[i - 1]    # Постійне читання кадрів

    while True:
        # Отримати поточний кадр
        frame = get_frame(cap, scaling_factor)
        # Конвертувати зображення в простір кольорів HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Визначення діапазону кольору шкіри в HSV
        '''
        HSV (відтінок, насиченість, яскравість)

            відтінок (0-360) - 0 червоний, 120 зелений, 240 синій
            насиченість (0-255)
            яскравість (0-255)
        '''
        # Фільтр 1
        lower_1 = np.array([0, 10, 0])
        upper_1 = np.array([25, 170, 255])
        # Порогова обробка зображення HSV, щоб отримати лише колір шкіри
        mask_1 = cv2.inRange(hsv, lower_1, upper_1)
        # Побітове І та між маскою та оригінальним зображенням
        img_bitwise_and_1 = cv2.bitwise_and(frame, frame, mask=mask_1)
        # Застосування медіанного розмиття
        img_median_blurred_1 = cv2.medianBlur(img_bitwise_and_1, 5)

        # Фільтр 2
        lower_2 = np.array([3, 30, 50])
        upper_2 = np.array([11, 180, 255])
        # Порогова обробка зображення HSV, щоб отримати лише колір шкіри
        mask_2 = cv2.inRange(hsv, lower_2, upper_2)
        # Побітове І та між маскою та оригінальним зображенням
        img_bitwise_and_2 = cv2.bitwise_and(frame, frame, mask=mask_2)
        # Застосування медіанного розмиття
        img_median_blurred_2 = cv2.medianBlur(img_bitwise_and_2, 5)

        # Показ вхідного зображення, зображення з контурами та обробленого зображення
        cv2.imshow('Input Image', frame)
        cv2.imshow('Filter_1', img_median_blurred_1)
        cv2.imshow('Filter_2', img_median_blurred_2)

        # Перевірка, чи натиснута клавіша 'Esc'
        c = cv2.waitKey(5)
        if c == 27:
            break

    cv2.destroyAllWindows()
