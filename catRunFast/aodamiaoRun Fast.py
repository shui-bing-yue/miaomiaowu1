# -*- coding: utf-8 -*-

import sys, time, random, math, pygame,locale
from pygame.locals import *
from MyLibrary import *

# 重置火箭函数
def reset_arrow():
    y = random.randint(270,350) # 产生随机整数 设置炮弹高度
    arrow.position = 800,y
    bullent_sound.play_sound()

# 定义一个滚动地图类
class MyMap(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bg = pygame.image.load("background.png").convert_alpha() # 可支持透明
    def map_rolling(self):
        if self.x < -300:
            self.x = 300
        else:
            self.x -=5
    def map_update(self):
        screen.blit(self.bg, (self.x,self.y))
    def set_pos(self,x,y):
        self.x =x
        self.y =y
# 定义一个按钮类
class Button(object):
    def __init__(self, upimage, downimage,position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.position = position
        self.game_start = False
        
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos() # 这个函数会返回鼠标当前的坐标x,y；
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position
        
        if self.isOver():
            screen.blit(self.imageDown, (x-w/2,y-h/2))
        else:
            screen.blit(self.imageUp, (x-w/2, y-h/2))
    def is_start(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                self.game_start = True
                bg_sound.play_pause()
                btn_sound.play_sound()
                bg_sound.play_sound()

def replay_music():
    bg_sound.play_pause()
    bg_sound.play_sound()

#定义一个数据IO的方法
def data_read():
    fd_1 = open("data.txt","r")
    best_score = fd_1.read()
    fd_1.close()
    return best_score

   
# 定义一个控制声音的类和初始音频的方法
def audio_init():
    global hit_au,btn_au,bg_au,bullent_au # 定义全局变量
    pygame.mixer.init()  # 启动mixer 声音模块   游戏中对声音的处理一般包括制造声音和播放声音两部分
    hit_au = pygame.mixer.Sound("exlposion.wav")  # 调用Sound对象
    btn_au = pygame.mixer.Sound("button.wav")   # .wav
    bg_au = pygame.mixer.Sound("background.ogg")
    bullent_au = pygame.mixer.Sound("bullet.wav")
class Music():
    def __init__(self,sound):
        self.channel = None
        self.sound = sound     
    def play_sound(self):
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(0.5)
        self.channel.play(self.sound)
    def play_pause(self):
        self.channel.set_volume(0.0)
        self.channel.play(self.sound)


# 主程序部分

pygame.init()  # 初始化pygame 启动6个函数
audio_init()  # 初始化游戏声音
screen = pygame.display.set_mode((800,600),0,32)  # 设置主屏幕大小
pygame.display.set_caption("嗷大喵快跑！")
font = pygame.font.Font(None, 22)  # 创建一个font对象 （字体名，大小）
font1 = pygame.font.Font(None, 40)
framerate = pygame.time.Clock()  # 创建一个对象来帮助跟踪时间
upImageFilename = 'game_start_up.png'
downImageFilename = 'game_start_down.png' # 点击开始游戏的图片
# 创建按钮对象
button = Button(upImageFilename,downImageFilename, (400,500))
interface = pygame.image.load("interface.png")

#创建地图对象
bg1 = MyMap(0,0)
bg2 = MyMap(300,0)
# 创建一个精灵组
group = pygame.sprite.Group()
group_exp = pygame.sprite.Group()
group_fruit = pygame.sprite.Group()
# 创建怪物精灵
dragon = MySprite()
dragon.load("dragon.png", 260, 150, 3)
dragon.position = 100, 230
group.add(dragon)

# 创建爆炸动画
explosion = MySprite()
explosion.load("explosion.png",128,128,6)
# 创建玩家精灵
player = MySprite()
player.load("sprite.png", 100, 100, 4)
player.position = 400, 270  # 270 表示 人物高度
group.add(player)

# 创建子弹精灵
arrow = MySprite()
arrow.load("flame.png", 40, 16, 1)
arrow.position = 800,320
group.add(arrow)


# 定义一些变量
arrow_vel = 10.0 #
game_over = False
you_win = False
player_jumping = False
jump_vel = 0.0
player_start_y = player.Y
player_hit = False
monster_hit = False
p_first = True
m_first = True
best_score = 0
global bg_sound,hit_sound,btn_sound,bullent_sound
bg_sound=Music(bg_au)
hit_sound=Music(hit_au)
btn_sound=Music(btn_au)
bullent_sound =Music(bullent_au)
game_round = {1:'ROUND ONE',2:'ROUND TWO',3:'ROUND THREE',4:'ROUND FOUR',5:'ROUND FIVE'}
game_pause = True
index =0
current_time = 0
start_time = 0
music_time = 0
score =0
replay_flag = True
#循环
bg_sound.play_sound() # 自动取得一个空闲的通道（没有音效正在播放的通道）。
best_score = data_read()
while True:
    framerate.tick(60) # 每秒循环60次
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():  # 用于循环的退出
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()  # 获得所有键盘按钮的状态
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    elif keys[K_SPACE]:
        if not player_jumping:
            player_jumping = True
            jump_vel = -12.0 # 跳的高度

#加载刚开始的页面
    screen.blit(interface,(0,0)) # 把一幅图像画在另一幅上（复制）
    button.render()
    button.is_start()   #  游戏开始
    if button.game_start == True:
        if game_pause :
            index +=1
            tmp_x =0
            if score >int (best_score):
                best_score = score
            fd_2 = open("data.txt","w+")
            fd_2.write(str(best_score))
            fd_2.close()
            #判断游戏是否通关
            if index == 6:
                you_win = True
            # 游戏通关后页面显示的内容
            if you_win:
                #在第一次调用的时候，返回的是程序运行的实际时间；
                #以第二次之后的调用，返回的是自第一次调用后,到这次调用的时间间隔
                start_time = time.perf_counter()
                current_time =time.perf_counter()-start_time
                while current_time<5:
                    screen.fill((200, 200, 200)) # 方法传入一个颜色值将颜色填充到整个对象
                    print_text(font1, 270, 150,"YOU WIN THE GAME!",(240,20,20))
                    current_time =time.perf_counter()-start_time
                    print_text(font1, 320, 250, "Best Score:",(120,224,22))
                    print_text(font1, 370, 290, str(best_score),(255,0,0))
                    print_text(font1, 270, 330, "This Game Score:",(120,224,22))
                    print_text(font1, 385, 380, str(score),(255,0,0))
                    pygame.display.update()
                pygame.quit()
                sys.exit()

            # 在游戏中添加加分的蓝条
            for i in range(0,100):
                element = MySprite()
                element.load("fruit.bmp", 35, 20, 20)  # 加分项
                tmp_x += random.randint(50,120)
                element.X = tmp_x + 300
                element.Y = random.randint(80, 200)
                group_fruit.add(element)
            start_time = time.perf_counter()
            current_time =time.perf_counter()-start_time

            while current_time<3:
                screen.fill((200, 200, 200))
                print_text(font1, 320, 250,game_round[index],(240,20,20))
                pygame.display.update()
                game_pause = False
                current_time =time.perf_counter()-start_time

        else:
            #更新子弹
            if not game_over:
                arrow.X -= arrow_vel #
            if arrow.X < -40: reset_arrow()
            #碰撞检测，子弹是否击中玩家
            # pygame.sprite.collide_rect() 两个精灵间的矩形冲突检测
            if pygame.sprite.collide_rect(arrow, player):
                reset_arrow()
                explosion.position =player.X,player.Y
                player_hit = True
                hit_sound.play_sound()
                if p_first:
                    group_exp.add(explosion)
                    p_first = False
                player.X -= 10  # 人物 位置减10

            # 碰撞检测，子弹是否击中怪物
            if pygame.sprite.collide_rect(arrow, dragon):
                reset_arrow()
                explosion.position =dragon.X+50,dragon.Y+50
                monster_hit = True
                hit_sound.play_sound()
                if m_first:
                    group_exp.add(explosion)
                    m_first = False
                dragon.X -= 10

            # 碰撞检测，玩家是否被怪物追上
            if pygame.sprite.collide_rect(player, dragon):
                game_over = True
            # 遍历果实，使果实移动
            for e in group_fruit:
                e.X -=5
            # 调用这个函数的时候，一个组中的所有精灵都会逐个地 pygame.sprite.spritecollide
            # 对另外一个单个精灵进行冲突检测，
            # 发生冲突的精灵会作为一个列表返回。
            # 这个函数的第一个参数就是单个精灵，第二个参数是精灵组，
            # 第三个参数是一个bool值，最后这个参数起了很大的作用。
            # 当为True的时候，会删除组中所有冲突的精灵，False的时候不会删除冲突的精灵
            collide_list = pygame.sprite.spritecollide(player,group_fruit,True)
            score +=len(collide_list)
            # 是否通过关卡
            if dragon.X < -100:
                game_pause = True
                reset_arrow()
                player.X = 400
                dragon.X = 100



            #检测玩家是否处于跳跃状态
            if player_jumping:
                if jump_vel <0:
                    jump_vel += 0.6
                elif jump_vel >= 0:
                    jump_vel += 0.8
                player.Y += jump_vel
                if player.Y > player_start_y:
                    player_jumping = False
                    player.Y = player_start_y
                    jump_vel = 0.0


            #绘制背景
            bg1.map_update()
            bg2.map_update()
            bg1.map_rolling()
            bg2.map_rolling()

            #更新精灵组
            if not game_over:
                group.update(ticks, 60)
                group_exp.update(ticks,60)
                group_fruit.update(ticks,60)
            #循环播放背景音乐
            music_time = time.perf_counter()
            if music_time   > 150 and replay_flag:
                replay_music()
                replay_flag =False
            #绘制精灵组
            group.draw(screen)
            group_fruit.draw(screen)
            if player_hit or monster_hit:
                group_exp.draw(screen)
            print_text(font, 330, 560, "press SPACE to jump up!")
            print_text(font, 200, 20, "You have get Score:",(219,224,22))
            print_text(font1, 380, 10, str(score),(255,0,0))
            if game_over:
                start_time = time.perf_counter()
                current_time =time.perf_counter()-start_time
                while current_time<5:
                    screen.fill((200, 200, 200))
                    print_text(font1, 300, 150,"GAME OVER!",(240,20,20))
                    current_time =time.perf_counter()-start_time
                    print_text(font1, 320, 250, "Best Score:",(120,224,22))
                    if score >int (best_score):
                        best_score = score
                    print_text(font1, 370, 290, str(best_score),(255,0,0))
                    print_text(font1, 270, 330, "This Game Score:",(120,224,22))
                    print_text(font1, 370, 380, str(score),(255,0,0))
                    pygame.display.update()
                fd_2 = open("data.txt","w+")
                fd_2.write(str(best_score))
                fd_2.close()
                pygame.quit()
                sys.exit()
    pygame.display.update() #刷新屏幕内容显示，稍后使用
