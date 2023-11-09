import tkinter as tk
from curveBezierApp import CurveBezierApp
if __name__ == "__main__":
    root = tk.Tk()
    app = CurveBezierApp(root)
    root.mainloop()


# newton_cache = {}
# def Newton(n, k):
#     global newton_cache
#     if (n, k) not in newton_cache:
#         licznik = 1
#         for i in range(n - k + 1, n + 1):
#             licznik *= i
#         mianownik = 1
#         for i in range(1, k + 1):
#             mianownik *= i
#         newton_cache[(n, k)] = licznik / mianownik
#     return newton_cache[(n, k)]
#
#
# def B(n, i, t):
#     return Newton(n, i) * (t ** i) * (1.0 - t) ** (n - i)
#
# def Bezier2D(punkty_kontrolne, k):
#     n = len(punkty_kontrolne) - 1
#     def p(t):
#         x = 0.0
#         y = 0.0
#         for i in range(n + 1):
#             x += punkty_kontrolne[i][0] * B(n, i, t)
#             y += punkty_kontrolne[i][1] * B(n, i, t)
#         return (x, y)
#
#     dt = 1.0 / k  # krok parametru t
#     return [p(i * dt) for i in range(k + 1)]
#
#
# if __name__ == '__main__':
#     from PIL import Image
#     from PIL import ImageDraw
#
#     n = 5
#
#     rozdzielczosc = 600
#     k = 200
#     l = 1
#
#     image = Image.new("RGB", (rozdzielczosc, rozdzielczosc))
#     draw = ImageDraw.Draw(image)
#     from random import randint as R
#
#     for i in range(l):
#         print("Tworzenie krzywej %d z %d" % (i + 1, l))
#
#         punkty_kontrolne = [(R(0, rozdzielczosc), R(0, rozdzielczosc)) for _ in range(n)]
#         print(punkty_kontrolne)
#         p = Bezier2D(punkty_kontrolne, k)
#         print(p)
#         draw.rectangle([0, 0, rozdzielczosc, rozdzielczosc], fill="#fff")
#         draw.line(punkty_kontrolne, fill="#ccc")
#         r = 2
#         for (x, y) in punkty_kontrolne:
#             draw.ellipse([x - r, y - r, x + r, y + r], fill="#00f")
#         draw.line(p, fill="#f00")
#         image.save("wynik/Krzywa-Beziera_%03d_%04d.png" % (n, i), "PNG")