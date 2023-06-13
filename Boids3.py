import random
import pygame as pg
import math
import colorsys


#--------------------------------------------------------------Global variables
WIDTH = 1000
HEIGHT = 1000
RUNNING = True

SEPARATION = 1
ALIGNMENT = 1.2
COHESION = -0.001

MARGIN = 200

MAGNITUDE = 18
BOIDSNUMBER = 2000

TURNFACTOR = MAGNITUDE*0.05


#-------------------------------------------------------------------Init pygame
pg.init()
wn = pg.display.set_mode((WIDTH, HEIGHT))

#-------------------------------------------------------------------------Lists
boids = []
cells = []
inner = []

#Loop to create nested list for cells
def makeCells():
    cells.clear()
    inner.clear()
    for y in range(11):
        row = []
        for x in range(10):
            row.append([])
        cells.append(row)
makeCells()

#-------------------------------------------------------------------Boids class
class boid:
    def __init__(self, x, y, vx, vy, hue):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.hue = hue
        self.fov = 120
    
    def move(self):
        self.x += (self.vx * MAGNITUDE)
        self.y += (self.vy * MAGNITUDE)

        RGB = colorsys.hsv_to_rgb(1-self.hue, 0.5 , 1)
        r = RGB[0]*255
        g = RGB[1]*255
        b = RGB[2]*255
        
        #r = 255
        #g = 255
        #b = 255
        
        x = self.x
        y = self.y 
        vx = (x + self.vx*20)
        vy = (y + self.vy*20)
        pg.draw.line(wn, (0,0,0), (x,y), (vx,vy),1)
        #pg.draw.circle(wn, (255,255,255), (x, y), 4)
        #pg.draw.circle(wn, (255,255,255), (vx, vy), 2)
        
        
        #EDGES
        if x > WIDTH - MARGIN:
            self.vx -= TURNFACTOR*1
        if x < 0 + MARGIN:
            self.vx += TURNFACTOR*1
        if y > HEIGHT - MARGIN:
            self.vy -= TURNFACTOR*1
        if y < 0 + MARGIN:
            self.vy += TURNFACTOR*1
        
        
    def visible(self, x, y):#**************************************************

        myAng = math.atan2(self.vx, self.vy)
        myDegs = math.degrees(myAng)
        getVX = self.x - x
        getVY = self.y - y
        ang = math.atan2(getVX, getVY)
        degs = math.degrees(ang)+180
        if myDegs < 0:
            myDegs += 359
        if myDegs > 359:
            myDegs -= 359
        if degs < 0:
            degs += 359
        if degs > 359:
            degs -= 359
        degsFovPort = degs-(self.fov/2)
        degsFovStar = degs+(self.fov/2)
        if myDegs > degsFovPort and myDegs < degsFovStar:
            return True
        else:
            return False
        
        
    def getDistance(self, x, y):
        line1 = abs(self.x - x) 
        line2 = abs(self.y - y) 
        distance = line1 + line2
        return(distance)

    def normalize(self):
        newVX = self.vx * self.vx
        newVY = self.vy * self.vy 
        normal = math.sqrt(newVX + newVY)
        self.vx = self.vx/normal
        self.vy = self.vy/normal
    
    def getCellX(self):
        cellX = math.floor(self.x/100)
        return(cellX)
    
    def getCellY(self):
        cellY = math.floor(self.y/100)
        return(cellY)
    
    
    
#---------------------------------------------------------------------Functions
#----------------------------------------------------------------MAKE THE BOIDS
def makeBoids(newBoids):
    for i in range(newBoids):
        x = random.randint(100, 900)
        y = random.randint(100, 900)

        
        vx = random.random()-0.5
        vy = random.random()-0.5
        hue = random.random()
        boids.append(boid(x, y, vx, vy, hue))
        boids[i].normalize()

makeBoids(BOIDSNUMBER)
 
#---------------------------------------------------------------------Normalize   
def normalize(x,y):
    newx = x**2
    newy = y**2
    combined = newx+newy
    normal = math.sqrt(combined)
    if x != 0: 
        x = x/normal
    if y != 0:
        y = y/normal
    normalized = [x,y]
    
    return(normalized)
 
