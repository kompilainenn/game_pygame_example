import pygame
import random
import sys
from items import StaticItem, AnimatedItem, AnimatedItemJump, Button, Slider
from pygame.sprite import Group
from colors import LIGHT_BLUE, WHITE, BLACK, GRAY, LIGHT_GOLDEN_YELLOW, GLASS, BLUE, RED, GREEN
from settings import Settings
from results import init_db, get_results, add_result

# pygame inits
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# fonts and its size
font_button = pygame.freetype.Font('fonts/Arial.ttf', 30)
font_slider = pygame.freetype.Font('fonts/Arial.ttf', 50)
font_message = pygame.freetype.Font('fonts/Arial.ttf', 50)

# database init with some data if it's a new install
init_db()

# main window settings
sett = Settings()
main_window = pygame.display.set_mode((sett.display_widht, sett.display_height))
x_center = sett.display_widht // 2
pygame.display.set_caption('Zombi Runner')
icon = pygame.image.load('images/zombi.png').convert()
pygame.display.set_icon(icon)

# the backgrounds
background = pygame.image.load('images/background.png').convert()
background_1440 = pygame.image.load('images/background_1440.png').convert()
background_1440 = pygame.transform.scale(background_1440, (1440, 900))
background_1920 = pygame.image.load('images/background_1920.png').convert()
menu_background = pygame.image.load('images/menu_background_4.jpg').convert()
menu_background = pygame.transform.scale(menu_background, (sett.display_widht, sett.display_height))

def print_text(message, font_color=(0, 0, 0), font_type='fonts/Arial.ttf', 
                font_size=30, x=None, y=0, surface=None):
    global main_window

    target_surface = surface if surface is not None else main_window
    font = pygame.freetype.Font(font_type, font_size)
    text_rect = font.get_rect(message)

    # Если x не указан, центрируем по горизонтали
    if x is None:
        text_rect.centerx = target_surface.get_rect().centerx
    else:
        text_rect.x = x
    text_rect.y = y

    
    # Рендерим текст напрямую на основное окно
    font.render_to(target_surface, text_rect.topleft, message, fgcolor=font_color)

def pause_game():
    global main_window

    # surface for controls
    pause_surface = pygame.Surface((450, 550), pygame.SRCALPHA)
    pause_surface.fill(GLASS)
    pause_surface_rect = pause_surface.get_rect()
    pause_surface_rect.center = main_window.get_rect().center

    # controls
    continue_button = Button(125, 250, 200, 50, font_button, "CONTINUE", LIGHT_BLUE, WHITE)
    options_button = Button(125, 325, 200, 50, font_button, "OPTIONS", LIGHT_BLUE, WHITE)
    main_menu_button = Button(125, 400, 200, 50, font_button, "MAIN MENU", LIGHT_BLUE, WHITE)
    quit_button = Button(125, 475, 200, 50, font_button, "QUIT", LIGHT_BLUE, WHITE)

    paused = True
    while paused:
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pause_pos = (
            mouse_pos[0] - pause_surface_rect.x,
            mouse_pos[1] - pause_surface_rect.y
        )
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if continue_button.is_clicked(mouse_pause_pos, event):
                print("Игра продолжена!")
                paused = False
                 
            if options_button.is_clicked(mouse_pause_pos, event):
                print("Открыты настройки")
                options_menu()

                pause_surface_rect.center = main_window.get_rect().center
                pause_surface.fill(GLASS)
                main_window.blit(pause_surface, pause_surface_rect)

                # main window background re-drawing
                if sett.display_widht == 800:
                    main_window.blit(background, (0, 0))
                elif sett.display_widht == 1440:
                    main_window.blit(background_1440, (0, 0))
                elif sett.display_widht == 1920:
                    main_window.blit(background_1920, (0, 0))
                

            if main_menu_button.is_clicked(mouse_pause_pos, event):
                print('Ушли в главное мню!')
                paused = False
                main_menu()

            if quit_button.is_clicked(mouse_pause_pos, event):
                pygame.quit()
                sys.exit()

        # Проверка наведения на кнопки
        continue_button.check_hover(mouse_pause_pos)
        options_button.check_hover(mouse_pause_pos)
        main_menu_button.check_hover(mouse_pause_pos)
        quit_button.check_hover(mouse_pause_pos)
        
        # Отрисовка
        
        main_window.blit(pause_surface, pause_surface_rect)

        # Отрисовка кнопок
        pause_surface.fill(GLASS)
        continue_button.draw(pause_surface)
        options_button.draw(pause_surface)
        main_menu_button.draw(pause_surface)
        quit_button.draw(pause_surface)
                
        pygame.display.update()
        

