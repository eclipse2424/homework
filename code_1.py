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

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stage 1")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# 폰트 설정
small_font = pygame.font.SysFont("Arial", 24)

# 플레이어 체력 예시
player_health = 100


# 전투 시스템 함수
def battle(player, enemy):
    turn = "player" if player.agility >= enemy.agility else "enemy"
    log = []  # 행동 로그 리스트
    turn_counter = 1  # 턴 카운터

    # 전투 시작 시 배경 이미지 로드
    battle_background_image_path = "C:/Users/bagja/TextMafia42/"
    battle_background_image = pygame.image.load("Lobby.webp")

    while player.is_alive() and enemy.is_alive():
        # 배경 이미지 그리기
        screen.blit(battle_background_image, (0, 0))

        # 상태 표시
        turn_text = small_font.render(f"Turn: {turn_counter}", True, BLACK)
        screen.blit(turn_text, (10, 10))
        draw_health_bar(player, 120, 10)  # 플레이어 체력 위치 수정
        draw_health_bar(enemy, (SCREEN_WIDTH - 200) // 2, 200)  # 상대 체력 위치

        # 상대 캐릭터 이미지 표시 (임시 박스로 대체)
        pygame.draw.rect(screen, GRAY, ((SCREEN_WIDTH - 120) // 2, 100, 120, 80))

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
                        time.sleep(2)  # 2초 대기

                        # 상대의 행동 처리
                        if enemy.is_alive():
                            damage, _ = enemy.attack_enemy(player)
                            player.take_damage(damage)
                            log.append(f"Enemy attacks for {damage} damage.")
                            turn = "player"
                            turn_counter += 1

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

    if player.is_alive():
        log.append("Victory!")
    else:
        log.append("Defeat...")


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
                    player = Character("Player", 150, 10, 10, 10, 10)
                    enemy = Character("Enemy", 80, 15, 5, 5, 5)
                    battle(player, enemy)
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

        pygame.time.Clock().tick(60)

# 대기 화면 시작
show_wait_screen()

