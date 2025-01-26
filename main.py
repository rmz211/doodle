import pygame
from settings import *
from sprites import create_sprite_groups, Player
# from levels import LevelManager
from score import ScoreManager
# import os

pygame.init()

# окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Только вверх!")
clock = pygame.time.Clock()

# фон
background = pygame.image.load(BACKGROUND_IMAGE)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# функция отображения текста
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(UI_FONT, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# стартовое окно
def show_start_screen():
    screen.fill(BLUE)
    draw_text(screen, "Только Вверх!", 60, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 4, TEXT_COLOR)
    draw_text(screen, "Выберите уровень сложности:", 40, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, TEXT_COLOR)
    draw_text(screen, "1 - Легкий, 2 - Средний, 3 - Сложный", 30, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 1.8, TEXT_COLOR)
    pygame.display.flip()
    return wait_for_level_choice()

# ожидание выбора уровня
def wait_for_level_choice():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy", 3
                elif event.key == pygame.K_2:
                    return "medium", 2
                elif event.key == pygame.K_3:
                    return "hard", 1

# финальное окно
def show_game_over_screen(score):
    screen.fill(BLUE)
    draw_text(screen, "Игра окончена!", 60, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 4, TEXT_COLOR)
    draw_text(screen, f"Ваш результат: {score}", 40, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, TEXT_COLOR)
    draw_text(screen, "Нажмите любую клавишу для выхода", 30, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 1.5, TEXT_COLOR)
    pygame.display.flip()
    wait_for_key()

# ожидание нажатия клавиши
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

# основной игровой процесс
def main_game(level, lives):
    player_group, platform_group = create_sprite_groups(level)
    player = next(iter(player_group))
    score_manager = ScoreManager()
    score = 0

    running = True
    while running:
        clock.tick(FPS)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_a:
                    player.move_left()
                if event.key == pygame.K_d:
                    player.move_right()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    player.stop()
                

        # обновление объектов
        player_group.update()
        platform_group.update()

        # проверка столкновений
        hits = pygame.sprite.spritecollide(player, platform_group, False)
        if hits and player.vel_y > 0:
            player.rect.bottom = hits[0].rect.top
            player.vel_y = JUMP_STRENGTH

        # перемещение экрана вверх
        if player.rect.top <= SCREEN_HEIGHT // 4:
            player.rect.y += abs(player.vel_y)
            for platform in platform_group:
                platform.rect.y += abs(player.vel_y)
                if platform.rect.top > SCREEN_HEIGHT:
                    platform_group.remove(platform)
                    new_platform = platform.generate_new()
                    platform_group.add(new_platform)

        # смерть персонажа
        if player.rect.top > SCREEN_HEIGHT:
            lives -= 1
            if lives <= 0:
                running = False
            else:
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # рисование
        screen.blit(background, (0, 0))
        platform_group.draw(screen)
        player_group.draw(screen)

        # отображение счёта и жизней
        score += 1
        draw_text(screen, f"Счет: {score}", 30, 10, 10, TEXT_COLOR)
        draw_text(screen, f"Жизни: {lives}", 30, 10, 50, TEXT_COLOR)
        draw_text(screen, f"Рекорд: {score_manager.get_high_score()}", 30, 10, 90, TEXT_COLOR)

        pygame.display.flip()

    score_manager.save_score(score)
    return score

# основной запуск
def main():
    level, lives = show_start_screen()
    score = main_game(level, lives)
    show_game_over_screen(score)

if __name__ == "__main__":
    main()
