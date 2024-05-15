import pygame
import pygame.gfxdraw
import sys
import math
from random import randint

pygame.init()

WIDTH, HEIGHT =  800, 800
ROAD_WIDTH = 80
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic SImulation")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GREEN = (57,200,20)
DARK_GREY = (80, 78, 81)

COLORS = [BLUE, GREEN, RED, YELLOW]

GREEN_TIME = 10
YELLOW_TIME = 5
RED_TIME = 3*GREEN_TIME + 3*YELLOW_TIME
LOOP_DURATION = 4*GREEN_TIME + 4*YELLOW_TIME

redLight = pygame.image.load("red.png")
yellowLight = pygame.image.load("yellow.png")
greenLight = pygame.image.load("green.png")

redLight = pygame.transform.scale(redLight, (30,90))
yellowLight = pygame.transform.scale(yellowLight, (30,90))
greenLight = pygame.transform.scale(greenLight, (30,90))




class Car:
    velocity = 2

    acc = 1/600
    deacc = -2/60
    point_index = 0

    def __init__(self, x, y, color, start, sec_track_index):
        self.x = x
        self.y = y
        self.color = color
        self.start = start
        self.track = first_track[start]
        self.track1 = first_track[start]
        self.track2 = second_trac[start][sec_track_index]
        self.finish = self.track2[-1]
        self.vel = Car.velocity
        self.brake = Car.deacc
        self.point_index = 0
        self.gap = 1000
    
    def updatePosition(self):
        '''fungsi untuk mengupdate posisi mobil'''

        global car_pass, waiting_cars
        current_dest = self.track[self.point_index]

        # menghitung vektor arah
        direction_vector = (current_dest[0] - self.x, current_dest[1] - self.y)
        distance = ((current_dest[0] - self.x)**2 + (current_dest[1] - self.y)**2)**0.5

        if self.gap < 60:
            self.vel += self.brake
            if self.vel < 0:
                self.vel =0
        else:
            self.vel = Car.velocity


        if distance > 0 and self.gap >= 30:
            step_x = (direction_vector[0]/distance*self.vel)
            step_y = (direction_vector[1]/distance*self.vel)            
            self.x += custom_round(step_x)
            self.y += custom_round(step_y)
        elif distance == 0:
            self.point_index += 1
            if(self.point_index > len(self.track)-1):
                self.point_index = len(self.track)-1

        if reds[self.start] == 0 and self.track == self.track1 and self.point_index == len(self.track)-1 and distance < 1:
            self.track = self.track2
            waiting_cars[self.start] -= 1
            car_pass +=1
            self.point_index = 0
        
        # menghapus mobil saat sudah tiba di tujuan
        if self.x == self.finish[0] and self.y == self.finish[1]:
            Cars[self.start].pop(0)

    def updateGap():
        '''fungsi untuk mengupdate jarak dengan mobil di depannya'''
        for i in range(4):
            if len(Cars[i]) != 0:
                Cars[i][0].gap = 1000
        for i in range(len(Cars)):
            for j in range(len(Cars[i])-1):
                gap = ((Cars[i][j].x-Cars[i][j+1].x)**2 + (Cars[i][j].y-Cars[i][j+1].y)**2)**0.5
                Cars[i][j+1].gap = gap

       
def custom_round(n):
    if n > 0:
        return math.ceil(n)
    else:
        return math.floor(n)
        
def Screen(width, height):
    SCREEN = pygame.display.set_mode((width, height))
    return SCREEN

def drawRoad():
    pygame.draw.rect(SCREEN, DARK_GREY, (WIDTH/2 - ROAD_WIDTH/2 ,0,ROAD_WIDTH, HEIGHT))
    pygame.draw.rect(SCREEN, DARK_GREY, (0, HEIGHT/2 - ROAD_WIDTH/2 ,WIDTH, ROAD_WIDTH))
    
    for i in range(1,10):
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2-40-10-40 - i*60, HEIGHT/2, 40, 5))
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2+40+10 + i*60, HEIGHT/2, 40, 5))
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2, HEIGHT/2 -40-10-40-i*60, 5, 40))
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2, HEIGHT/2+40+10 + i*60, 5, 40))
    for i in range(8):
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2-40-10-40, HEIGHT/2-40+8+i*12, 40, 5))
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2+40+10, HEIGHT/2-40+8+i*12, 40, 5))
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2-40+8+i*12, HEIGHT/2-40-10-40, 5, 40))
        pygame.draw.rect(SCREEN, WHITE, (WIDTH/2-40+8+i*12, HEIGHT/2+40+10, 5, 40))

