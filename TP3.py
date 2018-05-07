###
### Cecilia Ferrando - cferrand
### 15-112 Term Project
###
### I am grateful to all 15-112 teaching team
### Thank you for making this possible 
###
### To my parents
###
###THE HARMONOGRAPH - a digital drawing machine


from __future__ import division
import random
from tkinter import *
from PIL import Image, ImageTk, ImageOps, ImageDraw
import math
import numpy as np
import os
d2r = math.pi/180

##Rotating Gears

class Gear(object):

    def __init__(self,x,y,r,pradial,pangular,speed,r2,armLenght,armAngle):  #remove radial
        self.x=x
        self.y=y
        self.r=r
        self.pradial=self.r-30
        self.pangular=pangular
        self.speed=speed
        self.px=self.x+self.pradial*math.cos(self.pangular)
        self.py=self.y+self.pradial*math.sin(self.pangular)
        self.r2=r2
        self.armLenght=armLenght
        self.armAngle=armAngle
        self.fill1="gray"   #hardcoded for the moment
        self.fill2="gray70"
    
    def rotate(self):
        self.pangular+=self.speed/100*math.pi 
        #update the position of the anchor points
        self.px=self.x+self.pradial*math.cos(self.pangular)
        self.py=self.y+self.pradial*math.sin(self.pangular)
        
    def getCenter(self):
        return ((self.px, self.py))
        
    def getArmLenght(self):
        return (self.armLenght)

    def armAnchor(self):
        anchorX=self.px
        anchorY=self.py
        return((anchorX,anchorY))
        
    def armEnd(self, anchorX, anchorY):
        endX=anchorX+self.pradial*math.cos(self.armAngle)
        endY=anchorY+self.pradial*math.sin(self.armAngle)
        return((endX,endY))
        
    def areLegalGears(self, other):
        if (math.sqrt((self.x-other.x)**2+(self.y-other-y)**2)+self.pradial+
                    other.pradial)>self.armLenght+other.armLenght:
            return None
        return True
              
    def draw(self, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, 
                        self.y+self.r, fill=self.fill1, width=0)
        canvas.create_oval(self.px-self.r2, self.py-self.r2, self.px+self.r2, 
                        self.py+self.r2, fill=self.fill2, width=0) 


##GUI Buttons                  

class Button(object):
    def __init__(self,x,y,width,height,shape,fill,text):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.shape=shape
        self.fill=fill
        self.text=text
        
    def getButtonBounds(self):
        if self.shape=="rectangle":
            return (((self.x, self.y),(self.x+self.width,self.y+self.height)))
        
    def draw(self, canvas):
        textColor="gray20"
        if self.shape=="rectangle":
            canvas.create_rectangle(self.x, self.y, self.x+self.width, 
                        self.y+self.height, 
                                         fill=self.fill,width=2)
            canvas.create_text(self.x+self.width/2,self.y+self.height/2,
                            text=self.text,fill=textColor,font="Calibri 10",)
        else:
            canvas.create_oval(self.x-10,self.y-10,self.x+10,self.y+10,
                                fill=self.fill, text=self.fill, width=2)
            canvas.create_text(self.x,self.y,fill=textColor,text=self.text,
                                               font="Calibri 14")
                                
class Paper(object):
    def __init__(self,x,y,r,pradial,pangular):
        self.x=x
        self.y=y
        self.r=r
        self.pradial=pradial
        self.pangular=pangular
        self.px=self.x+self.pradial*math.cos(self.pangular)
        self.py=self.y+self.pradial*math.sin(self.pangular)
        self.fill="white"   #hardcoded for the moment
    
    def rotate(self):
        self.pangular+=1/720*math.pi 
        #update the position of the anchor points
        self.px=self.x+self.pradial*math.cos(self.pangular)
        self.py=self.y+self.pradial*math.sin(self.pangular)
        
    def getCenter(self):
        return ((self.px, self.py))
        
    def draw(self, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, 
                        self.y+self.r, fill=self.fill, width=0)
                                
##Computing the intersections of two circles on the plane______

