import random
import sys, pygame
import pygame.math as math
import math as pymath

pygame.init()

size = width, height = 1024,800
black = 0,0,0
grey = 200,200,200
red = 255,0,0
green = 180,250,180
screen = pygame.display.set_mode(size)
blobs = []
foods = []
eaten_food = []


class Blob:
    def __init__(self,position, size):
        self.life = random.randint(5000,10000)
        self.position = pygame.Vector2(position)
        # self.position = position
        self.size = size 
        self.direction = pygame.Vector2(random.randint(-10,10) , random.randint(-10,10) )
        self.speed = 0.1
        self.agility = 0.5
        self.los_length = 150
        self.target = pygame.Vector2()
        self.angle_to_target = 0
        self.angle_distance_target = 0
        
        self.direction = self.direction.normalize()
        # self.direction = random.randint(0,10) - 5, random.randint(0,10) - 5
    
    def __del__(self):
      # print('Inside the destructor')
      # print('Object gets destroyed')
      pass
    
    
    def draw(self):
        #self.sprite to use with collision detection
        
        self.size = 5+ (self.life / 2000)
        self.sprite = pygame.draw.circle(screen, (black), self.position, self.size, 0)
        pygame.draw.circle(screen, (red), self.target, 2, 0)
        pygame.draw.line(screen, black, self.position,  (self.size * 2 * self.direction) + self.position  )
    
    
    def look_for_food(self):
        for food in range(len(foods)):

            distance_vector = self.position - foods[food].position
            vector_to_target = self.position - self.target
            self.angle_to_target = vector_to_degrees(vector_to_target) 
            self.angle_distance_target = self.angle_to_target - (vector_to_degrees(self.direction) +180)
            self.angle_distance_target = map_to_range(self.angle_distance_target)

            distance_vector_target = self.target - self.position
            distance = distance_vector.length()
            distance_target = distance_vector_target.length()
            if distance < self.los_length:
                distance_orientation = vector_to_degrees(distance_vector)
                angular_distance = distance_orientation - (vector_to_degrees(self.direction) +180)
                angular_distance = map_to_range(angular_distance)


                if abs(angular_distance) < 70:
                    if distance < distance_target:
                        self.target = foods[food].position
                    
                    line_color = green
                    if foods[food].position == self.target:
                        line_color = black                 
                    pygame.draw.line(screen, line_color, self.position, foods[food].position  )
                
        pass
    
    
    def move(self):
        if self.position.x+self.direction.x < 20:
            self.target = pygame.Vector2((width/2, height/2))
        if self.position.x+self.direction.x > width-20:
            self.target = pygame.Vector2((width/2, height/2))
        if self.position.y < 20:
            self.target = pygame.Vector2((width/2, height/2))
        if self.position.y > height-20:
            self.target = pygame.Vector2((width/2, height/2))
        #print(self.angle_distance_target)
        if self.angle_distance_target > 0:
            self.direction = self.direction.rotate(-self.agility/2)
        if self.angle_distance_target < 0:
            self.direction = self.direction.rotate(self.agility/2)
        self.position = self.position + self.direction * self.speed
        if self.position == self.target:
            self.target = pygame.Vector2()
    
    
    def age(self):
        self.life -= 1
    
    
    def collision_detection(self):
        #Most likely need to put all food sprites in a group or something for this.
        #investigation best approach
        #pygame.sprite.collide_circle() is one approach
        eaten_food = []
        for food in range(len(foods)):
            # print(foods[food].sprite)
            if self.sprite.colliderect(foods[food].sprite):
                self.life += foods[food].size * 500
                
                foods.pop(food)
                
                eaten_food.append(food)
                self.target = pygame.Vector2()
                return
            #    print("Collision")
            # collisions = pygame.sprite.spritecollide(self.sprite.rect, foods[food].sprite.rect, False, pygame.sprite.collide_circle)
            # eaten_food.append(foods[food])
            # self.life += 1000
            
        pass
        
class Food:
    def __init__(self):
        self.sprite = pygame.sprite.Sprite()
        self.position = pygame.Vector2(random.randint(20, width-20), random.randint(20,height-20))
        self.size = random.randint(2,8)
    
    def draw(self):
        self.sprite = pygame.draw.circle(screen, (green), self.position, self.size, 0)
        # print(self.sprite)
        
    
         
        
# Function to generate blobs and put them in a list
def generate_Blobs(number):
    generated = 0
    while generated < number:
        pos = [random.randint(10, 1000), random.randint(10, 780)]
        size = random.randint(3, 10)
        blobs.append(Blob(pos, size))
        generated += 1
    return 

def generate_Food(number):
    generated = 0
    while generated < number:
        foods.append(Food())
        generated += 1
    return

def remove_eaten_food(eaten_food):
    for food in range(len(eaten_food)):
        print("Removing eaten food")
        print(food)
        try:
            foods.pop(food)
        except:
            print("Food not deletable index")
    eaten_food = []

    pass 

def remove_dead_blobs():
    blobs_to_kill = []
    for i in range(len(blobs)):
        if blobs[i].life <= 0:
            blobs_to_kill.append(i)    
            print("one mor blob is dead...")    
    for dead in blobs_to_kill:
        try:
            blobs.pop(dead)
        except:
            print("Cant delete food")


def vector_to_degrees(vector):
    """ Returns the angle from X+ axis to the given vector """
    return pymath.atan2(-vector[1], vector[0]) * (180/pymath.pi)


def map_to_range(orientation):
    """ Maps the angle orientation in degrees to range [-180, 180) """
    return orientation - 360*pymath.floor((orientation + 180) * (1/360))


generate_Food(100)
generate_Blobs(20)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(grey)
    
    for food in foods:
        food.draw()           
    
    for blob in blobs:
        blob.look_for_food()
        blob.move()
        blob.draw()
        blob.collision_detection() 
        blob.age()
    
    if len(foods) < 50:
        generate_Food(70)                

    remove_dead_blobs()
    
    pygame.display.flip()
    pygame.display.update()