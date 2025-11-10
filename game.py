import pygame, sys, random
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 35)

# Biến game
gravity, bird_movement = 0.1, 0
game_active, score, high_score = True, 0, 0
floor_x_pos, score_sound_countdown = 0, 100

# Tải tài nguyên
bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
floor = pygame.transform.scale2x(pygame.image.load('assets/floor.png').convert())

bird_list = [pygame.transform.scale2x(pygame.image.load(f'assets/yellowbird-{f}.png').convert_alpha()) for f in ['downflap', 'midflap', 'upflap']]
bird_index, bird = 0, bird_list[0]
bird_rect = bird.get_rect(center=(100, 384))

pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
pipe_list, pipe_height = [], [200, 300, 400]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# Timers
spawnpipe, birdflap = pygame.USEREVENT, pygame.USEREVENT + 1
pygame.time.set_timer(spawnpipe, 3000)
pygame.time.set_timer(birdflap, 200)

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    pos = random.choice(pipe_height)
    return pipe_surface.get_rect(midtop=(500, pos)), pipe_surface.get_rect(midtop=(500, pos - 700))
def move_pipe(pipes):
    global score
    for pipe in pipes:
        pipe.centerx -= 1
        if pipe.centerx == 100: 
            score += 1
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface if pipe.bottom >= 600 else pygame.transform.flip(pipe_surface, False, True), pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    return -75 < bird_rect.top < 650

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

def bird_animation():
    global bird_index
    bird_index = (bird_index + 1) % 3
    new_bird = bird_list[bird_index]
    return new_bird, new_bird.get_rect(center=(100, bird_rect.centery))

def score_display(state):
    if state == 'main':
        s = game_font.render(str(int(score)), True, (255, 255, 255))
        screen.blit(s, s.get_rect(center=(216, 100)))
    else:
        s = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        hs = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        screen.blit(s, s.get_rect(center=(216, 100)))
        screen.blit(hs, hs.get_rect(center=(216, 630)))

def update_score():
    return max(score, high_score)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(), sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_active:
                bird_movement = -4
                flap_sound.play()
            else:
                game_active, pipe_list = True, []
                bird_rect.center, bird_movement, score = (100, 384), 0, 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotate_bird(bird), bird_rect)

        game_active = check_collision(pipe_list)
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score_display('main')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score()
        score_display('over')

    floor_x_pos = (floor_x_pos - 1) % -432
    draw_floor()
    pygame.display.update()
    clock.tick(120)