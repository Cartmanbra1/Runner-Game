import pygame
from sys import exit
from os.path import join
from random import randint


def speed():
    count = 0
    speed_check = 1
    check_score = score
    while check_score > 100:
        check_score //= 10
        count += 1
        speed_check *= 10
    speed_check *= 2.5
    if score % speed_check >= 0 or score <= 10 :
        count += 1
    return count

def display_time():
    current_time = pygame.time.get_ticks() - game_time
    current_time //= speed_up - speed()
    score_surf = text.render("Score:" + f'{current_time}', False, 50)
    score_rect = score_surf.get_rect(topleft=(10, 10))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    global snail_surface, fly_surf, obstacle_index
    obstacle_index += 0.1
    if obstacle_index >= len(fly_surf) or obstacle_index >= len(snail_surface):
        obstacle_index = 0
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= obstacle_speed + speed()
            if obstacle_rect.bottom == 300:
                snail_surf = snail_surface[int(obstacle_index)]
                screen.blit(snail_surf, obstacle_rect)
            else:
                fly_surface = fly_surf[int(obstacle_index)]
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()
game_active = False
game_time = 0
speed_up = 10
score = 0
obstacle_speed = 4
obstacle_index = 0

player = pygame.sprite.GroupSingle()
#player.add(Player())

path = join("UltimatePygameIntro-main", "graphics")

text = pygame.font.Font(path.strip("graphics") + "font\Pixeltype.ttf", 50)

sky_surface = pygame.image.load(path + "\Sky.png").convert()
ground_surface = pygame.image.load(path + "\ground.png").convert()

hit_surface = text.render("Hit!", False, "Red")
hit_rect = hit_surface.get_rect(midleft=(80, 200))

snail_surface1 = pygame.image.load(path + "\snail\snail1.png").convert_alpha()
snail_surface2 = pygame.image.load(path + "\snail\snail2.png").convert_alpha()
snail_surface = [snail_surface1, snail_surface2]

fly_surf1 = pygame.image.load(path + "/fly/fly1.png").convert_alpha()
fly_surf2 = pygame.image.load(path + "/fly/fly2.png").convert_alpha()
fly_surf = [fly_surf1, fly_surf2]

player_walk_1 = pygame.image.load(path + "\Player\player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load(path + "\Player\player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load(path + "\Player\jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80,300))
player_gravity = 0


# Game over

def games_score(score):
    game_score = text.render("Your score: " + f'{score}', False, (111, 196, 169))
    game_score_rect = game_score.get_rect(midbottom=(400, 322))
    return game_score, game_score_rect


game_name = text.render("Pixel runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(midbottom=(400, 120))

game_message = text.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(midbottom=(400, 322))

player_stand = pygame.image.load(path + "\Player\player_stand.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (120, 150))
player_stand_rect = player_stand.get_rect(midtop=(400, 130))

# Game over

# Obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)
obstacle_rect_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
                    player_rect.y += player_gravity
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20
                    player_rect.y += player_gravity
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface[int(obstacle_index)].get_rect(midbottom=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf[int(obstacle_index)].get_rect(midbottom=(randint(900, 1100), 200)))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    game_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_time()

        # Player

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        for obstacle in obstacle_rect_list:
            if player_rect.colliderect(obstacle):
                game_active = False
                obstacle_rect_list = []
                player_rect.midbottom = (80, 300)
                player_gravity = 0
    else:
        screen.blit(hit_surface, hit_rect)
        screen.fill((94, 129, 162))
        game_score, game_score_rect = games_score(score)
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(game_score, game_score_rect)

    pygame.display.update()
    clock.tick(60)