#SOURCE OF THE CIRCLE INTERSECTION CODE:
#http://stackoverflow.com/a/3349134/798588
def circle_intersection(circle1, circle2):   
    #
    #summary: calculates intersection points of two circles
    #param circle1: tuple(x,y,radius)
    #param circle2: tuple(x,y,radius)
    #result: tuple of intersection points (which are (x,y) tuple)
    #
    # return self.circle_intersection_sympy(circle1,circle2)
    x1,y1,r1 = circle1
   # print(x1,y1,r1)
    x2,y2,r2 = circle2
   # print(x2,y2,r2)
    dx,dy = x2-x1,y2-y1
    d = math.sqrt(dx*dx+dy*dy)
    if d > r1+r2:
        print (1)
        return None # no solutions, the circles are separate
    if d < abs(r1-r2):
        print (2)
        return None # no solutions because one circle is contained within the other
    if d == 0 and r1 == r2:
        print (3)
        return None # circles are coincident and there are an infinite number of solutions

    a = (r1*r1-r2*r2+d*d)/(2*d)
    h = math.sqrt(r1*r1-a*a)
    xm = x1 + a*dx/d
    ym = y1 + a*dy/d
    xs1 = xm + h*dy/d
    xs2 = xm - h*dy/d
    ys1 = ym - h*dx/d
    ys2 = ym + h*dx/d
    if ys1<ys2:
        return (xs2,ys2)
    else:
        return (xs1,ys1)
    #return (xs1,ys1),(xs2,ys2)  we need t filter one point out

def circle_intersection_sympy(circle1, circle2):
    from sympy.geometry import Circle, Point
    x1,y1,r1 = circle1
    x2,y2,r2 = circle2
    c1=Circle(Point(x1,y1),r1)
    c2=Circle(Point(x2,y2),r2)
    intersection = c1.intersection(c2)
    if len(intersection) == 1:
        intersection.append(intersection[0])
    p1 = intersection[0]
    p2 = intersection[1]
    xs1,ys1 = p1.x,p1.y
    xs2,ys2 = p2.x,p2.y
    if ys1>ys2:
        return (xs2,ys2)
    else:
        return (xs1,ys1)

def test_circle_intersection():
    geom = Geometry()
    np.testing.assert_almost_equal(
        geom.circle_intersection((0,0,1),(2,0,1)),
        ((1,0),(1,0)))
    np.testing.assert_almost_equal(
        geom.circle_intersection((2,0,1),(0,0,1)),
        ((1,0),(1,0)))
    np.testing.assert_almost_equal(
        geom.circle_intersection((1,1,1),(3,1,1)),
        ((2,1),(2,1)))
    np.testing.assert_almost_equal(
        geom.circle_intersection((0,0,1),(cos(d2r*45)*2,0,1)),
        ((cos(d2r*45),-sin(d2r*45)),
         (cos(d2r*45),+sin(d2r*45))))
##INIT

settings=33

