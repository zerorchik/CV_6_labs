import numpy as np
import matplotlib.pyplot as plt

# Задання відних даних
def data_x():
    # Знак "більше"
    more = [
        1, 0, 0, 0, 0,
        0, 1, 1, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 0, 0, 1,
        0, 0, 0, 1, 0,
        0, 1, 1, 0, 0,
        1, 0, 0, 0, 0
    ]

    # Знак "ділити"
    divide = [
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0
    ]

    # Знак "усі"
    all = [
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 1, 1, 1, 1,
        0, 1, 0, 1, 0,
        0, 1, 0, 1, 0,
        0, 0, 1, 0, 0
    ]

    # Знак "належить"
    belong = [
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 1,
        0, 0, 0, 0, 1,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 1,
        0, 0, 0, 0, 1,
        1, 1, 1, 1, 1
    ]

    x = [
        np.array(more).reshape(1, 35),
        np.array(divide).reshape(1, 35),
        np.array(all).reshape(1, 35),
        np.array(belong).reshape(1, 35),
    ]

    plt.subplot(1, 5, 1)
    plt.imshow(np.array(more).reshape(7, 5))
    plt.subplot(1, 5, 2)
    plt.imshow(np.array(divide).reshape(7, 5))
    plt.subplot(1, 5, 3)
    plt.imshow(np.array(all).reshape(7, 5))
    plt.subplot(1, 5, 4)
    plt.imshow(np.array(belong).reshape(7, 5))
    plt.show()

    return x

# Мітки
def data_y():
    out = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    y = np.array(out)

    return y

# Генерація вагових коефіцієнтів
def generate(x, y):
    l = []
    for _ in range(x * y):
        l.append(np.random.randn())

    return np.array(l).reshape(x, y)

# Функція активації - сигмоїд
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Архітектура нейромоежі
def print_architecture():
    print('\nАрхітектура нейромережі:')
    print('Вхідний шар (35 нейронів)')
    print('Прихований шар (4 нейрони)')
    print('Вихідний шар (4 нейрони)')

# Прохід уперед
def forward(x, w1, w2):
    # Арихований шар
    z1 = x.dot(w1)
    a1 = sigmoid(z1)

    # Вихідний шар
    z2 = a1.dot(w2)
    a2 = sigmoid(z2)

    return a2

# Прохід назад
def back_prop(x, y, w1, w2, alpha):
    # Прихований шар
    z1 = x.dot(w1)
    a1 = sigmoid(z1)

    # Вихідний шар
    z2 = a1.dot(w2)
    a2 = sigmoid(z2)
    d2 = (a2 - y)
    d1 = np.multiply((w2.dot((d2.transpose()))).transpose(),
    np.multiply(a1, 1 - a1))
    w1_adj = x.transpose().dot(d1)
    w2_adj = a1.transpose().dot(d2)
    w1 = w1 - (alpha * w1_adj)
    w2 = w2 - (alpha * w2_adj)

    return w1, w2

# Тренування нейромережі
def train(x, Y, w1, w2, alpha, epoch):
    acc = []
    loss_val = []
    for j in range(epoch):
        l = []
        for i in range(len(x)):
            out = forward(x[i], w1, w2)
            l.append((loss(out, Y[i])))
            w1, w2 = back_prop(x[i], y[i], w1, w2, alpha)
        if (j + 1) % 10 == 0:
            print("Епоха: ", j + 1, " Точність: ", (1 - (sum(l) / len(x))) * 100)
        acc.append((1 - (sum(l) / len(x))) * 100)
        loss_val.append(sum(l) / len(x))

    return acc, loss_val, w1, w2

# Функція втрат
def loss(out, Y):
    s = (np.square(out - Y))
    s = np.sum(s) / len(y)

    return s

# Класифікація
def predict(x, w1, w2):
    res = forward(x, w1, w2)
    max_w = 0
    k = 0
    for i in range(len(res[0])):
        if max_w < res[0][i]:
            max_w = res[0][i]
            k = i

    return k

# Візуалізація результату
def print_results(x, w1, w2):
    symbols = ['>', '÷', '∀', '∃']
    print('Очікувано\tРозпізнано\tСпівпало')
    for i in range(4):
        expected_letter = symbols[i]
        recognized_letter = symbols[predict(x[i], w1, w2)]
        print(f'{expected_letter}\t\t\t{recognized_letter}\t\t\t{True if expected_letter == recognized_letter else False}')


# Головні виклики
if __name__ == '__main__':
    x = data_x()
    y = data_y()
    print('Датасет:')
    print(f'x =\n{x[0]}\n{x[1]}\n{x[2]}\n{x[3]}\n')
    print(f'y =\n{y}')

    print_architecture()

    w1 = generate(35, 4)
    w2 = generate(4, 4)
    print('\nІніціалізуємо вагові коефіцієнти:')
    print(f'w1 =\n{w1}\n')
    print(f'w2 =\n{w2}\n')

    print('\nТренування нейромережі:')
    acc, loss_value, w1, w2 = train(x, y, w1, w2, 0.1, 200)

    print('\nВагові коефіцієнти:')
    print(f'w1 =\n{w1}\n')
    print(f'w2 =\n{w2}\n')

    plt.plot(acc)
    plt.ylabel('Точність')
    plt.xlabel('Епохи')
    plt.show()

    plt.plot(loss_value)
    plt.ylabel('Втрати')
    plt.xlabel('Епохи')
    plt.show()

    print_results(x, w1, w2)
