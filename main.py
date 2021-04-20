import random


def pp(a):
    for i in range(5):
        for j in range(5):
            print("{:5d}".format(a[i][j]), end=" ")
        print()
    print()


a = [[random.randint(-5, 7) for j in range(5)] for i in range(5)]
pp(a)
# -----------------------------
import random


def d(a):
    d = []
    for i in range(5):
        for j in range(5):
            if int(a[i][j]) % 3 == 0:
                d.append(a[i][j])
                print("{:5d}".format(a[i][j]), end=" ")


a = [[random.randint(-5, 7) for j in range(5)] for i in range(5)]
d(a)
# -----------------------------
import random


def F(a):
    F = []
    for i in range(5):
        f1 = 0
        for j in range(5):
            if a[i][j] < 3:
                f1 += a[i][j]
        F.append(f1)
        print("{:5d}".format(f1), end=" ")


a = [[random.randint(-5, 7) for j in range(5)] for i in range(5)]
F(a)
# -----------------------------
import random


def c(a):
    c = []
    for i in range(5):
        for j in range(5):
            if (5 - i) < 5 and (5 - i) == j:
                c.append(a[i][j])
                print("{:5d}".format(a[i][j]), end=" ")


a = [[random.randint(-5, 7) for j in range(5)] for i in range(5)]
c(a)
# ---------------------------------------
import random


def E(a):
    E = []
    for i in range(5):
        e1 = 0
        for j in range(5):
            if a[j][i] > -1:
                e1 += a[j][i]
        E.append(e1)
        print("{:5d}".format(e1), end=" ")


a = [[random.randint(-5, 7) for j in range(5)] for i in range(5)]
E(a)
# --------------------------------------
import random


def b(a):
    b = []
    for i in range(5):
        for j in range(5):
            if (1 + i) == j:
                b.append(a[i][j])
                print("{:5d}".format(a[i][j]), end=" ")


a = [[random.randint(-5, 7) for j in range(5)] for i in range(5)]
b(a)