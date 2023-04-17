from pygame import *
from random import randint
from time import sleep
import pygame
'''Необходимые классы'''


#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (wight, height)) #вместе 55,55 - параметры
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y


   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
   def update_r(self):
       keys = key.get_pressed()
       if keys[K_UP] and self.rect.y > 34:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 100:
           self.rect.y += self.speed
   def update_l(self):
       keys = key.get_pressed()
       if keys[K_w] and self.rect.y > 34:
           self.rect.y -= self.speed
       if keys[K_s] and self.rect.y < win_height - 100:
           self.rect.y += self.speed
   def sbros(self):
       self.rect.y = 185


#игровая сцена:
back = (201, 201, 201) #цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)


#флаги, отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60


#создания мяча и ракетки   
racket1 = Player('t/синяя платформа.png',20, 200, 4, 20, 100) 
racket2 = Player('t/розовая платформа.png', 600 - 40, 200, 4, 20, 100)
ball = GameSprite('t/мяч.png', 300, 250, 4, 20, 20)


font.init()
font1 = font.Font(None, 35)
lose1 = font1.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font1.render('PLAYER 2 LOSE!', True, (180, 0, 0))
draw = font1.render('NOBODY', True, (0, 200, 0))
fontsp = font.Font(None, 30)
score1txt = font1.render('score player1: 0',True,(255,255,255))
score2txt = font1.render('score player2: 0',True,(255,255,255))
torestart = font1.render('25',True,(0,200,0))
score1 = 0
score2 = 0

strike = 0
tt = 0
speed_x = randint(-5,5)
speed_y = randint(-3,3)
if speed_x == 0 or speed_y == 0:
    speed_x = 3
    speed_y = -2
surf1 = pygame.Surface((600,30))
surf1.fill((190, 190, 190)) 
surfC = pygame.Surface((4,500))
surfGr = pygame.Surface((600,4))
surfGr.fill((170, 170, 170))  


surfC.fill((190, 200-10, 190))  
strike_to_draw = 50
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
        

        score1txt = fontsp.render('score player1: '+ str(score1),True,(255,255,255))
        score2txt = fontsp.render('score player2: '+ str(score2),True,(255,255,255))
        if strike_to_draw - strike > 30:
            torestart = fontsp.render(str(strike_to_draw - strike),True,(0,200,0))
        elif strike_to_draw - strike <= 30 and strike_to_draw - strike > 10:
            torestart = fontsp.render(str(strike_to_draw - strike),True,(247, 223, 41))
        elif strike_to_draw - strike <= 10:
            torestart = fontsp.render(str(strike_to_draw - strike),True,(200,0,0))
        window.fill(back)

        racket1.update_l()
        racket2.update_r()
        if tt == 0:
            sleep(2)
            tt = 1
        menu = Rect((0, 0, 600, 20))
        window.blit(surf1,menu)
        window.blit(score1txt,(5,5))
        window.blit(score2txt,(430,5))
        window.blit(torestart,(290,10))


        ball.rect.x += speed_x
        ball.rect.y += speed_y


        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            strike += 1
        window.blit(surfC,(298,30))
        window.blit(surfGr,(0,30))
        if strike >= strike_to_draw:
            finish = True
            window.blit(draw,(250, 200))
        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-20 or ball.rect.y < 34:
            speed_y *= -1

        
        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            score2 += 1
            window.blit(lose1, (200, 200))
            game_over = True


       #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            score1 += 1
            game_over = True

        
        racket1.reset()
        racket2.reset()
        ball.reset()
    else:
        
        ball.rect.x, ball.rect.y = 300, 250
        speed_x = randint(-5,5)
        speed_y = randint(-3,3)
        if speed_x == 0 or speed_y == 0:
            speed_x = 3
            speed_y = -2
        strike = 0
        finish = False
        racket1.sbros()
        racket2.sbros()
        display.update()
        torestart = fontsp.render(str(strike_to_draw - strike),True,(200,0,0))
        for i in range(10):
            display.update()
            sleep(0.3)



    display.update()
    clock.tick(FPS)