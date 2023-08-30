# 모듈 호출 및 초기화
import pygame, sys, random
pygame.init()
clock = pygame.time.Clock()

def img_load(obj):
    img = pygame.image.load('resources/'+str(obj)+'.png') # 이미지 로드
    img_size = img.get_rect().size
    return img, img_size[0], img_size[1] # 이미지, 가로 길이, 세로 길이

#화면 설정
width = 480 # 가로 크기
height = 640 # 세로 크기
pad = pygame.display.set_mode((width, height)) # 화면 크기설정
pygame.display.set_caption('Shooting Game')

#배경 설정
bg = img_load('bg')[0] # 배경 이미지 로드

#전투기 그리기
p, pw, ph = img_load('fighter01') # 전투기 이미지 로드
px = width * 0.45 # 전투기 X좌표
py = height * 0.85 # 전투기 Y좌표
ps = 0 # 전투기 속도

#운석 그리기
rlist = ['rock01', 'rock02', 'rock03', 'rock04', 'rock05', 'rock06', 'rock07', 'rock08', 'rock09']
r, rw, rh = img_load(random.choice(rlist)) # 운석 이미지 로드
rx = random.randint(0, width - rw) # 운석의 x좌표
ry = 0
rs = 5 # 운석 속도

def rock_init():
    global r, rw, rh, rx, ry
    r, rw, rh = img_load(random.choice(rlist)) # 운석 이미지 랜덤 로드
    rx = random.randint(0, width - rw) # 운석의 랜덤 x좌표
    ry = 0

#미사일 설정
m, mw, mh = img_load('missile') # 미사일 이미지 로드
mx = px + pw / 2 - mw / 2 # 미사일의 초기 x좌표
my = py - mh # 미사일의 초기 y좌표
mlist = [] # 미사일 여러 개 담을 리스트

#충돌 이미지 설정
exp = img_load('explosion')[0]

pad.blit(bg, (0, 0))
pad.blit(p, (px, py))
pad.blit(r, (200, 0))

pygame.display.update()

#게임 실행 코드
while True:
    for event in pygame.event.get(): # 이벤트 탐색
        if event.type == pygame.QUIT: # 종료 이벤트 감지
            pygame.quit() # pygame 종료
            sys.exit() # 창 종료
        if event.type in [pygame.KEYDOWN]: # 키 다운 감지
            if event.key == pygame.K_LEFT: # 왼쪽 화살표 다운
                ps = -5 # 왼쪽으로 이동
            elif event.key == pygame.K_RIGHT: # 오른쪽 화살표 다운
                ps = 5 # 오른쪽으로 이동
            elif event.key == pygame.K_SPACE: # 스페이스 키 다운
                mx = px + pw / 2 - mw / 2 # 미사일 x좌표
                my = py - mh # 미사일 y좌표
                mlist.append([mx, my]) # 발사한 미사일을 리스트에 추가
        # if event.type in [pygame.KEYUP]: # 키 업 감지
        #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # 왼쪽 또는 오른쪽 화살표 업
        #         ps = 0 # 전투기 멈춤

    px += ps # 전투기 속도만큼 이동. for문 밖에 있음. 위치 중요!
    if px < 0:
        px = 0 # 전투기가 왼쪽을 벗어나면 x좌표를 0으로 고정
    elif px > width - pw:
        px = width - pw # 전투기가 오른쪽을 벗어나면 x좌표를 width - pw로 고정
    pad.blit(bg, (0, 0)) # 배경 그리기
    pad.blit(p, (px, py)) # 전투기 그리기

    ry += rs # 운석 떨어뜨리기
    if ry > height:
        rock_init() # 랜덤 운석 초기화
    pad.blit(r, (rx, ry)) # 바위 그리기

    # 전투기와 운석 충돌 체크
    if(py < ry + rh) and (px < rx + rw) and (px + pw > rx):
        pad.blit(exp, (rx, ry)) # 충돌 이미지 그리기
        rock_init() # 랜덤 운석 초기화

    if len(mlist) != 0: # 미사일 리스트가 비어있지 않으면
        for mis in mlist:
            mis[1] -= 10 # 미사일이 전진함
            if (mis[1] < ry + rh) and (mis[0] < rx + rw) and (mis[0] + mw > rx):
                mlist.remove(mis) # 미사일을 리스트에서 제거
                pad.blit(exp, (rx, ry)) # 충돌 이미지 그리기
                rock_init() # 랜덤 운석 초기화
            elif mis[1] < 0 - mh: # 미사일의 꼬리가 화면을 벗어나면
                mlist.remove(mis) # 미사일을 리스트에서 제거
            pad.blit(m, (mis[0], mis[1])) # 미사일 그리기
    pygame.display.update()
    clock.tick(50)