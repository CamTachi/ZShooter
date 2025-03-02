import pygame
import random
import time
pygame.init()

window_width = 1200
window_height = 700
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Арканоид с астероидами")
zombies = []
bullets = []
barricades = []
clock = pygame.time.Clock()

dark = (0, 0, 0)
orange = (255, 155, 0)
red = (225, 0, 0)
green = (0, 225, 0)
white = (255, 255, 255)
fon = pygame.transform.scale(pygame.image.load("images//fon.png"), (window_width, window_height))

class Ship:
    def __init__(self):
        self.rect = pygame.Rect(window_width // 2 - 25, window_height - 60, 50, 50)
        self.image = pygame.transform.scale(pygame.image.load("images//player.png"), (50, 50))
        self.hp = 4
        self.magazine = 5
        self.big_bullet = 3
        self.reload = False
        self.flag_time = True
        self.last_time = time.time()
    def shoot(self):
        if self.magazine > 0:
            self.magazine -= 1
            bullet = Bullet(self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2)
            bullets.append(bullet)
    def big_shoot(self):
        if self.big_bullet > 0:
            self.big_bullet -= 1
            for j in range(5):
                bullet = Bullet(self.rect.x + self.rect.width // 5 * j, random.randint(self.rect.y - 5, self.rect.y + 5))
                bullets.append(bullet)
    def update(self):
        if self.magazine <= 0:
            self.reload = True
        if self.reload:
            if self.flag_time:
                self.last_time = time.time()
                self.flag_time = False
            if time.time() - self.last_time > 0.65:
                self.magazine = 5
                self.reload = False
                self.flag_time = True
        self.rect.x = pygame.mouse.get_pos()[0] - self.rect.width // 2
        window.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-3, y, 6, 10)
        self.image = pygame.transform.scale(pygame.image.load("images//bullet.png"), (8, 10))
    def update(self):
        self.rect.y -= 9
        if self.rect.y < 0:
            bullets.remove(self)
        window.blit(self.image, self.rect)

class Zombie:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(5, window_width - 50), random.randint(-100, -10), 45, 45)
        self.image = pygame.transform.scale(pygame.image.load("images//zombie.png"), (45, 45))
        self.speed = random.randint(1, 3)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_height:
            ship.hp -= 1
            zombies.remove(self)
        window.blit(self.image, self.rect)

class Barricade:
    def __init__(self, x, y, weight, height):
        self.rect = pygame.Rect(x, y, weight, height)
        self.image = pygame.transform.scale(pygame.image.load("images//block.png"), (weight, height))
        self.hp = 4
    def update(self):
        window.blit(self.image, self.rect)

def spawn_zombies(amount):
    for i in range(amount):
        zombie = Zombie()
        zombies.append(zombie)

ship = Ship()
level = 0
running = True
flag_time = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ship.shoot()
            elif event.button == 3:
                ship.big_shoot()
    if ship.hp <= 0:                                                                                                           # !!!
        window.blit(pygame.font.Font(None, 91).render("YOU LOSE", True, dark), (window_width/2 - 358, window_height/2 - 153))  # !!!
        window.blit(pygame.font.Font(None, 90).render("YOU LOSE", True, red), (window_width/2 - 350, window_height/2 - 150))   # !!!
        time.sleep(1)                                                                                                          # !!!
        running = False                                                                                                        # !!!
    if level == 5:                                                                                                             # !!!
        window.blit(pygame.font.Font(None, 91).render("WIN", True, dark), (window_width/2 - 358, window_height/2 - 153))       # !!!
        window.blit(pygame.font.Font(None, 90).render("WIN", True, green), (window_width/2 - 350, window_height/2 - 150))      # !!!
        time.sleep(1)                                                                                                          # !!!
        running = False                                                                                                        # !!!

    window.blit(fon, (0, 0, window_width, window_height))
    for zombie in zombies:
        zombie.update()
        if ship.rect.colliderect(zombie.rect):
            ship.hp -= 1
            zombies.remove(zombie)
    for barricade in barricades:
        barricade.update()
        for zombie in zombies:
            if zombie.rect.colliderect(barricade.rect):
                barricade.hp -= 1
                zombies.remove(zombie)
                if barricade.hp <= 0:
                    barricades.remove(barricade)
    for bullet in bullets:
        bullet.update()
        for zombie in zombies:
            if bullet.rect.colliderect(zombie.rect):
                bullets.remove(bullet)
                zombies.remove(zombie)
                break
    ship.update()
    
    if not zombies:
        if flag_time:
            last_time = time.time()
        flag_time = False
        if time.time() - last_time < 4:
            window.blit(pygame.font.Font(None, 91).render("ХВИЛЯ НАБЛИЖУЄТЬСЯ", True, dark), (window_width/2 - 358, window_height/2 - 153))
            window.blit(pygame.font.Font(None, 90).render("ХВИЛЯ НАБЛИЖУЄТЬСЯ", True, red), (window_width/2 - 350, window_height/2 - 150))
        elif time.time() - last_time > 5:
            level += 1
            flag_time = True
            spawn_zombies(9 + level * 3)
            ship.hp += 2
            ship.big_bullet += 2
            barricade = Barricade(random.randint(0, window_width-50), window_height*0.8, 50, 50)
            barricades.append(barricade)
    
    for i in range(ship.hp):
        pygame.draw.rect(window, dark, (4 + i*20, 9, 16, 16))
        pygame.draw.rect(window, red, (6 + i*20, 10, 16, 16))
    for i in range(ship.big_bullet):
        pygame.draw.rect(window, dark, (4 + i*12, 29, 8, 16))
        pygame.draw.rect(window, orange, (6 + i*12, 30, 8, 16))
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.line(window, white, (mouse_pos[0]-4, mouse_pos[1]+5), (mouse_pos[0]-4, mouse_pos[1]+22))
    pygame.draw.line(window, white, (mouse_pos[0]-4, mouse_pos[1]+22), (mouse_pos[0]-16, mouse_pos[1]+22))
    pygame.draw.line(window, white, (mouse_pos[0]-16, mouse_pos[1]+22), (mouse_pos[0]-16, mouse_pos[1]+5))
    for i in range(ship.magazine):
        pygame.draw.rect(window, orange, (mouse_pos[0]-14, mouse_pos[1]+4*i+2, 9, 3))
    
    pygame.display.flip()
    clock.tick(60)