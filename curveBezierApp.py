import logging
import time
from tkinter import *
import tkinter.font as font
from time import perf_counter


class CurveBezierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image viewer Piotr Szumowski")
        bigFont = font.Font(size=12, weight="bold")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.frame = LabelFrame(self.root, padx=0, pady=0, labelanchor="w")
        self.frame.pack(side="left", fill="both")
        # Supporting variables
        self.entries = []
        self.points = []
        self.selectedPoint = None
        self.offsetX, self.offsetY = 0, 0
        self.newtonCache = {}
        # number of segments
        self.kLabel = Label(self.frame, text="Number of segments")
        self.kLabel.grid(row=0, column=0, columnspan=2)
        self.kLabel['font'] = bigFont
        self.vcmd = (self.frame.register(self.validateEntry))
        self.kVar = StringVar()
        self.kEntry = Entry(self.frame, justify=CENTER, textvariable=self.kVar, validate='all', validatecommand=(self.vcmd, '%P'))
        self.kVar.trace('w', self.numberOfSegmentsChanged)
        self.kEntry.grid(row=1, column=0, columnspan=2)
        self.kEntry.insert(0, "1000")
        # X and Y labels
        self.positionXLabel = Label(self.frame, text="X")
        self.positionXLabel.grid(row=2, column=0)
        self.positionXLabel['font'] = bigFont
        self.positionYLabel = Label(self.frame, text="Y")
        self.positionYLabel.grid(row=2, column=1)
        self.positionYLabel['font'] = bigFont
        # X and Y entries
        self.positionXEntry = Entry(self.frame, justify=CENTER, width=13, validate='all', validatecommand=(self.vcmd, '%P'))
        self.positionXEntry.grid(row=3, column=0)
        self.positionYEntry = Entry(self.frame, justify=CENTER, width=13, validate='all', validatecommand=(self.vcmd, '%P'))
        self.positionYEntry.grid(row=3, column=1)
        # Button to add point
        self.addPointButton = Button(self.frame, text="Add point", command=lambda: self.addPointByParameters(self.positionXEntry.get(), self.positionYEntry.get()))
        self.addPointButton.grid(row=4, column=0, columnspan=2, sticky="WE")
        self.addPointButton['font'] = bigFont
        # Frame for points
        self.pointsLabel = LabelFrame(self.frame, text="Points positions", labelanchor="nw", padx=4)
        self.pointsLabel.grid(row=5, column=0, columnspan=2, sticky="WE")
        # White space to draw Bezier Curve
        self.drawSpace = Canvas(self.root, bg="white")
        self.drawSpace.pack(fill="both", expand=True)
        # Binding of mouse click and drag
        self.drawSpace.bind("<ButtonPress-1>", self.drawOrMovePoint)
        self.drawSpace.bind("<B1-Motion>", self.movePointByMouse)
        self.drawSpace.bind("<ButtonRelease-1>", self.endMovePointByMouse)

    def NewtonBinomialCoefficient(self, n, k):
        if (n, k) not in self.newtonCache:
            licznik = 1
            for i in range(n - k + 1, n + 1):
                licznik *= i
            mianownik = 1
            for i in range(1, k + 1):
                mianownik *= i
            self.newtonCache[(n, k)] = licznik / mianownik
        return self.newtonCache[(n, k)]

    def BernsteinBasicPolynomial(self, n, i, t):
        return self.NewtonBinomialCoefficient(n, i) * (t ** i) * (1.0 - t) ** (n - i)

    def BezierCurvePoints(self):
        n = len(self.points)-1  # degree Bezier curve
        k = int(self.kEntry.get())  # number of segments

        def p(t):
            x, y = 0, 0
            for i in range(n+1):
                x += self.points[i][0] * self.BernsteinBasicPolynomial(n, i, t)
                y += self.points[i][1] * self.BernsteinBasicPolynomial(n, i, t)
            return x, y
        dt = 1.0/k
        return [p(i*dt) for i in range(k+1)]

    def drawBezierCurve(self):
        if len(self.points) < 2:
            return  # Minimum two points required to draw a Bezier curve
        if self.kEntry.get() == "":
            return  # There must be integer number of segments
        self.drawSpace.delete("bezier_curve")  # Clear previous Bezier curve
        curvePoints = self.BezierCurvePoints()
        for i in range(0, len(curvePoints) - 1):
            x0, y0 = curvePoints[i]
            x1, y1 = curvePoints[i + 1]
            self.drawSpace.create_line(x0, y0, x1, y1, tags="bezier_curve")

    def getPointByPointIndexInCanvas(self, pointIndexInCanvas):
        for sub in self.points:
            if sub[2] == pointIndexInCanvas:
                return sub
        return None

    def movePointByMouse(self, event):
        if self.selectedPoint and any(self.selectedPoint == sub[2] for sub in self.points):
            x, y = event.x, event.y
            self.drawSpace.coords(self.selectedPoint, x - self.offsetX, y - self.offsetY, x - self.offsetX + self.drawSpace.coords(self.selectedPoint)[2] - self.drawSpace.coords(self.selectedPoint)[0], y - self.offsetY + self.drawSpace.coords(self.selectedPoint)[3] - self.drawSpace.coords(self.selectedPoint)[1])
            point = self.getPointByPointIndexInCanvas(self.selectedPoint)
            pointIndex = self.points.index(point)
            logging.info(f"Wybrany punkt = {self.selectedPoint} Punkty = {self.points} Punkt = {point} Index punktu w punktach = {pointIndex}")
            self.points[pointIndex][0], self.points[pointIndex][1] = x, y
            entryX, entryY = self.entries[pointIndex][0], self.entries[pointIndex][1]
            entryX.delete(0, END)
            entryX.insert(0, str(x))
            entryY.delete(0, END)
            entryY.insert(0, str(y))

    def endMovePointByMouse(self, event):
        self.selectedPoint = None

    def drawOrMovePoint(self, event):
        x, y = event.x, event.y
        shapes = self.drawSpace.find_overlapping(x, y, x, y)
        if shapes:
            # move point
            self.selectedPoint = shapes[-1]
            self.offsetX = x - self.drawSpace.coords(self.selectedPoint)[0]
            self.offsetY = y - self.drawSpace.coords(self.selectedPoint)[1]
        else:
            # draw  point
            point = self.drawSpace.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill="black")
            self.points.append([x, y, point])
            self.addPointToLabel(x, y)
        self.drawBezierCurve()

    def addPointToLabel(self, x, y):
        rowIndex = len(self.points) - 1
        myVarX = StringVar()
        entryX = Entry(self.pointsLabel, justify=CENTER, width=12, textvariable=myVarX, validate="all", validatecommand=(self.vcmd, '%P'))
        myVarX.trace('w', lambda name, index, mode, var=myVarX, row=rowIndex, col=0: self.pointEntryChanged(row, col, var.get()))
        entryX.grid(row=rowIndex, column=0, sticky="ew")
        entryX.insert(0, x)
        myVarY = StringVar()
        entryY = Entry(self.pointsLabel, justify=CENTER, width=12, textvariable=myVarY, validate="all", validatecommand=(self.vcmd, '%P'))
        myVarY.trace('w', lambda name, index, mode, var=myVarY, row=rowIndex, col=1: self.pointEntryChanged(row, col, var.get()))
        entryY.grid(row=rowIndex, column=1, sticky="ew")
        entryY.insert(0, y)
        self.entries.append([entryX, entryY])

    def addPointByParameters(self, x, y):
        if x and y:
            self.drawOrMovePoint(EventWithXY(x, y))

    def pointEntryChanged(self, row, column, value):
        if value:
            self.points[row][column] = int(value)
            logging.info(f"Row={row} Column={column} Value={value} points = {self.points}")
            self.movePointByParameters(self.points[row][2], self.points[row][0], self.points[row][1])

    def movePointByParameters(self, itemIndex, newX, newY):
        logging.info(f"Parameters = {itemIndex} {newX} {newY}")
        self.drawSpace.coords(itemIndex, newX - 5, newY - 5, newX + 5, newY + 5)
        self.drawBezierCurve()

    def numberOfSegmentsChanged(self, *args):
        startMeasureTime = time.perf_counter()
        self.drawBezierCurve()
        endMeasureTime = time.perf_counter()
        logging.info(endMeasureTime-startMeasureTime)
        print("Wykonalo sie")

    @staticmethod
    def validateEntry(P):
        if P == "" or (str.isdigit(P)):
            return True
        else:
            return False


class EventWithXY:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
