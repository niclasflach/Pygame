import random
import sys, pygame
import pygame.math as math
pygame.init()

size = width, height = 1024,800
black = 0,0,0
grey = 200,200,200
green = 180,250,180
screen = pygame.display.set_mode(size)
blobs = []
foods = []


class Blob:
    def __init__(self,position, size):
        self.life = random.randint(5000,10000)
        self.position = pygame.Vector2(position)
        # self.position = position
        self.size = size 
        self.direction = pygame.Vector2(random.randint(-10,10) , random.randint(-10,10) )
        self.speed = 0.1
        self.agility = 10
        
        self.direction = self.direction.normalize()
        print(self.direction * 5)
        # self.direction = random.randint(0,10) - 5, random.randint(0,10) - 5
    def __del__(self):
      print('Inside the destructor')
      print('Object gets destroyed')
    def draw(self):
        pygame.draw.circle(screen, (black), self.position, self.size, 0)
        pygame.draw.line(screen, black, self.position,  (self.size * 2 * self.direction) + self.position  )
    def look_for_food(self):
        pass
    def move(self):
        if self.position.x+self.direction.x < 20:
            self.direction = self.direction.rotate(self.agility)
        if self.position.x+self.direction.x > width-20:
            self.direction = self.direction.rotate(self.agility)
        if self.position.y < 20:
            self.direction = self.direction.rotate(self.agility)
        if self.position.y > height-20:
            self.direction = self.direction.rotate(self.agility)
        self.position = self.position + self.direction * self.speed
    def age(self):
        self.life -= 1
        
class Food:
    def __init__(self) -> None:
        self.position = pygame.Vector2(random.randint(0, width), random.randint(0,height))
        self.size = 3
    
    def draw(self):
        pygame.draw.circle(screen, (green), self.position, self.size, 0)
        
    
        
            
        

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

def remove_dead_blobs():
    blobs_to_kill = []
    for i in range(len(blobs)):
        if blobs[i].life <= 0:
            blobs_to_kill.append(i)    
            print("one mor blob is dead...")    
    for dead in blobs_to_kill:
        blobs.pop(dead)
        



generate_Food(100)
generate_Blobs(10)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(grey)
    
    for blob in blobs:
        blob.look_for_food()
        blob.move()
        blob.draw()
        blob.age()
                 
        #print(blob.life)
    for food in foods:
        food.draw()            
    remove_dead_blobs()
    
    pygame.display.flip()
    pygame.display.update()