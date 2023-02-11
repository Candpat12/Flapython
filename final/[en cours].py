#   importation des modules qui vont être utilisés
import pygame
import os
import sys
import math
import random
import csv

pygame.init()           #   initialisation de pygame (obligatoire)
pygame.mixer.init()     #   initialisation du son

#   définition des propriétés de la fenêtre
width = 1280
height = 720
FPS = 60
screen = pygame.display.set_mode((width, height))       #   initialisation de la fenêtre /!\ bien mettre un tuple en argument et pas 2 valeurs /!\
pygame.display.set_caption("Flapython")                 #   nom de la fenêtre
icon = pygame.image.load("logo.png")                    #   icône du jeu
pygame.display.set_icon(icon)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])  #   initialisation des différents événements qui vont être utlisés (afin d'améliorer les performances)

#   placement dans les dossiers
game_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(game_folder, "Sprites")
backgrounds_folder = os.path.join(sprites_folder, "Backgrounds")
birds_folder = os.path.join(sprites_folder, "Birds")

#   récupération des sprites
background_img = pygame.image.load(os.path.join(backgrounds_folder, "background_1.png")).convert()
bird_img = pygame.image.load(os.path.join(birds_folder, "bird_1.png")).convert_alpha()
pipe_top_img = pygame.image.load(os.path.join(sprites_folder, "pipe_top.png")).convert_alpha()
pipe_bottom_img = pygame.image.load(os.path.join(sprites_folder, "pipe_bottom.png")).convert_alpha()
icon_img = pygame.image.load(os.path.join(sprites_folder, "icon.png")).convert()
icon_hovered_img = pygame.image.load(os.path.join(sprites_folder, "icon_hovered.png")).convert()
icon_settings_img = pygame.image.load(os.path.join(sprites_folder, "icon_settings.png")).convert_alpha()
icon_credits_img = pygame.image.load(os.path.join(sprites_folder, "icon_credits.png")).convert_alpha()
button_img = pygame.image.load(os.path.join(sprites_folder, "button.png")).convert()
button_hovered_img = pygame.image.load(os.path.join(sprites_folder, "button_hovered.png")).convert()
sign_img = pygame.image.load(os.path.join(sprites_folder, "sign.png")).convert_alpha()
board_img = pygame.image.load(os.path.join(sprites_folder, "board.png")).convert()
new_img = pygame.image.load(os.path.join(sprites_folder, "new.png")).convert()

#   récupération des police d'écritures et des sons
fonts = [pygame.font.Font("Fonts/font_1.ttf", 42), pygame.font.Font("Fonts/font_2.ttf", 21), pygame.font.Font("Fonts/font_3.ttf", 38), pygame.font.Font("Fonts/font_4.ttf", 40)]
sounds = [pygame.mixer.Sound("Sounds/sound_1.ogg"), pygame.mixer.Sound("Sounds/sound_2.ogg"), pygame.mixer.Sound("Sounds/sound_3.ogg")]

clock = pygame.time.Clock()                     #   création d'une "horloge"
all_sprites = pygame.sprite.Group()             #   création d'un groupe qui regroupe tous les sprites principaux
all_pipes = pygame.sprite.Group()               #   création d'un groupe qui regroupe seulement les tuyaux

#   récupération du record
record_file = open("record.csv")
for row in csv.reader(record_file) :
    record_value = int(row[0])

#   création de la classe "Bird" => oiseau
class Bird(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2.7, height / 2.08)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0

    def update(self) :
        self.rect.y += self.speed   #   à chaque frame, l'oiseau est tiré vers le bas de plus en plus fort de manière exponentielle (positif => descend et négatif => monte)
        self.speed += 0.65

#   création de la classe "Pipe" => tuyaux
class Pipe(pygame.sprite.Sprite) :
    def __init__(self, x, y, image) :
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.reached = False
    
    def update(self) :
        self.rect.x -= 4                        #   à chaque frame, on déplace le tuyaux vers la gauche de manière continue (cela correspond à sa vitesse)
        if self.rect.x <= -self.rect.width :
            self.kill()                         #   on supprime les tuyaux qui ne sont plus visibles sur l'écran
            pipes.pop(0)

