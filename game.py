import pygame
import random
import sys
import pygame_widgets
from pygame_widgets.button import Button


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (255, 0, 0), (50, 50), 35)
        self.x = sc_xy[0] // 2
        self.y = sc_xy[1] - 250
        self.speed = 15
        self.score = 0
        self.lives = 3
        self.level = 0
        self.uron = 1

    def update(self):
        self.rect = pygame.Rect([self.x, self.y, 100, 100])
        if pygame.mouse.get_pos()[0] < sc_xy[0] // 2:
            if self.x - self.speed > 0:
                self.x -= self.speed
        else:
            if self.x + self.speed < sc_xy[0]-100:
                self.x += self.speed
        screen.blit(self.image, (self.x, self.y))


class Knopkins(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h, text):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.image = pygame.Surface((w,h), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        self.f = pygame.font.SysFont(pygame.font.get_fonts()[5], 60)
        self.text_ = self.f.render(f'{self.text}', True, 'white')
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.image.blit(self.text_, (0,0))

    def update(self):
        self.image.fill((0,0,0,0))
        self.text_ = self.f.render(f'{self.text}', True, 'white')
        self.image.blit(self.text_, (0, 0))
        screen.blit(self.image, (self.x, self.y))


class Enemy(pygame.sprite.Sprite):
    liv = 10
    speed_y = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = Enemy.liv
        self.image = pygame.Surface((100, 100))
        self.image.fill((random.randint(100,255),random.randint(100,255),random.randint(100,255)))
        self.x = random.randint(100, sc_xy[0]-100)
        self.y = 0
        self.speed = 5
        self.speed_y = Enemy.speed_y
        self.level = 1
        self.f = pygame.font.SysFont(pygame.font.get_fonts()[5], 90)
        self.color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        self.text = self.f.render(f'{self.lives}', True, self.color)
        self.image.blit(self.text, (0, 0))
        self.otskok = True
        self.rect = pygame.Rect([self.x, self.y, 100, 100])

    def update(self):
        self.rect = pygame.Rect([self.x, self.y, 100, 100])
        if self.x - self.speed > 0 and self.otskok:
            self.x -= self.speed
        else:
            self.otskok = False
        if self.x + self.speed < sc_xy[0]-100 and not self.otskok:
            self.x += self.speed
        else:
            self.otskok = True
        self.text = self.f.render(f'{self.lives}', True, 'black')
        self.y += self.speed_y
        self.image.fill(self.color)
        pygame.draw.circle(self.image, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)),
                           (50, 50), self.lives*5)
        self.image.blit(self.text, (0, 0))
        screen.blit(self.image, (self.x, self.y))

        if self.lives < 1:
            self.kill()
        if self.y > sc_xy[1]:
            gamover()


