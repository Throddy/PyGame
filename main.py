import pygame, os, sys


pygame.init()
pygame.display.set_caption('ChaseBlueSquare')
size = width, height = 800, 800
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join(f'data\{name}')
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MainChar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(MCGroup)
        self.a = 20
        self.image = pygame.Surface((self.a, self.a),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, 'blue',
                         (0, 0, self.a, self.a))
        self.rect = pygame.Rect(x, y, self.a, self.a)

    def update(self, vx, vy):
        if abs(vx) == abs(vy) == 5:
            vx = vx / (2 ** 0.5)
            vy = vy / (2 ** 0.5)
        self.rect = self.rect.move(vx, vy)


class MCBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(BulletsGroup)
        self.a = 10
        self.b = 50
        self.image = pygame.Surface((self.a, self.b),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('red'),
                         (0, 0, self.a, self.b))
        self.rect = pygame.Rect(x, y, self.a, self.b)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(EnemiesGroup)
        self.a = 10
        self.b = 10
        self.image = pygame.Surface((self.a, self.b),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('yellow'),
                         (0, 0, self.a, self.b))
        self.rect = pygame.Rect(x, y, self.a, self.b)
        self.collide_MC = False

    def update(self, x2, y2, norm_v=5 / (2 ** 0.5)):
        if not self.collide_MC:
            x1, y1 = self.rect.x, self.rect.y

            perp_x = x2 - x1
            perp_y = y2 - y1

            dist = (perp_x ** 2 + perp_y ** 2) ** 0.5
            if dist != 0:
                vx = (perp_x / dist) * norm_v
                vy = (perp_y / dist) * norm_v
                collided_enemies = pygame.sprite.spritecollide(self, EnemiesGroup, False)
                if len(collided_enemies) > 1:
                    vx += abs(collided_enemies[1].rect.x - x1 - 15 * norm_v)
                    vy += abs(collided_enemies[1].rect.y - y1 - 25 * norm_v)
                    self.rect = self.rect.move(vx, vy)
                elif pygame.sprite.spritecollideany(self, MCGroup):
                    self.collide_MC = True
                else:
                    self.rect = self.rect.move(vx, vy)


if __name__ == '__main__':
    MCGroup = pygame.sprite.Group()
    character = MainChar(50, 400)
    MCGroup.add(character)
    BulletsGroup = pygame.sprite.Group()
    EnemiesGroup = pygame.sprite.Group()
    for x in range(100, 780, 140):
        for y in range(60, 760, 140):
            EnemiesGroup.add(Enemy(x, y))
    running = True
    FPS = 60
    clock = pygame.time.Clock()

    while running:
        vx, vy = 0, 0
        screen.fill('black')

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_a]:
                    vx = -10
            if keys[pygame.K_d]:
                    vx = 10
            if keys[pygame.K_w]:
                    vy = -10
            if keys[pygame.K_s]:
                    vy = 10

        chX, chY = character.rect.x, character.rect.y
        MCGroup.update(vx=vx, vy=vy)
        MCGroup.draw(screen)

        BulletsGroup.draw(screen)

        EnemiesGroup.update(chX, chY)
        EnemiesGroup.draw(screen)


        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()