def init(data):
    data.width=1000
    data.height=600
    data.mode="harmonograph"
    #settings__________________
    data.settingsTextX=data.width/3
    data.settingsTextDir=False
    data.sampleList=[]
    loadSamples(data)
    data.listOfDrawingModes=[1,2,3,4,11,22,33,44,111,222,333,444]
    data.userSettings=settings
    if data.userSettings==1:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/5,data.height/5
        data.gear2x,data.gear2y=data.width/5*4,data.height/4
        data.gear1radius=150
        data.gear2radius=100
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*1/2
        data.gear2pangular=math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=400
        data.gear2armLenght=410
        data.gear1armAngle=80
        data.gear2armAngle=80
    elif data.userSettings==2:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/5,data.height/5
        data.gear2x,data.gear2y=data.width/5*4,data.height/4
        data.gear1radius=150
        data.gear2radius=100
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*1/2
        data.gear2pangular=math.pi*2/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=400
        data.gear2armLenght=410
        data.gear1armAngle=80
        data.gear2armAngle=80
    elif data.userSettings==3:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/5,data.height/5
        data.gear2x,data.gear2y=data.width/5*4,data.height/4
        data.gear1radius=150
        data.gear2radius=100
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*1/2
        data.gear2pangular=math.pi*3/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=400
        data.gear2armLenght=410
        data.gear1armAngle=80
        data.gear2armAngle=80
    elif data.userSettings==4:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/5,data.height/5
        data.gear2x,data.gear2y=data.width/5*4,data.height/4
        data.gear1radius=150
        data.gear2radius=100
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*1/2
        data.gear2pangular=math.pi*4/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=400
        data.gear2armLenght=410
        data.gear1armAngle=80
        data.gear2armAngle=80
    elif data.userSettings==11:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=120
        data.gear2radius=140
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*1/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=380
        data.gear2armLenght=370
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==22:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=120
        data.gear2radius=140
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*2/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=380
        data.gear2armLenght=370
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==33:
        data.damping1=0.03
        data.damping2=0.05
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=120
        data.gear2radius=140
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*3/2*2
        data.gear2pangular=-math.pi*1/2*2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=380
        data.gear2armLenght=370
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==44:
        data.damping1=0.01
        data.damping2=0.03
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=120
        data.gear2radius=140
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*4/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=380
        data.gear2armLenght=370
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==111:
        data.damping1=0.05
        data.damping2=0.08
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=180
        data.gear2radius=200
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*1/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=400
        data.gear2armLenght=400
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==222:
        data.damping1=0.05
        data.damping2=0.08
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=180
        data.gear2radius=200
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*2/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=400
        data.gear2armLenght=400
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==333:
        data.damping1=0.05
        data.damping2=0.08
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=170
        data.gear2radius=190
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*3/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=420
        data.gear2armLenght=420
        data.gear1armAngle=120
        data.gear2armAngle=120
    elif data.userSettings==444:
        data.damping1=0.05
        data.damping2=0.08
        data.gear1x,data.gear1y=data.width/7,data.height/6
        data.gear2x,data.gear2y=data.width/7*5,data.height/9*2
        data.gear1radius=170
        data.gear2radius=190
        data.gear1pradial=data.gear1radius-30
        data.gear2pradial=data.gear2radius-30
        data.gear1pangular=math.pi*4/2
        data.gear2pangular=-math.pi*1/2
        data.gear1speed=data.gear1pangular
        data.gear2speed=data.gear2pangular
        data.gearJointRadius=5
        data.gear1armLenght=430
        data.gear2armLenght=430
        data.gear1armAngle=120
        data.gear2armAngle=120
    data.gearImages=[]
    data.gearImagesIndex=0
    data.gearImageRotationAngle=1/100*math.pi
    #harmonograph______________
    data.wallpaper=None
    loadWallPaper(data)
    data.pencil=None
    loadPencil(data)
    data.gearImageIndex=0
    data.gear1=Gear(data.gear1x,data.gear1y,data.gear1radius,
                  data.gear1pradial,data.gear1speed,data.gear1pangular,
                  data.gearJointRadius,data.gear1armLenght,data.gear1armAngle)
    data.gear2=Gear(data.gear2x,data.gear2y,data.gear2radius,
             data.gear2pradial,data.gear2speed,data.gear2pangular,
                   data.gearJointRadius,data.gear2armLenght,data.gear2armAngle)
    data.anchor1x=data.gear1.armAnchor()[0]
    data.anchor1y=data.gear1.armAnchor()[1]
    data.anchor2x=data.gear2.armAnchor()[0]
    data.anchor2y=data.gear2.armAnchor()[1]
    data.end1x=data.gear1.armEnd(data.anchor1x,data.anchor1y)[0]
    data.end1y=data.gear1.armEnd(data.anchor1x,data.anchor1y)[1]
    data.end2x=data.gear2.armEnd(data.anchor2x,data.anchor2y)[0]
    data.end2y=data.gear2.armEnd(data.anchor2x,data.anchor2y)[1]
    data.points=[]
    data.paperX=(data.gear2x+data.gear1x)/2
    data.paperY=data.height/5*3
    data.paperRadius=300
    data.paperRadial=300
    data.paperAngular=math.pi/2000
    data.paper=Paper(data.paperX,data.paperY,data.paperRadius,data.paperRadial,
                        data.paperAngular)
    data.timer=0
    data.speedUp=False
    #colors
    data.colorMode="grayscale"
    data.colorPalette=['gray1','gray10','gray18','gray25','gray35','gray45',
                   'gray55','gray65','gray75','gray65','gray55','gray45', 
                    'gray35','gray25','gray18','gray10', 'gray1']
    if data.colorMode=="rainbow":
        data.colorPalette=["red3","firebrick2", "DeepPink3","VioletRed4",
                                "magenta4","purple4","SlateBlue4","blue4",
                                "DeepSkyBlue4","aquamarine4","chartreuse4",
                                "yellow4","gold3","goldenrod1",
                                "chocolate2","OrangeRed2"]
    if data.colorMode=="black":
        data.color="black"
    elif data.colorMode=="grayscale":
        data.color=data.colorPalette[0]
    elif data.colorMode=="rainbow":
        data.color=data.colorPalette[0]
        print("color=colorpalette")
    data.colorCounter=0
    data.gearImages=[]
    loadGears(data)
    data.imageH=loadHarmonographSketch(data)
    data.visualizeMechanism=True
    data.stopDrawing=False
    #initScreen______________
    data.initHarmonograms=[]
    loadHarmonograms(data)
    data.margin=30
    #buttons
    data.infoButton=Button(data.width-data.margin-225,data.height/5*4,200,40,"rectangle","white","info")
    data.mainButton=Button(data.width-data.margin-225,data.height/5*4,200,40,"rectangle","white","main")
    data.playButton=Button(data.width-data.margin-225,data.height/8*7,200,40,"rectangle","white","play")
    data.creditsButton=Button(data.margin,data.height/8*7,200,40,"rectangle","white","credits")
    data.creditsButton=Button(data.margin,data.height/8*7,200,40,"rectangle","white","credits")
    data.credits=False
    
