import pygame
import sys
import random
import copy
from bird import Bird
from utils import *

# initializing the game engine
pygame.init()

# initializing variables
game_active = False
is_game_over = False
start_time = None
score = 1
best_bird = None
bird_on_display = None  # determines which birds to draw vector lines
best_score = 1
generation = 0

# initializing constants
MACHINE_LEARNING_MODE = True
VECTOR_DEBUG_MODE = True
clock = pygame.time.Clock()
GRAVITY = 120
VELOCITY = 420
NUM_OF_BIRDS = 70 if MACHINE_LEARNING_MODE else 1
screen = pygame.display.set_mode((576, 1024))

# creating score text
font = pygame.font.Font("asset/FlappyBirdy.ttf", 64)

# creating menu message
menu_surface = pygame.image.load("asset/message.png").convert_alpha()
menu_surface = pygame.transform.scale2x(menu_surface)
menu_rect = menu_surface.get_rect(center=(288, 512))

# creating game over message
game_over_surface = pygame.image.load("asset/gameover.png").convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_surface_rect = game_over_surface.get_rect(center=(288, 400))

# creating background
background = pygame.image.load("asset/background-day.png").convert()
background = pygame.transform.scale2x(background)

# creating floor
floor = pygame.image.load("asset/base.png").convert()
floor = pygame.transform.scale2x(floor)
floor_pos = floor.get_rect()

# creating pipes
pipe_surface = pygame.image.load("asset/pipe-green.png").convert_alpha()
pipe_surface = pygame.transform.scale2x(pipe_surface)
red_pipe_surface = pygame.image.load("asset/pipe-red.png").convert_alpha()
red_pipe_surface = pygame.transform.scale2x(red_pipe_surface)
if not VECTOR_DEBUG_MODE:
    red_pipe_surface = pipe_surface

pipe_list = []
pipe_height = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT


def create_pipe():
    rand_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700, rand_pipe_pos - 200))
    bottom_pipe = pipe_surface.get_rect(midtop=(700, rand_pipe_pos))
    return bottom_pipe, top_pipe


# creating birds
birds = []
UPDATE_BIRD_ON_DISPLAY = pygame.USEREVENT
for n in range(NUM_OF_BIRDS):
    birds.append(Bird(False))

# feeding bird images
birdImages = []
current_bird_image_frame = 1
for bird in birds:
    birdImage = pygame.image.load(bird.image[current_bird_image_frame]).convert_alpha()
    scaledBirdImage = pygame.transform.scale2x(birdImage)
    birdImages.append(scaledBirdImage)
    bird.rect = scaledBirdImage.get_rect()
    bird.rect.x = 180 - birdImage.get_rect().width / 2
    bird.create_genes()


def check_and_update_bird_image(surf, time, game):
    global birdImages, birds, current_bird_image_frame
    calculated_frame = int(time) % 3
    frame_has_changed = current_bird_image_frame != calculated_frame
    current_bird_image_frame = calculated_frame if frame_has_changed else current_bird_image_frame
    if frame_has_changed:
        for idx in range(len(birds)):
            new_bird_image = pygame.image.load(birds[idx].image[current_bird_image_frame]).convert_alpha()
            birdImages[idx] = pygame.transform.scale2x(new_bird_image)
    for i in range(len(birds)):
        if birds[i].y < 876:
            blit_rotate(surf, birdImages[i], (birds[i].x, birds[i].y), (34, 24), birds[i].getAngle(), game)


def reset_game():
    reset_birds(birds, 200, 512, best_bird)
    global game_active, pipe_list, score
    game_active = True
    score = 1
    pipe_list.clear()


def force_game_start():
    reset_game()
    global is_game_over, bird_on_display
    is_game_over = False
    bird_on_display = best_bird
    for b in birds:
        b.jump()


def draw_input_lines(surf, b, close_pipes):
    pygame.draw.line(surf, [0, 0, 0], (200, b.y), (close_pipes[1].x, b.y), width=3)
    pygame.draw.line(surf, [255, 0, 0], (200, b.y), (close_pipes[1].x, close_pipes[1].bottom), width=3)
    pygame.draw.line(surf, [0, 255, 0], (197, b.y), (close_pipes[0].x, close_pipes[0].top), width=3)


def create_text_surface(text, x, y, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    return text_surface, text_rect


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                birds[0].jump()
        if event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_SPACE:
                reset_game()
                game_active = True
                is_game_over = False
                birds[0].jump()
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
            if len(pipe_list) > 4:
                pipe_list.pop(0)
                pipe_list.pop(0)
        if event.type == UPDATE_BIRD_ON_DISPLAY and game_active and best_bird is not None:
            if not best_bird.alive:
                bird_on_display = get_bird_to_display(birds)

    if len(pipe_list) == 0 and game_active:
        pipe_list.extend(create_pipe())
        pygame.time.set_timer(SPAWNPIPE, int(672000 / VELOCITY))

    screen.blit(background, (0, 0))
    dt = clock.tick(200) / 1000

    update_birds(birds, GRAVITY, VELOCITY, MACHINE_LEARNING_MODE, dt)
    update_pipes(pipe_list, VELOCITY, dt, game_active)
    closest_pipes_temp = None
    if len(pipe_list) > 0:
        closest_pipes_temp = get_closest_pipes(pipe_list, 156)
    render_pipes(screen, pipe_surface, pipe_list, pygame, closest_pipes_temp, red_pipe_surface)
    render_floor(screen, floor, floor_pos, VELOCITY, dt, game_active)
    check_and_update_bird_image(screen, int((pygame.time.get_ticks() * 4) / 1000), pygame)

    if game_active:
        for bird in birds:
            if bird.alive:
                closest_pipes = get_closest_pipes(pipe_list, 156)
                distance_to_bottom = closest_pipes[0].top - bird.y
                distance_to_top = bird.y - closest_pipes[1].bottom
                if MACHINE_LEARNING_MODE:
                    if bird == bird_on_display and VECTOR_DEBUG_MODE:
                        draw_input_lines(screen, bird_on_display, closest_pipes)
                    if bird.calculate_jump(distance_to_bottom, distance_to_top):
                        bird.jump()
                if check_collision(bird, pipe_list):
                    bird.alive = False
                    if bird == best_bird:
                        bird_on_display = get_bird_to_display(birds)
                    if not check_if_game_stop(birds) and MACHINE_LEARNING_MODE:
                        generation += 1
                        if score > best_score:
                            best_score = score
                            print('new score: ', best_score)
                            bird_copy = copy.deepcopy(bird)
                            best_bird = bird_copy
        score += dt * 100
        game_active = check_if_game_stop(birds)
        if not game_active:
            is_game_over = True
    if not game_active:
        if is_game_over:
            screen.blit(game_over_surface, game_over_surface_rect)
        else:
            screen.blit(menu_surface, menu_rect)
        # resets the game and force all birds to jump
        if MACHINE_LEARNING_MODE:
            force_game_start()

    score_surfaces = create_score_surfaces(font, score, is_game_over)
    screen.blit(score_surfaces[1][0], score_surfaces[1][1])
    screen.blit(score_surfaces[0][0], score_surfaces[0][1])
    if MACHINE_LEARNING_MODE:
        generation_text = create_text_surface("Gen:" + str(generation), 80, 50, (255, 255, 255))
        generation_text_outline = create_text_surface("Gen:" + str(generation), 85, 55, (84, 56, 71))
        screen.blit(generation_text_outline[0], generation_text_outline[1])
        screen.blit(generation_text[0], generation_text[1])
    pygame.display.update()

# def updateImage():
