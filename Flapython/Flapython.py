#   importation des modules qui vont être utilisés
import pygame
from os import path
import sys
import math
import random
import csv

pygame.init()           # initialisation de pygame
pygame.mixer.init()     # initialisation du son
pygame.mixer.music.set_volume(0.15)     # initialisation du volume des musiques

#   définition des propriétés de la fenêtre
width = 1280
height = 720
FPS = 60

#   création de la fenêtre
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flapython")                 # nom de la fenêtre
favicon = pygame.image.load("Sprites/favicon.ico")      # icône du jeu
pygame.display.set_icon(favicon)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])     # met en place les types d'input autorisés dans le jeu (afin de trier ceux qui vont être amenés à être utilisé)

#   placement dans les dossiers
game_folder = path.dirname(__file__)
sprites_folder = path.join(game_folder, "Sprites")
backgrounds_folder = path.join(sprites_folder, "Backgrounds")
birds_folder = path.join(sprites_folder, "Birds")
data_folder = path.join(game_folder, "Data")

#   récupération des sprites
background_1_img = pygame.image.load(path.join(backgrounds_folder, "background_1.png")).convert()
background_2_img = pygame.image.load(path.join(backgrounds_folder, "background_2.png")).convert()
background_3_img = pygame.image.load(path.join(backgrounds_folder, "background_3.png")).convert()
background_4_img = pygame.image.load(path.join(backgrounds_folder, "background_4.png")).convert()
background_5_img = pygame.image.load(path.join(backgrounds_folder, "background_5.png")).convert()
background_6_img = pygame.image.load(path.join(backgrounds_folder, "background_6.png")).convert()
bird_1_img = pygame.image.load(path.join(birds_folder, "bird_1.png")).convert_alpha()
bird_2_img = pygame.image.load(path.join(birds_folder, "bird_2.png")).convert_alpha()
bird_3_img = pygame.image.load(path.join(birds_folder, "bird_3.png")).convert_alpha()
bird_4_img = pygame.image.load(path.join(birds_folder, "bird_4.png")).convert_alpha()
bird_5_img = pygame.image.load(path.join(birds_folder, "bird_5.png")).convert_alpha()
bird_6_img = pygame.image.load(path.join(birds_folder, "bird_6.png")).convert_alpha()
logo_img = pygame.image.load(path.join(sprites_folder, "logo.png")).convert_alpha()
icon_img = pygame.image.load(path.join(sprites_folder, "icon.png")).convert()
icon_hovered_img = pygame.image.load(path.join(sprites_folder, "icon_hovered.png")).convert()
music_1_icon_img = pygame.image.load(path.join(sprites_folder, "icon_music_1.png")).convert_alpha()
music_2_icon_img = pygame.image.load(path.join(sprites_folder, "icon_music_2.png")).convert_alpha()
music_3_icon_img = pygame.image.load(path.join(sprites_folder, "icon_music_3.png")).convert_alpha()
music_4_icon_img = pygame.image.load(path.join(sprites_folder, "icon_music_4.png")).convert_alpha()
music_cross_icon_img = pygame.image.load(path.join(sprites_folder, "icon_music_cross.png")).convert_alpha()
input_keyboard_icon_img = pygame.image.load(path.join(sprites_folder, "icon_input_keyboard.png")).convert_alpha()
input_mouse_icon_img = pygame.image.load(path.join(sprites_folder, "icon_input_mouse.png")).convert_alpha()
skin_icon_img = pygame.image.load(path.join(sprites_folder, "icon_skin.png")).convert_alpha()
background_icon_img = pygame.image.load(path.join(sprites_folder, "icon_background.png")).convert_alpha()
coins_img = pygame.image.load(path.join(sprites_folder, "coin.png")).convert_alpha()
pipe_top_img = pygame.image.load(path.join(sprites_folder, "pipe_top.png")).convert_alpha()
pipe_bottom_img = pygame.image.load(path.join(sprites_folder, "pipe_bottom.png")).convert_alpha()
pause_icon_img = pygame.image.load(path.join(sprites_folder, "icon_pause.png")).convert_alpha()
play_icon_img = pygame.image.load(path.join(sprites_folder, "icon_play.png")).convert_alpha()
board_img = pygame.image.load(path.join(sprites_folder, "board.png")).convert()
button_img = pygame.image.load(path.join(sprites_folder, "button.png")).convert()
button_hovered_img = pygame.image.load(path.join(sprites_folder, "button_hovered.png")).convert()
new_img = pygame.image.load(path.join(sprites_folder, "new.png")).convert()