##Zen Mode
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
    data.pointsZen=[]
    # data.mode="harmonograph"
    data.drawSpeed="slow"   #"fast"
    data.drawColorZenMode="black" #random
    data.drawColorZen="black"
    data.drawPointsZen=False


def writeFile(path, contents):         #from CMU 15-112 course materials
    with open(path, "wt") as f:
        f.write(contents) 
        
def parameters(data):
    return (data.gear1x,data.gear1y,data.gear2x,data.gear2y,data.gear1radius,
              data.gear2radius,data.gear1pangular,data.gear2pangular,
                                data.gear1armLenght,data.gear2armLenght)

def loadHarmonograms(data):     #from 15-112 course material    
    Harmonograms=2
    for i in range(Harmonograms):
        filename="Harmonograms/Harmonogram%d.gif"%(i)
        data.initHarmonograms.append(PhotoImage(file=filename))
        
def loadWallPaper(data):
    filename="wall.gif"
    data.wallPaper=PhotoImage(file=filename)

def loadGears(data):
    if data.colorMode=="grayscale" or data.colorMode=="black":
        image1=Image.open("Gears/gearA.png").convert("RGBA")
        image2=Image.open("Gears/gearB.png").convert("RGBA")
    else:
        image1=Image.open("Gears/gearA2.png").convert("RGBA")
        image2=Image.open("Gears/gearB2.png").convert("RGBA")
    image1r=image1.resize((int(2*data.gear1radius),int(2*data.gear1radius)),
                                                                   resample=0)
    image2r=image2.resize((int(2*data.gear2radius),int(2*data.gear2radius)),
                                                                   resample=0)
    photo1=ImageTk.PhotoImage(image1r)
    photo2=ImageTk.PhotoImage(image2r)
    return ([image1r,image2r])

def loadSamples(data):
    list=[1,2,3,4,11,22,33,44,111,222,333,444]
    for i in range(len(list)):
        image=Image.open("Samples/%d.gif"%(list[i]))
        imager=image.resize((150,150),resample=0)
        photo=ImageTk.PhotoImage(imager)
        data.sampleList.append(photo)
    
def loadPencil(data):
    #SOURCE: http://www.softicons.com/object-icons/free-pencil-icon-pack-by-crinsp/pencil-shadow-20-icon
    filename="pencil2.gif"
    data.pencil=PhotoImage(file=filename)
    
def loadHarmonographSketch(data):
    image=Image.open("harmonographsketch.gif")
    photo=ImageTk.PhotoImage(image)
    return (photo)
    
def ithCellBounds(data, i):
    #returns the bounds of a button as coordinates
    p1x=data.width/4*(i%4)+120-100
    p1y=data.height/3*(i%3)+40
    p2x=data.width/4*(i%4)+120+100
    p2y=data.height/3*(i%3)+200
    return ([p1x, p1y, p2x, p2y])


## Helper Functions

def findIntersectionOfCircles(data):
    #returns only the intersection of interest
    x1=data.anchor1x
    y1=data.anchor1y
    x2=data.anchor2x
    y2=data.anchor2y
    d1=data.gear1.armLenght
    d2=data.gear1.armLenght
    for x in range(0, data.width):
        if (x-x2)**2-(x-x1)**2==d2**2-d1**2:
            y=math.sqrt(d1**2-(x-x1)**2)
            return ((x,y))
        elif (-(x-x2)**2+(x-x1)**2==-d2**2+d1**2):
            y=math.sqrt(d1**2-(x-x1)**2)
            return ((x,y))
    return None
    
