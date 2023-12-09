import pygame, sys
from pygame.locals import *
import random, time
import os


pygame.init()

# 초당 프레임 설정
FPS = 60
FramePerSec = pygame.time.Clock()

# 색상 세팅(RGB코드)
RED = (255, 0, 0)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SEAGREEN = (60, 179, 113)
BLUE = (0, 51, 255)
BLUE2 = (0, 51, 153)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (204, 153, 255)
PINK = (255, 153, 153)

GREY = (213,213,213)
LIGHT_GREY = (246,246,246)
LIGHT_BLACK = (76,76,76)
# 게임 진행에 필요한 변수들 설정
SPEED = 5  # 게임 진행 속도
SCORE = 0  # 플레이어 점수

# 폰트 설정
font = pygame.font.Font('DNFBitBitv2.ttf', 45)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.Font('DNFBitBitv2.ttf', 18)#,bold=True)  # 작은 사이즈 폰트(폰트2)
middle_font = pygame.font.Font('DNFBitBitv2.ttf', 40) # 중간 사이즈 폰트(폰트3)
game_over = font.render("GG", True, BLACK)  # 게임 종료시 문구


# 게임 화면 생성 및 설정
display_width = 700
display_height = 500
GameDisplay = pygame.display.set_mode((display_width,display_height))
GameDisplay.fill(PINK)
pygame.display.set_caption("CAU Game")

# 게임 배경화면
background = pygame.image.load('background.jpg')  # 배경화면 사진 로드
background = pygame.transform.scale(background, (display_width, display_height))  # 배경화면 크기 조정



#버튼 생성 함수
def button(msg,x,y,w,h,ic,ac,action=None,fcolor=BLUE):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.ellipse(GameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            return True
    else:
        pygame.draw.ellipse(GameDisplay, ic,(x,y,w,h))

    textSurf = middle_font.render(msg,True,fcolor)
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    GameDisplay.blit(textSurf, textRect)


# 텍스트생성 및 get_rect 함수
def text_objects(text, font1, color=BLACK):  # 기본 색은 검정색
    textSurface = font1.render(text, True, color)  # color 변수를 적용하여 텍스트 색상 설정
    return textSurface, textSurface.get_rect()

# 시작(intro) 화면
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 배경화면 사진 게임창에 불러오기(사진, 위치)
        GameDisplay.blit(background, (0, 0)) #TODO
        # 텍스트 생성 및 배치하기
        large_Text = pygame.font.Font('DNFBitBitv2.ttf', 65)
        Text1,Text1Rect = text_objects("우당탕탕 대학생활",large_Text,color=BLUE2)
        Text2,Text2Rect = text_objects("How to Play",font)
        Text3,Text3Rect = text_objects("커피와 A+학점은 플레이어의 속도를 증가시켜줘요!",small_font)
        Text4,Text4Rect = text_objects("방향키 ← , →를 사용하여 과제와 F학점을을 피하세요!",small_font)
        Text1Rect.center = ((display_width/2),(display_height/5.3))
        Text2Rect.center = ((display_width/2),(display_height/2.9))
        Text3Rect.center = ((display_width/2),(display_height/2.1))
        Text4Rect.center = ((display_width/2),(display_height/1.8))
        GameDisplay.blit(Text1, Text1Rect)
        GameDisplay.blit(Text2,Text2Rect)
        GameDisplay.blit(Text3,Text3Rect)
        GameDisplay.blit(Text4,Text4Rect)
        #start,quit버튼
        introBtn1 = button("START",display_width/5.8,display_height/1.5,200,100,BLUE2,BLUE,action=True,fcolor=WHITE)
        introBtn2 = button("QUIT",display_width/1.8,display_height/1.5,200,100,BLUE2,RED,action=True,fcolor=WHITE) 
        #TODO: 버튼 누르면 동작
        if introBtn1 == True:
            return game()
        if introBtn2 ==True:
            pygame.quit()
            quit()
        pygame.display.update()
        FramePerSec.tick(FPS)

#score reset
def reset():
    global SCORE
    SCORE = 0
    return SCORE

## 게임 내에서 동작할 클래스 설정 ##

## 플레이어에게 적용할 클래스
class Player(pygame.sprite.Sprite):
    # 플레이어 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('puang.png')
        
        self.image = pygame.transform.scale(self.image, (70, 90))  # 너비와 높이를 조정해주세요
        self.rect = self.image.get_rect()
        # 이미지 시작 위치 설정
        self.rect.center = (540, 430)
        #시작 속도설정
        self.speed = 2

    # 플레이어 키보드움직임 설정 함수
    def move(self):
        prssdKeys = pygame.key.get_pressed()
        # 왼쪽 방향키를 누르면 5만큼 왼쪽 이동
        if self.rect.left > 0:
            if prssdKeys[K_LEFT]:
                self.rect.move_ip(-self.speed, 0)
                position_p = self.rect.center
                return position_p
        # 오른쪽을 누르면 5만큼 오른쪽으로 이동
        if self.rect.right < 700:
            if prssdKeys[K_RIGHT]:
                self.rect.move_ip(self.speed, 0)
                position_p = self.rect.center
                return position_p


## 적에게 적용할 클래스
class Enemy(pygame.sprite.Sprite):

    # 적의 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 적 사진 불러오기
        self.image = pygame.image.load('f.png')
       
        # 크기 조정(충돌판정 이미지에 맞추기 위함)
        self.image = pygame.transform.scale(self.image, (40, 50))
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # 이미지 시작 위치 설정
        self.rect.center = (random.randint(30, 600), 0)

    # 적의 움직임 설정 함수+ 플레이어 점수 측정
    def move(self):
        global SCORE

        # 적을 10픽셀크기만큼 위에서 아래로 떨어지도록 설정
        self.rect.move_ip(0, SPEED)  # x,y좌표 설정
        # 이미지 가 화면 끝에 있으면(플레이어가 물체를 피하면) 다시 이미지 위치 세팅 + 1점 추가
        if (self.rect.bottom > 440):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 600), 0)
        return self.rect.center

