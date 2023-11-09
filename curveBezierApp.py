from tkinter import *
import tkinter.font as font


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
        # t value label and entry
        self.tLabel = Label(self.frame, text="T value")
        self.tLabel.grid(row=0, column=0, columnspan=2)
        self.tLabel['font'] = bigFont
        self.vcmd = (self.frame.register(self.validateEntry))
        self.tEntry = Entry(self.frame, justify=CENTER, validate='all', validatecommand=(self.vcmd, '%P'))
        self.tEntry.grid(row=1, column=0, columnspan=2)
        # X and Y labels
        self.positionXLabel = Label(self.frame, text="X")
        self.positionXLabel.grid(row=2, column=0)
        self.positionXLabel['font'] = bigFont
        self.positionYLabel = Label(self.frame, text="Y")
        self.positionYLabel.grid(row=2, column=1)
        self.positionYLabel['font'] = bigFont
        # X and Y entries
        self.positionXEntry = Entry(self.frame, justify=CENTER, width=10, validate='all', validatecommand=(self.vcmd, '%P'))
        self.positionXEntry.grid(row=3, column=0)
        self.positionYEntry = Entry(self.frame, justify=CENTER, width=10, validate='all', validatecommand=(self.vcmd, '%P'))
        self.positionYEntry.grid(row=3, column=1)
        # Button to add point
        self.addPointButton = Button(self.frame, text="Add point", command=lambda: self.addPointByParameters(self.positionXEntry.get(), self.positionYEntry.get()))
        self.addPointButton.grid(row=4, column=0, columnspan=2, sticky="WE")
        self.addPointButton['font'] = bigFont
        # Frame for points
        self.pointsLabel = LabelFrame(self.frame, text="Points positions", labelanchor="nw")
        self.pointsLabel.grid(row=5, column=0, columnspan=2, sticky="WE")
        # White space to draw Bezier Curve
        self.drawSpace = Canvas(self.root, bg="white")
        self.drawSpace.pack(fill="both", expand=True)

        self.drawSpace.bind("<ButtonPress-1>", self.drawOrMovePoint)
        self.drawSpace.bind("<B1-Motion>", self.movePointByMouse)
        self.drawSpace.bind("<ButtonRelease-1>", self.endMovePointByMouse)

        self.entries = []
        self.points = []
        self.selectedPoint = None
        self.offsetX, self.offsetY = 0, 0

    def validateEntry(self, P):
        if P == "" or (str.isdigit(P)):
            return True
        else:
            return False

    def addPointByParameters(self, x, y):
        if x and y:
            self.drawOrMovePoint(EventWithXY(x, y))

    def drawOrMovePoint(self, event):
        print(f"Event = {event} x={event.x} y={event.y}")
        x, y = event.x, event.y
        shapes = self.drawSpace.find_overlapping(x - 1, y - 1, x + 1, y + 1)
        if shapes:
            # move point
            self.selectedPoint = shapes[-1]
            self.offsetX = x - self.drawSpace.coords(self.selectedPoint)[0]
            self.offsetY = y - self.drawSpace.coords(self.selectedPoint)[1]
        else:
            # draw  point
            self.drawSpace.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill="black")
            self.points.append([x, y])
            self.addPointToLabel(x, y)

    def movePointByMouse(self, event):
        if self.selectedPoint:
            x, y = event.x, event.y
            self.drawSpace.coords(self.selectedPoint, x - self.offsetX, y - self.offsetY, x - self.offsetX + self.drawSpace.coords(self.selectedPoint)[2] - self.drawSpace.coords(self.selectedPoint)[0], y - self.offsetY + self.drawSpace.coords(self.selectedPoint)[3] - self.drawSpace.coords(self.selectedPoint)[1])
            self.points[self.selectedPoint-1] = [x, y]
            entryX, entryY = self.entries[self.selectedPoint-1][0], self.entries[self.selectedPoint-1][1]
            entryX.delete(0, END)
            entryX.insert(0, str(x))
            entryY.delete(0, END)
            entryY.insert(0, str(y))
    def endMovePointByMouse(self, event):
        self.selectedPoint = None

    def addPointToLabel(self, x, y):
        rowIndex = len(self.points) - 1
        myVarX = StringVar()
        entryX = Entry(self.pointsLabel, justify=CENTER, width=10, textvariable=myVarX, validate="all", validatecommand=(self.vcmd, '%P'))
        myVarX.trace('w', lambda name, index, mode, var=myVarX, row=rowIndex, col=0: self.pointEntryChanged(row, col, var.get()))
        entryX.grid(row=rowIndex, column=0)
        entryX.insert(0, int(x))
        myVarY = StringVar()
        entryY = Entry(self.pointsLabel, justify=CENTER, width=10, textvariable=myVarY, validate="all", validatecommand=(self.vcmd, '%P'))
        myVarY.trace('w', lambda name, index, mode, var=myVarY, row=rowIndex, col=1: self.pointEntryChanged(row, col, var.get()))
        entryY.grid(row=rowIndex, column=1)
        entryY.insert(0, int(y))
        self.entries.append([entryX, entryY])

    def pointEntryChanged(self, row, column, value):
        if value:
            print(f"Row={row} Column={column} Value={value}")
            self.points[row][column] = int(value)
            print(self.points)
            self.movePointByParameters(row+1, self.points[row][0], self.points[row][1])

    def movePointByParameters(self, itemIndex, newX, newY):
        print(f"Parameters = {itemIndex} {newX} {newY}")
        self.drawSpace.coords(itemIndex, newX - 5, newY - 5, newX + 5, newY + 5)


class EventWithXY:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