def rotatePoint(data, x, y):
    pangular=1/720*math.pi 
    #update the position of the points
    pradial=math.sqrt((x-data.paperX)**2+(y-data.paperY)**2)
    newX=x+pradial*math.cos(pangular)
    newY=y+pradial*math.sin(pangular)
    return ([newX, newY])
    
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
def getPoint(data):
    cX=data.width/2
    cY=data.height/2
    t=data.timer if data.drawSpeed=="fast" else data.timer/50
    #HARMONOGRAPH EQUATIONS
    #from the physics of pendulum motion
    x_t=cX+(data.a1*math.sin(data.f1*t+(data.p1/2))*math.exp(-data.d*t)-
                  data.a2*math.cos(data.f2*t+(data.p2/2))*math.exp(-data.d*t))  
    y_t=cY+(data.a3*math.cos(data.f3*t+(data.p3/2))*math.exp(-data.d*t)-
                  data.a4*math.sin(data.f4*t+(data.p4/2))*math.exp(-data.d*t)) 
    return ((x_t,y_t))

##Structure
#similar structure as 15-112

def mousePressed(event, data):
    if (data.mode == "initScreen"):     initScreenMousePressed(event, data)
    elif (data.mode == "info"):         infoMousePressed(event, data)
    elif (data.mode == "settings"):     settingsMousePressed(event, data)
    elif (data.mode == "harmonograph"): harmonographMousePressed(event, data)
    elif (data.mode == "zen"):          zenMousePressed(event, data)
    
def keyPressed(event, data):
    if (data.mode == "initScreen"):     initScreenKeyPressed(event, data)
    elif (data.mode == "info"):         infoKeyPressed(event, data)
    elif (data.mode == "settings"):     settingsKeyPressed(event, data)
    elif (data.mode == "harmonograph"): harmonographKeyPressed(event, data)
    elif (data.mode == "zen"):          zenKeyPressed(event, data)
    
def timerFired(data):
    if (data.mode == "initScreen"):     initScreenTimerFired(data)
    elif (data.mode == "info"):         infoTimerFired(data)
    elif (data.mode == "settings"):     settingsTimerFired(data)
    elif (data.mode == "harmonograph"): harmonographTimerFired(data)
    elif (data.mode == "zen"):          zenTimerFired(data)

## TimerFired
    
def initScreenTimerFired(data):
    pass
    
def infoTimerFired(data):
    pass
    
def settingsTimerFired(data):
    if data.settingsTextDir==False:
        data.settingsTextX-=0.5
        if data.settingsTextX<10:
            data.settingsTextDir=True
    elif data.settingsTextDir==True:
        data.settingsTextX+=0.5
        if data.settingsTextX>data.width-10:
            data.settingsTextDir=False
    
def harmonographTimerFired(data):
    if data.stopDrawing==False:
        data.timer+=1
        data.gearImageRotationAngle+=1/100*math.pi
        if data.timer<2000:
            data.gear1.pradial-=data.damping1
            data.gear2.pradial-=data.damping2
        else:
            data.stopDrawing=True
            data.visualizeMechanism=False
        data.gear1.rotate()
        data.gear2.rotate()
        gearImage1,gearImage2=loadGears(data)[0],loadGears(data)[1]
        gearImage1R=gearImage1.rotate(-data.timer*data.gear1pangular)
        gearImage2R=gearImage2.rotate(-data.timer*data.gear2pangular)
        gearImage1RTk=ImageTk.PhotoImage(gearImage1R)
        gearImage2RTk=ImageTk.PhotoImage(gearImage2R)
        data.gearImages=[gearImage1RTk,gearImage2RTk]
        data.anchor1x=data.gear1.armAnchor()[0]
        data.anchor1y=data.gear1.armAnchor()[1]
        data.anchor2x=data.gear2.armAnchor()[0]
        data.anchor2y=data.gear2.armAnchor()[1]
        cX1=data.gear1.getCenter()[0]
        cY1=data.gear1.getCenter()[1]
        r1=data.gear1.getArmLenght()
        circle1=(cX1,cY1,r1)
        cX2=data.gear2.getCenter()[0]
        cY2=data.gear2.getCenter()[1]
        r2=data.gear2.getArmLenght()
        circle2=(cX2,cY2,r2)
        data.end1x=circle_intersection(circle1,circle2)[0]
        data.end1y=circle_intersection(circle1,circle2)[1]
        data.end2x=circle_intersection(circle1,circle2)[0]
        data.end2y=circle_intersection(circle1,circle2)[1]
        data.points.append([data.end1x,data.end1y])
        if data.colorMode!="black":
            if data.timer%50==0:
                data.color=data.colorPalette[data.colorCounter%16]
        if data.settingsTextDir==False:
            data.settingsTextX-=1
            if data.settingsTextX<10:
                data.settingsTextDir=True
        elif data.settingsTextDir==True:
            data.settingsTextX+=1
            if data.settingsTextX>data.width-10:
                data.settingsTextDir=False
    if data.stopDrawing==True:
        path="parameters"
        content=""
        for point in data.points:
            content+=str(point[0])+","+str(point[1])+";"
        writeFile(path,content)
    if data.mode=="zen":
        data.timer+=1
        (x,y)=getPoint(data)
        data.pointsZen.append((x,y))
    