#   mise en place des police d'écritures, des sons, des musiques, des icônes et des images dans des listes afin que tout cela soit beaucoup plus simple à retrouver
fonts = [pygame.font.Font("Fonts/font_1.ttf", 44), pygame.font.Font("Fonts/font_2.ttf", 40), pygame.font.Font("Fonts/font_3.ttf", 45), pygame.font.Font("Fonts/font_4.ttf", 38)]
sounds = [pygame.mixer.Sound("Sounds/sound_1.ogg"), pygame.mixer.Sound("Sounds/sound_2.ogg"), pygame.mixer.Sound("Sounds/sound_3.ogg"), pygame.mixer.Sound("Sounds/sound_4.ogg"), pygame.mixer.Sound("Sounds/sound_5.ogg"), pygame.mixer.Sound("Sounds/sound_6.ogg"), pygame.mixer.Sound("Sounds/sound_7.ogg"), pygame.mixer.Sound("Sounds/sound_8.ogg")]
musics = ["Musics/music_1.mp3", "Musics/music_2.mp3", "Musics/music_3.mp3", "Musics/music_4.mp3"]
music_icons = [music_1_icon_img, music_2_icon_img, music_3_icon_img, music_4_icon_img, music_cross_icon_img]
inputs = [input_keyboard_icon_img, input_mouse_icon_img]
backgrounds = [background_1_img, background_2_img, background_3_img, background_4_img, background_5_img, background_6_img]
skins = [bird_1_img, bird_2_img, bird_3_img, bird_4_img, bird_5_img, bird_6_img]

clock = pygame.time.Clock()                     # création d'une "horloge"
all_sprites = pygame.sprite.Group()             # création d'un groupe qui regroupe tous les sprites principaux
all_pipes = pygame.sprite.Group()               # création d'un groupe qui regroupe seulement les tuyaux

#   récupération de la musique actuelle (afin de ne pas devoir la changer à chaque lancement du jeu)
current_music_file = open(path.join(data_folder,"current_music.csv"))
for row in csv.reader(current_music_file):
    current_music = int(row[0])

#   récupération du mode de saut actuel (afin de ne pas devoir le changer à chaque lancement du jeu)
current_input_mode_file = open(path.join(data_folder,"current_input_mode.csv"))
for row in csv.reader(current_input_mode_file):
    current_input_mode = int(row[0])

#   récupération du skin de l'oiseau
current_skin_file = open(path.join(data_folder,"current_skin.csv"))
for row in csv.reader(current_skin_file):
    current_skin = int(row[0])

#   récupération du fond d'arrière-plan
current_background_file = open(path.join(data_folder,"current_background.csv"))
for row in csv.reader(current_background_file):
    current_background = int(row[0])

#   récupération du record
record_file = open(path.join(data_folder,"record.csv"))
for row in csv.reader(record_file):
    record_value = int(row[0])

#   récupération du nombre de pièces
coins_file = open(path.join(data_folder,"coins.csv"))
for row in csv.reader(coins_file):
    coins_value = int(row[0])


# ----------------------------------------------------- DÉFINITION DES CLASSES -----------------------------------------------------


class Bird(pygame.sprite.Sprite):

    '''
    création de la classe "Bird" => oiseau
    '''

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.skin = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2.7, height / 2.08)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0

    def update(self):
        self.rect.y += self.speed   # à chaque frame, l'oiseau est tiré vers le bas de manière exponentielle (positif = descend et négatif = monte)
        self.speed += 0.85


class Icon(pygame.sprite.Sprite):

    '''
    création de la classe "Icon" => icônes
    '''

    def __init__(self, x, y, add_sizeX, icon, iconX, iconY):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.add_sizeX = add_sizeX
        self.icon = icon
        self.iconX = iconX
        self.iconY = iconY
        self.image = icon_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x - (self.rect.width * 0.25), self.y)     # on centre le bouton au milieu des coordonnées x données (pas y car non nécessaire)
        self.image = pygame.transform.scale(self.image, (self.rect.width + self.add_sizeX, self.rect.height))    # si on renseigne un add_sizeX, alors elle se rajoutera à la width de base du bouton (positif => + grand et négatif => + petit)
        self.rect.width = self.rect.width + self.add_sizeX                 # on adapte la hitbox du bouton en fonction du add_sizeX
        self.image.blit(self.icon, (self.rect.width / 2 - self.icon.get_width() / 2 + self.iconX, self.icon.get_height() / 2 - 2 + self.iconY))     # on place l'icône au milieu du bouton

    def hovered(self):
        self.image = icon_hovered_img      # on applique l'animation de hover sur l'icône
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.icon, (self.rect.width / 2 - self.icon.get_width() / 2 + self.iconX, self.icon.get_height() / 2 - 2 + self.iconY))

    def reset(self):
        self.image = icon_img              # on enlève l'animation de hover sur l'icône
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.icon, (self.rect.width / 2 - self.icon.get_width() / 2 + self.iconX, self.icon.get_height() / 2 - 2 + self.iconY))


