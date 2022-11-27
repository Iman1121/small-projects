#creating a platformer game with pygame. The goal of the game is to jump around and reach the exit.
#the dimentions of the game are 500 by 500 pixels.
#This version of the game doesn't look pretty





# starting pygame
import pygame
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
fps = 24
#creating a window where the game will occur
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("platformer game")

#global variables
win = 0
tile_size = 25

#not part of code. just there to help me place objects. this function creates gridlines
'''def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))'''

#images
background_img = pygame.image.load('img/bg.png')
background_img = pygame.transform.scale(background_img, (500,500))
start_img = pygame.image.load('img/start2.png')
quit_img = pygame.image.load('img/quit2.png')
restart_img = pygame.image.load('img/restart2.png')

#for creating buttons
class Button():
        def __init__(self, x, y, image):
            
                self.image = pygame.transform.scale(image, (100,50))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.click = False
        def draw(self):
                mouse_click = False

                #get mouse position
                pos = pygame.mouse.get_pos()

                #check if mouse is over button  
                if self.rect.collidepoint(pos):
                        # checking for click
                        if pygame.mouse.get_pressed()[0] == 1:
                                mouse_click = True
                                self.click = True
                if pygame.mouse.get_pressed()[0] == 0:
                        self.click = False
                
                
                #draw buttons
                screen.blit(self.image, self.rect)
                #returning mouseclick in case I want an action based upon a click
                return mouse_click  


#class for player 
class Player():
        def __init__(self, x, y):
                #I don't give his atributes in his initialize state. I made a reset method so I can call on it when the player wants replay level
                self.reset(x,y)
        def update(self, win):
                #variables for calculating if collision occurs between player and sprites
                dx = 0
                dy = 0
                #if the player has won this code won't run
                if win == 0:
                        
                        #get keypresses for moving character
                        key = pygame.key.get_pressed()
                        if key[pygame.K_UP] and self.jump == False and self.jumping == False:
                                self.velocity = -15
                                self.jump = True
                        if key[pygame.K_UP] == False:
                                self.jump = False
                        if key[pygame.K_LEFT]:
                                dx -= 5
                                
                        if key[pygame.K_RIGHT]:
                                dx += 5
                        #gravity
                        self.velocity += 1
                        
                        if self.velocity > 10:
                                self.velocity = 10
                        dy += self.velocity
                        
                        #check for collision
                        self.jumping = True
                        for tile in world.tile_list:
                                #checking for collision by the x axis
                                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0
                                #checking for collision by the y axis
                                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        #check if below a platform
                                        if self.velocity < 0:
                                                dy = tile[1].bottom - self.rect.top
                                                self.velocity = 0
                                        #check if over a platform
                                        elif self.velocity >= 0:
                                                dy = tile[1].top - self.rect.bottom
                                                self.velocity = 0
                                                self.jumping = False

                        #check for collision between player and winning_point
                        if pygame.sprite.spritecollide(self, exit_group, False):
                                #if player has won, new screen will open up 
                                win = 1


                #move player        
                self.rect.x += dx
                self.rect.y += dy


                #draw player
                screen.blit(self.image, self.rect)
                return win
        def reset(self, x, y):
                self.images_right = []
                self.index = 0
                self.counter = 0
                #everything about character is stored here
                img = pygame.image.load('img/character1.png')
                self.image = pygame.transform.scale(img, (15,22))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.velocity = 0
                self.jump = False
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.jumping = True

#class for winning the level
class Exit(pygame.sprite.Sprite):
        def __init__(self,x,y):
                
                pygame.sprite.Sprite.__init__(self)
                img = pygame.image.load('img/door.png')
                self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5 )))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

#class for map and everything thats inside it
class World():
    def __init__(self, data):
        #stores all relevant map data
        self.tile_list = []

        #platform image
        blocks = pygame.image.load('img/background.png')
        dirt_img = pygame.image.load('img/dirt.png')
        #going through mapdata list to extract map data. The y axis
        row_count = 0
        for row in data:
            colomn_count = 0
            #going through lists inside the mapdata list. The x axis
            for tile in row:
                if tile == 1:
                        #loading in blocks to place in the map. if the data is written as 1 in the mapdata lists, then that spot will be filled
                        #with a blue block
                    img = pygame.transform.scale(blocks,(tile_size, tile_size))
                        #creating an invisible rectangle. This is created for collisions
                    img_rect = img.get_rect()
                    img_rect.x = colomn_count * tile_size
                    img_rect.y = row_count * tile_size
                       #storing the x and y cord of where the blue block and rectangle is created
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                        #loading in blocks to place in the map. if the data is written as 1 in the mapdata lists, then that spot will be filled
                        #with a blue block
                    img = pygame.transform.scale(dirt_img,(tile_size, tile_size))
                        #creating an invisible rectangle. This is created for collisions
                    img_rect = img.get_rect()
                    img_rect.x = colomn_count * tile_size
                    img_rect.y = row_count * tile_size
                       #storing the x and y cord of where the blue block and rectangle is created
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                        #placing exit on the map
                        #used to calculate the x and y cord of the exit
                    close = Exit(colomn_count * tile_size, row_count * tile_size - 10)
                    exit_group.add(close)
                colomn_count += 1
            row_count += 1
    def draw(self):
            #drawing the map
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

#creating map data
#1 = border , 0 = empty space, 2 = exit, 3 = dirt
mapdata = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,1],
[1,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
#instances of classes
exit_group = pygame.sprite.Group()
world = World(mapdata)
player = Player(50, screen_height - 72)

#buttons
start_button = Button(screen_width//2 - 200, screen_height//2, start_img)
quit_button = Button(screen_width//2 + 100, screen_height//2, quit_img)
restart_button = Button(screen_width//2 - 200, screen_height//2, restart_img)

#main loop
run = True
main_menu = True
while run:
    clock.tick(fps)
        #10 milisecond delay between each iteration to slow everything down
    pygame.time.delay(10)
    #background image
    screen.blit(background_img, (0,0))
    #menu screen
    if main_menu:    
            if quit_button.draw():
                run = False
            if start_button.draw():
                main_menu = False
    else:
        #checking if the player won 
            if win == 1:
                if restart_button.draw():
                        player.reset(50, screen_height - 72)    
                        win = 0
                if quit_button.draw():
                        run = False
            else:
                    #going through code
                    world.draw()
                    exit_group.draw(screen)
                    

                    win = player.update(win)
            #draw_grid()
#setting up and a way to exit game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#to refresh whenever somethinig occurs. For example character changing location
    pygame.display.update()

pygame.quit()