def zenTimerFired(data):
    data.timer+=1
    (x,y)=getPoint(data)
    data.pointsZen.append((x,y))
    
## MousePressed

def initScreenMousePressed(event, data):
    x,y=event.x,event.y
    infoBounds=data.infoButton.getButtonBounds()
    playBounds=data.playButton.getButtonBounds()
    if (infoBounds[0][0]<x<infoBounds[1][0] 
                               and infoBounds[0][1]<y<infoBounds[1][1]):
        data.mode="info"
    elif (playBounds[0][0]<x<playBounds[1][0]
                               and playBounds[0][1]<y<playBounds[1][1]):
        data.mode="settings"
    elif (playBounds[0][0]<x<playBounds[1][0]
                               and playBounds[0][1]<y<playBounds[1][1]):
        data.credits=True
        
def infoMousePressed(event, data):
    x,y=event.x,event.y
    mainBounds=data.mainButton.getButtonBounds()
    playBounds=data.playButton.getButtonBounds()
    if (mainBounds[0][0]<x<mainBounds[1][0] 
                               and mainBounds[0][1]<y<mainBounds[1][1]):
        data.mode="initScreen"
    elif (playBounds[0][0]<x<playBounds[1][0]
                               and playBounds[0][1]<y<playBounds[1][1]):
        data.mode="settings"

def settingsMousePressed(event, data):
    for i in range(len(data.sampleList)):
        coordinates=ithCellBounds(data, i)
        if (coordinates[0]<event.x<coordinates[2] and 
                         coordinates[1]<event.y<coordinates[3]):
            data.points=[]
            global settings
            settings=data.listOfDrawingModes[i]
    init(data)

def harmonographMousePressed(event, data):
    pass
    
def zenMousePressed(event, data):
    pass
    
## KeyPressed
    
def initScreenKeyPressed(event, data):
    pass
        
def infoKeyPressed(event, data):
    if event.keysym=="left":
        data.mode=="initScreen"

def settingsKeyPressed(event, data):
    pass
    
def harmonographKeyPressed(event, data):
    if event.keysym=="v":
        if data.visualizeMechanism==False:
            data.visualizeMechanism=True
        else:
            data.visualizeMechanism=False
    elif event.keysym=="m":
        data.mode="initScreen"
    elif event.keysym=="h":
        data.mode="help"
    elif event.keysym=="r":
        data.colorMode="rainbow"
        data.colorPalette=["red3","firebrick2", "DeepPink3","VioletRed4",
                                "magenta4","purple4","SlateBlue4","blue4",
                                "DeepSkyBlue4","aquamarine4","chartreuse4",
                                "yellow4","gold3","goldenrod1",
                                "chocolate2","OrangeRed2"]
        print("now I changed to rainbow")
    elif event.keysym=="g":
        data.colorMode="grayscale"
        data.colorPalette=['gray1','gray10','gray18','gray25','gray35','gray45',
                   'gray55','gray65','gray75','gray65','gray55','gray45', 
                    'gray35','gray25','gray18','gray10', 'gray1']
    elif event.keysym=="b":
        data.colorMode="black"
    elif event.keysym=="z":
        data.mode="zen"
    elif event.keysym=="+":
        data.damping1+=0.01
        data.damping2+=0.01
    elif event.keysym=="-":
        data.damping1-=0.01
        data.damping2-=0.01
    