#   création de la classe "Icon" => icônes du menu principal
class Icon(pygame.sprite.Sprite) :
    def __init__(self, x, y, add_sizeX, icon) :
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.add_sizeX = add_sizeX
        self.icon = icon
        self.image = icon_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x - (self.rect.width * 0.25), self.y)     #   on centre le bouton au milieu des coordonnées x données (pas y car non nécessaire)
        self.image = pygame.transform.scale(self.image, (self.rect.width + self.add_sizeX, self.rect.height))    #   si on renseigne un add_sizeX, alors elle se rajoutera à la width de base du bouton (positif => + grand et négatif => + petit)
        self.rect.width = self.rect.width + self.add_sizeX                 #   on adapte la hitbox du bouton en fonction du add_sizeX
        self.image.blit(self.icon, (self.rect.width / 2 - self.icon.get_width() / 2, self.icon.get_height() / 2 - 2))     #   on place l'icône au milieu du bouton
    
    def hovered(self) :
        self.image = icon_hovered_img      #   on applique l'animation de hover sur l'icône
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.icon, (self.rect.width / 2 - self.icon.get_width() / 2, self.icon.get_height() / 2 - 2))
    
    def reset(self) :
        self.image = icon_img              #   on enlève l'animation de hover sur l'icône
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.icon, (self.rect.width / 2 - self.icon.get_width() / 2, self.icon.get_height() / 2 - 2))

#   création de la classe "Button" => boutons
class Button(pygame.sprite.Sprite) :
    def __init__(self, x, y, add_sizeX, text) :
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.add_sizeX = add_sizeX
        self.text = text
        self.image = button_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)     #   on centre le bouton au milieu des coordonnées x données (pas y car non nécessaire)
        self.image = pygame.transform.scale(self.image, (self.rect.width + self.add_sizeX, self.rect.height))    #   si on renseigne un add_sizeX, alors elle se rajoutera à la width de base du bouton (positif => + grand et négatif => + petit)
        self.rect.width = self.rect.width + self.add_sizeX                 #   on adapte la hitbox du bouton en fonction du add_sizeX
        self.render = fonts[3].render(self.text, True, (255, 255, 255))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, 0))               #   on place le texte au milieu du bouton
    
    def hovered(self) :
        self.image = button_hovered_img      #   on applique l'animation de hover sur le bouton
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, 0))
    
    def reset(self) :
        self.image = button_img              #   on enlève l'animation de hover sur le bouton
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, 0))

#   création de la classe "Sign" => panneaux
class Sign(pygame.sprite.Sprite) :
    def __init__(self, x, y, add_sizeX, text) :
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.add_sizeX = add_sizeX
        self.text = text
        self.image = sign_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image = pygame.transform.scale(self.image, (self.rect.width + self.add_sizeX, self.rect.height))    #   si on renseigne un add_sizeX, alors elle se rajoutera à la width de base du panneau (positif => + grand et négatif => + petit)
        self.rect.width = self.rect.width + self.add_sizeX                 #   on adapte la hitbox du panneau en fonction du add_sizeX
        self.render = addOutline(fonts[1].render(self.text, False, (255, 255, 255)).convert(), 2.25, (1, 1, 1))
        self.image.blit(self.render, (self.rect.width / 2 - self.render.get_width() / 2, self.rect.height / 2 - self.render.get_height() / 2))               #   on place le texte au milieu du panneau

class Board(pygame.sprite.Sprite) :
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = board_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

def addOutline(text, thickness, color, color_key = (255, 0, 255)) :

    '''
    l'ajout d'un contour sur les lettres, on peut choisir l'épaisseur et la couleur
    '''

    mask = pygame.mask.from_surface(text)
    mask_surf = mask.to_surface(setcolor = color)
    mask_surf.set_colorkey((0, 0, 0))

    new_text = pygame.Surface((text.get_width() + 2, text.get_height() + 2))
    new_text.fill(color_key)
    new_text.set_colorkey(color_key)

    for pixel in -thickness, thickness :
        new_text.blit(mask_surf, (pixel + thickness, thickness))
        new_text.blit(mask_surf, (thickness, pixel + thickness))
    
    new_text.blit(text, (thickness, thickness))

    return new_text

#   définition des propriétés du défilement du fond
background_img = pygame.transform.scale(background_img, (width, height))
background_tiles = math.ceil(width / background_img.get_width()) + 1
background_scroll = 0

#   définition de certaines propriétés des tuyaux
pipe_timer = 0
pipe_offset = 225   #   espacement entre le tuyau du haut et du bas
pipes = []

