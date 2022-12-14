from pygame import *
from random import *

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
score = 0
goal = 10
lost = 0
max_lost = 3



class GameSprite(sprite.Sprite):
    def __init__(self, character_image, x, y, width, height, speed):
        
        sprite.Sprite.__init__(self)
        self.image = image.load(character_image)
        self.image = transform.scale(self.image, (width, height))

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()


bullets = sprite.Group()

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            #monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 5))
            #monsters.add(monster)

        if lost >= max_lost or sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()
    
    else:
        finish = False
        score = 0
        lost = 0

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)


    for i in range(0, 1):
        monster = Enemy(img_enemy, randint(80, win_width - 80), 40, 80, 50, randint(1, 2))
        monsters.add(monster)

    time.delay(50)