class Pipe(pygame.sprite.Sprite):

    '''
    création de la classe "Pipe" => tuyaux
    '''

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.reached = False

    def update(self):
        self.rect.x -= 4                        # à chaque frame, on déplace le tuyaux vers la gauche de manière continue (cela correspond à sa vitesse)
        if self.rect.x <= -self.rect.width:
            self.kill()                         # on supprime les tuyaux qui ne sont plus visibles sur l'écran
            pipes.pop(0)


class Button(pygame.sprite.Sprite):

    '''
    création de la classe "Button" => boutons
    '''

    def __init__(self, x, y, add_sizeX, add_sizeY, text, textY):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.add_sizeX = add_sizeX
        self.add_sizeY = add_sizeY
        self.text = text
        self.textY = textY
        self.image = button_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)     # on centre le bouton au milieu des coordonnées x données (pas y car non nécessaire)
        self.image = pygame.transform.scale(self.image, (self.rect.width + self.add_sizeX, self.rect.height + self.add_sizeY))    # si on renseigne un add_sizeX, alors elle se rajoutera à la width de base du bouton (positif => + grand et négatif => + petit)
        self.rect.width = self.rect.width + self.add_sizeX                 # on adapte la hitbox du bouton en fonction du add_sizeX
        self.rect.height = self.rect.height + self.add_sizeY
        self.render = fonts[1].render(self.text, True, (255, 255, 255))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, self.textY))               # on place le texte au milieu du bouton

    def hovered(self):
        self.image = button_hovered_img      # on applique l'animation de hover sur le bouton
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, self.textY))

    def reset(self):
        self.image = button_img              # on enlève l'animation de hover sur le bouton
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, self.textY))


class Board(pygame.sprite.Sprite):

    '''
    création de la classe "Board" => tableau de l'écran de mort
    '''

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = board_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


# ---------------------------------------------------- DÉFINITION DES FONCTIONS ----------------------------------------------------

def checkWindowExit(event):

    '''
    la vérification de sortie du jeu, se déclenche quand le joueur clique sur la croix de la fenêtre ou sur la touche "echap"
    '''

    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()


def addOutline(text, thickness, color, color_key=(255, 0, 255)):

    '''
    l'ajout d'un contour sur les lettres, on peut choisir l'épaisseur et la couleur
    '''

    mask = pygame.mask.from_surface(text)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_text = pygame.Surface((text.get_width() + 2, text.get_height() + 2))
    new_text.fill(color_key)
    new_text.set_colorkey(color_key)

    for pixel in -thickness, thickness:
        new_text.blit(mask_surf, (pixel + thickness, thickness))
        new_text.blit(mask_surf, (thickness, pixel + thickness))

    new_text.blit(text, (thickness, thickness))

    return new_text