#   mise en place des différents éléments du jeu avant son lancement
bird = Bird()
gamestart_text = addOutline(fonts[0].render('APPUYEZ  SUR  "ESPACE"  POUR  COMMENCER', False, (255, 255, 255)).convert(), 3.5, (1, 1, 1))
icon_settings = Icon(width - 35, 50, 0, icon_settings_img)
icon_credits = Icon(65, height - 50, 0, icon_credits_img)
record_sign = Sign(width - sign_img.get_width() - 15, height - sign_img.get_height() + 15, 55, "RECORD : " + str(record_value))
board = Board(width / 2, height / 2)
gameover_text = addOutline(fonts[0].render("GAME OVER", False, (255, 255, 255)).convert(), 3.5, (1, 1, 1))
restart_button = Button(width / 2.42, height / 1.7, 40, "RÉESSAYER")
leave_button = Button(width / 1.8, height / 1.7, 40, "QUITTER")

#   mise en place de la valeur initiale du score
score_value = 0

#   mise en place de l'état d'un nouveau record (si on en fait un, alors la variable devient "True")
new_state = False

def checkWindowExit(event) :

    '''
    la vérification de sortie du jeu, se déclenche quand le joueur clique sur la croix de la fenêtre ou sur "echap"
    '''

    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
        pygame.quit()
        sys.exit()

def backgroundLoop() :

    '''
    le défilement du fond, se déclenche partout sauf au menu principal
    '''
    
    global background_tiles
    global background_scroll
    for frame in range(background_tiles) :
            screen.blit(background_img, (frame * background_img.get_width() + background_scroll, 0))
    background_scroll -= 1.5                             #    background_scroll correspond à la vitesse de défilement du fond (plus la valeur est élevée, plus le fond défilera rapidement et inversement)
    if abs(background_scroll) > background_img.get_width() :
        background_scroll = 0

def createPipes() :

    '''
    la création des tuyaux, se déclenche en boucle lors du déroulement du jeu
    '''

    global pipe_timer
    global pipe_offset
    global pipes
    if pipe_timer <= 0 :
        pipe_top_y = random.randint(-height, -pipe_offset)                      #   on définit la hauteur du tuyau d'en haut (en y) de manière aléatoire
        pipe_bottom_y = pipe_top_y + pipe_top_img.get_height() + pipe_offset                #   on définit la hauteur du tuyau d'en bas (en y) en fonction de celui d'en haut

        pipe_top = Pipe(width, pipe_top_y, pipe_top_img)              #   on crée les 2 tuyaux
        pipe_bottom = Pipe(width, pipe_bottom_y, pipe_bottom_img)

        all_pipes.add(pipe_top)
        all_pipes.add(pipe_bottom)

        pipes.append(pipe_top)              #   on ajoute les 2 tuyaux dans la liste de tous les tuyaux (ce qui permetra de les manipuler + facilement)
        pipes.append(pipe_bottom)
            
        pipe_timer = 100
    pipe_timer -= 0.65                      #   pipe_timer correspond au temps d'attente entre la création des tuyaux (plus la valeur est élevée, plus les tuyaux se créeront rapidement et inversement)

def deleteAllPipes() :

    '''
    la suppression des tuyaux, se déclenche quand ils ne sont plus visibles sur l'écran ou quand l'oiseau meurt
    '''

    global pipes
    for pipe in pipes :
        pipe.kill()
    pipes.clear()       #   on supprime tous les tuyaux de la liste

def updateScore() :

    '''
    la mise à jour du score, se produit à chaque fois que l'on passe une paire de tuyaux (ajoute 1 point au score)
    
    '''

    global score_value
    score_text = addOutline(fonts[2].render(str(score_value), False, (255, 255, 255)).convert(), 3.5, (1, 1, 1))
    screen.blit(score_text, (width / 2 - score_text.get_width() / 2, height / 4.85 - score_text.get_height() / 2))