#적 추가
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 적 사진 불러오기
        self.image = pygame.image.load('book.png')
       
        # 크기 조정(충돌판정 이미지에 맞추기 위함)
        self.image = pygame.transform.scale(self.image, (50, 40))
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # 이미지 시작 위치 설정
        self.rect.center = (random.randint(30, 600), 0)

    def move(self):
        global SCORE
        # 적의 움직임 설정 + 플레이어 점수 측정
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 440):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 600), 0)
        return self.rect.center

#아이템 설정
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coffee.png')  # 아이템 이미지 불러오기
        
        # 아이템 이미지 크기 조정
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, 600), 0)  # 시작 위치 설정

    def move(self):
        self.rect.move_ip(0, SPEED)  # 아이템 아래로 이동

        # 아이템이 화면 아래로 나가면 다시 위로 시작하도록 설정
        if self.rect.bottom > 440:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 600), 0)
        return self.rect.center
    


class Item2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('A.png')  # 아이템 이미지 불러오기
        
        # 아이템 이미지 크기 조정
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, 600), 0)  # 시작 위치 설정

    def move(self):
        self.rect.move_ip(0, SPEED)  # 아이템 아래로 이동

        # 아이템이 화면 아래로 나가면 다시 위로 시작하도록 설정
        if self.rect.bottom > 440:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 600), 5)
        return self.rect.center