def checkStart():

    '''
    vérifie avant le début du jeu si l'on appuie sur la touche "espace" ou "clic gauche" pour lancer la partie et si l'on appuie sur les icônes du menu principal
    '''

    global bird
    global all_sprites
    global coins_value
    global music_icons
    global current_music
    global current_input_mode
    global current_skin
    global current_background
    for event in pygame.event.get():
        checkWindowExit(event)
        if current_input_mode == 0 :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # quand le joueur appuie sur "espace", alors la partie commence
                    pygame.mixer.Sound.play(sounds[3])
                    bird.speed = -12
                    bird.image = pygame.transform.rotozoom(bird.skin, 45, 1)         # on utilise "rotozoom" afin de garder la meilleure qualité d'image possible car "rotate" la détériore
                    bird.rect = bird.image.get_rect(center=bird.rect.center)        # à chaque fois qu'on modifie l'angle d'un sprite sa taille change, donc il faut qu'on l'adapte
                    all_sprites.remove(music_icon, input_icon, skin_icon, background_icon, record_button)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
        elif current_input_mode == 1 :
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not music_icon.rect.collidepoint(pygame.mouse.get_pos()) and not input_icon.rect.collidepoint(pygame.mouse.get_pos()) and not skin_icon.rect.collidepoint(pygame.mouse.get_pos()) and not background_icon.rect.collidepoint(pygame.mouse.get_pos()) and not bird.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.Sound.play(sounds[3])
                    bird.speed = -12
                    bird.image = pygame.transform.rotozoom(bird.skin, 45, 1)
                    bird.rect = bird.image.get_rect(center=bird.rect.center)
                    all_sprites.remove(music_icon, input_icon, skin_icon, background_icon, record_button)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if music_icon.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.Sound.play(sounds[1])
                current_music += 1
                if current_music == 5 :
                    current_music = 0
                music_icon.icon = music_icons[current_music]
                current_music_file = open(path.join(data_folder,"current_music.csv"),'w')
                current_music_file.write(str(current_music))
            elif input_icon.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.Sound.play(sounds[1])
                current_input_mode += 1
                if current_input_mode == 2 :
                    current_input_mode = 0
                input_icon.icon = inputs[current_input_mode]
                current_input_mode_file = open(path.join(data_folder,"current_input_mode.csv"),'w')
                current_input_mode_file.write(str(current_input_mode))
            elif skin_icon.rect.collidepoint(pygame.mouse.get_pos()):
                if coins_value >= 10 :
                    pygame.mixer.Sound.play(sounds[1])
                    coins_value -= 10
                    coins_file = open(path.join(data_folder,"coins.csv"), "w")
                    coins_file.write(str(coins_value))
                    current_skin += 1
                    if current_skin == 6 :
                        current_skin = 0
                    bird.skin = skins[current_skin]
                    bird.image = skins[current_skin]
                    current_skin_file = open(path.join(data_folder,"current_skin.csv"),'w')
                    current_skin_file.write(str(current_skin))
                else:
                    pygame.mixer.Sound.play(sounds[2])
            elif background_icon.rect.collidepoint(pygame.mouse.get_pos()):
                if coins_value >= 25 :
                    pygame.mixer.Sound.play(sounds[1])
                    coins_value -= 25
                    coins_file = open(path.join(data_folder,"coins.csv"), "w")
                    coins_file.write(str(coins_value))
                    current_background += 1
                    if current_background == 6 :
                        current_background = 0
                    current_background_file = open(path.join(data_folder,"current_background.csv"),'w')
                    current_background_file.write(str(current_background))
                else:
                    pygame.mixer.Sound.play(sounds[2])
            elif bird.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.Sound.play(sounds[7])
    return False


def iconStart():

    '''
    vérifie avant le début du jeu si l'on survole une icône afin de leur appliquer un effet de hover
    '''

    global music_icon
    global input_icon
    global skin_icon
    global coins_text
    if music_icon.rect.collidepoint(pygame.mouse.get_pos()):
        music_icon.hovered()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif input_icon.rect.collidepoint(pygame.mouse.get_pos()):
        input_icon.hovered()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif skin_icon.rect.collidepoint(pygame.mouse.get_pos()):
        skin_icon.hovered()
        if coins_value >= 10:
            purchase_text = addOutline(fonts[0].render('-10', False, (0, 255, 0)).convert(), 3.75, (1, 1, 1))
        else:
            purchase_text = addOutline(fonts[0].render('-10', False, (255, 0, 0)).convert(), 3.75, (1, 1, 1))
        screen.blit(purchase_text, (75 + coins_text.get_width(), 18))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif background_icon.rect.collidepoint(pygame.mouse.get_pos()):
        background_icon.hovered()
        if coins_value >= 25:
            purchase_text = addOutline(fonts[0].render('-25', False, (0, 255, 0)).convert(), 3.75, (1, 1, 1))
        else:
            purchase_text = addOutline(fonts[0].render('-25', False, (255, 0, 0)).convert(), 3.75, (1, 1, 1))
        screen.blit(purchase_text, (75 + coins_text.get_width(), 18))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif bird.rect.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        music_icon.reset()
        input_icon.reset()
        skin_icon.reset()
        background_icon.reset()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def drawAll():

    '''
    dessine tout les éléments lors du déroulement du jeu
    '''
    global all_sprites
    global all_pipes
    clock.tick(FPS)         # permet de bien avoir le nombre de FPS souhaité => cela doit être exécuté pour chaque image, donc chaque itération d'une boucle "while"
    backgroundLoop()
    createPipes()           # on crée les tuyaux en boucle
    all_pipes.update()
    all_pipes.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)


def backgroundLoop():

    '''
    le défilement du fond, se déclenche lors du déroulement du jeu
    '''

    global background_tiles
    global background_scroll
    for frame in range(background_tiles):
        screen.blit(backgrounds[current_background], (frame * backgrounds[current_background].get_width() + background_scroll, 0))
    background_scroll -= 1.5                             # background_scroll correspond à la vitesse de défilement du fond (plus la valeur est élevée, plus le fond défilera rapidement et inversement)
    if abs(background_scroll) > backgrounds[current_background].get_width():
        background_scroll = 0