def updateRecord() :

    '''
    la vérification entre le score obtenu et le record, le met à jour si on le dépasse
    '''

    global record_value
    global record_sign
    global new_state
    if score_value > record_value :
        record_file = open("record.csv", "w")
        record_file.write(str(score_value))
        record_value = score_value
        record_sign.text = "RECORD : " + str(record_value)
        record_sign.image = sign_img
        record_sign.rect = record_sign.image.get_rect()
        record_sign.rect.center = (record_sign.x, record_sign.y)
        record_sign.image = pygame.transform.scale(record_sign.image, (record_sign.rect.width + record_sign.add_sizeX, record_sign.rect.height))
        record_sign.rect.width = record_sign.rect.width + record_sign.add_sizeX
        record_sign.render = addOutline(fonts[1].render(record_sign.text, False, (255, 255, 255)).convert(), 2.25, (1, 1, 1))
        record_sign.image.blit(record_sign.render, (record_sign.rect.width / 2 - record_sign.render.get_width() / 2, record_sign.rect.height / 2 - record_sign.render.get_height() / 2))
        new_state = True

# ---------------------------------------------------- DÉROULEMENT DU JEU ----------------------------------------------------


def gameStart() :

    '''
    le menu principal, en attendant que le joueur appuie sur "espace" pour commencer la partie
    '''

    start = False
    global background_scroll
    global pipe_timer
    global score_value
    background_scroll = 0                               #    on initialise le niveau de scroll de base du fond (par défaut 0)
    pipe_timer = 0                                      #    on initialise le timer des tuyaux (par défaut 0)
    score_value = 0                                     #    on initialise la valeur du score (par défaut 0)
    all_sprites.add(bird, icon_settings, icon_credits, record_sign)
    bird.rect.center = (width / 2.7, height / 2.08)     #    on initialise la position de l'oiseau à chaque fois que l'on est dans le menu principal
    bird.image = pygame.transform.rotozoom(bird_img, 0, 1)
    bird.rect = bird.image.get_rect(center = bird.rect.center)
    while not start :
        clock.tick(FPS)
        screen.blit(background_img, (0, 0))
        screen.blit(gamestart_text, (width / 2 - gamestart_text.get_width() / 2, height / 2.8 - gamestart_text.get_height() / 2))
        all_sprites.draw(screen)
        if bird.rect.centery == height / 2.08 or bird.rect.centery >= height / 2.08 + 16 :    #   fait l'annimation de montée
            while not start and bird.rect.centery > height / 2.08 - 16 :
                clock.tick(FPS)
                bird.rect.centery -= 1
                screen.blit(background_img, (0, 0))
                screen.blit(gamestart_text, (width / 2 - gamestart_text.get_width() / 2, height / 2.8 - gamestart_text.get_height() / 2))
                all_sprites.draw(screen)
                if icon_settings.rect.collidepoint(pygame.mouse.get_pos()) :
                    icon_settings.hovered()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif icon_credits.rect.collidepoint(pygame.mouse.get_pos()) :
                    icon_credits.hovered()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else :
                    icon_settings.reset()
                    icon_credits.reset()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.display.flip()
                for event in pygame.event.get() :
                    checkWindowExit(event)
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_SPACE :     #  quand le joueur appuie sur "espace", alors la partie commence
                            pygame.mixer.Sound.play(sounds[1])
                            bird.speed = -9.5
                            bird.image = pygame.transform.rotozoom(bird_img, 45, 1)         #   on utilise "rotozoom" afin de garder la meilleure qualité d'image possible car "rotate" la détériore
                            bird.rect = bird.image.get_rect(center = bird.rect.center)      #   à chaque fois qu'on modifie l'angle d'un sprite sa taille change, donc il faut qu'on l'adapte
                            icon_settings.reset()
                            all_sprites.remove(icon_settings, icon_credits, record_sign)
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            start = True
        elif bird.rect.centery <= height / 2.08 :            #   fait l'annimation de descente
            while not start and bird.rect.centery < height / 2.08 + 16 :
                clock.tick(FPS)
                bird.rect.centery += 1
                screen.blit(background_img, (0, 0))
                screen.blit(gamestart_text, (width / 2 - gamestart_text.get_width() / 2, height / 2.8 - gamestart_text.get_height() / 2))
                all_sprites.draw(screen)
                if icon_settings.rect.collidepoint(pygame.mouse.get_pos()) :
                    icon_settings.hovered()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif icon_credits.rect.collidepoint(pygame.mouse.get_pos()) :
                    icon_credits.hovered()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else :
                    icon_settings.reset()
                    icon_credits.reset()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.display.flip()
                for event in pygame.event.get() :
                    checkWindowExit(event)
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_SPACE :
                            pygame.mixer.Sound.play(sounds[1])
                            bird.speed = -9.5
                            bird.image = pygame.transform.rotozoom(bird_img, 45, 1)
                            bird.rect = bird.image.get_rect(center = bird.rect.center)
                            icon_settings.reset()
                            all_sprites.remove(icon_settings, icon_credits, record_sign)
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                            start = True

