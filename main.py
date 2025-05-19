import pygame
import sys
import random
import time

# pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("42City")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 폰트 설정
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
middle_font = pygame.font.Font(None, 25)
storyfont= pygame.font.Font(None, 18)

# 배경 이미지 로드 (이미지 파일 경로 설정)
background_image_path = "C:/Users/bagja/TextMafia42/"
background_image = pygame.image.load("startscreen.jpg")
lobby_background_image_path = "C:/Users/bagja/TextMafia42/"
lobby_background_image = pygame.image.load("Lobby.webp")

# 게임 대기화면에 필요한 변수들
blink_time = 500  # 깜빡임 간격 (밀리초)
last_blink_time = pygame.time.get_ticks()
blinking = True

bgm_files = ["C:/Users/bagja/Text Mafia42/music/startscreenbgm.mp3"]
bgm_index = 0  # 현재 BGM 인덱스

def play_bgm():
    global bgm_index
    pygame.mixer.music.load(bgm_files[bgm_index])  # BGM 파일 로드
    pygame.mixer.music.play(-1, 0.0)  # 무한 반복 재생

pygame.mixer.init()  # 믹서 초기화
play_bgm()

# 캐릭터 클래스
class Character:
    def __init__(self, name, max_health, attack, defense, agility, crit_chance):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.crit_chance = crit_chance  # 치명타 확률 (0-100%)
        self.is_defending = False

    def take_damage(self, damage):
        if self.is_defending:
            damage = max(damage - self.defense, 0)
        else:
            damage = max(damage, 0)
        self.health = max(self.health - damage, 0)
        return damage

    def is_alive(self):
        return self.health > 0

    def attack_enemy(self, enemy):
        if random.randint(1, 100) <= self.crit_chance:
            damage = self.attack * 2  # 치명타
            return damage, True
        else:
            damage = self.attack
        return damage, False

# 체력 바 그리기 함수
def draw_health_bar(character, x, y, width=200, height=20):
    health_ratio = character.health / character.max_health
    pygame.draw.rect(screen, GRAY, (x, y, width, height))  # 배경 바
    pygame.draw.rect(screen, RED, (x, y, width * health_ratio, height))  # 체력 바
    health_text = small_font.render(f"{character.health}/{character.max_health}", True, BLACK)
    text_rect = health_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(health_text, text_rect)