###### 게임 설정 ########
# 플레이어 및 적 개체 생성
def game(speed = SPEED):

    P1 = Player()

    E1 = Enemy()

    E2 = Enemy2()

    I1 = Item()

    I2 = Item2()
    
    # Sprites Groups 생성하기
    # 게임 물체들을 그룹화 하여 그룹별로 접근하여 설정 시 용이하게 만들기
    # 적(enemy) 객체 그룹화하기
    Enemies = pygame.sprite.Group()
    Enemies.add(E1)
    Enemies.add(E2)

    Items = pygame.sprite.Group()
    Items.add(I1)
    Items.add(I2)
    # 전체 그룹을 묶기
    All_groups = pygame.sprite.Group()
    All_groups.add(P1)
    All_groups.add(E1)
    All_groups.add(E2)
    All_groups.add(I1)
    All_groups.add(I2)

    # 적 개체 1초(1000ms)마다 새로 생기는 이벤트 생성
    increaseSpeed = pygame.USEREVENT + 1
    pygame.time.set_timer(increaseSpeed, 1000)

   
    ## 게임 루프 설정 ##
    # 게임 종료되기 전까지 실행되는 루프(이벤트) 설정
    while True:
        for event in pygame.event.get():
            # type increaseSpeed이면 속도 증가하여 어렵게 만듬(적 물체 이벤트)
            if event.type == increaseSpeed:
                speed += 0.5

            # 아이템과 플레이어의 충돌 검사
            if pygame.sprite.spritecollideany(P1, Items):
                P1.speed += 1  # 플레이어 속도 증가
                I1.rect.top = 0
                I1.rect.center = (random.randint(30, 610), 0)
            # 이벤트가 종료되면 게임도 종료시킴
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 배경화면 사진 게임창에 불러오기(사진, 위치)
        GameDisplay.blit(background, (0, 0))
        # 하단부에 위치할 스코어 점수(적을 피할때마다 +1점 증가)
        scores = small_font.render("Score: " + str(SCORE), True, BLACK)
        GameDisplay.blit(scores, (10, 470))

        # group1 = '<Player Sprite(in 1 groups)>'
        # group2 = '<Enemy Sprite(in 2 groups)>'

        # 게임 내 물체 움직임 생성
        for i in All_groups:
            GameDisplay.blit(i.image, i.rect)
            i.move()
            if str(i) == '<Player Sprite(in 1 groups)>':
                player_pos = i
            else:
                enemy_pos = i

        # <Player Sprite(in 1 groups)>
        # 플레이어 충돌 판정(게임종료)시
        if pygame.sprite.spritecollideany(P1, Enemies):
            for i in All_groups:
                i.kill()
            # 물체 이미지 변경(충돌후 변경되는 이미지)
            # 플레이어
            GameDisplay.blit(background, (0, 0))
            image0 = pygame.image.load('puang2.png')
            image0 = pygame.transform.scale(image0, (70,90))
            GameDisplay.blit(image0, player_pos)

            # 충격효과
            image1 = pygame.image.load('wow.png')
            image1 = pygame.transform.scale(image1, (70, 50))
            GameDisplay.blit(image1,(P1.rect.center[0], P1.rect.center[1] - image1.get_height()*1.3))
            pygame.display.update()

            
            
            pygame.display.update()
            game_outro()

        pygame.display.update()
        # 초당 프레임 설정
        FramePerSec.tick(FPS)
        
## 게임오버 페이지
def game_outro():
    outro = True

    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        GameDisplay.blit(background, (0, 0))
        final_scores = font.render("Your Score: " + str(SCORE), True, BLACK)
        Music = small_font.render("Opensource Programing",True,BLACK)
        Photos = small_font.render("CAU",True,BLACK)
        Madeby = small_font.render("20232486 이류희",True,BLACK)
        GameDisplay.blit(final_scores, (180, 120))
        GameDisplay.blit(game_over, (320, 190))
        GameDisplay.blit(Music,(10,445))
        GameDisplay.blit(Photos,(10,420))
        GameDisplay.blit(Madeby,(10,470))
        #retry,quit버튼
        outroBtn1 = button("RETRY",display_width/5.8,display_height/1.7,200,100,BLUE2,BLUE,action=True,fcolor=WHITE)
        outroBtn2 = button("QUIT",display_width/1.8,display_height/1.7,200,100,BLUE2,RED,action=True,fcolor=WHITE)
        #TODO: 버튼 누르면 동작
        if outroBtn1 == True:
            reset()
            game()
        if outroBtn2 ==True:
            pygame.quit()
            sys.exit()
        pygame.display.update()
        FramePerSec.tick(FPS)


#####게임 시작#####
game_intro()