#------------------------------------------------------Populate the cells array   
def populateCells():
    cells.clear()
    makeCells()
    for i in range(len(boids)):
        cellX = boids[i].getCellX()
        cellY = boids[i].getCellY()
        
        if cellX < 0:
            cellX = 0
        if cellX > 9:
            cellX = 9
        if cellY < 0:
            cellY = 0
        if cellY > 9:
            cellY = 9    
        
        
        
        cells[cellX][cellY].append(i)
        
        cellpop = len(cells[cellX][cellY])*5
        if cellpop > 255:
            cellpop = 255
        
        
        b = ((255-cellpop))
        g = 0
        r = cellpop
        
        
        pg.draw.rect(wn, (b, 255, b), ((cellX*100), (cellY*100), 100, 100),1)
        

#---------------------------------------------Get the boids in the nearby cells        
def getPopulation(x, y):
    if x < 1:
        x = 1
    if x > 8:
        x = 8
    if y < 1:
        y = 1
    if y > 8:
        y = 8    
    
    x=int(x)
    y=int(y)
        
    l1 = cells[x-1][y+1]
    l2 = cells[x][y+1] 
    l3 = cells[x+1][y+1]
    
    l4 = cells[x-1][y]
    l5 = cells[x][y]
    l6 = cells[x+1][y]
    
    l7 = cells[x-1][y-1]
    l8 = cells[x][y-1]
    l9 = cells[x+1][y-1]
    newList = l1+l2+l3+l4+l5+l6+l7+l8+l9
    return(newList)
    #return(l5)
   
#---------------------------------------------------------------------Main loop
#==============================================================================
breedAmount = 0
while RUNNING:
    wn.fill((255, 255, 255))
    
    
    

    
    for out in range(len(boids)):
        populateCells()
        boids[out].normalize()
        boids[out].move()
        visX = boids[out].x
        visY = boids[out].y
        zeroX = boids[out].x
        zeroY = boids[out].y
    
        pop=getPopulation(boids[out].getCellX(), boids[out].getCellY())
        
        separationX = 0
        separationY = 0
        separationVX = 0
        separationVY  = 0
        separationCount = 0
        separationVector = []
        desireVector = []
        desireVX = 0
        desireVY = 0
        racism = 0
        racismAvoid = 0
        
        
        alignmentVX = 0
        alignmentVY = 0
        alignmentVector = []
        alignmentCount = 0
    
        cohesionVX = 0
        cohesionVY = 0
        cohesionX = 0
        cohesionY = 0
        
        cohesionVector = []
        cohesionCount = 0
        
        #print(pop)
        if pop:
            for j in pop:
                #====================================================SEPARATION
                if boids[out].getDistance(boids[j].x, boids[j].y) < 4 and boids[out].getDistance(boids[j].x, boids[j].y) > 0:
                    separationX += boids[j].x
                    separationY += boids[j].y
                    separationCount +=1
                
                #=====================================================ALIGNMENT
                if boids[out].visible(boids[j].x, boids[j].y):
                    alignmentCount += 1
                    alignmentVX += boids[j].vx
                    alignmentVY += boids[j].vy               
                    
                #======================================================COHESION 
                if boids[out].visible(boids[j].x, boids[j].y):
                    cohesionCount += 1
                    cohesionX += boids[j].x
                    cohesionY += boids[j].y


            if separationCount > 0:
                separationX = separationX / separationCount
                separationY = separationY / separationCount
                separationVX = boids[out].x - separationX
                separationVY = boids[out].y - separationY
                separationVector = (normalize(separationVX, separationVY))
                separationVector[0]=separationVector[0]*SEPARATION
                separationVector[1]=separationVector[1]*SEPARATION
                desireVX += separationVector[0]
                desireVX += separationVector[1]
                
            if alignmentCount > 0:
                alignmentVector = normalize(alignmentVX, alignmentVY)
                
                alignmentVector[0] *= ALIGNMENT 
                alignmentVector[1] *= ALIGNMENT
                
                desireVX += alignmentVector[0]
                desireVY += alignmentVector[1]
                
            if cohesionCount > 0:
                cohesionX /= cohesionCount
                cohesionY /= cohesionCount
                cohesionVX = boids[out].x - cohesionX
                cohesionVY = boids[out].y - cohesionY
                cohesionVector = normalize(cohesionVX, cohesionVY)
                
                cohesionVector[0] *= COHESION
                cohesionVector[1] *= COHESION
                
                desireVX += cohesionVector[0]
                desireVY += cohesionVector[1]   
             
            desireVector = [desireVX, desireVY]
            boids[out].vx += (desireVector[0]*TURNFACTOR)
            boids[out].vy += (desireVector[1]*TURNFACTOR)

    pg.display.update()    

    
    breedAmount += 1
    #print(breedAmount)
    fname = "frames/" + str(breedAmount) + ".jpg"
    
    pg.image.save(wn, fname)

    
    #RUNNING = False