# 전투 시스템 함수
def battle(player, enemy):
    turn = "player" if player.agility >= enemy.agility else "enemy"
    log = []  # 행동 로그 리스트
    turn_counter = 1  # 턴 카운터

    # 전투 시작 시 배경 이미지 로드
    battle_background_image_path = "C:/Users/bagja/TextMafia42/"
    battle_background_image = pygame.image.load("Lobby.webp")
    enemy_image_path = "C:/Users/bagja/TextMafia42/"  # 상대 이미지 로드
    enemy_image = pygame.image.load("beast.png")

    # 이미지 비율 조정 (예: 33% 크기로 줄이기)
    enemy_image = pygame.transform.scale(enemy_image, (enemy_image.get_width() // 6, enemy_image.get_height() // 6))

    while player.is_alive() and enemy.is_alive():
        # 배경 이미지 그리기
        screen.blit(battle_background_image, (0, 0))

        # 상태 표시
        turn_text = small_font.render(f"Turn: {turn_counter}", True, BLACK)
        screen.blit(turn_text, (10, 10))
        draw_health_bar(player, 120, 10)  # 플레이어 체력 위치 수정
        draw_health_bar(enemy, (SCREEN_WIDTH - 200) // 2, 200)  # 상대 체력 위치

        # 상대 캐릭터 이미지 표시 (왼쪽 상단으로 이동)
        screen.blit(enemy_image, (130, 50))  # 상대 이미지를 왼쪽 상단에 위치시킴

        # 행동 로그 표시 영역 그리기
        log_area = pygame.Rect(10, 360, 338, 100)  # 로그 영역 설정
        pygame.draw.rect(screen, (200, 200, 200), log_area)  # 회색으로 채우기

        # 행동 로그 표시 (최대 5개만 표시)
        for i, log_entry in enumerate(log[-5:]):
            log_text = small_font.render(log_entry, True, BLACK)
            screen.blit(log_text, (10, 360 + i * 20))

        # 버튼 생성
        attack_button = pygame.Rect(20, 500, 100, 40)
        defend_button = pygame.Rect(130, 500, 100, 40)
        run_button = pygame.Rect(240, 500, 100, 40)
        pygame.draw.rect(screen, GRAY, attack_button)
        pygame.draw.rect(screen, GRAY, defend_button)
        pygame.draw.rect(screen, GRAY, run_button)

        screen.blit(small_font.render("Attack", True, WHITE), attack_button.move(10, 10))
        screen.blit(small_font.render("Defend", True, WHITE), defend_button.move(10, 10))
        screen.blit(small_font.render("Run", True, WHITE), run_button.move(10, 10))

        # 화면 업데이트
        pygame.display.flip()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == "player":
                    if attack_button.collidepoint(event.pos):
                        damage, is_crit = player.attack_enemy(enemy)
                        enemy.take_damage(damage)
                        if is_crit:
                            log.append(f"Player's critical hit! {damage} damage!")
                        else:
                            log.append(f"Player attacks for {damage} damage.")

                        # 플레이어 공격 후 상대 체력 업데이트
                        pygame.display.flip()
                        time.sleep(1)  # 1초 대기

                        # 상대의 행동 처리
                        if enemy.is_alive():
                            damage, _ = enemy.attack_enemy(player)
                            player.take_damage(damage)
                            log.append(f"Enemy attacks for {damage} damage.")
                            turn = "player"
                            turn_counter += 1
                        else:
                            # 상대 처치 시 능력치 상승
                            stat_increase = int(enemy.attack * 0.3)  # 상대의 공격력 30%
                            player.attack += stat_increase
                            player.defense += stat_increase
                            player.max_health += stat_increase
                            player.health = min(player.health + stat_increase, player.max_health)  # 체력 회복
                            log.append(f"You defeated the enemy! Your stats increased by {stat_increase}.")

                    elif defend_button.collidepoint(event.pos):
                        player.is_defending = True
                        log.append("Player is defending.")
                        turn = "enemy"

                        # 플레이어 행동 후 상대 행동 처리
                        if enemy.is_alive():
                            pygame.display.flip()
                            time.sleep(2)  # 2초 대기 후 상대 행동

                            damage, _ = enemy.attack_enemy(player)
                            player.take_damage(damage)
                            log.append(f"Enemy attacks for {damage} damage.")
                            turn = "player"
                            turn_counter += 1

                    elif run_button.collidepoint(event.pos):
                        log.append("Player ran away!")
                        return
# 체력이 0이 될 경우
    if not player.is_alive():
        # 배경 변경
        game_over_background_path ="C:/Users/bagja/TextMafia42/"
        game_over_background = pygame.image.load("backstreet.webp")
        screen.blit(game_over_background, (0, 0))

        # 게임 오버 메시지 출력
        game_over_text = small_font.render("You could not stop their plans.", True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(game_over_text, text_rect)

        # Retry 버튼 생성
        retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 20, 150, 40)
        pygame.draw.rect(screen, GRAY, retry_button)
        retry_text = small_font.render("Retry", True, WHITE)
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 25))

        pygame.display.flip()

        # 이벤트 처리
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        run_stages()  # 스테이지 1로 돌아가기
                        return

    if player.is_alive():
        log.append("Victory!")
    else:
        log.append("Defeat...")

# 스테이지 함수
def stage(player, stage_number, enemy_name, enemy_health, enemy_attack, enemy_defense, enemy_agility, enemy_crit_chance, story_text_1, story_text_2):
    enemy = Character(enemy_name, enemy_health, enemy_attack, enemy_defense, enemy_agility, enemy_crit_chance)

    while True:
        # 배경 이미지 그리기
        screen.fill(WHITE)
        screen.blit(lobby_background_image, (0, 0))

        # 스테이지 표시
        stage_text = small_font.render(f"Stage {stage_number}/5", True, BLACK)
        screen.blit(stage_text, (10, 10))

        # 플레이어 체력 표시
        health_text = small_font.render(f"Health: {player.health}", True, BLACK)
        screen.blit(health_text, (10, 40))

        # 스토리 텍스트 표시
        story_text_1_rendered = small_font.render(story_text_1, True, BLACK)
        story_text_2_rendered = small_font.render(story_text_2, True, BLACK)
        screen.blit(story_text_1_rendered, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40))
        screen.blit(story_text_2_rendered, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 10))

        # 버튼 생성
        enter_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 20, 150, 40)
        pygame.draw.rect(screen, GRAY, enter_button)
        button_text = small_font.render("Enter the alley", True, WHITE)
        screen.blit(button_text, (SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 + 25))

        # 화면 업데이트
        pygame.display.flip()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button.collidepoint(event.pos):
                    battle(player, enemy)  # 전투 씬으로 이동
                    if player.is_alive():  # 전투 후 플레이어가 살아있으면 다음 스테이지로 이동
                        return
                    else:
                        sys.exit()  # 플레이어가 패배하면 종료

