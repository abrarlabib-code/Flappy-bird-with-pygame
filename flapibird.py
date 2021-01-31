import pygame
import random
pygame.init()

win = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("flapi bird")
bg = pygame.image.load("bgtestgame.svg")
clock = pygame.time.Clock()


birdpos = [pygame.image.load("birdupforgame.png")]
pillarpic = [pygame.image.load("pillardown1.png")]
pillarvel = 7
pillarback = True
sbartap = False


class bird:
    def __init__(self, x, y, width, height, jumpstep):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumpstep = jumpstep
        self.gravity = 20
        self.fly = False
        self.gethit = False
        self.hitbox = (self.x + 8, self.y + 4, 46, 58)

    def draw(self, win):
        win.blit(birdpos[0], (self.x, self.y))
        self.hitbox = (self.x + 8, self.y + 4, 46, 58)
        # pygame.draw.rect(win,(255,0,0),self.hitbox,2)


class pillarcls:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y-300, 76, 847)
        self.hitbox2 = (self.x, self.y + 650, 72, 847)

    def draw(self, win):
        win.blit(pillarpic[0], (self.x, self.y))
        win.blit(pillarpic[0], (self.x, self.y+740))
        self.hitbox = (self.x, self.y-300, 76, 847)
        self.hitbox2 = (self.x, self.y + 740, 72, 847)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox2, 2)


# gamewindow
def gamedraw():
    win.blit(bg, (0, 0))
    text = font.render("Score: " + str(score//2), 0, (0, 0, 255))
    overtext = overfont.render("Game over", 0, (0, 0, 0))
    if sbartap == False:
        barinfotxt = barinfo.render("Tap Space-bar to start the game", 0, (255, 0, 0))
        flyinfo = barinfo.render("Tap/hold Space-bar to make the bird fly",0,(255,0,0))
        win.blit(barinfotxt, (100, 400))
        win.blit(flyinfo,(100,460))
    win.blit(text, (0, 10))
    parrot.draw(win)
    for pillar in pillars:
        pillar.draw(win)
        if pillarback == True:
            pillar.x -= pillarvel

    if parrot.gethit == True:
        pygame.draw.rect(win, (200, 100, 0), (0, 0, 1000, 600))
        win.blit(overtext, (250, 100))
        win.blit(text, (400, 300))
    pygame.display.update()


# pillarposition
plrx = 1000

# fonts
overfont = pygame.font.SysFont("comicsens", 100, True)
font = pygame.font.SysFont("comicsens", 30, True, True)
barinfo = pygame.font.SysFont("comicsens", 50, True)

# characters
pillars = []
parrot = bird(100, 100, 64, 64, 25)
flyloop = 1
score = 0

# mainloop
flying = True
while flying:
    clock.tick(20)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            flying = False

    if keys[pygame.K_SPACE]:
        sbartap = True

    if sbartap == True:
        plry = random.choice([-300,-200,-400,-500])

        if flyloop > 0:
            flyloop += 1
        if flyloop > 25:
            flyloop = 1

        if parrot.gethit == False:
            if not(keys[pygame.K_SPACE]):
                parrot.y += parrot.gravity
            if keys[pygame.K_SPACE] and parrot.y - 10 >= 0:
                parrot.fly = True
                parrot.y -= parrot.jumpstep
            else:
                parrot.fly = False

        if pillarback == True:
            for pillar in pillars:
                if not (parrot.x > pillar.hitbox[0]+pillar.hitbox[2]):
                    if (parrot.y < pillar.hitbox[1] - 20 + pillar.hitbox[3] and not (parrot.x > pillar.hitbox[0] + pillar.hitbox[2])):
                        if (parrot.x + parrot.hitbox[2] > pillar.hitbox[0] and parrot.x < pillar.hitbox[0] + pillar.hitbox[2] and not (parrot.x > pillar.hitbox[0] + pillar.hitbox[2])):
                            pillarback = False
                            parrot.gethit = True
                            parrot.fly = False
                            pygame.time.delay(750)
                    if (parrot.y + parrot.hitbox[3] - 15 > pillar.hitbox2[1] and not (parrot.x > pillar.hitbox2[0] + pillar.hitbox2[2])):
                        if (parrot.x + parrot.hitbox[2] > pillar.hitbox2[0] and parrot.x < pillar.hitbox2[0] + pillar.hitbox2[2] and not (parrot.x > pillar.hitbox2[0] + pillar.hitbox2[2])):
                            pillarback = False
                            parrot.gethit = True
                            parrot.fly = False
                            pygame.time.delay(750)
                if parrot.x > pillar.hitbox[0] + pillar.hitbox[2]:
                    score += 1
                if pillar.x < 1000 and pillar.x > 0:
                    for i in range(pillarvel):
                        pillar.x -= 1
                else:
                    pillars.pop(pillars.index(pillar))
            if parrot.y + parrot.hitbox[3] - 10 >= 600:
                pillarback = False
                parrot.gethit = True
                parrot.fly = False
                pygame.time.delay(750)
            if flyloop == 25:
                pillars.append(pillarcls(plrx, plry))

    gamedraw()

pygame.quit()
