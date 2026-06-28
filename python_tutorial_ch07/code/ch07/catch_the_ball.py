"""catch_the_ball.py — 最简单的 Pygame 小游戏：接住下落的小球

核心概念：
窗口、事件循环、键盘输入、碰撞检测、状态更新和即时反馈。
"""
import pygame
import random

# ============================================================
# 第 1 步：初始化 Pygame
# ============================================================
pygame.init()                            # 打开 Pygame 的"总开关"
WIDTH, HEIGHT = 600, 500                 # 窗口宽和高（像素）
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # 创建游戏窗口
pygame.display.set_caption("接球小游戏 — Pygame 入门")  # 窗口标题
clock = pygame.time.Clock()              # 时钟，控制游戏刷新速度
font = pygame.font.SysFont("simhei", 32) # 字体，用于显示文字
big_font = pygame.font.SysFont("simhei", 48)

# ============================================================
# 第 2 步：设置游戏状态（变量记录一切）
# ============================================================
player_x = 250        # 挡板的 x 坐标（左上角）
ball_x = random.randint(50, 550)   # 小球的 x 坐标（随机）
ball_y = 50           # 小球的 y 坐标
score = 0             # 得分
lives = 3             # 剩余生命
speed = 5             # 小球下落速度（每帧像素数）
running = True        # 主循环是否继续
game_over = False     # 游戏是否结束

# ============================================================
# 第 3 步：游戏主循环（每秒钟重复约 60 次）
# ============================================================
while running:
    # ------ 3a. 事件处理：侦测玩家的操作 ------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:          # 点×关闭窗口
            running = False

        # 游戏结束后按 R 键重新开始
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # 重置所有游戏状态
                player_x = 250
                ball_x = random.randint(50, 550)
                ball_y = 50
                score = 0
                lives = 3
                speed = 5
                game_over = False

    # ------ 3b. 游戏逻辑更新 ------
    if not game_over:
        # 读取键盘状态（左右方向键控制挡板）
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 7                     # 向左移动
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 100:
            player_x += 7                     # 向右移动

        # 小球下落
        ball_y += speed

        # 球落地了（没接住）
        if ball_y > HEIGHT:
            lives -= 1                        # 扣一条命
            ball_x = random.randint(50, 550)  # 新球出现在顶部
            ball_y = 50
            if lives <= 0:
                game_over = True              # 生命归零，游戏结束

        # 碰撞检测：球碰到挡板了吗？
        if (ball_y > HEIGHT - 35 and
            player_x < ball_x < player_x + 100):
            score += 1                        # 加分
            ball_x = random.randint(50, 550)  # 新球
            ball_y = 50
            if score % 5 == 0:                # 每得 5 分加速一次
                speed += 1

    # ------ 3c. 绘制画面 ------
    screen.fill((30, 30, 60))                 # 用深蓝色清空画面

    # 画小球（圆形）
    pygame.draw.circle(screen, (255, 200, 50),
                       (ball_x, int(ball_y)), 15)

    # 画挡板（矩形）
    pygame.draw.rect(screen, (100, 200, 255),
                     (player_x, HEIGHT - 25, 100, 20))

    # 显示分数和生命值
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 140, 10))

    # 游戏结束画面
    if game_over:
        over_text = big_font.render("Game Over!", True, (255, 80, 80))
        tip_text = font.render("Press R to Restart", True, (200, 200, 200))
        screen.blit(over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
        screen.blit(tip_text, (WIDTH // 2 - 130, HEIGHT // 2 + 20))

    # 把画好的内容真正显示到屏幕上
    pygame.display.flip()

    # 控制帧率：每秒最多 60 帧
    clock.tick(60)

# ============================================================
# 第 4 步：退出清理
# ============================================================
pygame.quit()
