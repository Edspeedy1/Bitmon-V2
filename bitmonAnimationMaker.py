import pygame, random
pygame.init()
SCREEN = pygame.display.set_mode((700,700))

def function():
    global legsF, legsB, body, head
    colors = []
    for i in range(3):
        C = [0,0,0]
        while True:
            if sum(C) > (40,40,200)[i]: break
            for i in range(3): C[i] = random.randint(0,255) 
        for i in range(3):
            C[i] = C[i]/255
        colors.append(C)

    body = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\Body'+str(random.randint(1, 12))+'.png')
    head = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\Head'+str(random.randint(1, 15))+'.png')
    legVar = random.randint(1, 9)
    legsF = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsF'+str(legVar)+'.png')
    legsB = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsB'+str(legVar)+'.png')

    def invert(img):
        for i in range(32):
            for j in range(32):
                color = img.get_at((i,j))
                if sum(color) > 15 and color[3] > 255:
                    pygame.draw.rect(img, (color[2], color[1], color[0]), (i,j,1,1))
        return img

    if random.randint(0, 1) == 1:
        body = invert(body)
    if random.randint(0, 1) == 1:
        head = invert(head)
    wingList = (5,7)
    ifwings = random.randint(0, 50) == 1 and legVar not in wingList
    wings = random.choice(wingList)
    surface = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\template.png')
    animationTemp = (((0,0), (-1,0), (0,-1), (0,0)), ((0,0), (-1,0), (-1,-1), (0,-1)), ((0,0), (0,-1), (-1,0), (0,0)), ((0,0), (1,0), (1,1), (0,1)))
    for ir, i in enumerate(random.choice(animationTemp)):
        surface.blit(legsB, (32*ir,0))
        if ifwings:
            surface.blit(pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsB'+str(wings)+'.png'), (32*ir+i[0],i[1]))
            surface.blit(body, (32*ir+i[0],i[1]))
            surface.blit(pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsF'+str(wings)+'.png'), (32*ir+i[0],i[1]))
        else: surface.blit(body, (32*ir+i[0],i[1]))
        surface.blit(head, (32*ir+i[0],i[1]))
        surface.blit(legsF, (32*ir,0))

    for i in range(128):
        for j in range(32):
            color = surface.get_at((i,j))
            if color[3] != 255: continue
            if color[0] >= 10 and color[1] <= 55 and color[2] <= 55:
                pygame.draw.rect(surface, (color[0]*colors[0][0], color[0]*colors[0][1], color[0]*colors[0][2]), (i,j,1,1))
            elif color[0] <= 55 and color[1] >= 10 and color[2] <= 55:
                pygame.draw.rect(surface, (color[1]*colors[1][0], color[1]*colors[1][1], color[1]*colors[1][2]), (i,j,1,1))
            elif color[0] <= 55 and color[1] <= 55 and color[2] >= 10:
                pygame.draw.rect(surface, (color[2]*colors[2][0], color[2]*colors[2][1], color[2]*colors[2][2]), (i,j,1,1))
    return surface

V = pygame.transform.scale(function(), (2800,700))

i = 0
c = 0
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                V = pygame.transform.scale(function(), (2800,700))
            if event.key == pygame.K_e:
                for j in [legsB, legsF,head,body]:
                    SCREEN.fill((25,25,55))
                    SCREEN.blit(pygame.transform.scale(j, (700,700)), (0,0))
                    pygame.display.update()
                    pygame.time.wait(1000)

    clock.tick(60)
    i += 1
    if i >= 60: 
        i = 0
        if c == 2: 
            V = pygame.transform.scale(function(), (2800,700))
            c = 0
        else: c += 1
    SCREEN.fill((25,25,55))
    SCREEN.blit(V, (-700*(i//15), 0))
    pygame.display.update()
