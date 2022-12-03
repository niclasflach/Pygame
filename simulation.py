import random
import sys, pygame
import pygame.math as math
import math as pymath
import time

clock = pygame.time.Clock()


pygame.init()

size = width, height = 1024,800
black = 0,0,0
grey = 200,200,200
red = 255,0,0
green = 180,250,180
pink = 237, 104, 224
blue = 44, 44, 230
font = pygame.font.Font('freesansbold.ttf', 22)
prev_time = time.time()
FPS = 60


screen = pygame.display.set_mode(size)
blobs = []
foods = []
eaten_food = []


class Blob:
    def __init__(self,position, size, gender):
        self.life = random.randint(5000,10000)
        self.position = pygame.Vector2(position)
        # self.position = position
        self.gender = gender
        self.size = size 
        self.direction = pygame.Vector2(random.randint(-10,10) , random.randint(-10,10) )
        self.speed = 500
        self.agility = 0.5
        self.los_length = 450
        self.target = pygame.Vector2()
        self.angle_to_target = 0
        self.angle_distance_target = 0
        self.status = 0
        
        try:
            self.direction = self.direction.normalize()
        except:
            print("vector error")
        # self.direction = random.randint(0,10) - 5, random.randint(0,10) - 5
    
    def __del__(self):
      # print('Inside the destructor')
      # print('Object gets destroyed')
      pass
    
    
    def draw(self):
        #self.sprite to use with collision detection
        if self.gender == "male":
            blob_color = blue
        if self.gender == "female":
            blob_color = pink
        self.size = 5+ (self.life / 2000)
        self.sprite = pygame.draw.circle(screen, blob_color , self.position, self.size/2, 0)
        self.targetsprite = pygame.draw.circle(screen, blob_color , self.target, 2, 0)
        # pygame.draw.line(screen, black, self.position,  (self.size * 2 * self.direction) + self.position  )
    
    
    def look_for_food(self):
        for food in range(len(foods)):

            distance_vector = self.position - foods[food].position
            vector_to_target = self.position - self.target
            self.angle_to_target = vector_to_degrees(vector_to_target) 
            self.angle_distance_target = self.angle_to_target - (vector_to_degrees(self.direction) +180)
            self.angle_distance_target = map_to_range(self.angle_distance_target)
            #Whats the distance to the target
            distance_vector_target = self.target - self.position
            distance = distance_vector.length()
            distance_target = distance_vector_target.length()
            
            #Is it within the range of view
            if distance < self.los_length:
                distance_orientation = vector_to_degrees(distance_vector)
                angular_distance = distance_orientation - (vector_to_degrees(self.direction) +180)
                angular_distance = map_to_range(angular_distance)

                #Is the food with in the Point of View
                if abs(angular_distance) < 70:
                    if distance < distance_target:
                        self.target = foods[food].position
                    
                    line_color = green
                    #if foods[food].position == self.target:
                    #    line_color = black                 
                    #    pygame.draw.line(screen, line_color, self.position, foods[food].position  )
                
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
            self.direction = self.direction.rotate((-self.agility/self.size)*40)
        if self.angle_distance_target < 0:
            self.direction = self.direction.rotate((self.agility/self.size)*40)
        self.position = self.position + self.direction * (self.speed /(self.size)*dt)
        if self.position == self.target:
            self.target = pygame.Vector2()
    
    def mate(self):
        if self.status != 2:
            self.status = 1
        if self.gender == "female":
            self.speed = 0
        if self.gender == "male":
            for blob in range(len(blobs)):
                if blobs[blob].gender == "female" and blobs[blob].status == 1:
                    self.target = blobs[blob].position
                    vector_to_female = self.position - blobs[blob].position
                    distance_to_female = vector_to_female.length()
                    if distance_to_female < 50:
                        blobs[blob].status = 2
                    
                    
    
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
                #We have collided with a food
                #increase life
                self.life += foods[food].size * 80
                foods.pop(food)
                eaten_food.append(food)
                self.target = pygame.Vector2()
                return
            if self.sprite.colliderect(self.targetsprite):
                self.target = pygame.Vector2()
                return

            
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
def generate_Blobs(number, gender):
    """Generating a certain number of blobs with specified gender

    Args:
        number (int): Number of Blobs to generate
        gender (str "male" or "female"): Gender of the blobs to be created
    """
    generated = 0
    while generated < number:
        pos = [random.randint(10, 1000), random.randint(10, 780)]
        size = random.randint(3, 10)
        blobs.append(Blob(pos, size, gender))
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


generate_Food(20)
generate_Blobs(10, "male")
generate_Blobs(10, "female")

while True:
    clock.tick(FPS)    
    
    now = time.time()
    dt = now - prev_time
    prev_time = now
    
    generate_Food(1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(grey)
    
    for food in foods:
        food.draw()           
    
    blobs_life = []
    for blob in blobs:
        blob.look_for_food()
        blobs_life.append(blob.life)
        if blob.life > 15000 and blob.status != 2:
            blob.mate()
        if blob.life > 15000 and blob.status == 2:
            #Status 2 means pergnant and here two new babies are born
            generate_Blobs(1, "female")
            generate_Blobs(1, "male")
            blob.status = 0
        if blob.life < 10000 and blob.gender =="female":
            blob.speed = 500
        blob.move()
        blob.draw()
        blob.collision_detection() 
        blob.age()
    #if len(foods) < 10:
    #    generate_Food(20)                

    remove_dead_blobs()
    average = sum(blobs_life) // len(blobs_life)
    number_of_blobs = len(blobs)
    text = font.render('Average life:'+str(average), True, green, blue)
    text2 = font.render('Number of blobs:'+str(number_of_blobs), True, green, blue)
    textRect = text.get_rect()
    textRect2 = text2.get_rect()
    textRect.center = (400, height - 30)
    textRect2.center = (400, height - 10)
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    
    
    pygame.display.flip()
    pygame.display.update()