def game_over(scores):

    font = pygame.freetype.Font('fonts/Arial.ttf', 30)
    input_field_text = ""
    active = False
    input_field_rect = pygame.Rect(sett.display_widht // 2 - 150, 400, 300, 32)
    color_inactive = BLACK
    color_active = GREEN
    color = color_inactive

    stopped = True
    while stopped:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if scores >= get_results()[4][1]:
                print_text('Congrats! You are in TOP 5 now!', y=300)
                print_text('Please enter your name for table of records:', y=350)
        
                # Активация/деактивация поля по клику
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_field_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    color = color_active if active else color_inactive
                
                # Ввод текста
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        print("Введённый текст:", input_field_text)
                        add_result(input_field_text, scores)
                        print_text('Your result have been written!', y=450)
                        print_text('Press Escape to go to main menu', y=500)
                    elif event.key == pygame.K_BACKSPACE:
                        input_field_text = input_field_text[:-1]
                    else:
                        input_field_text += event.unicode
                
                

        if scores >= get_results()[4][1]:
            pygame.draw.rect(main_window, color, input_field_rect, 2)

            # Текст внутри поля
            text_surface = font.render(input_field_text, fgcolor=(0, 0, 0))
            main_window.blit(text_surface[0], (input_field_rect.x + 5, input_field_rect.y + 5))
            
            # Подсказка (placeholder)
            if not input_field_text and not active:
                placeholder = font.render("Enter your name here", True, (100, 100, 100))
                main_window.blit(placeholder[0], (input_field_rect.x + 5, input_field_rect.y + 5))

        else:
            print_text('Game over! Press Escape to go to main menu', y=300)
        
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            main_menu()

        pygame.display.update()
        

def main_menu():
    global main_window, menu_background

    # music in menus
    pygame.mixer.music.load('sounds/main_menu.mp3')
    pygame.mixer.music.play(-1)

    # surface for controls
    main_menu_surface = pygame.Surface((450, 550), pygame.SRCALPHA)
    main_menu_surface.fill(GLASS)
    main_menu_surface_rect = main_menu_surface.get_rect()
    main_menu_surface_rect.center = main_window.get_rect().center

    # controls
    start_button = Button(125, 250, 200, 50, font_button, "PLAY", LIGHT_BLUE, WHITE)
    options_button = Button(125, 325, 200, 50, font_button, "OPTIONS", LIGHT_BLUE, WHITE)
    records_button = Button(125, 400, 200, 50, font_button, "RECORDS", LIGHT_BLUE, WHITE)
    quit_button = Button(125, 475, 200, 50, font_button, "QUIT", LIGHT_BLUE, WHITE)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_main_menu_pos = (
            mouse_pos[0] - main_menu_surface_rect.x,
            mouse_pos[1] - main_menu_surface_rect.y
        )
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.is_clicked(mouse_main_menu_pos, event):
                print("Игра начата!")
                pygame.mixer.music.stop()
                run_game()
                 
            if options_button.is_clicked(mouse_main_menu_pos, event):
                print("Открыты настройки")
                options_menu()
                main_menu_surface_rect.center = main_window.get_rect().center

            if records_button.is_clicked(mouse_main_menu_pos, event):
                print('Открыты результаты!')
                records_menu()

            if quit_button.is_clicked(mouse_main_menu_pos, event):
                pygame.quit()
                sys.exit()

        # Проверка наведения на кнопки
        start_button.check_hover(mouse_main_menu_pos)
        options_button.check_hover(mouse_main_menu_pos)
        records_button.check_hover(mouse_main_menu_pos)
        quit_button.check_hover(mouse_main_menu_pos)
        
        # Отрисовка
        main_window.blit(menu_background, (0, 0))
        main_window.blit(main_menu_surface, main_menu_surface_rect)

        # Отрисовка кнопок
        main_menu_surface.fill(GLASS)
        start_button.draw(main_menu_surface)
        options_button.draw(main_menu_surface)
        records_button.draw(main_menu_surface)
        quit_button.draw(main_menu_surface)
        
        pygame.display.flip()

# slider creating for volume saving
slider = Slider(25, 150, 400, 10, font_button)

def options_menu():
    global main_window, menu_background, x_center

    # surface for controls
    options_surface = pygame.Surface((450, 550), pygame.SRCALPHA)
    options_surface.fill(LIGHT_GOLDEN_YELLOW)
    options_surface_rect = options_surface.get_rect()
    options_surface_rect.center = main_window.get_rect().center

    # controls
    
    mode_800_button = Button(125, 200, 200, 50, font_button, "800 x 600", LIGHT_BLUE, WHITE)
    mode_1440_button = Button(125, 275, 200, 50, font_button, "1440 x 900", LIGHT_BLUE, WHITE)
    mode_1920_button = Button(125, 350, 200, 50, font_button, "1920 x 1080", LIGHT_BLUE, WHITE)
    back_button = Button(125, 450, 200, 50, font_button, "BACK", LIGHT_BLUE, WHITE)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_options_pos = (
            mouse_pos[0] - options_surface_rect.x,
            mouse_pos[1] - options_surface_rect.y
        )
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if mode_800_button.is_clicked(mouse_options_pos, event):
                sett.display_widht = 800
                sett.display_height = 600
                main_window = pygame.display.set_mode((sett.display_widht, sett.display_height))
                menu_background = pygame.image.load('images/menu_background_4.jpg').convert()
                menu_background = pygame.transform.scale(menu_background, (sett.display_widht, sett.display_height))
                options_surface_rect.center = main_window.get_rect().center
                x_center = sett.display_widht // 2
            if mode_1440_button.is_clicked(mouse_options_pos, event):
                sett.display_widht = 1440
                sett.display_height = 900
                menu_background = pygame.image.load('images/menu_background_1440.jpg').convert()
                menu_background = pygame.transform.scale(menu_background, (sett.display_widht, sett.display_height))
                main_window = pygame.display.set_mode((sett.display_widht, sett.display_height))
                options_surface_rect.center = main_window.get_rect().center
                x_center = sett.display_widht // 2
            if mode_1920_button.is_clicked(mouse_options_pos, event):
                sett.display_widht = 1920
                sett.display_height = 1080
                main_window = pygame.display.set_mode((sett.display_widht, sett.display_height), 
                                                        flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
                menu_background = pygame.image.load('images/menu_background_1920.jpg').convert()
                options_surface_rect.center = main_window.get_rect().center
                x_center = sett.display_widht // 2
            if back_button.is_clicked(mouse_options_pos, event):
                running = False
        
        # Отрисовка
        main_window.blit(menu_background, (0, 0))
        main_window.blit(options_surface, options_surface_rect)

        # Отрисовка кнопок
        options_surface.fill(LIGHT_GOLDEN_YELLOW)
        slider.draw(options_surface)
        mode_800_button.draw(options_surface)
        mode_1440_button.draw(options_surface)
        mode_1920_button.draw(options_surface)
        back_button.draw(options_surface)

        # Проверка наведения на кнопки
        slider.update(mouse_options_pos)
        pygame.mixer.music.set_volume(slider.value / 100)
        sett.volume = slider.value

        back_button.check_hover(mouse_options_pos)
        mode_800_button.check_hover(mouse_options_pos)
        mode_1440_button.check_hover(mouse_options_pos)
        mode_1920_button.check_hover(mouse_options_pos)

        pygame.display.flip()

def records_menu():
    global main_window, menu_background, x_center

    # surface for data and controls
    records_surface = pygame.Surface((450, 550), pygame.SRCALPHA)
    records_surface.fill(LIGHT_GOLDEN_YELLOW)
    records_surface_rect = records_surface.get_rect()
    records_surface_rect.center = main_window.get_rect().center

    # controls
    back_button = Button(125, 450, 200, 50, font_button, "BACK", LIGHT_BLUE, WHITE)

    # get table of the records from DB
    data = get_results()
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_records_pos = (
            mouse_pos[0] - records_surface_rect.x,
            mouse_pos[1] - records_surface_rect.y
        )
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.is_clicked(mouse_records_pos, event):
                running = False
        
        # Отрисовка
        main_window.blit(menu_background, (0, 0))

        # Отрисовка текста с рекордами (обязательно ДО отрисовки его поверхности)
        print_text('Table of the records', font_type='fonts/robotomono.ttf', 
                    font_size=35, y=20, surface=records_surface)
        counter = 100
        max_text_lenght = 20
        for (count, (item)) in enumerate(data):
            dots = '.' * (max_text_lenght - len(item[0]) - len(str(item[1])))
            print_text(f'{count + 1}. {item[0]}{dots}{item[1]}', 
                            font_type='fonts/robotomono.ttf', x=20, y=counter, surface=records_surface)
            counter += 65
        
        main_window.blit(records_surface, records_surface_rect)
        
        # Отрисовка кнопок
        records_surface.fill(LIGHT_GOLDEN_YELLOW)
        back_button.draw(records_surface)

        # Проверка наведения на кнопки
        back_button.check_hover(mouse_records_pos)
        
        pygame.display.flip()

def run_game():
    # sounds and music
    pygame.mixer.music.load('sounds/Arcade_Kid.mp3')
    pygame.mixer.music.play(-1)

    # ground line Y coordinate
    ground = sett.display_height - 100
    
    # zombi creating
    zombi = AnimatedItemJump('images/Runner_game_', 10, 90, 110, 0.07, ground)
    zombi.rect.bottomleft = (sett.display_widht // 3, ground)
    zombi_group = Group(zombi)

    # cactus objects creating
    cactus_images = [f'images/cactus_0{x}.png' for x in range(1, 8)]
    cactus_group = Group()

    # cloud objects creating
    cloud_group = Group()

    # sun object creating
    sun = AnimatedItem('images/sun_', 12, 140, 140, 0.1)
    sun.rect.topright = (sett.display_widht, 0)
    sun_group = Group(sun)

    # mountain object creating
    if sett.display_widht == 800:
        mountain = StaticItem('images/background_mountain.png', 800, 499, speed=0.5)
    elif sett.display_widht == 1440:
        mountain = StaticItem('images/background_mountain.png', 1440, 799, speed=0.5)
    elif sett.display_widht == 1920:
        mountain = StaticItem('images/background_mountain.png', 1920, 979, speed=0.5)
        
    mountain.rect.topleft = (0, 0)
    mountain_group = Group(mountain)

    # scores start value
    scores = 0
    
    # timers for object creating
    last_spawn_time = 0
    last_cloud_time = 0
    
    running = True
    while running:
        
        current_time = pygame.time.get_ticks()

        # if right-top corner cross was pressed - close the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # if Space key was pressed - zombi jumps
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            zombi.jump()

        # if Escape key was pressed - game paused
        if keys[pygame.K_ESCAPE]:
            pause_game()

        # main window background re-drawing
        if sett.display_widht == 800:
            main_window.blit(background, (0, 0))
        elif sett.display_widht == 1440:
            main_window.blit(background_1440, (0, 0))
        elif sett.display_widht == 1920:
            main_window.blit(background_1920, (0, 0))

        # mountain drawing
        mountain_group.update()
        mountain_group.draw(main_window)

        # scores and FPS showing
        print_text(f'Scores: {scores}', font_size=40, x=100, y=sett.display_height - 70)
        print_text(f'FPS: {int(clock.get_fps())}', x=80, y=10)

        # cactus creating and drawing
        if current_time - last_spawn_time > random.randint(70, 300) * (1000 / sett.FPS):
            next_cactus = StaticItem(random.choice(cactus_images), 
                                random.randint(40, 60), random.randint(50, 90))
            next_cactus.rect.bottomleft = (sett.display_widht, ground)
            cactus_group.add(next_cactus)
            last_spawn_time = current_time

        cactus_group.update()
        cactus_group.draw(main_window)

        # sun drawing
        sun_group.update()
        sun_group.draw(main_window)

        # cloud creating and drawing
        if current_time - last_cloud_time > random.randint(300, 500) * (1000 / sett.FPS):
            next_cloud = StaticItem('images/cloud_3.png', 
                                random.randint(90, 300), random.randint(50, 90), speed=2)
            next_cloud.rect.topleft = (sett.display_widht, random.randint(70, 150))
            cloud_group.add(next_cloud)
            last_cloud_time = current_time

        cloud_group.update()
        cloud_group.draw(main_window)

        # zombi drawing
        zombi_group.update()
        zombi_group.draw(main_window)

        if pygame.sprite.spritecollide(zombi, cactus_group, False, pygame.sprite.collide_mask):
            pygame.mixer.music.stop()
            game_over(scores)
        
        for cactus in cactus_group:
            if not hasattr(cactus, 'scored') and cactus.rect.right <= zombi.rect.left:
                scores += 1
                cactus.scored = True  # Помечаем как учтённый
        
        # display updating
        
        pygame.display.update()
        
        clock.tick(sett.FPS) 

main_menu()
