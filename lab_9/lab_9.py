from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time

# Кут
angle = 0

# Вершини паралелепіпеда
prlpd = np.array([
    [0, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [0, 1, 0],
    [0, 0, 2],
    [2, 0, 2],
    [2, 1, 2],
    [0, 1, 2]
])

# Грані паралелепіпеда
faces = np.array([
    [0, 1, 2, 3],  # нижня грань
    [4, 5, 6, 7],  # верхня грань
    [0, 1, 5, 4],  # передня грань
    [2, 3, 7, 6],  # задня грань
    [0, 3, 7, 4],  # ліва грань
    [1, 2, 6, 5]   # права грань
])

# Нормалі до граней паралелепіпеда
normals = np.array([
    [0, 0, -1],  # нижня грань
    [0, 0, 1],   # верхня грань
    [0, -1, 0],  # передня грань
    [0, 1, 0],   # задня грань
    [-1, 0, 0],  # ліва грань
    [1, 0, 0]    # права грань
])

# Ініціалізація сцени
def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_FLAT)

# Проекція
def reshape(w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 0.1, 100.0)  # Збільшили відстань огляду
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Візуалізація паралелепіпеда
def draw_prlpd():
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for vertex in face:
            glVertex3fv(prlpd[vertex])
    glEnd()

# Візуалізація
def display():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Налаштування камери
    gluLookAt(8, 8, 8, 0, 0, 0, 0, 1, 0)  # Камера далі від сцени

    # Визначення джерела світла
    light_pos = [5, 5, 5, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    # Обертання об'єктів навколо осі X
    glRotatef(angle, 1, 0, 0)

    # Відображення паралелепіпеда
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)  # Сірий колір
    draw_prlpd()
    glPopMatrix()

    # Відображення сфери
    glPushMatrix()
    glColor3f(1.0, 0.5, 0.0)  # Помаранчевий колір
    glTranslatef(3, 0.5, 1)  # Центрування сфери навпроти однієї з граней паралелепіпеда
    glutSolidSphere(0.5, 50, 50)  # Зменшили розмір сфери
    glPopMatrix()

    glutSwapBuffers()

    angle += 1

    # Додаємо затримку в 0.01 секунди для плавної анімації
    time.sleep(0.01)

# Основний цикл
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Scene")
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)
    init()
    glutMainLoop()

# Головні виклики
if __name__ == "__main__":
    main()