def gameLoop() :

    '''
    le déroulement du jeu, où tout se passe => l'oiseau peut sauter et meurt s'il dépasse le plafond, le sol ou un tuyau + les animations
    '''

    on = True
    global score_value
    dead = False
    while on :
        clock.tick(FPS)         #   permet de bien avoir le nombre de FPS souhaité (en l'occurence ici 60) => cela doit être exécuté pour chaque image, donc chaque itération d'une boucle "while"
        backgroundLoop()
        all_sprites.update()
        all_sprites.draw(screen)
        createPipes()           #   on crée les tuyaux en boucle
        all_pipes.update()
        all_pipes.draw(screen)
        updateScore()
        for pipe in pipes :
            if not dead and pygame.sprite.collide_mask(bird, pipe) and pipes.index(pipe) % 2 == 0 :     #   mort à cause des tuyaux du haut + animation
                dead = True
                pygame.mixer.Sound.play(sounds[2])
                rotation = 45
                bird.speed = 0
                while bird.rect.y < height + 230 :
                    clock.tick(FPS)
                    backgroundLoop()
                    rotation += 10
                    bird.rect.x -= 8
                    all_sprites.update()
                    all_sprites.draw(screen)
                    all_pipes.update()
                    all_pipes.draw(screen)
                    updateScore()
                    bird.image = pygame.transform.rotozoom(bird_img, rotation, 1)
                    bird.rect = bird.image.get_rect(center = bird.rect.center)
                    pygame.display.flip()
                    if pygame.sprite.collide_mask(bird, pipes[pipes.index(pipe) + 1]) :
                        bird.speed = -4
                    for event in pygame.event.get() :
                        checkWindowExit(event)
                all_sprites.remove(bird)
                screen.fill((0, 0, 0))
                backgroundLoop()
                all_pipes.draw(screen)
                on = False
            elif not dead and pygame.sprite.collide_mask(bird, pipe) and pipes.index(pipe) % 2 == 1 :     #   mort à cause des tuyaux du bas + animation
                dead = True
                pygame.mixer.Sound.play(sounds[2])
                rotation = 45
                bird.speed = -9.5
                while bird.rect.y < height + 230 :
                    clock.tick(FPS)
                    backgroundLoop()
                    rotation += 10
                    bird.rect.x -= 8
                    all_sprites.update()
                    all_sprites.draw(screen)
                    all_pipes.update()
                    all_pipes.draw(screen)
                    updateScore()
                    bird.image = pygame.transform.rotozoom(bird_img, rotation, 1)
                    bird.rect = bird.image.get_rect(center = bird.rect.center)
                    pygame.display.flip()
                    if pygame.sprite.collide_mask(bird, pipe) :
                        bird.speed = -4
                    for event in pygame.event.get() :
                        checkWindowExit(event)
                all_sprites.remove(bird)
                screen.fill((0, 0, 0))
                backgroundLoop()
                all_pipes.draw(screen)
                on = False
            elif not dead and not pipe.reached and pipe.rect.x <= bird.rect.x - (pipe_top_img.get_width() / 2) and pipe.image == pipe_top_img :    #   ajoute 1 point au score quand on passe une paire de tuyaux
                pipe.reached = True
                pipes[1].reached = True
                score_value = score_value + 1
                updateScore()
        if not dead and (bird.rect.y <= -20 or bird.rect.y >= height - 70) :    #   fait les animations de mort en fonction de l'endroit où l'oiseau touche la fenêtre
            dead = True
            pygame.mixer.Sound.play(sounds[2])
            bird_bounce = 0
            if bird.rect.y <= -20 :                              #   mort à cause du plafond + animation
                rotation = 45
                while bird.rect.y < height + 250 :
                    clock.tick(FPS)
                    backgroundLoop()
                    rotation += 10
                    all_sprites.update()
                    all_sprites.draw(screen)
                    all_pipes.update()
                    all_pipes.draw(screen)
                    updateScore()
                    bird.rect.x += bird_bounce
                    bird.image = pygame.transform.rotozoom(bird_img, rotation, 1)
                    bird.rect = bird.image.get_rect(center = bird.rect.center)
                    pygame.display.flip()
                    for pipe in pipes :
                        if pygame.sprite.collide_mask(bird, pipe) :
                            bird_bounce = -10
                    for event in pygame.event.get() :
                        checkWindowExit(event)
            elif bird.rect.y >= height - 70 :                    #   mort à cause du sol + animation
                bird.speed = -14
                rotation = -45
                while bird.rect.y < height + 150 :
                    clock.tick(FPS)
                    backgroundLoop()
                    rotation += 10
                    all_sprites.update()
                    all_sprites.draw(screen)
                    all_pipes.update()
                    all_pipes.draw(screen)
                    updateScore()
                    bird.rect.x += bird_bounce
                    bird.image = pygame.transform.rotozoom(bird_img, rotation, 1)
                    bird.rect = bird.image.get_rect(center = bird.rect.center)
                    pygame.display.flip()
                    for pipe in pipes :
                        if pygame.sprite.collide_mask(bird, pipe) :
                            bird_bounce = -8
                    for event in pygame.event.get() :
                        checkWindowExit(event)
            all_sprites.remove(bird)            #   on supprime l'oiseau de l'écran
            screen.fill((0, 0, 0))
            backgroundLoop()
            all_pipes.draw(screen)
            on = False

        if bird.speed < 0 :       # saute
            bird.image = pygame.transform.rotozoom(bird_img, 45, 1)
            bird.rect = bird.image.get_rect(center = bird.rect.center)
        elif bird.speed > 8.5 :     # tombe
            bird.image = pygame.transform.rotozoom(bird_img, -45, 1)
            bird.rect = bird.image.get_rect(center = bird.rect.center)
        else :                    # stable
            bird.image = pygame.transform.rotozoom(bird_img, 0, 1)
            bird.rect = bird.image.get_rect(center = bird.rect.center)
        bird.mask = pygame.mask.from_surface(bird.image)
        
        pygame.display.flip()

        for event in pygame.event.get() :
            checkWindowExit(event)
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE and dead == False :     #   quand le joueur appuie sur "espace", alors l'oiseau saute
                    pygame.mixer.Sound.play(sounds[1])
                    bird.speed = -9.5