def createPipes():

    '''
    la création des tuyaux, se déclenche en boucle lors du déroulement du jeu
    '''

    global pipe_timer
    global pipe_offset
    global pipes
    if pipe_timer <= 0:
        pipe_top_y = random.randint(-height - 25, -pipe_offset + 25)                        # on définit la hauteur du tuyau d'en haut (en y) de manière aléatoire
        pipe_bottom_y = pipe_top_y + pipe_top_img.get_height() + pipe_offset                # on définit la hauteur du tuyau d'en bas (en y) en fonction de celui d'en haut

        pipe_top = Pipe(width, pipe_top_y, pipe_top_img)              # on crée les 2 tuyaux
        pipe_bottom = Pipe(width, pipe_bottom_y, pipe_bottom_img)

        all_pipes.add(pipe_top)
        all_pipes.add(pipe_bottom)

        pipes.append(pipe_top)              # on ajoute les 2 tuyaux dans la liste de tous les tuyaux (ce qui permetra de les manipuler + facilement)
        pipes.append(pipe_bottom)

        pipe_timer = 100
    pipe_timer -= 0.7                      # pipe_timer correspond au temps d'attente entre la création des tuyaux (plus la valeur est élevée, plus les tuyaux se créeront rapidement et inversement)


def deleteAllPipes():

    '''
    la suppression des tuyaux, se déclenche quand ils ne sont plus visibles sur l'écran ou quand on revient au menu principal
    '''

    global pipes
    for pipe in pipes:
        pipe.kill()
    pipes.clear()       # on supprime tous les tuyaux de la liste


def updateScore():

    '''
    la mise à jour du score, se produit à chaque fois que l'on passe une paire de tuyaux (ajoute 1 point au score)
    '''

    global score_value
    score_text = addOutline(fonts[3].render(str(score_value), False, (255, 255, 255)).convert(), 3.5, (1, 1, 1))
    screen.blit(score_text, (width / 2 - score_text.get_width() / 2 - 10, height / 2 - 220))

def updateCoins():

    '''
    la mise à jour du nombre de pièces, se produit à chaque fois que le score augmente de 1
    '''

    global coins_value
    global score_value
    if score_value != 0 :
        coins_value += score_value
        coins_file = open(path.join(data_folder,"coins.csv"), "w")
        coins_file.write(str(coins_value))

def updateRecord():

    '''
    la vérification entre le score obtenu et le record, le met à jour si on le dépasse
    '''

    global record_value
    global record_button
    global new_state
    if score_value > record_value:
        record_file = open(path.join(data_folder,"record.csv"), "w")
        record_file.write(str(score_value))
        record_value = score_value
        record_button.text = "RECORD : " + str(record_value)
        record_button.image = button_img
        record_button.image = pygame.transform.scale(record_button.image, (record_button.rect.width, record_button.rect.height))
        record_button.render = fonts[1].render(record_button.text, True, (255, 255, 255))
        record_button.image.blit(record_button.render, (record_button.rect.width / 2 - record_button.render.get_width() / 2, record_button.textY))
        new_state = True
        pygame.mixer.Sound.play(sounds[6])


#   définition des propriétés du défilement du fond
background_tiles = math.ceil(width / backgrounds[current_background].get_width()) + 1
background_scroll = 0

#   définition de certaines propriétés des tuyaux
pipe_timer = 0
pipe_offset = 210   # espacement entre le tuyau du haut et du bas
pipes = []   # liste contenant tous les tuyaux crées pour les manipuler plus facilement