def drawTrafficLamp():
    SCREEN.blit(traffic_lights[lamps[0]], lamp_coordinates[0])
    SCREEN.blit(pygame.transform.rotate(traffic_lights[lamps[1]], 90), lamp_coordinates[1])
    SCREEN.blit(traffic_lights[lamps[2]], lamp_coordinates[2])
    SCREEN.blit(pygame.transform.rotate(traffic_lights[lamps[3]], -90), lamp_coordinates[3])

def generateCar():
    global waiting_cars
    str_index = randint(0,3)
    car = Car(int(starting_point[str_index][0]),int(starting_point[str_index][1]), COLORS[randint(0, len(COLORS)-1)], str_index, randint(0,2))
    Cars[str_index].append(car)
    waiting_cars[str_index] +=1
    if waiting_cars[str_index] > waiting_cars[4]:
        waiting_cars[4] = waiting_cars[str_index]

def updateLampsCol(time):
    default_lamps = ["red","red","red","red"]
    global lamps
    lamps = default_lamps
    if time < GREEN_TIME:
        lamps = default_lamps
        lamps[0] = "green"
    elif time < GREEN_TIME + YELLOW_TIME:
        lamps = default_lamps
        lamps[0] = "yellow"
    elif time < (2*GREEN_TIME + YELLOW_TIME):
        lamps = default_lamps
        lamps[1] = "green"
    elif time < 2*(GREEN_TIME + YELLOW_TIME):
        lamps = default_lamps
        lamps[1] = "yellow"
    elif time < 2*(GREEN_TIME + YELLOW_TIME)+GREEN_TIME:
        lamps = default_lamps
        lamps[2] = "green"
    elif time < 3*(GREEN_TIME + YELLOW_TIME):
        lamps = default_lamps
        lamps[2] = "yellow"
    elif time < 3*(GREEN_TIME + YELLOW_TIME)+GREEN_TIME:
        lamps = default_lamps
        lamps[3] = "green"
    else:
        lamps = default_lamps
        lamps[3] = "yellow"
    
def upadateRed():
    global reds, lamps
    for i in range(4):
        if lamps[i] == "red" or lamps[i] == "yellow":
            reds[i] = 1
        else:
            reds[i] = 0

FONT = pygame.font.SysFont(None, 20)
FPS = 60
clock = pygame.time.Clock()

def displayTxt():
    time = FONT.render(                     "Time                   " + str(int(secconds/60)) +" : "+ str(int(secconds%60)), True, BLACK)
    total_cars = FONT.render(               "Total Cars             :" + str(car_generate),True, BLACK)
    cars_passed = FONT.render(              "Car Passed             :" + str(car_pass),True, BLACK)
    car_per_minutes = FONT.render(          "Cars per Minute        :" + str("{:.4f}".format(car_generate/(secconds/60))),True, BLACK)
    cars_passed_per_min = FONT.render(      "Car Passed per Minute  :" + str("{:.4f}".format(car_pass/(secconds/60))),True, BLACK)

    green_duration = FONT.render(           "Green Time             :" + str(GREEN_TIME),True, BLACK)
    yellow_duration = FONT.render(          "Yellow Time            :" + str(YELLOW_TIME),True, BLACK)
    red_duration = FONT.render(             "Red Time                :" + str(RED_TIME),True, BLACK)

    cars_waiting_1 = FONT.render(           "Cars Waiting lane 1         :" + str(waiting_cars[0]),True, BLACK)
    cars_waiting_2 = FONT.render(           "Cars Waiting lane 2         :" + str(waiting_cars[1]),True, BLACK)
    cars_waiting_3 = FONT.render(           "Cars Waiting lane 3         :" + str(waiting_cars[2]),True, BLACK)
    cars_waiting_4 = FONT.render(           "Cars Waiting lane 4         :" + str(waiting_cars[3]),True, BLACK)
    maximum_waiting = FONT.render(          "Maximum Cars Waiting    :" + str(waiting_cars[4]),True, BLACK)
    text = (time, total_cars, cars_passed, car_per_minutes, cars_passed_per_min,
            green_duration,yellow_duration, red_duration, 
            cars_waiting_1, cars_waiting_2, cars_waiting_3, cars_waiting_4,
            maximum_waiting)

    for i in range(len(text)):
        SCREEN.blit(text[i], (20, 20 + i*20))

Cars = [[],[],[],[]]
waiting_cars = [0,0,0,0,0]
reds = [1, 1, 1, 1]
lamps = ["red","red","red","red"]



starting_point = (
    (WIDTH/2+20,0),
    (WIDTH, HEIGHT/2+20),
    (WIDTH/2-20, HEIGHT),
    (0, HEIGHT/2-20),
)



