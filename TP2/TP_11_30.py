import random
from tkinter import *
import math

def init(data):
    #PENDULUM MOTION PARAMETERS
    #a=amplitude
    #f=frequency
    #p=phase
    #d=damping factor
    data.width=1000
    data.height=600
    data.aRange=300
    data.fRange=15
    data.pRange=15
    #parameter control is temporarily set to be random. it will be controlled
    #by the user
    data.a1=random.randint(100,data.aRange)        #suggested---->200
    data.a2=random.randint(80,200)            #suggested---->170
    data.a3=random.randint(0,data.aRange)   #suggested---->190                       
    data.a4=random.randint(60,90)  # suggested---->80                        
    data.f1=3
    data.f2=1
    data.f3=9
    data.f4=2
    data.p1=0.8*math.pi
    data.p2=1*math.pi
    data.p3=10*math.pi
    data.p4=3*math.pi
    data.d=0.01
    data.points=[]
    data.mode="harmonograph"
    data.drawSpeed="slow"   #"fast"
    data.drawColorMode="black" #random
    data.drawColor="black"
    data.colorChoice=['gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 
    'gray7', 'gray8', 'gray9', 'gray10','gray11', 'gray12', 'gray13', 'gray14', 
    'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 
    'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 
    'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 
    'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 
    'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 
    'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 
    'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 
    'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 
    'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']
    data.visualizeMechanism=True
    data.drawPoints=True
    data.timer=0
    
def getPoint(data):
    cX=data.width/2
    cY=data.height/2
    t=data.timer if data.drawSpeed=="fast" else data.timer/20
    #HARMONOGRAPH EQUATIONS
    x_t=cX+(data.a1*math.sin(data.f1*t+(data.p1/2))*math.exp(-data.d*t)-
                  data.a2*math.cos(data.f2*t+(data.p2/2))*math.exp(-data.d*t))  
    y_t=cY+(data.a3*math.cos(data.f3*t+(data.p3/2))*math.exp(-data.d*t)-
                  data.a4*math.sin(data.f4*t+(data.p4/2))*math.exp(-data.d*t)) 
    return ((x_t,y_t))
    
def mousePressed(event, data):
    if (data.mode == "initScreen"):     initScreenMousePressed(event, data)
    elif (data.mode == "harmonograph"): harmonographMousePressed(event, data)
    elif (data.mode == "help"):         helpMousePressed(event, data)
    
def keyPressed(event, data):
    if (data.mode == "initScreen"):     initScreenKeyPressed(event, data)
    elif (data.mode == "harmonograph"): harmonographKeyPressed(event, data)
    elif (data.mode == "help"):         helpKeyPressed(event, data)
    
def timerFired(data):
    if (data.mode == "splashScreen"):   initScreenTimerFired(data)
    elif (data.mode == "harmonograph"): harmonographTimerFired(data)
    elif (data.mode == "help"):         helpTimerFired(data)
    

## TimerFired
    
def initScreenTimerFired(data):
    pass
    
def harmonographTimerFired(data):
    data.timer+=1
    #if data.timer<=1000:
    (x,y)=getPoint(data)
    data.points.append((x,y))
    
def helpTimerFired(data):
    pass
    
## MousePressed

def initScreenMousePressed(event, data):
    pass
    
def harmonographMousePressed(event, data):
    pass
    
def helpMousePressed(event, data):
    pass
    
## KeyPressed
    
def initScreenKeyPressed(event, data):
    pass
    
def harmonographKeyPressed(event, data):
    if event.keysym=="v":
        if data.visualizeMechanism==False:
            data.visualizeMechanism=True
        else:
            data.visualizeMechanism=False
    elif event.keysym=="h":
        data.mode="help"
    elif event.keysym=="c":
        data.drawColorMode="black" if data.drawColorMode=="random" else "random"
    elif event.keysym=="s":
        data.drawSpeed="fast" if data.drawSpeed=="slow" else "fast"
    elif event.keysym=="p":
        data.drawPoints=False if data.drawPoints==True else True
    
def helpKeyPressed(event, data):
    pass
    
    
## draw

def drawPoint(canvas, data):
    if data.drawColorMode=="random":
        data.drawColor=random.choice(data.colorChoice)
    elif data.drawColorMode=="black":
        data.drawColor="black"
    for point in data.points:
        x,y=point[0],point[1]
        canvas.create_oval(x-1,y-1,x+1,y+1, fill=data.drawColor)

def drawLines(canvas, data):
    for i in range (len(data.points)-1):
        point1x=data.points[i][0]
        point1y=data.points[i][1]
        point2x=data.points[i+1][0]
        point2y=data.points[i+1][1]
        canvas.create_line(point1x,point1y,point2x,point2y,width=1,
                                           fill=data.drawColor)
        
def drawHelp(canvas, data):
    helpText="A harmonograph is a mechanical apparatus that employs pendulums to create a geometric image"
    canvas.create_text(data.width/2, data.height/2, text=helpText, anchor=SW,
                       fill="gray", font="Times 28 bold italic")

def redrawAll(canvas, data):
    if data.mode=="help":
        drawHelp(canvas, data)
    elif data.mode=="harmonograph":
        if data.drawPoints==True:
            drawPoint(canvas,data)
        drawLines(canvas,data)
    elif data.mode=="initScreen":
        drawInit(canvas,data)
    
## redrawAll


####################################
# use the run function as-is
####################################

def run(width=1000, height=600):   #from 112
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

####################################
# run call
####################################

run (1000, 600)