def zenKeyPressed(event, data):
    if event.keysym=="p":
        data.drawPointsZen=False if data.drawPointsZen==True else True
    
## draw

def drawInit(canvas, data):
    image=data.initHarmonograms[1]
    canvas.create_image(data.width/6,data.height/3*2,image=image)
    boardOffset=10
    shadeOffset=1
    initText="The Harmonograph"
    canvas.create_text(data.width-data.margin+shadeOffset,data.height/4*3+shadeOffset,
                                          text=initText,
                                      anchor=E, fill="gray60",font="Courier 20")
    canvas.create_text(data.width-data.margin,data.height/4*3,
                                 text=initText,
                                      anchor=E, fill="gray10",font="Courier 20")
    if data.credits==True:
        canvas.create_text(data.width-data.margin,data.height/4*3,
                                text=initText,anchor=E, fill="gray10",font="Courier 20")
    creditText="A CMU 15-112 term project. Special thanks to all 15-112 teaching team."
    canvas.create_text(data.width-50,data.height/30*29,
                                 text=creditText,
                                      anchor=NE,fill="gray20",font="Courier 9 bold")

def drawInfoText(canvas, data):
    text="A harmonograph is a drawing machine controlled by the motion of pendulums or rotating disks. \nIt generates beautiful and complex curves - ellipses, spirals, figure eights, Lissajous figures."
    ellipses="ellipses"
    spirals="spirals"
    figure8="figure eights"
    lissajous="Lissajous figures"
    canvas.create_text(data.width/2,data.height/5,
                                 text=text,
                                      anchor=N, fill="black",font="Courier 12")
    canvas.create_image(data.width/3,data.height/3*2,image=data.imageH)


def drawGears(canvas, data):    
        data.gear1.draw(canvas)
        data.gear2.draw(canvas)

def drawArms(canvas, data):  
    jointR=10
    canvas.create_line(data.anchor1x,data.anchor1y,data.end1x,
                                             data.end1y,width=6,fill="gray70")
    canvas.create_oval(data.anchor1x-jointR,data.anchor1y-
                                     jointR,data.anchor1x+jointR,data.anchor1y+
                                                   jointR,width=0,fill="gray20")
    canvas.create_line(data.anchor2x,data.anchor2y,data.end2x,
                                             data.end2y,width=6,fill="gray70")
    canvas.create_oval(data.anchor2x-jointR,data.anchor2y-
                                     jointR,data.anchor2x+jointR,data.anchor2y+
                                                   jointR,width=0,fill="gray20")
    
def drawPoints(canvas, data):
    for point in data.points:
        x,y=point[0],point[1]
        canvas.create_oval(x-1,y-1,x+1,y+1,fill="black")
                                           
def drawLines(canvas, data):
    for i in range (len(data.points)-1):
        lineFill="black" if data.colorMode=="black" else data.colorPalette[i%16]
        point1x=data.points[i][0]
        point1y=data.points[i][1]
        point2x=data.points[i+1][0]
        point2y=data.points[i+1][1]
        canvas.create_line(point1x,point1y,point2x,point2y,
                                           fill=lineFill)
                                        
def drawWall(canvas, data):
    image=data.wallPaper
    canvas.create_image(data.width/2,data.height/2,image=image)

def instructions(canvas, data):
    text="Press b to draw in black, g to draw in grayscale, r to draw in rainbow mode. Press m for main menu. Press z for zen mode."
    canvas.create_text(data.width/2+2+data.settingsTextX,data.height/30*29+2,
                                 text=text,fill="gray70",font="Courier 14 bold")
    canvas.create_text(data.width/2+data.settingsTextX,data.height/30*29,
                                 text=text,fill="gray30",font="Courier 14 bold")
                                 
def instructionsZen(canvas, data):
    text="Press m for main menu"
    canvas.create_text(data.width/2+2+data.settingsTextX,data.height/30*29+2,
                                 text=text,fill="gray70",font="Courier 14 bold")
    canvas.create_text(data.width/2+data.settingsTextX,data.height/30*29,
                                 text=text,fill="gray30",font="Courier 14 bold")
                                 