def gameOver() :

    '''
    l'écran de mort, en attendant que le joueur choisisse entre recommencer la partie ou quitter le jeu
    '''

    start = False
    all_sprites.add(board, restart_button, leave_button)
    updateRecord()
    global score_value
    global new_state
    score_text = addOutline(fonts[2].render(str(score_value), False, (255, 255, 255)).convert(), 3.5, (1, 1, 1))
    screen.blit(score_text, (width / 2 - score_text.get_width() / 2, height / 2.15 - score_text.get_height() / 2))
    while not start :
        clock.tick(FPS)
        all_sprites.draw(screen)
        screen.blit(gameover_text, (width / 2 - gameover_text.get_width() / 2, height / 2.65 - gameover_text.get_height() / 2))
        screen.blit(score_text, (width / 2 - score_text.get_width() / 2, height / 2.15 - score_text.get_height() / 2))
        if new_state :
            screen.blit(new_img, (width / 2 - 225, height / 2 - 96))
        if restart_button.rect.collidepoint(pygame.mouse.get_pos()) :           #   applique l'animation de hover si la souris survole les boutons "restart_button" et "leave_button"
            restart_button.hovered()
            leave_button.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif leave_button.rect.collidepoint(pygame.mouse.get_pos()) :
            leave_button.hovered()
            restart_button.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else :
            restart_button.reset()                     #   enlève l'animation de hover sur les 2 boutons
            leave_button.reset()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        pygame.display.flip()

        for event in pygame.event.get() :
            checkWindowExit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                if restart_button.rect.collidepoint(pygame.mouse.get_pos()) :   #   recommence la partie quand le joueur clique sur le bouton "restart_button"
                    pygame.mixer.Sound.play(sounds[0])
                    deleteAllPipes()
                    all_sprites.remove(board, restart_button, leave_button)
                    restart_button.reset()
                    leave_button.reset()
                    new_state = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    start = True
                elif leave_button.rect.collidepoint(pygame.mouse.get_pos()) :   #   quitte le jeu quand le joueur clique sur le bouton "leave_button"
                    pygame.mixer.Sound.play(sounds[0])
                    pygame.time.delay(375)
                    pygame.quit()
                    sys.exit()

while True :
    gameStart()    #   lance le menu principal
    gameLoop()     #   lance la partie
    gameOver()     #   lance l'écran de mort