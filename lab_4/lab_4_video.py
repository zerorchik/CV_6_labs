import cv2
import time

# Відео з файлу
cap = cv2.VideoCapture('timelapse.mp4')

# Параметри вихідного відео (назва файлу, чотирьохсимвольний кодек, кадрова швидкість, розмір кадру)
out = cv2.VideoWriter('result_video.mp4', cv2.VideoWriter_fourcc(*'avc1'), 30, (int(cap.get(3)), int(cap.get(4))))


while True:
    ret, frame = cap.read()
    if not ret:
        break  # Вийти з циклу, якщо відео закінчилося

    # Затримка для плавності відео
    time.sleep(0.03)

    # Кадр в ЧБ
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Перетворення яскравості (відсікання діапазону)
    normalized_frame = cv2.normalize(gray, None, 70, 72, cv2.NORM_MINMAX)
    # Перетворення яскравості (розтягування діапазону на весь спектр)
    equ_frame = cv2.equalizeHist(normalized_frame)

    # Відображення
    cv2.imshow('Video', frame)
    cv2.imshow('Frame', equ_frame)

    # Запис кожного кадру у вихідне відео
    out.write(equ_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()