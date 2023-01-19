from email.mime import image
from tkinter.tix import CELL
from turtle import position, speed
import pygame
import os

#버블 클래스 만들기
class Bubble(pygame.sprite.Sprite):
    def __init__(self,image,color,position,angle):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center = position)
        self.angle = angle

class Pointer (pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = image
        
        self.rect = image.get_rect(center = position)
        self.original_image = image = 10
        
    def rotate(self,angle):
        self.angle += angle
        #각도 조정
        if self.angle + angle > 170:
            self.angle = 170
        if self.angle + angle < 10:
            self.angle = 10
        
        
    def draw(self,screen):
        screen.blit(self.image,self.rect)
#스테이지 별로 맵 만들기
def setup():
    global map
    map = [
           #["R","R","Y","Y","B"...]
           list("RRYYBBGG"),
           list("RRYYBBG/"), #/는 버블이 위치 할 수 없는 곳 이라는 의미
           list("BBGGRRYY"),
           list("BGGRRYY/"),
           list("........"),
           list("......./"),
           list("........"),
           list("......./"),
           list("........"), 
           list("......./"),
           list("........")
           ]
    for row_idx,row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col == "." or col == "/":
                continue
            position = get_bubble_postion(row_idx,col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image,col,position))
            
def get_bubble_postion(row_idx,col_idx):
    #x좌표는 col_idx * cell_size + bubble_width//2
    #y좌표는 row_idx * cell_size + bubble_height//2
    # + 홀수 인덱스면 x += cell_size//2
    pos_x = col_idx * CELL_SIZE + BUBBLE_WIDTH//2
    pos_y = row_idx * CELL_SIZE + BUBBLE_HEIGHT//2
    if row_idx % 2 == 1:
        pos_x += CELL_SIZE//2
    return pos_x, pos_y
    
def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "B":
        return bubble_images[1]
    elif color == "Y":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:
        return bubble_images[-1]
    
    
    
pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Puzzle Bobble")
clock = pygame.time.Clock()


current_path = os.path.dirname(__file__)
#배경
background = pygame.image.load(os.path.join(current_path,"background.png"))

bubble_images = [
    pygame.image.load(os.path.join(current_path,"red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path,"blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path,"yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path,"green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path,"purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path,"black.png")).convert_alpha()
]
pointer_image = pygame.image.load(os.path.join(current_path,"pointer.png"))
pointer = Pointer(pointer_image, (screen_width//2,624),90)
#게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62

#화살표 관련 변수   
to_angle = 0
angle_speed = 1.5
map = []

bubble_group = pygame.sprite.Group()
setup()

running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle += speed
            elif event.key == pygame.K_RIGHT:
                to_angle -= speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle = 0
            elif event.key == pygame.K_RIGHT:
                to_angle = 0
        
    screen.blit(background,(0,0))
    bubble_group.draw(screen)
    pointer.rotate(to_angle)
    pointer.draw(screen)
    pygame.display.update()
    
    
    
pygame.quit()