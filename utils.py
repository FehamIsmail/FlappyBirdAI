def update_birds(birds, gravity, velocity, machine_learning_mode, dt):
    for x in range(len(birds)):
        if birds[x].has_jumped:
            updatePosition(birds[x], gravity, velocity, machine_learning_mode, dt)


def updatePosition(birdToUpdate, gravity, velocity, machine_learning_mode, dt):
    birdToUpdate.v += 25 * gravity * dt
    if birdToUpdate.alive is False and machine_learning_mode:
        birdToUpdate.setX(birdToUpdate.x - velocity * dt)

    birdToUpdate.setY(birdToUpdate.y + birdToUpdate.v * dt + gravity * dt)


def blit_rotate(surf, image, pos, originPos, angle, pygame):
    zoom = 1
    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    move = (-originPos[0] + min_box[0] - pivot_move[0], -originPos[1] - max_box[1] + pivot_move[1])
    origin = (pos[0] + zoom * move[0], pos[1] + zoom * move[1])

    # get a rotated image
    rotozoom_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotozoom_image, origin)


def render_floor(surf, floor, floor_pos, velocity, dt, game_active):
    floor_delta_x = velocity * dt
    if game_active:
        floor_pos.x -= floor_delta_x if floor_pos.x > -floor_pos.w else -floor_pos.w
    surf.blit(floor, (floor_pos.x, 900))
    surf.blit(floor, (floor_pos.x + 576, 900))


def check_collision(bird, pipes):
    # pipe collision
    for pipe in pipes:
        if bird.rect.colliderect(pipe):
            return True
    # floor collision
    if bird.rect.top <= -100 or bird.rect.bottom >= 900:
        return True
    return False


def check_if_game_stop(birds):
    game_finished = True
    for b in birds:
        if b.alive:
            game_finished = False
    return not game_finished


def reset_birds(birds, x, y, best_bird):
    if best_bird is not None:
        reset_one_bird(best_bird, x, y)
    for bird in birds:
        if best_bird is not None:
            bird.parent_genes = best_bird.genes
        reset_one_bird(bird, x, y)
        bird.genes = [[], [], []]
        bird.create_genes()

    if best_bird is not None:
        birds.pop(len(birds) - 1)
        birds.append(best_bird)
        birds[len(birds) - 1].updateImage(True)


def reset_one_bird(bird, x, y):
    bird.setY(y)
    bird.setX(x)
    bird.alive = True
    bird.v = 0
    bird.has_jumped = False


def update_pipes(pipes, velocity, dt, game_active):
    if game_active:
        for pipe in pipes:
            if pipe is not None:
                pipe.x -= velocity * dt / 2
    return pipes


def render_pipes(surf, pipe_surface, pipes, pygame, close_pipes, red_pipe_surface):
    if len(pipes) > 0:
        for pipe in pipes:
            if pipe.bottom >= 1024:
                if pipe.x + pipe.w >= 0:
                    if close_pipes is not None and close_pipes[0] == pipe:
                        surf.blit(red_pipe_surface, pipe)
                    else:
                        surf.blit(pipe_surface, pipe)
            else:
                if pipe.x + pipe.w >= 0:
                    if close_pipes is not None and close_pipes[1] == pipe:
                        flip_pipe = pygame.transform.flip(red_pipe_surface, False, True)
                    else:
                        flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                    surf.blit(flip_pipe, pipe)

# counter = 0
def get_closest_pipes(pipe_list, bird_x_pos):
    if len(pipe_list) == 2:
        return pipe_list[0], pipe_list[1]
    is_pipe_behind = pipe_list[1].x < bird_x_pos - pipe_list[0].width
    if is_pipe_behind:
        return pipe_list[2], pipe_list[3]
    else:
        return pipe_list[0], pipe_list[1]


def create_score_surfaces(font, score, is_game_over):
    offset_x = 540 if not is_game_over else 288
    offset_y = 50 if not is_game_over else 500
    score_surface_outline = font.render(str(round(score)), True, (84, 56, 71))
    score_rect_outline = score_surface_outline.get_rect()
    delta_x = score_rect_outline.width / 2 if not is_game_over else 0
    score_rect_outline.center = (offset_x - delta_x + 5, offset_y + 5)

    score_surface = font.render(str(round(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.center = (offset_x - delta_x, offset_y)
    return (score_surface, score_rect), (score_surface_outline, score_rect_outline)


def get_bird_to_display(birds):
    for bird in birds:
        if bird.alive:
            return bird