import cv2

image = cv2.imread('photo.jpg')

# Зменшення розміру зображення до 50% від оригінального розміру
scale_percent = 50 # відсотків оригінального розміру
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)

image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Ініціалізація класифікаторів для виявлення облич, очей та усмішок
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Конвертація зображення у відтінки сірого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Виявлення облич на зображенні
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(85, 85))
num_faces = len(faces)

# Виявлення очей та усмішок
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = image[y:y + h, x:x + w]
    # Виявлення очей
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.001, minNeighbors=30, minSize=(1, 1))
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    # Виявлення усмішки
    smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.01, minNeighbors=10, minSize=(30, 30))
    for (sx, sy, sw, sh) in smiles:
        cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

print("Кількість осіб на фото:", num_faces)

cv2.imshow('Face Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()