def parameters(canvas, data):
    text1="centerX=%d \ncenterY=%d \nradius=%d \nangular momentum=%0.1f"%(int(data.gear1x),int(data.gear1y),int(data.gear1radius),data.gear1pangular)
    canvas.create_text(data.width/8,data.height/5*4,
                                 text=text1,fill="maroon",font="Courier 13 bold")
    text2="centerX=%d \ncenterY=%d \nradius=%d \nangular momentum=%0.1f"%(int(data.gear2x),int(data.gear2y),int(data.gear2radius),data.gear2pangular)
    canvas.create_text(data.width/9*8,data.height/5*4,
                                 text=text2,fill="midnightblue",font="Courier 13 bold")

def drawSettingsText(canvas, data):
    text="Click on a harmonogram to check how it was created"
    canvas.create_text(data.width-5,data.height/30,
                                 text=text,
                                      anchor=E,fill="maroon",font="Courier 14 bold")
    
def drawSamples(canvas, data):
    image=data.initHarmonograms[1]
    canvas.create_image(data.width/6,data.height/3*2,image=image)
    for i in range(len(data.sampleList)):
        canvas.create_rectangle(data.width/4*(i%4)+120-100,data.height/3*(i%3)+40,
                                data.width/4*(i%4)+120+100,data.height/3*(i%3)+200, fill="white", width=3)
        image=data.sampleList[i]
        canvas.create_image(data.width/4*(i%4)+120,data.height/3*(i%3)+120,image=image)

def drawPencil(canvas, data):
    image=data.pencil
    canvas.create_image(data.points[-1][0]+15,data.points[-1][1]-15,image=image)
    
def createImage(canvas, data):
    canvas.create_image(data.width/8,data.height/8,image=data.photo222)
    
def drawGearImages(canvas, data):
    image1=data.gearImages[0]
    image2=data.gearImages[1]
    canvas.create_image(data.gear1x,data.gear1y,image=image1)
    canvas.create_image(data.gear2x,data.gear2y,image=image2)

def drawPaper(canvas, data):
    data.paper.draw(canvas)
    
def drawPointZen(canvas, data):
    for point in data.pointsZen:
        x,y=point[0],point[1]
        canvas.create_oval(x-1,y-1,x+1,y+1, fill=data.drawColorZen)
        
def drawLinesZen(canvas, data):
    for i in range (len(data.pointsZen)-1):
        point1x=data.pointsZen[i][0]
        point1y=data.pointsZen[i][1]
        point2x=data.pointsZen[i+1][0]
        point2y=data.pointsZen[i+1][1]
        canvas.create_line(point1x,point1y,point2x,point2y,width=1,
                                           fill=data.drawColorZen)
                                           
# def drawCredits(canvas, data):
#     text="A CMU 15-112 term project. \nSpecial thanks to all 15-112 teaching team."
#     canvas.create_text(data.width/3*2,data.height/30*28,
#                                  text=text,
#                                       anchor=E,fill="gray50",font="Courier 9 bold")
        
        
##Redraw All

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width+100, data.height+100, fill="white")
    if data.mode=="initScreen":
        drawInit(canvas, data)
        data.infoButton.draw(canvas)
        data.playButton.draw(canvas)
        #data.creditsButton.draw(canvas)
        if data.credits==True:
            drawCredits(canvas, data)
    elif data.mode=="info":
        drawInfoText(canvas, data)
        data.mainButton.draw(canvas)
        data.playButton.draw(canvas)
    elif data.mode=="settings":
        drawSamples(canvas, data)
        drawSettingsText(canvas, data)
    elif data.mode=="zen":
        #drawPointZen(canvas,data)
        drawLinesZen(canvas,data)
        instructionsZen(canvas, data)
    elif data.mode=="harmonograph":
        drawWall(canvas, data)
        drawPaper(canvas, data)
        if data.visualizeMechanism==True:
            drawGears(canvas, data)
            drawGearImages(canvas, data)
        #drawPoints(canvas,data)
        drawLines(canvas, data)
        if data.visualizeMechanism==True:
            drawArms(canvas, data)
            drawPencil(canvas, data)
        instructions(canvas, data)
        parameters(canvas, data)
        #data.zenButton.draw(canvas)
    #createImage(canvas, data)

##RUN FUNCTION
#SOURCE OF THE RUN FUNCTION: CMU 15-112 course materials
####################################
# use the run function as-is
####################################

def run(width=1000, height=600):   #from CMU 15-112
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
    # create the root and the canvas
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root=Tk()
    root.configure(background="white")
    init(data)
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
    ("bye!")

####################################
# run call
####################################

run (1000, 700)