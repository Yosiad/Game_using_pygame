import pygame
import os
import random
pygame.init()

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1300


BG = pygame.image.load(os.path.join("Assets/Other", "sunrise.jpg"))


#MUSIC

pygame.mixer.music.load(os.path.join("Assets/music", "musi.mp3"))
pygame.mixer.music.play(-1)

#IMAGES

birds = pygame.image.load(os.path.join("Assets/Other", "birds.png"))
homePage = [pygame.image.load(os.path.join("Assets/horse", "home.png"))]
flags    = [pygame.image.load(os.path.join("Assets/Other", "ethiopia flag.png")),
            pygame.image.load(os.path.join("Assets/Other", "italy flag.png"))]
tank     = [pygame.image.load(os.path.join("Assets/Other", "tank.png"))]
road     = pygame.image.load(os.path.join("Assets/Other", "road 3.jpg"))
RUNNING  = [pygame.image.load(os.path.join("Assets/horse", "run_1.png")),
           pygame.image.load(os.path.join("Assets/horse", "run_2.png")),
           pygame.image.load(os.path.join("Assets/horse", "run_3.png"))] 
JUMPING  = pygame.image.load(os.path.join("Assets/horse", "jump 2.png"))
down     = pygame.image.load(os.path.join("Assets/horse", "down.png"))
largeObstacle = [pygame.image.load(os.path.join("Assets/fire", "largeFire.png")),
                pygame.image.load(os.path.join("Assets/fire", "stone 1.png")),
                pygame.image.load(os.path.join("Assets/fire", "stone 2.png")),
                ]
foods = [pygame.image.load(os.path.join("Assets/Other", "food.png"))]

ARROWS  = [pygame.image.load(os.path.join("Assets/arrow", "arrow.png")),
        pygame.image.load(os.path.join("Assets/arrow", "arrow.png")),
        pygame.image.load(os.path.join("Assets/arrow", "arrow.png")),
        pygame.image.load(os.path.join("Assets/arrow", "arrow.png"))]

planes = [pygame.image.load(os.path.join("Assets/Other", "plane 1.png")),
          pygame.image.load(os.path.join("Assets/Other", "plane 2.png"))]




SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG_image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.blit(BG_image, (0, 0))


class HORSE:
    X_POS = 40
    Y_POS = 430
    Y_POS_DOWN = 510
    JUMP_VEL = 6

    def __init__(self):
        self.down_img = down
        self.run_img = RUNNING
        self.jump_img = JUMPING
        
        self.horse_down = False
        self.horse_run = True
        self.horse_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.horse_rect = self.image.get_rect()
        self.horse_rect.x = self.X_POS
        self.horse_rect.y = self.Y_POS

    def update(self, userInput):
        if self.horse_down:
            self.down()
        if self.horse_run:
            self.run()
        if self.horse_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.horse_jump:
            self.horse_down = False
            self.horse_run = False
            self.horse_jump = True
        elif userInput[pygame.K_DOWN] and not self.horse_jump:
            self.horse_down = True
            self.horse_run = False
            self.horse_jump = False
        elif not (self.horse_jump or userInput[pygame.K_DOWN]):
            self.horse_down = False
            self.horse_run = True
            self.horse_jump = False

    def down(self):
        self.image = self.down_img
        self.horse_rect = self.image.get_rect()
        self.horse_rect.x = self.X_POS
        self.horse_rect.y = self.Y_POS_DOWN
        self.step_index += 1
        
        

        
        
    def run(self):
        self.image = self.run_img[self.step_index // 4]
        self.horse_rect = self.image.get_rect()
        self.horse_rect.x = self.X_POS
        self.horse_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.horse_jump:
            self.horse_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.4
        if self.jump_vel < - self.JUMP_VEL:
            self.horse_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.horse_rect.x, self.horse_rect.y))
        


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH - 380

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def eatFood(self):
        obstacles.pop()

class Food(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        
        rand = random.randint(0, 3)
        
        if rand == 0:
            self.rect.y = 350
        elif rand == 1:
            self.rect.y = 500
        else:
            self.rect.y = 550
    
    

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 540


class ARROW(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 430
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 4], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = HORSE()
    game_speed = 15
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0


    
    def score(pnt = 1):
        global points, game_speed
        points += pnt
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

 
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

        bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_surface.blit(BG_image, (0, 0))
        SCREEN.blit(bg_surface, (0, 0))
        userInput = pygame.key.get_pressed()
        
        SCREEN.blit(birds,(20,140))
        
        SCREEN.blit(road, (0, 580))
        
        SCREEN.blit(planes[0], (1000, 100))
        
        SCREEN.blit(flags[0], (SCREEN_WIDTH // 2 - 320, 0))
        SCREEN.blit(flags[1], (SCREEN_WIDTH // 2 + 80, 0))
        
        
        SCREEN.blit(tank[0], (SCREEN_WIDTH - 400,500))
        
        
        
        player.draw(SCREEN)
        player.update(userInput)



        
        if len(obstacles) == 0:
            if random.randint(0, 3) <= 1:
                obstacles.append(LargeCactus(largeObstacle))
            elif random.randint(0, 3) == 2:
                obstacles.append(ARROW(ARROWS))
            else:
                obstacles.append(Food(foods))
                

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            
            if type(obstacle) == Food:
                if player.horse_rect.colliderect(obstacle.rect):
                    points += 100
                    obstacle.eatFood()
                    
            else:
                if type(obstacle) == LargeCactus:
                    tolerance = -60
                else:
                    tolerance = - 65 

                if player.horse_rect.inflate(tolerance, tolerance).colliderect(obstacle.rect.inflate(tolerance, tolerance)):
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)


        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        
        SCREEN.fill((255, 255, 255))
        
        font = pygame.font.Font('freesansbold.ttf', 30)
        
        text1 = font.render("ADWA GAME", True, (0, 0, 0))
        textRect1 = text1.get_rect()
        textRect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 210)
        SCREEN.blit(text1, textRect1)
        
        if death_count == 0:
            
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 135)
            SCREEN.blit(score, scoreRect)
            
        
        
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170)
        SCREEN.blit(text, textRect)
        SCREEN.blit(homePage[0], (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 310))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