# 각 스테이지를 호출하는 함수
def run_stages():
    player = Character("Player", 150, 13, 0, 10, 10)
    initial_health = player.health  # 초기 체력 저장

    # 스테이지 정보 (이름, 체력, 공격력, 방어력, 민첩성, 치명타 확률, 스토리 텍스트)
    stages = [
        ("Enemy 1", 50, 12, 5, 5, 5, "A scream was heard from the alley.", "Did I hear it wrong?"),
        ("Enemy 2", 60, 13, 7, 6, 6, "You enter a darker alley.", "What awaits you here?"),
        ("Enemy 3", 70, 14, 9, 7, 7, "You hear whispers in the shadows.", "Is someone watching you?"),
        ("Enemy 4", 80, 15, 11, 8, 18, "The atmosphere grows tense.", "You feel a presence nearby."),
        ("Enemy 5", 100, 16, 13, 10, 10, "The final challenge awaits.", "Can you overcome this trial?")
    ]

    for stage_number, (enemy_name, enemy_health, enemy_attack, enemy_defense, enemy_agility, enemy_crit_chance, story_text_1, story_text_2) in enumerate(stages, start=1):
        stage(player, stage_number, enemy_name, enemy_health, enemy_attack, enemy_defense, enemy_agility, enemy_crit_chance, story_text_1, story_text_2)
        
        # 스테이지 클리어 시 체력 회복
        if player.is_alive():
            health_lost = initial_health - player.health  # 잃은 체력 계산
            recovery_amount = health_lost // 2  # 잃은 체력의 절반 회복
            player.health = min(player.health + recovery_amount, player.max_health)  # 체력 회복
            initial_health = player.health  # 현재 체력 업데이트
        else:
            break  # 플레이어가 죽으면 루프 종료

        if stage_number == 5 and player.is_alive():  # 스테이지 5 클리어 후
            # 배경 변경
            victory_background_path = "C:/Users/bagja/TextMafia42/"
            victory_background = pygame.image.load("victory.webp")
            screen.blit(victory_background, (0, 0))

            # 승리 메시지 출력
            victory_text = storyfont.render("You have preserved the peace of the city!", True, BLACK)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(victory_text, text_rect)

            # New Game 버튼 생성
            new_game_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 20, 150, 40)
            pygame.draw.rect(screen, GRAY, new_game_button)
            new_game_text = small_font.render("New Game", True, WHITE)
            screen.blit(new_game_text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 25))

            pygame.display.flip()

            # 이벤트 처리
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if new_game_button.collidepoint(event.pos):
                            run_stages()  # 새로운 게임 시작
                            waiting_for_input = False  # 입력 대기 종료

# 대기 화면 함수
def show_wait_screen():
    global blinking, last_blink_time

    # 대기화면 루프
    while True:
        screen.fill(WHITE)
        
        # 배경 이미지 그리기
        screen.blit(background_image, (0, 0))
        
        # "touch to start" 문구 깜빡이기
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_time:
            blinking = not blinking
            last_blink_time = current_time
        
        if blinking:
            text = font.render("Touch to Start", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        # 화면 업데이트
        pygame.display.flip()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 마우스 왼쪽 버튼 클릭 시
                    run_stages()  # 스테이지 실행
                    return

# 로비 화면 함수
def show_lobby_screen():
    while True:
        # 로비 배경 이미지 그리기
        screen.blit(lobby_background_image, (0, 0))

        # 로비 제목 텍스트
        title_text = font.render("42City", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # 버튼 생성 (게임 시작 버튼)
        button_rect = pygame.Rect(100, 300, 160, 50)
        pygame.draw.rect(screen, WHITE, button_rect)
        button_text = small_font.render("Start Game", True, BLACK)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        # 화면 업데이트
        pygame.display.flip()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    print("게임이 시작됩니다!")
                    run_stages()  # 스테이지 실행
                    return

# 대기 화면 함수
def show_wait_screen():
    global blinking, last_blink_time

    # 대기화면 루프
    while True:
        screen.fill(WHITE)
        
        # 배경 이미지 그리기
        screen.blit(background_image, (0, 0))
        
        # "touch to start" 문구 깜빡이기
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_time:
            blinking = not blinking
            last_blink_time = current_time
        
        if blinking:
            text = font.render("Touch to Start", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        # 화면 업데이트
        pygame.display.flip()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 마우스 왼쪽 버튼 클릭 시
                    show_lobby_screen()  # 로비 화면으로 이동
                    return

# 대기 화면 시작
show_wait_screen()