def gamover():
    while True:
        f = pygame.font.SysFont(pygame.font.get_fonts()[5], random.randint(10, 100))
        text = f.render(f'{ochki_.ochki_g}', True, (random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        screen.blit(pygame.transform.rotate(text, random.randint(1,360)), (random.randint(-100,sc_xy[0]), random.randint(-10, sc_xy[1])))
        text = f.render(f'Игра Окончена', True, (random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        screen.blit(pygame.transform.rotate(text, random.randint(1,360)), (random.randint(-100, sc_xy[0]), random.randint(-10, sc_xy[1])))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == oboi_spawn:
                sprite_oboi.add(Oboi())
            if event.type == bonus_spawn:
                sprite_bonus.add(Bonus())
            if event.type == pygame.MOUSEBUTTONDOWN:
                exit_()

        sprite_bonus.update()
        sprite_oboi.update()
        pygame.display.update()


class Pulya(pygame.sprite.Sprite):
    def __init__(self, napravlenie=0):
        self.napravlenie = napravlenie
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 2))
        self.image.fill('red')
        self.x = player.x+50
        self.y = player.y
        self.i = 1
        self.rect = pygame.Rect([self.x, self.y, 10, 10])
        self.otskok = True

    def update(self):
        if self.x + self.napravlenie <= 0:
            self.napravlenie = abs(self.napravlenie)
        elif self.x + self.napravlenie >= sc_xy[0]:
            self.napravlenie = -self.napravlenie
        self.x += self.napravlenie
        self.i += 5
        self.y -= self.i
        pygame.draw.circle(self.image, (255, 255, 255), (5, 5), self.i//9)
        self.rect = pygame.Rect([self.x, self.y, 10, 10])
        screen.blit(self.image, (self.x, self.y))
        if self.y < 0:
            self.kill()


def vibor_puli():
    if player.level == 0:
        return [Pulya()]
    elif player.level == 1:
        return [Pulya(3), Pulya(-3)]
    elif player.level == 2:
        return [Pulya(), Pulya(2), Pulya(-2)]
    elif player.level == 3:
        return [Pulya(30), Pulya(40), Pulya(-30), Pulya(-40)]


class Ochki(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ochki = 0
        self.ochki_g = 0
        self.f = pygame.font.SysFont(pygame.font.get_fonts()[5], 136)
        self.text = self.f.render(f'{self.ochki}', True, 'white')

    def update(self):
        self.text = self.f.render(f'{self.ochki}', True, 'white')
        screen.blit(self.text, (sc_xy[0]-len(str(self.ochki)) * 80, 50))


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill((random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        self.x = random.randint(100, sc_xy[0] - 100)
        self.level = random.randint(0, 3)
        self.y = 0
        self.speed = 10
        self.level = random.randint(0, 2)
        self.rect = pygame.Rect([self.x, self.y, 150, 150])
        self.otskok = True
        self.i = 0

    def update(self):
        self.i += 1
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect = pygame.Rect([self.x, self.y,150,150])
        if self.x - self.speed > 0 and self.otskok:
            self.x -= self.speed
        else:
            self.otskok = False
        if self.x + self.speed < sc_xy[0] - 100 and not self.otskok:
            self.x += self.speed
        else:
            self.otskok = True
        self.y += self.speed

        screen.blit(pygame.transform.rotate(self.image, self.i), (self.x, self.y))

        if self.y > sc_xy[1]:
            self.kill()


class Oboi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.verh_niz = random.choice([True, False])
        if self.verh_niz:
            self.x = random.randint(0, sc_xy[0])
            self.y = sc_xy[1]
        else:
            self.x = random.randint(0, sc_xy[0])
            self.y = -100
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.i = 1
        self.alpha = 100
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        if self.verh_niz:
            self.i += 1
            self.y -= 8
            self.alpha -= 1
            self.image.fill((0,0,255,self.alpha))
            self.rect = self.image.get_rect(center=self.rect.center)
            if self.alpha < 1 or self.y < -100:
                self.kill()
        else:
            self.i += 1
            self.y += 8
            self.alpha -= 1
            self.image.fill((255, 0, 155, self.alpha))
            self.rect = self.image.get_rect(center=self.rect.center)
            if self.alpha < 1 or self.y < -100:
                self.kill()

        screen.blit(pygame.transform.rotate(self.image, self.i), (self.x, self.y))


def exit_():
    pygame.quit()
    sys.exit()


def game():
    clock = pygame.time.Clock()
    i = 1
    bobo = True
    button_menu = pygame.Surface((200,100), pygame.SRCALPHA)

    f = pygame.font.SysFont(pygame.font.get_fonts()[5], 70)
    text = f.render(f'Меню', True, 'white')

    while True:
        if i == 255:
            bobo = False
        if i == 1:
            bobo = True
        if bobo:
            i += 1
        else:
            i -= 1
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == enemy_spawn:
                sprite_enemy.add(Enemy())

            if event.type == pulya_spawn:
                for vib_ in vibor_puli():
                    sprite_pulya.add(vib_)

            if event.type == bonus_spawn:
                sprite_bonus.add(Bonus())
                Enemy.liv += 1
                Enemy.speed_y += 1

            if event.type == oboi_spawn:
                sprite_oboi.add(Oboi())

            if event.type == pygame.MOUSEBUTTONDOWN and button_menu.get_rect().collidepoint(pygame.mouse.get_pos()):
                return

        for enemy_ in sprite_enemy.sprites():
            for pulya_ in sprite_pulya.sprites():
                if pygame.sprite.collide_rect(pulya_, enemy_):
                    pulya_.kill()
                    enemy_.lives -= player.uron
                    enemy_.color = (100,255,random.randint(1,255))
                    ochki_.ochki += player.uron
                    ochki_.ochki_g += player.uron

        for bonus_ in sprite_bonus.sprites():
            if pygame.sprite.collide_rect(player, bonus_):
                player.level = bonus_.level
                ochki_.ochki += 500
                ochki_.ochki_g += 500
                bonus_.kill()

        sprite_oboi.update()
        sprite_player.update()
        sprite_pulya.update()
        sprite_enemy.update()
        sprite_ochki.update()
        sprite_bonus.update()
        button_menu.fill((255, 255, 255, 0))
        button_menu.blit(text, (0, 0))
        screen.blit(button_menu, (10, 10))
        #pygame_widgets.update(event)

        pygame.display.flip()
        clock.tick(60) / 1000

def nastroiki():
    f = pygame.font.SysFont(pygame.font.get_fonts()[5], 60)
    clock = pygame.time.Clock()
    while True:
        text = f.render(f'{player.uron}', True, 'white')
        text_s = f.render(f'{player.speed}', True, 'white')
        screen.fill('black')
        screen.blit(text, (400,300))
        screen.blit(text_s, (400,400))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == oboi_spawn:
                sprite_oboi.add(Oboi())

            if event.type == pygame.MOUSEBUTTONDOWN and but_nazad.rect.collidepoint(pygame.mouse.get_pos()):
                return

            if event.type == pygame.MOUSEBUTTONDOWN and but_uron_plus.rect.collidepoint(pygame.mouse.get_pos()):
                if ochki_.ochki >= 1000:
                    player.uron += 1
                    ochki_.ochki -= 1000
                    sprite_knopkin.update()

            if event.type == pygame.MOUSEBUTTONDOWN and but_speed_plus.rect.collidepoint(pygame.mouse.get_pos()):
                if ochki_.ochki >= 1000:
                    player.speed += 5
                    ochki_.ochki -= 1000

        sprite_ochki.update()
        sprite_knopkin.update()
        sprite_oboi.update()
        pygame.display.flip()
        clock.tick(60) / 1000

def start():
    clock = pygame.time.Clock()
    button_start = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        100,  # X-coordinate of top left corner
        100,  # Y-coordinate of top left corner
        300,  # Width
        150,  # Height

        # Optional Parameters
        text='Играть',  # Text to display
        fontSize=100,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=80,  # Radius of border corners (leave empty for not curved)
        onClick=game  # Function to call when clicked on
    )
    button_exit = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        100,  # X-coordinate of top left corner
        300,  # Y-coordinate of top left corner
        300,  # Width
        150,  # Height

        # Optional Parameters
        text='Настройки',  # Text to display
        fontSize=80,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=80,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: nastroiki()  # Function to call when clicked on
    )
    button_exit = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        100,  # X-coordinate of top left corner
        500,  # Y-coordinate of top left corner
        300,  # Width
        150,  # Height

        # Optional Parameters
        text='Выход',  # Text to display
        fontSize=100,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=80,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: exit_()  # Function to call when clicked on
    )
    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == enemy_spawn:
                for i in range(2):
                    sprite_oboi.add(Oboi())

        sprite_oboi.update()
        sprite_ochki.update()
        pygame_widgets.update(event)
        pygame.display.update()
        clock.tick(60) / 1000


pygame.init()
#'''
if pygame.display.get_active():
    screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[pygame.display.get_active()], pygame.FULLSCREEN)
    sc_xy = pygame.display.get_desktop_sizes()[pygame.display.get_active()]
else:
    screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[-1], pygame.FULLSCREEN)
    sc_xy = pygame.display.get_desktop_sizes()[-1]
#'''
#screen = pygame.display.set_mode((600,800))
#sc_xy = (600,800)


sprite_pulya = pygame.sprite.Group()
sprite_enemy = pygame.sprite.Group()
sprite_player = pygame.sprite.Group()
sprite_ochki = pygame.sprite.Group()
sprite_bonus = pygame.sprite.Group()
sprite_oboi = pygame.sprite.Group()
sprite_knopkin = pygame.sprite.Group()
player = Player()
sprite_player.add(player)
ochki_ = Ochki()
sprite_ochki.add(ochki_)
but1 = Knopkins(100, 300, 300, 100, 'Урон')
but_uron_plus = Knopkins(500, 300, 100, 100, '+')
but2 = Knopkins(100, 400, 300, 200, 'Скорость')
but_speed_plus = Knopkins(500, 400, 100, 100, '+')
but_nazad = Knopkins(100, 500, 300, 100, 'Назад')

sprite_knopkin.add(but1)
sprite_knopkin.add(but2)
sprite_knopkin.add(but_nazad)
sprite_knopkin.add(but_uron_plus)
sprite_knopkin.add(but_speed_plus)

enemy_spawn = pygame.USEREVENT + 0
pygame.time.set_timer(enemy_spawn, 1000)
pulya_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(pulya_spawn, 100)
bonus_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(bonus_spawn, 13000)
oboi_spawn = pygame.USEREVENT + 3
pygame.time.set_timer(oboi_spawn, 50)

#gamover()
start()
#game()

