# main.py

import pygame
from settings import *
from sprites import create_sprite_groups
from levels import LevelManager
from score import ScoreManager


pygame.init()
# сам экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")

score_manager = ScoreManager()
level_manager = LevelManager()

# очки
score_manager.load_scores()

# текст на экр
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# старт экр
def show_start_screen():
    screen.fill(BLUE)
    draw_text(screen, "Doodle Jump", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, "Нажмите любую клавишу, чтобы начать", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

# финал экр
def show_game_over_screen(score):
    screen.fill(BLUE)
    draw_text(screen, "Игра окончена", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, f"Ваш результат: {score}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Нажмите любую клавишу, чтобы выйти", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    pygame.display.flip()
    wait_for_key()

# Ожидание нажатия клавиши
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

# основной игровой цикл
def main_game():
    # группы спрайтов
    player_group, platform_group = create_sprite_groups()
    player = next(iter(player_group))  # объект игрока
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        
        # события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        # обновление объектов
        player_group.update()
        platform_group.update()

        # столкновения игрока с платформами
        hits = pygame.sprite.spritecollide(player, platform_group, False)
        if hits and player.vel_y > 0:  # Столкновение с платформой только если игрок падает
            player.rect.bottom = hits[0].rect.top
            player.vel_y = JUMP_STRENGTH

        # обновление уровня и счета
        level_manager.calculate_score(player)
        level_manager.update_level(player_group, platform_group)

        screen.fill(BLUE)
        player_group.draw(screen)
        platform_group.draw(screen)
        draw_text(screen, f"Очки: {level_manager.total_score}", 20, 50, 10)
        draw_text(screen, f"Уровень: {level_manager.current_level}", 20, SCREEN_WIDTH - 100, 10)
        pygame.display.flip()


        if player.rect.top > SCREEN_HEIGHT:
            running = False

    return level_manager.total_score


def main():
    show_start_screen()
    while True:
        score = main_game()
        score_manager.save_score("Player", score)
        show_game_over_screen(score)

if __name__ == "__main__":
    main()