#   mise en place des différents éléments du jeu avant son lancement
bird = Bird(skins[current_skin])
gamestart_text = addOutline(fonts[0].render('APPUYEZ  SUR  "ESPACE"  POUR  COMMENCER', False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
record_button = Button(width - button_img.get_width() - 15, height - button_img.get_height() - 10, 55, 15, "RECORD : " + str(record_value), 7)
music_icon = Icon(width - 35, 50, 0, music_icons[current_music], 0, -1)
input_icon = Icon(width - 35, 125, 0, inputs[current_input_mode], 0, 0)
skin_icon = Icon(65, height / 2 - icon_img.get_height() - 5, 0, skin_icon_img, 0, 0)
background_icon = Icon(65, height / 2 - background_icon_img.get_height() + 35, 0, background_icon_img, 0, 6)
coins_text = addOutline(fonts[2].render(str(coins_value), False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
authors_text = addOutline(fonts[1].render('CRÉÉ PAR HUGO VILLER & ESTEBAN JUNCOSA - TROPHÉE NSI', False, (255, 255, 255)).convert(), 3, (1, 1, 1))
pause_icon = Icon(pause_icon_img.get_width() + 37, 50, 0, pause_icon_img, 0, 2)
board = Board(width / 2 - 5, height / 2)
gameover_text = addOutline(fonts[0].render("GAME OVER", False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
restart_button = Button(width / 2.42 - 5, height / 1.7, 40, 0, "RÉESSAYER", 0)
leave_button = Button(width / 1.8 - 5, height / 1.7, 40, 0, "QUITTER", 0)

#   mise en place de la valeur initiale du score
score_value = 0

#   mise en place de l'état d'un nouveau record (si on en fait un, alors la variable devient "True" et une petite icône s'affichera sur l'écran de mort)
new_state = False

# ------------------------------------------------------- DÉROULEMENT DU JEU -------------------------------------------------------

pygame.mixer.Sound.play(sounds[0])

def gameStart():

    '''
    le menu principal, en attendant que le joueur appuie sur la touche "espace" ou "clic gauche" pour commencer la partie
    '''

    global background_scroll
    global pipe_timer
    global score_value
    start = False
    background_scroll = 0                               # on initialise le niveau de scroll de base du fond (par défaut 0)
    pipe_timer = 0                                      # on initialise le timer des tuyaux (par défaut 0)
    score_value = 0                                     # on initialise la valeur du score (par défaut 0)
    all_sprites.add(bird, music_icon, input_icon, skin_icon, background_icon, record_button)
    bird.rect.center = (width / 2.7, height / 2.08)     # on initialise la position de l'oiseau à chaque fois que l'on est dans le menu principal
    bird.image = pygame.transform.rotozoom(bird.skin, 0, 1)
    bird.rect = bird.image.get_rect(center=bird.rect.center)
    while not start:
        if bird.rect.centery == height / 2.08 or bird.rect.centery >= height / 2.08 + 16:    # fait l'animation de montée
            while not start and bird.rect.centery > height / 2.08 - 16:
                clock.tick(FPS)
                bird.rect.centery -= 1
                screen.blit(backgrounds[current_background], (0, 0))
                screen.blit(logo_img, (width / 2 - logo_img.get_width() / 2 + 5, height / 6 - logo_img.get_height() / 2))
                if current_input_mode == 0 :
                    gamestart_text = addOutline(fonts[0].render('APPUYEZ  SUR  "ESPACE"  POUR  COMMENCER', False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
                elif current_input_mode == 1 :
                    gamestart_text = addOutline(fonts[0].render('APPUYEZ  SUR  "CLIC GAUCHE"  POUR  COMMENCER', False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
                screen.blit(gamestart_text, (width / 2 - gamestart_text.get_width() / 2 + 10, height / 2.8 - gamestart_text.get_height() / 2 - 5))
                screen.blit(authors_text, (25, height - 45))
                coins_text = addOutline(fonts[2].render(str(coins_value), False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
                screen.blit(coins_text, (20, 20))
                screen.blit(coins_img, (coins_text.get_width() + 30, 24))
                all_sprites.draw(screen)
                iconStart()
                start = checkStart()
                pygame.display.flip()
        elif bird.rect.centery <= height / 2.08:            # fait l'annimation de descente
            while not start and bird.rect.centery < height / 2.08 + 16:
                clock.tick(FPS)
                bird.rect.centery += 1
                screen.blit(backgrounds[current_background], (0, 0))
                screen.blit(logo_img, (width / 2 - logo_img.get_width() / 2 + 5, height / 6 - logo_img.get_height() / 2))
                if current_input_mode == 0 :
                    gamestart_text = addOutline(fonts[0].render('APPUYEZ  SUR  "ESPACE"  POUR  COMMENCER', False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
                elif current_input_mode == 1 :
                    gamestart_text = addOutline(fonts[0].render('APPUYEZ  SUR  "CLIC GAUCHE"  POUR  COMMENCER', False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
                screen.blit(gamestart_text, (width / 2 - gamestart_text.get_width() / 2 + 10, height / 2.8 - gamestart_text.get_height() / 2 - 5))
                screen.blit(authors_text, (25, height - 45))
                coins_text = addOutline(fonts[2].render(str(coins_value), False, (255, 255, 255)).convert(), 3.75, (1, 1, 1))
                screen.blit(coins_text, (20, 20))
                screen.blit(coins_img, (coins_text.get_width() + 30, 24))
                all_sprites.draw(screen)
                iconStart()
                start = checkStart()
                pygame.display.flip()


def gameLoop():

    '''
    le déroulement du jeu, où tout se passe => l'oiseau peut sauter et meurt s'il touche le plafond, le sol ou un tuyau
    '''
    global score_value
    global current_music
    global current_input_mode
    on = True
    dead = False
    pause = False
    rotation = 45
    all_sprites.add(pause_icon)
    if current_music != 4 :
        pygame.mixer.music.load(musics[current_music])
        pygame.mixer.music.play(-1)
    while on:
        drawAll()
        updateScore()
        for pipe in pipes:
            if not dead and not pause and pygame.sprite.collide_mask(bird, pipe) and pipes.index(pipe) % 2 == 0:     # mort à cause des tuyaux du haut + animation
                dead = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if current_music != 4 :
                    pygame.mixer.music.fadeout(500)
                pygame.mixer.Sound.play(sounds[5])
                bird.speed = 0
                all_sprites.remove(pause_icon)
                while bird.rect.y < height + 230:
                    drawAll()
                    rotation += 10
                    bird.rect.x -= 9
                    bird.image = pygame.transform.rotozoom(bird.skin, rotation, 1)
                    bird.rect = bird.image.get_rect(center=bird.rect.center)
                    pygame.display.flip()
                    if pygame.sprite.collide_mask(bird, pipes[pipes.index(pipe) + 1]):
                        bird.speed = -7.5
                    for event in pygame.event.get():
                        checkWindowExit(event)
                all_sprites.remove(bird)
                backgroundLoop()
                all_pipes.draw(screen)
                on = False
            elif not dead and not pause and pygame.sprite.collide_mask(bird, pipe) and pipes.index(pipe) % 2 == 1:     # mort à cause des tuyaux du bas + animation
                dead = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if current_music != 4 :
                    pygame.mixer.music.fadeout(500)
                pygame.mixer.Sound.play(sounds[5])
                bird.speed = -9.5
                all_sprites.remove(pause_icon)
                while bird.rect.y < height + 230:
                    drawAll()
                    rotation += 10
                    bird.rect.x -= 8
                    bird.image = pygame.transform.rotozoom(bird.skin, rotation, 1)
                    bird.rect = bird.image.get_rect(center=bird.rect.center)
                    pygame.display.flip()
                    if pygame.sprite.collide_mask(bird, pipe):
                        bird.speed = -7.5
                    for event in pygame.event.get():
                        checkWindowExit(event)
                all_sprites.remove(bird)
                backgroundLoop()
                all_pipes.draw(screen)
                on = False
            elif not dead and not pause and not pipe.reached and pipe.rect.x <= bird.rect.x - (pipe_top_img.get_width() / 2) and pipe.image == pipe_top_img:    # ajoute 1 point au score quand on passe une paire de tuyaux
                pipe.reached = True
                pipes[1].reached = True
                pygame.mixer.Sound.play(sounds[4])
                score_value = score_value + 1
                updateScore()
        if not dead and not pause and (bird.rect.y <= -20 or bird.rect.y >= height - 70):    # fait les animations de mort en fonction de l'endroit où l'oiseau touche la fenêtre
            dead = True
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if current_music != 4 :
                    pygame.mixer.music.fadeout(500)
            pygame.mixer.Sound.play(sounds[5])
            bird_bounce = 0
            all_sprites.remove(pause_icon)
            if bird.rect.y <= -20:                              # mort à cause du plafond + animation
                while bird.rect.y < height + 250:
                    drawAll()
                    rotation += 10
                    bird.rect.x += bird_bounce
                    bird.image = pygame.transform.rotozoom(bird.skin, rotation, 1)
                    bird.rect = bird.image.get_rect(center=bird.rect.center)
                    pygame.display.flip()
                    for pipe in pipes:
                        if pygame.sprite.collide_mask(bird, pipe):
                            bird_bounce = -10
                    for event in pygame.event.get():
                        checkWindowExit(event)
            elif bird.rect.y >= height - 70:                    # mort à cause du sol + animation
                bird.speed = -14
                rotation = -45
                while bird.rect.y < height + 150:
                    drawAll()
                    rotation += 10
                    bird.rect.x += bird_bounce
                    bird.image = pygame.transform.rotozoom(bird.skin, rotation, 1)
                    bird.rect = bird.image.get_rect(center=bird.rect.center)
                    pygame.display.flip()
                    for pipe in pipes:
                        if pygame.sprite.collide_mask(bird, pipe):
                            bird_bounce = -8
                    for event in pygame.event.get():
                        checkWindowExit(event)
            all_sprites.remove(bird)            # on supprime l'oiseau de l'écran
            backgroundLoop()
            all_pipes.draw(screen)
            on = False

        if bird.speed < 0:       # saute
            bird.image = pygame.transform.rotozoom(bird.skin, 45, 1)
            bird.rect = bird.image.get_rect(center=bird.rect.center)
        elif bird.speed > 8:   # tombe
            bird.image = pygame.transform.rotozoom(bird.skin, -45, 1)
            bird.rect = bird.image.get_rect(center=bird.rect.center)
        else:                    # stable
            bird.image = pygame.transform.rotozoom(bird.skin, 0, 1)
            bird.rect = bird.image.get_rect(center=bird.rect.center)
        bird.mask = pygame.mask.from_surface(bird.image)
        pygame.display.flip()

        if pause_icon.rect.collidepoint(pygame.mouse.get_pos()):
            pause_icon.hovered()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pause_icon.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            checkWindowExit(event)
            if current_input_mode == 0 :
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not dead:     # quand le joueur appuie sur "espace", alors l'oiseau saute (si c'est bien ce mode de saut)
                        pygame.mixer.Sound.play(sounds[3])
                        bird.speed = -12
            elif current_input_mode == 1 :
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not pause_icon.rect.collidepoint(pygame.mouse.get_pos()) and not dead:     # quand le joueur appuie sur "clic gauche", alors l'oiseau saute (si c'est bien ce mode de saut)
                        pygame.mixer.Sound.play(sounds[3])
                        bird.speed = -12
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_icon.rect.collidepoint(pygame.mouse.get_pos()):    # quand le joueur appuie sur l'icône "pause", la partie se met en pause
                    if current_music != 4 :
                        pygame.mixer.music.pause()
                    pygame.mixer.Sound.play(sounds[1])
                    pause = True
                    pause_icon.icon = play_icon_img
                    pause_icon.iconX = 1
                    pause_icon.iconY = 4
                    pause_icon_group = pygame.sprite.Group()
                    pause_icon_group.add(pause_icon)
                    
        while pause:    # situation lorsque le jeu est en pause, où plus rien de bouge
            pause_icon_group.update()
            pause_icon_group.draw(screen)
            if pause_icon.rect.collidepoint(pygame.mouse.get_pos()):
                pause_icon.hovered()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pause_icon.reset()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.flip()
            for event in pygame.event.get():
                checkWindowExit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # quand le joueur appuie sur l'icône "play", la partie reprend
                    if pause_icon.rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.mixer.Sound.play(sounds[1])
                        if current_music != 4 :
                            pygame.mixer.music.unpause()
                        pause = False
                        pause_icon.icon = pause_icon_img
                        pause_icon.iconX = 0
                        pause_icon.iconY = 2
                        pause_icon_group.remove(pause_icon)


def gameOver():

    '''
    l'écran de mort, en attendant que le joueur choisisse entre recommencer la partie ou quitter le jeu
    '''
    
    global score_value
    global new_state
    start = False
    all_sprites.add(board, restart_button, leave_button)
    updateRecord()
    updateCoins()
    score_text = addOutline(fonts[3].render(str(score_value), False, (255, 255, 255)).convert(), 3.5, (1, 1, 1))
    while not start:
        clock.tick(FPS)
        all_sprites.draw(screen)
        screen.blit(gameover_text, (width / 2 - gameover_text.get_width() / 2 - 5, height / 2.65 - gameover_text.get_height() / 2))
        screen.blit(score_text, (width / 2 - score_text.get_width() / 2 - 5, height / 2.15 - score_text.get_height() / 2))
        if new_state:
            screen.blit(new_img, (width / 2 - 230, height / 2 - 100))
        if restart_button.rect.collidepoint(pygame.mouse.get_pos()):           # applique l'animation de hover si la souris survole les boutons "restart_button" et "leave_button"
            restart_button.hovered()
            leave_button.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif leave_button.rect.collidepoint(pygame.mouse.get_pos()):
            leave_button.hovered()
            restart_button.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            restart_button.reset()                     # enlève l'animation de hover sur les 2 boutons
            leave_button.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()

        for event in pygame.event.get():
            checkWindowExit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:     # se déclenche seulement si c'est un clic gauche
                if restart_button.rect.collidepoint(pygame.mouse.get_pos()):   # recommence la partie quand le joueur clique sur le bouton "restart_button"
                    pygame.mixer.Sound.play(sounds[1])
                    deleteAllPipes()
                    all_sprites.remove(board, restart_button, leave_button)
                    restart_button.reset()
                    leave_button.reset()
                    new_state = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    start = True
                elif leave_button.rect.collidepoint(pygame.mouse.get_pos()):   # quitte le jeu quand le joueur clique sur le bouton "leave_button"
                    pygame.mixer.Sound.play(sounds[1])
                    pygame.time.delay(500)
                    pygame.quit()
                    sys.exit()


while True:
    gameStart()    # lance le menu principal
    gameLoop()     # lance la partie
    gameOver()     # lance l'écran de mort