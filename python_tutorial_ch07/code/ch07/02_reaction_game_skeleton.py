"""A minimal pygame reaction-game skeleton."""
try:
    import pygame
except ImportError:
    print("请先安装 pygame：python -m pip install pygame")
    raise SystemExit

pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("关键词反应小游戏")
clock = pygame.time.Clock()
running = True
score = 0
last_key = "等待按键"


def get_font(size: int, bold: bool = False):
    for path in [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]:
        try:
            return pygame.font.Font(path, size)
        except FileNotFoundError:
            continue
    return pygame.font.SysFont(None, size)


title_font = get_font(34, bold=True)
word_font = get_font(72, bold=True)
small_font = get_font(24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            last_key = f"刚才按下：{key_name}"
            if event.key == pygame.K_SPACE:
                score += 10
            print("按键：", key_name, "当前得分：", score)

    screen.fill((245, 248, 252))
    pygame.draw.rect(screen, (255, 255, 255), (70, 55, 660, 360), border_radius=28)
    pygame.draw.rect(screen, (216, 224, 236), (70, 55, 660, 360), width=2, border_radius=28)

    title = title_font.render("关键词反应小游戏", True, (22, 32, 51))
    screen.blit(title, (110, 92))

    prompt = small_font.render("看到目标词时按 Space；先把窗口、事件、刷新跑通。", True, (82, 96, 113))
    screen.blit(prompt, (110, 145))

    word = word_font.render("BLUE", True, (47, 107, 255))
    screen.blit(word, (110, 218))

    hint = small_font.render(last_key, True, (36, 160, 107))
    screen.blit(hint, (110, 335))

    score_text = small_font.render(f"Score: {score}", True, (232, 76, 97))
    screen.blit(score_text, (585, 335))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