lamp_coordinates = (
    (int(WIDTH/2 + ROAD_WIDTH/2 + 20), int(HEIGHT/2 - ROAD_WIDTH/2 - 20 -90)),
    (int(WIDTH/2 + ROAD_WIDTH/2 + 20), int(HEIGHT/2 + ROAD_WIDTH/2 + 20)),
    (int(WIDTH/2 - ROAD_WIDTH/2 - 20 -30), int(HEIGHT/2 + ROAD_WIDTH/2 + 20)),
    (int(WIDTH/2 - ROAD_WIDTH/2 - 20 - 90), int(HEIGHT/2 - ROAD_WIDTH/2 - 20 -30))
)

traffic_lights = {
    "red":redLight,
    "yellow":yellowLight,
    "green" : greenLight
}

first_track = (
    ((WIDTH/2+20,0),(WIDTH/2+20,HEIGHT/2-40-20-60)),            #top
    ((WIDTH, HEIGHT/2+20),(WIDTH/2+40+20+60, HEIGHT/2+20)),     #right
    ((WIDTH/2-20, HEIGHT),(WIDTH/2-20, HEIGHT/2+40+20+60)),     #bottom
    ((0, HEIGHT/2-20),(WIDTH/2-40-20-60,HEIGHT/2-20)))          #left
second_trac = (
    (
        ((WIDTH/2+20,HEIGHT/2-20), (WIDTH/2+20,HEIGHT/2-20), (WIDTH/2+20, HEIGHT)),     #top-bottom
        ((WIDTH/2+20,HEIGHT/2-20), (WIDTH/2+20,HEIGHT/2-20), (WIDTH, HEIGHT/2-20)),     #top-right
        ((WIDTH/2+20,HEIGHT/2+20), (WIDTH/2+20,HEIGHT/2+20), (0, HEIGHT/2+20)),        #top-left
    ),
    (
        ((WIDTH/2+20,HEIGHT/2+20), (WIDTH/2+20,HEIGHT/2+20),(WIDTH/2+20, HEIGHT)),     #right-bottom
        ((WIDTH/2+20,HEIGHT/2+20), (WIDTH/2+20,HEIGHT/2+20),(0, HEIGHT/2+20)),         #right-left
        ((WIDTH/2-20,HEIGHT/2+20), (WIDTH/2-20,HEIGHT/2+20),(WIDTH/2-20,0))            #right-top
    ),
    (
        ((WIDTH/2-20,HEIGHT/2+20), (WIDTH/2-20,HEIGHT/2+20),(0, HEIGHT/2+20)),         #bottom-left    
        ((WIDTH/2-20,HEIGHT/2-20), (WIDTH/2-20,HEIGHT/2-20),(WIDTH, HEIGHT/2-20)),     #bottom-right
        ((WIDTH/2-20,HEIGHT/2+20), (WIDTH/2-20,HEIGHT/2+20),(WIDTH/2-20,0))            #bottom-top
    ),
    (
        ((WIDTH/2+20,HEIGHT/2-20), (WIDTH/2+20,HEIGHT/2-20),(WIDTH/2+20, HEIGHT)),     #left-bottom
        ((WIDTH/2-20,HEIGHT/2-20), (WIDTH/2-20,HEIGHT/2-20),(WIDTH/2-20,0)),           #left-top
        ((WIDTH/2-20,HEIGHT/2-20), (WIDTH/2-20,HEIGHT/2-20),(WIDTH, HEIGHT/2-20))      #left-right
    ),
)


car_pass = 0
car_generate = 0
secconds = 1
cars_per_sec = 2

def main():
    global reds, secconds, car_generate
    loop = 0
    i = 0
    j = 0


    global WIDTH, HEIGHT
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    run = True

    while run:

        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:  
                WIDTH, HEIGHT = event.size
                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        SCREEN.fill(WHITE)
        displayTxt()
        drawRoad()
        upadateRed()
        drawTrafficLamp()
        updateLampsCol(int(loop/60))

        if j%(cars_per_sec*60) == 0:
            generateCar()
            car_generate +=1
            

        for car_list in Cars:
            for car in car_list:
                
                pygame.gfxdraw.aacircle(SCREEN, car.x, car.y, 10, car.color)
                pygame.gfxdraw.filled_circle(SCREEN, car.x, car.y, 10, car.color)
                Car.updatePosition(car)
        Car.updateGap() 

             
        i+=1
        j+=1
        if(i%60 == 0):
            secconds +=1
            print(lamps, loop/60, LOOP_DURATION)
        #     print(car1.x, car1.y, direction_vector[0], direction_vector[1], distance, int(direction_vector[0]/distance*car1.vel), int(direction_vector[1]/distance*car1.vel))
        loop += 1
        if int(loop/60) == LOOP_DURATION:
            loop = 0
        pygame.display.update()
        
main()