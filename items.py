import pygame
from pygame.sprite import Sprite, Group
from colors import BLACK, GRAY, BLUE, WHITE, LIGHT_BLUE, RED


# Создаем класс для не анимированных объектов
class StaticItem(Sprite):
    def __init__(self, image_path, target_width, target_height, speed=5):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (target_width, target_height))
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0: # pygame.display.get_surface().get_rect().left
            self.kill()

# Создаем класс для анимированных объектов
class AnimatedItem(Sprite):
    def __init__(self, path_prefix: str, sprite_amount: int, target_width: int, target_height: int, anim_speed: float):
        super().__init__()
        # Загрузка изображений для анимации
        temp = [pygame.image.load(f'{path_prefix}{x}.png').convert_alpha() for x in range(1, sprite_amount + 1)]
        self.frames = [pygame.transform.scale(x, (target_width, target_height)) for x in temp]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.animation_speed = anim_speed  # Скорость анимации
        self.last_update = pygame.time.get_ticks()

    def update(self):
        # Обновление кадра анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class AnimatedItemJump(AnimatedItem):
    def __init__(self, path_prefix: str, sprite_amount: int, target_width: int, target_height: int, anim_speed: float, ground: int):
        super().__init__(path_prefix, sprite_amount, target_width, target_height, anim_speed)
        self.velocity_y = 0  # Скорость по вертикали
        self.jumping = False  # В прыжке ли персонаж
        self.gravity = 1  # Гравитация
        self.jump_speed = -22  # Начальная скорость прыжка (вверх)
        self.ground = ground
    
    def update(self):
        # Обновление кадра анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        
        # Гравитация (постоянное ускорение вниз)
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Проверка "на земле" (чтобы нельзя было прыгать в воздухе)
        if self.rect.bottom >= self.ground:
            self.rect.bottom = self.ground
            self.velocity_y = 0
            self.jumping = False
    
    def jump(self):
        if not self.jumping:  # Прыгать можно только с земли
            self.velocity_y = self.jump_speed
            self.jumping = True

class Button:
    def __init__(self, x, y, width, height, font, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_rect = self.font.get_rect(self.text)
        text_rect.center = self.rect.center
        self.font.render_to(surface, text_rect.topleft, self.text, fgcolor=BLACK)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Slider:
    def __init__(self, x, y, width, height, font, min_val=0, max_val=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.knob_rect = pygame.Rect(x + width // 2 - 7, y - 8, 14, height + 16)
        self.min = min_val
        self.max = max_val
        self.value = 50  # Начальное значение (50%)
        self.dragging = False
        

    def update(self, mouse_pos):
        mouse_pos = mouse_pos
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Проверка нажатия на ползунок
        if mouse_pressed and self.knob_rect.collidepoint(mouse_pos):
            self.dragging = True

        # Перетаскивание ползунка
        if self.dragging:
            if mouse_pressed:
                self.knob_rect.x = max(self.rect.x, min(mouse_pos[0] - 10, self.rect.x + self.rect.width - 20))
                self.value = int(((self.knob_rect.x - self.rect.x) / (self.rect.width - 20)) * (self.max - self.min) + self.min)
            else:
                self.dragging = False

    def draw(self, surface):
        # Отрисовка линии слайдера
        pygame.draw.rect(surface, LIGHT_BLUE, self.rect, border_radius=5)
        # Отрисовка ползунка
        pygame.draw.rect(surface, BLACK if not self.dragging else LIGHT_BLUE, self.knob_rect, border_radius=5)
        # Текст над ползунком
        text_rect = self.font.get_rect(f"VOLUME: {self.value}%")
        text_rect.centerx = self.rect.centerx
        text_rect.y = self.rect.y - 50
        self.font.render_to(surface, text_rect.topleft, f"VOLUME: {self.value}%", fgcolor=BLACK)
