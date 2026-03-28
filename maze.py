#Подключение библиотек
from pygame import *
mixer.init()
font.init()

#Создание окна
window = display.set_mode((700, 500))
display.set_caption('Maze')

#Фоновая музыка

mixer.music.load('jungles.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y  += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = 'left'
    
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x > 615:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        if self.direction == 'right':
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Создание переменных
game = True
finish = False
clock = time.Clock()
hero = transform.scale(image.load('hero.png'), (100, 100))
cyborg = transform.scale(image.load('cyborg.png'), (100, 100))
background = transform.scale(image.load('background.jpg'), (700, 500))

x1 = 100
x2 = 300
y1 = 300
y2 = 300

player = Player('hero.png', 50, 300, 6)
enemy = Enemy('cyborg.png', 400, 300, 3)
treasure = GameSprite('treasure.png', 600, 400, 10)

wall1 = Wall(0, 190, 0, 150, 0, 10, 400)
wall2 = Wall(0, 190, 0, 270, 200, 10, 300)
wall3 = Wall(0, 190, 0, 270, 200, 200, 10)
wall4 = Wall(0, 190, 0, 470, 200, 10, 300)
wall5 = Wall(0, 190, 0, 470, 200, 100, 10)
wall6 = Wall(0, 190, 0, 470, 100, 10, 100)
wall7 = Wall(0, 190, 0, 270, 100, 10, 100)

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font1 = font.Font(None, 60)
text1 = font1.render('YOU WIN!', True, (233, 215, 0))
font2 = font.Font(None, 60)
text2 = font2.render('YOU LOOSE!', True, (250, 0, 0))
#Основной цикл
while game:

    for i in event.get():
        if i.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        enemy.reset()
        treasure.reset()
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()

        player.update()
        enemy.update()

        if sprite.collide_rect(player, treasure):
            finish = True
            money.play()
            mixer.music.stop()
            window.blit(text1, (220, 220))
        if (sprite.collide_rect(player, enemy) or
            sprite.collide_rect(player, wall1) or
            sprite.collide_rect(player, wall2) or
            sprite.collide_rect(player, wall3) or
            sprite.collide_rect(player, wall4) or
            sprite.collide_rect(player, wall5) or
            sprite.collide_rect(player, wall6) or
            sprite.collide_rect(player, wall7)):
            finish = True
            kick.play()
            mixer.music.stop()
            window.blit(text2, (220, 220))

    clock.tick(60)
    display.update()
