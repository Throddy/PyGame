import pygame, os, sys
from random import randint

pygame.init()
pygame.display.set_caption('Walking')
size = width, height = 1400, 800
min_width, min_height = 1200, 700
screen = pygame.display.set_mode(size, pygame.RESIZABLE, pygame.FULLSCREEN)


def load_image(name, colorkey=None):
    fullname = os.path.join(f'data/{name}')
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


"""
def load_level(filename):
    filename = "data/game/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('tree', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y
"""


# test


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def final_screen():
    outro_text = ["Окочание",
                  "Спасибо за тестирование игры.",
                  "Покедава!"]
    screen.fill('white')
    fon = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in outro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        outro_rect = string_rendered.get_rect()
        text_coord += 30
        outro_rect.top = text_coord
        outro_rect.x = 30
        text_coord += outro_rect.height
        screen.blit(string_rendered, outro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def make_img(img, w, h, persW, persH):
    return pygame.transform.scale(img, (w // (w // persW), h // (h // persH)))


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(trees_group, all_sprites)
        self.width, self.height = tree_width, tree_height
        self.cur_img = tile_images['tree']
        self.image = make_img(self.cur_img, width, height, self.width, self.height)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)

    def resize(self, SW, SH):
        global tree_width, tree_height, width, height
        new_W, new_H = self.width * (SW / width), self.height * (SH / height)
        self.image = pygame.transform.scale(self.cur_img,
                                            (new_W, new_H))
        tree_width, tree_height = new_W, new_H


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.images = player_images
        self.image = make_img(self.images['stay'], width, height, MC_width, MC_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.directory = 'f'

    def resize(self, SW, SH):
        global MC_width, MC_height, width, height
        new_W, new_H = MC_width * (SW / width), MC_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MC_width, MC_height = new_W, new_H

    def update(self, keys, vx=0, vy=0):
        l, r, f, d = 0, 0, 0, 0
        if not keys[pygame.K_SPACE]:
            if keys[pygame.K_a]:
                vx = -mc_def_v
                l = 1
            if keys[pygame.K_d]:
                vx = mc_def_v
                r = 1
            if keys[pygame.K_w]:
                vy = -mc_def_v
                f = 1
            if keys[pygame.K_s]:
                vy = mc_def_v
                d = 1

            if abs(vx) == abs(vy) == mc_def_v:
                vx = vx / (2 ** 0.5) + 1
                vy = vy / (2 ** 0.5) + 1

            self.rect.x += vx
            if pygame.sprite.spritecollideany(self, trees_group):
                self.rect.x -= vx
                vx = 0

            self.rect.y += vy
            if pygame.sprite.spritecollideany(self, trees_group):
                self.rect.y -= vy
                vy = 0

            if f:
                if r:
                    self.image = make_img(self.images['fr'], width, height, MC_width, MC_height)
                    self.directory = 'fr'
                elif l:
                    self.image = make_img(self.images['fl'], width, height, MC_width, MC_height)
                    self.directory = 'fl'
                else:
                    self.image = make_img(self.images['f'], width, height, MC_width, MC_height)
                    self.directory = 'f'
            elif d:
                if r:
                    self.image = make_img(self.images['dr'], width, height, MC_width, MC_height)
                    self.directory = 'dr'
                elif l:
                    self.image = make_img(self.images['dl'], width, height, MC_width, MC_height)
                    self.directory = 'dl'
                else:
                    self.image = make_img(self.images['d'], width, height, MC_width, MC_height)
                    self.directory = 'd'
            elif r:
                self.image = make_img(self.images['r'], width, height, MC_width, MC_height)
                self.directory = 'r'
            elif l:
                self.image = make_img(self.images['l'], width, height, MC_width, MC_height)
                self.directory = 'l'
            else:
                self.image = make_img(self.images['stay'], width, height, MC_width, MC_height)
                self.directory = 'f'

        else:
            self.rect.x, self.rect.y = width // 2, height // 2


class MCBullet(pygame.sprite.Sprite):
    def __init__(self, coords, dir):
        super().__init__(MCbullet_group, all_sprites)
        self.images = MCbullet_images
        self.dir = dir
        self.image = make_img(self.images[self.dir], width, height, MCbullet_width, MCbullet_height)
        self.rect = self.image.get_rect().move(
            coords[0] + MCbullet_width // 5.5, coords[1] + MCbullet_height // 2)
        if 'f' in self.dir:
            if self.dir == 'fr':
                vx, vy = bullet_def_v / (2 ** 0.5), -bullet_def_v / (2 ** 0.5)
            elif self.dir == 'fl':
                vx, vy = -bullet_def_v / (2 ** 0.5), -bullet_def_v / (2 ** 0.5)
            else:
                vx, vy = 0, -bullet_def_v
        elif 'd' in self.dir:
            if self.dir == 'dr':
                vx, vy = bullet_def_v / (2 ** 0.5), bullet_def_v / (2 ** 0.5)
            elif self.dir == 'dl':
                vx, vy = -bullet_def_v / (2 ** 0.5), bullet_def_v / (2 ** 0.5)
            else:
                vx, vy = 0, bullet_def_v
        elif self.dir == 'r':
            vx, vy = bullet_def_v, 0
        else:
            vx, vy = -bullet_def_v, 0
        self.vx, self.vy = vx, vy

    def resize(self, SW, SH):
        global MCbullet_width, MCbullet_height, width, height
        new_W, new_H = MCbullet_width * (SW / width), MCbullet_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MCbullet_width, MCbullet_height = new_W, new_H

    def update(self):
        if not -MCbullet_width <= self.rect.x <= width + MCbullet_width or \
                not -MCbullet_height <= self.rect.y <= height + MCbullet_height:
            self.kill()
        else:
            self.rect.x += self.vx
            self.rect.y += self.vy


class Villager(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.images = enemy_images
        self.image = make_img(self.images['stay'], width, height, MC_width, MC_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.directory = 'f'

    def update(self, x2, y2, norm_v=3 / (2 ** 0.5)):
        x1, y1 = self.rect.x, self.rect.y

        perp_x = x2 - x1
        perp_y = y2 - y1

        dist = (perp_x ** 2 + perp_y ** 2) ** 0.5
        if dist != 0:
            vx = (perp_x / dist) * norm_v
            vy = (perp_y / dist) * norm_v
            if pygame.sprite.spritecollideany(self, MCbullet_group):
                pygame.sprite.spritecollide(self, MCbullet_group, dokill=True)
                self.kill()
            else:
                self.rect = self.rect.move(vx, vy)

    def resize(self, SW, SH):
        global MCbullet_width, MCbullet_height, width, height
        new_W, new_H = MCbullet_width * (SW / width), MCbullet_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MCbullet_width, MCbullet_height = new_W, new_H


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = 0  # -(target.rect.x + target.rect.w // 2 - width // 2) - tile_width
        self.dy = 0  # -(target.rect.y + target.rect.h // 2 - height // 2) - tile_height


def level1(screen):
    global background, width, height
    resized_flag = False
    camera = Camera()
    generate_enemies(3)
    n_enemies = 0

    while True:
        screen.fill('black')
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        generate_borders(width, height)

        if n_enemies < 15:
            if len(enemy_group) < 2:
                generate_enemies(n := randint(1, 5))
                n_enemies += n

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return
            if event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                resized_flag = True
                new_SW, new_SH = new_width, new_height
                background = pygame.transform.scale(background, (new_SW, new_SH))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    MCBullet((MainCharacter.rect.x, MainCharacter.rect.y), MainCharacter.directory)

        camera.update(MainCharacter)
        for sprite in all_sprites:
            if resized_flag:
                sprite.resize(new_SW, new_SH)
            camera.apply(sprite)
        if resized_flag:
            width, height = new_SW, new_SH
        resized_flag = False

        trees_group.draw(screen)
        player_group.update(keys)
        player_group.draw(screen)
        MCbullet_group.update()
        MCbullet_group.draw(screen)
        enemy_group.update(MainCharacter.rect.x, MainCharacter.rect.y)
        enemy_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def generate_borders(w, h):
    for sprite in trees_group:
        sprite.kill()

    horz_step = max(1, (w - tree_width) // (Ntrees_horz - 1))
    for i in range(Ntrees_horz):
        Tree(i * horz_step, 0)
        Tree(i * horz_step, h - tree_height)

    vert_step = max(1, (h - tree_height) // (Ntrees_vert - 1))
    for i in range(Ntrees_vert):
        Tree(0, i * vert_step)
        Tree(w - tree_width, i * vert_step)


def generate_enemies(n):
    for _ in range(n):
        side = randint(1, 4)
        if side == 1:
            Villager(0, randint(0, height))
        elif side == 2:
            Villager(randint(0, width), 0)
        elif side == 4:
            Villager(width, randint(0, height))
        else:
            Villager(randint(0, width), height)


all_sprites = pygame.sprite.Group()
trees_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
MCbullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

tile_images = {
    'tree': load_image(r'game/tree.png')
}
Ntrees_horz, Ntrees_vert = 30, 18
background = pygame.transform.scale(load_image(r'game/background1.jpg'), (width, height))

player_images = {'f': load_image('game/MC_moving/MC_up.png'), 'd': load_image('game/MC_moving/MC_down.png'),
                 'l': load_image('game/MC_moving/MC_left.png'), 'r': load_image('game/MC_moving/MC_right.png'),
                 'fr': load_image('game/MC_moving/MC_UR.png'), 'fl': load_image('game/MC_moving/MC_UL.png'),
                 'dr': load_image('game/MC_moving/MC_DR.png'), 'dl': load_image('game/MC_moving/MC_DL.png'),
                 'stay': load_image('game/MC_moving/MC_up.png')}
MCbullet_images = {'f': load_image(r'game/MCBullet_moving/Bullet_up.png'),
                   'd': load_image(r'game/MCBullet_moving/Bullet_down.png'),
                   'l': load_image(r'game/MCBullet_moving/Bullet_left.png'),
                   'r': load_image(r'game/MCBullet_moving/Bullet_right.png'),
                   'fr': load_image(r'game/MCBullet_moving/Bullet_UR.png'),
                   'fl': load_image(r'game/MCBullet_moving/Bullet_UL.png'),
                   'dr': load_image(r'game/MCBullet_moving/Bullet_DR.png'),
                   'dl': load_image(r'game/MCBullet_moving/Bullet_DL.png')}
enemy_images = {'stay': load_image(r'game/enemy/EK.png')}

MC_width, MC_height = 50, 70
mc_def_v = 10
MCbullet_width, MCbullet_height = 40, 40
bullet_def_v = 20
tree_width = tree_height = 100
MainCharacter = Player(width // 2, height // 2)

clock = pygame.time.Clock()
FPS = 60

"""
player, level_x, level_y = generate_level(load_level('lvl1.txt'))
"""

if __name__ == '__main__':
    start_screen()
    level1(screen)
    final_screen()
    terminate()
