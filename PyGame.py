## This library installed under PLAYING
import pygame
from sys import exit
from random import randint
import pygame.image 

def display_score(): 
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = text_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surface.get_rect(center = (200,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8

            if obstacle_rect.bottom == 550:
                screen.blit(snail_frames[snail_frame_index], obstacle_rect)
            else:
                screen.blit(fly_frames[fly_frame_index], obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list
                         if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_Rect in obstacles:
            if player.colliderect(obstacle_Rect):
                return False
    return True

def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 550:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((1080, 720))#This is tuple, may not change
pygame.display.set_caption("Ultimate Runner")
## Music
clock = pygame.time.Clock()
jump_sound = pygame.mixer.Sound('jump.mp3')  
bgm_music = pygame.mixer.Sound('music.wav')  
jump_sound.set_volume(0.2)
bgm_music.set_volume(0.1)
bgm_music.play(loops=-1)

text_font = pygame.font.Font('Pixeltype.ttf', 50)
game_active = True
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()


## Background
sky_surface = pygame.image.load('background.png').convert_alpha()
ground_surface = pygame.image.load('ground.png').convert_alpha()
score_surface = text_font.render('My game', False, 'Black')
score_rect = score_surface.get_rect(center = (540, 360))

## Background size.convert()
player_walk1 = pygame.image.load('run.png').convert_alpha()
player_walk2 = pygame.image.load('run1.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump= pygame.image.load('run.png').convert_alpha()

player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom = (80,550))
sky_surface = pygame.transform.scale(sky_surface, (int(sky_surface.get_width() * 0.8), int(sky_surface.get_height() * 0.45)))
ground_surface = pygame.transform.scale(ground_surface, (int(ground_surface.get_width() * 1.8), int(ground_surface.get_height() )))
# player_surface = pygame.transform.scale(player_surface, (int(player_surface.get_width() * 0.2), int(player_surface.get_height() *0.2)))

player_gravity = 0
#Intro screen
player_stand1 = pygame.image.load("stand.png").convert_alpha()
player_stand_rect = player_stand1.get_rect(center = (540,360))

#Obstacles
snail_frame1 = pygame.image.load('snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load("Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("Fly2.png").convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []
##Game Intro text
game_name = text_font.render('Da Wang Go!!!',False, (111,196,169))
game_name_rect = game_name.get_rect(center = (540, 100))

game_message = text_font.render('Press space to run!',False, (111,196,169))
game_message_rect = game_message.get_rect(center = (540, 600))

##Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    ## Position of surface
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 565:
                    player_gravity = -20
                    jump_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 565:
                    player_gravity = -20
                    jump_sound.play()
        else:       
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 1000
                start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(1100,1400), 550)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(1100,1400), 450)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                    snail_surface = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                    fly_surface = fly_frames[fly_frame_index]
   
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,550))

        score = display_score()

        player_animation()
        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 565:
            player_rect.bottom = 565
        screen.blit(player_surface, player_rect)
       
        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collison
        game_active = collisions(player_rect,obstacle_rect_list)
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
    else:
        ##Game over screen
        screen.fill((94,129,162))
        screen.blit(player_stand1,player_stand_rect)
        obstacle_rect_list.clear()
        score_message = text_font.render(f"Your score {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (540, 700))
        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
            screen.blit(game_message,game_message_rect)
    pygame.mouse.get_pressed()
    pygame.display.update()
    clock.tick(60) ## Set the framerate under 60 FPS