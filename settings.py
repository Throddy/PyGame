import pygame


# все используемые данные(настройки обьектов игры), размеры, количества, хп, константы и тд.
size = width, height = v_width, v_height = 1400, 800
min_width, min_height = 1200, 700

pygame.init()

pygame.display.set_caption('The Horsehead')
screen = pygame.display.set_mode(size, pygame.RESIZABLE, pygame.FULLSCREEN)
virtual_surface = pygame.Surface((width, height))

UNIT_width, UNIT_height = 80, 80

MC_width, MC_height = 80, 80
mc_def_v = 7
MCbullet_width, MCbullet_height = 40, 40
bullet_def_v = 20
tree_width = tree_height = 100
Ntrees_horz, Ntrees_vert = 30, 18

MC_hp, Vil_hp, Musk_hp, Mag_hp = 100, 100, 75, 150
MC_damage, Vil_damage, Musk_damage, Mag_damage = 10, 10, 10, 10
v_damage_delay = 2

enemies_firing_range = 250
MC_firing_range = 300
musketeer_firing_delay = 300

BAR_LENGTH, BAR_HEIGHT = UNIT_width, 10

stat_file_name = 'stat.csv'
headers = ["Total VILLAGERS you've destroyed", "Total MUSKETEERS you've destroyed",
           "Total MAGICIANS you've destroyed", "Total ENEMIES you've killed",
           "Total SHOTS you've done", "Total TIME(seconds) you' spent"]

non_stop_mode_flag = False

FPS = 60
clock = pygame.time.Clock()
