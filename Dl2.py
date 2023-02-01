import pygame, time, sys, math, random

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

#
#BLOCK SETTING IS BROKEN A BIT
#

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
ROSE=(253,10,245)
BLUE=(26,102,255)
PURPLE=(204,0,204)
YELLOW=(255,255,0)


dev_mode=False
#intro=True

pygame.display.set_caption('platformer')
window_size=screenX,screenY=1366,768
window=pygame.display.set_mode(window_size,pygame.RESIZABLE)
FPS=70
fpsClock=pygame.time.Clock()

x,y=0,0
mousex,mousey=0,0
pygame.mouse.set_visible(False)

leg1=pygame.image.load('resources/leg1.png')
body=pygame.image.load('resources/body.png')
head=pygame.image.load('resources/head.png')
pistol=pygame.image.load('resources/pistol1.png')
sword=pygame.image.load('resources/blade12.png')
wall_image=pygame.image.load('resources/wall.png')
plat_image=pygame.image.load('resources/plat.png')
heart=pygame.image.load('resources/heart.png')
box=pygame.image.load('resources/box.png')

smallfont=pygame.font.Font('resources/kongtext.ttf',20)
medfont=pygame.font.Font('resources/kongtext.ttf',30)
largefont=pygame.font.Font('resources/kongtext.ttf',60)

sword_hit=pygame.mixer.Sound('resources/sword_hit.wav')
pistol_shot=pygame.mixer.Sound('resources/pistol_shot3.wav')
main_theme=pygame.mixer.Sound('resources/main_theme.wav')
powerup=pygame.mixer.Sound('resources/powerup.wav')
menu_bg=pygame.mixer.Sound('resources/menu_bg.wav')
death_sound=pygame.mixer.Sound('resources/death.wav')
got_damage=pygame.mixer.Sound('resources/damage.wav')
victory1=pygame.mixer.Sound('resources/victory1.wav')
victory2=pygame.mixer.Sound('resources/victory2.wav')

menu_bg.set_volume(0.1)
pistol_shot.set_volume(0.1)
sword_hit.set_volume(0.1)
main_theme.set_volume(0.03)
powerup.set_volume(0.1)
death_sound.set_volume(0.5)
got_damage.set_volume(0.1)
victory1.set_volume(0.5)
victory2.set_volume(0.5)

SCORE=0

#game rectangles
hero=pygame.Rect(100,100,30,90)
hero.center=screenX/2,screenY/2

bullet_rect=pygame.Rect(0,0,6,6)
bullet_rect.center=screenX/2,screenY/2

#hitboxes
speedx=3
speedy=6
hb_left=pygame.Rect(screenX/2-hero.width/2-(speedx*2),screenY/2-hero.height/2-speedy,speedx*2,hero.height-speedy)
hb_top=pygame.Rect(screenX/2-hero.width/2,screenY/2-hero.height/2-(speedy*2),hero.width,speedy)
hb_right=pygame.Rect(screenX/2+hero.width/2,screenY/2-hero.height/2-speedy,speedx*2,hero.height-speedy)
hb_bottom=pygame.Rect(screenX/2-hero.width/2,screenY/2+hero.height/2-speedy*2,hero.width,speedy+1)
hb_hero=pygame.Rect(100,100,30,95)

right_ledge_hb=pygame.Rect(hero.x+36, hero.y,-8,-10)
left_ledge_hb=pygame.Rect(hero.x, hero.y,-8,-10)

hitboxes=[]
hitboxes.append(hb_left);hitboxes.append(hb_top);hitboxes.append(hb_right);hitboxes.append(hb_bottom)
walls=[]
platforms=[]

def pause():
    pause_k=0
    pau=[]
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pause_k-=1
                if event.key == pygame.K_DOWN:
                    pause_k+=1
                if event.key == pygame.K_SPACE and pause_k==0:
                    paused=False
                if event.key == pygame.K_SPACE and pause_k==1:
                    settings_func()
                if event.key == pygame.K_SPACE and pause_k==2:
                    pygame.quit()
                    quit()

        window.fill(BLACK)
        t0=message_to_screen('Continue',WHITE,50,'medium');pau.append(t0)
        t1=message_to_screen('SETTINGS',WHITE,100,'medium');pau.append(t1)
        t2=message_to_screen('Quit the GAME',WHITE,200,'medium');pau.append(t2)

        if pause_k>=3:pause_k=0
        elif pause_k<=-1:pause_k=2

        for indx,i in enumerate(pau):
            if indx==pause_k:
                rec=pygame.Rect(0,0,8,8)
                rec.right=i.left-10
                rec.centery=i.centery
                pygame.draw.rect(window,WHITE,rec)
                break
                pau=[]
        message_to_screen('PAUSE',WHITE,-200,size='medium')
        pygame.display.update()
        fpsClock.tick(10)
        
main_menu=True
def game_intro():
    global SCORE, main_menu, damage_push, HEALTH, walls, plats, plxright, plydown, plxleft, plyup, globalx, globaly, hero, screen_shaking, intro
    menu=[];menu_k=0
    music=True
    while main_menu:
        if music==True:
            menu_bg.play(loops=-1)
            music=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_k-=1
                elif event.key == pygame.K_DOWN:
                    menu_k+=1
                elif event.key == pygame.K_SPACE and menu_k==0:
                    menu_bg.stop()
                    main_menu=False
                    HEALTH=1
                    SCORE=0
                    if choosen_level=='level1':
                        for i in walls+ plats+ plxright+ plydown+ plxleft+ plyup+topleft_points+ topright_points:
                            i.x-=1600+globalx
                            i.y-=-1000+globaly
                        globalx=-1600
                        globaly=1000
                        hero.center=screenX/2,screenY/2
                        screen_shaking=False
                        damage_push=False
                        if dev_mode==False:
                            intro=True
                        lvl1Enemies()
                elif event.key == pygame.K_SPACE and menu_k==1:
                    controls()
                elif event.key == pygame.K_SPACE and menu_k==2:
                    settings_func()
                elif event.key == pygame.K_SPACE and menu_k==3:
                    credits_def()
                elif event.key == pygame.K_SPACE and menu_k==4:
                    pygame.quit()
                    quit()

        window.fill(BLACK)
        t0=message_to_screen('PLAY',WHITE,0,'medium');menu.append(t0)
        t1=message_to_screen('CONTROLS',WHITE,50,'medium');menu.append(t1)
        t2=message_to_screen('SETTINGS',WHITE,100,'medium');menu.append(t2)
        t3=message_to_screen('CREDITS',WHITE,150,'medium');menu.append(t3)
        t4=message_to_screen('QUIT',WHITE,250,'medium');menu.append(t4)

        if menu_k>=5:menu_k=0
        elif menu_k<=-1:menu_k=4

        for indx,i in enumerate(menu):
            if indx==menu_k:
                rec=pygame.Rect(0,0,8,8)
                rec.right=i.left-10
                rec.centery=i.centery
                pygame.draw.rect(window,WHITE,rec)
                break
                menu=[]
        message_to_screen('Welcome to the game!',WHITE,-250,'medium')
        message_to_screen('Dl2',(random.randint(0,255),random.randint(0,255),random.randint(0,255)),-150,'large')
        pygame.display.update()
        fpsClock.tick(15)

sound_k=4
def settings_func():
    settings_menu=True;settings_k=0;settings=[]
    fscreen=True
    global window, sound_k
    while settings_menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    settings_k-=1
                if event.key == pygame.K_DOWN:
                    settings_k+=1
                if event.key == pygame.K_LEFT and settings_k==1:
                    sound_k-=1
                if event.key == pygame.K_RIGHT and settings_k==1:
                    sound_k+=1
                if event.key == pygame.K_SPACE and settings_k==0:
                    if fscreen==True:window=pygame.display.set_mode(window_size);fscreen=False
                    elif fscreen==False:window=pygame.display.set_mode(window_size,pygame.FULLSCREEN);fscreen=True
                if event.key == pygame.K_SPACE and settings_k==2:
                    settings_menu=False;main_menu=True
                    
        window.fill(BLACK)
        t0=message_to_screen('TOGGLE FULLSCREEN',WHITE,-100,'small');settings.append(t0)
        if sound_k<0:sound_k=0
        elif sound_k>9:sound_k=9
        t1=message_to_screen('SOUND         <'+str(sound_k)+'>',WHITE,-50,'small');settings.append(t1)
        t2=message_to_screen('BACK',WHITE,250,'medium');settings.append(t2)
        
        message_to_screen('SETTINGS',WHITE,-250,'medium')
        if settings_k>=3:settings_k=0
        elif settings_k<=-1:settings_k=2

        for indx,i in enumerate(settings):
            if indx==settings_k:
                rec=pygame.Rect(0,0,8,8)
                rec.right=i.left-10
                rec.centery=i.centery
                pygame.draw.rect(window,WHITE,rec)
                break
                settings=[]

        menu_bg.set_volume(0.025*sound_k)
        pistol_shot.set_volume(0.025*sound_k)
        sword_hit.set_volume(0.025*sound_k)
        main_theme.set_volume(0.0075*sound_k)
        powerup.set_volume(0.025*sound_k)
        death_sound.set_volume(0.175*sound_k)
        got_damage.set_volume(0.025*sound_k)
        victory1.set_volume(0.175*sound_k)
        victory2.set_volume(0.175*sound_k)
        
        pygame.display.update()
        fpsClock.tick(10)

def controls():
    cont_menu=True
    cont_k=0
    while cont_menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cont_k-=1
                if event.key == pygame.K_DOWN:
                    cont_k+=1
                if event.key == pygame.K_SPACE:
                    cont_menu=False
                    
        window.fill(BLACK)
        message_to_screen('CONTROLS',WHITE,-250,'medium')
        message_to_screen('a/d.........go left/right',WHITE,-100,'small')
        message_to_screen('SPACE................jump',WHITE,-50,'small')
        message_to_screen('CTRL...............crouch',WHITE,0,'small')
        message_to_screen('k...................sword',WHITE,50,'small')
        message_to_screen('l.....................gun',WHITE,100,'small')
        message_to_screen('ESC............pause menu',WHITE,150,'small')
        t0=message_to_screen('BACK',WHITE,250,'medium')

        rec=pygame.Rect(0,0,8,8)
        rec.right=t0.left-10
        rec.centery=t0.centery
        pygame.draw.rect(window,WHITE,rec)

        pygame.display.update()
        fpsClock.tick(10)

def credits_def():
    cred_menu=True
    cred_k=0
    while cred_menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cred_k-=1
                if event.key == pygame.K_DOWN:
                    cred_k+=1
                if event.key == pygame.K_SPACE:
                    cred_menu=False
                    
        window.fill(BLACK)
        message_to_screen('CREDITS',WHITE,-250,'medium')
        message_to_screen('I-game bg music: http://teknoaxe.com',WHITE,-50,'small')
        message_to_screen('More sounds in README file(resources)',WHITE,0,'small')
        message_to_screen('Font is also there.',WHITE,50,'small')
        t0=message_to_screen('BACK',WHITE,250,'medium')

        rec=pygame.Rect(0,0,8,8)
        rec.right=t0.left-10
        rec.centery=t0.centery
        pygame.draw.rect(window,WHITE,rec)

        pygame.display.update()
        fpsClock.tick(10)

def death():
    global main_menu, play_bg_sound
    death_k=0
    pau=[]
    died = True
    main_theme.stop()
    death_sound.play()
    while died:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    death_k-=1
                if event.key == pygame.K_DOWN:
                    death_k+=1
                if event.key == pygame.K_SPACE and death_k==0:
                    died=False;main_menu=True
                    play_bg_sound=False
                if event.key == pygame.K_SPACE and death_k==1:
                    pygame.quit()
                    quit()

        window.fill(BLACK)
        t0=message_to_screen('Quit to the Main Menu',WHITE,100,'medium');pau.append(t0)
        t1=message_to_screen('Quit the GAME',WHITE,200,'medium');pau.append(t1)

        if death_k>=2:death_k=0
        elif death_k<=-1:death_k=1

        for indx,i in enumerate(pau):
            if indx==death_k:
                rec=pygame.Rect(0,0,8,8)
                rec.right=i.left-10
                rec.centery=i.centery
                pygame.draw.rect(window,WHITE,rec)
                break
                pau=[]
        message_to_screen('YOU ARE DEAD',RED,-200,size='large')
        pygame.display.update()
        fpsClock.tick(10)

def text_objects(text,color,size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace=0, size='small',x_displace=0,xx=None):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (screenX / 2)+x_displace, (screenY / 2)+y_displace
    if xx!=None:textRect.x=xx
    window.blit(textSurf, textRect)
    return textSurf.get_rect(center=(textRect.center))

#game objects
plxright=[]
plxleft=[]
plydown=[]
plyup=[]
plats=[]
topleft_points=[]
topright_points=[]

box_objects=[]
class Box():
    def __init__(self,posx, posy, box_type, direction='left', hidden=False, difficulty='medium', distance=None):
        self.rect=pygame.Rect(posx,posy,40,40)
        self.box_type=box_type
        self.direction=direction
        self.posx=posx
        self.posy=posy-40
        self.hidden=hidden
        self.difficulty = difficulty
        self.distance=distance
    def the_box(self):
        self.rect.x=self.posx+globalx
        self.rect.y=self.posy+globaly
        if self.hidden==False:
            window.blit(box, self.rect)
    def get_rect(self):
        return self.rect
    def open_box(self):
        global heart_objects
        if self.box_type=='heart':
            heart_objects.append(Heart(self.rect.x-globalx,self.rect.y-globaly+10))
        if self.box_type=='turret':
            basic_enemies.append(Enemy(self.rect.x-globalx,self.rect.y-globaly+43,'turret', difficulty=self.difficulty,direction=self.direction, speed=4, distance=self.distance, firerate=100))

heart_objects=[]
class Heart():
    def __init__(self, posx, posy):
        self.rect=pygame.Rect(posx,posy,40,40)
        self.posx=posx
        self.posy=posy
    def heart(self):
        self.rect.x=self.posx+globalx
        self.rect.y=self.posy+globaly
        window.blit(heart, self.rect)
    def get_rect(self):
        return self.rect


def secret_block(posx, posy, sizex, sizey):
    rect=pygame.Rect(posx+globalx, posy+globaly, sizex, sizey)
    window.blit(wall_image,rect)

class Wall():
    def block(self, posx, posy, sizex, sizey):
        self.rect=pygame.Rect(posx, posy, sizex, sizey)
        window.blit(wall_image,self.rect)
        walls.append(self.rect)

class Plat():
    def block(self, posx, posy, sizex, sizey, pl=None):
        global topleft_points, topright_points
        self.rect=pygame.Rect(posx, posy, sizex, sizey)
        
        if pl==None:
            self.tl=pygame.Rect(0,0,15,speedy+1)
            self.tl.center=self.rect.topleft[0]+5,self.rect.topright[1]
            self.tr=pygame.Rect(0,0,15,speedy+1)
            self.tr.center=self.rect.topright[0]-5,self.rect.topright[1]

        topleft_points.append(self.tl)
        topright_points.append(self.tr)
        if pl==None:plats.append(self.rect);window.blit(plat_image,self.rect)
        elif pl=='plxright':plxright.append(self.rect);window.blit(wall_image,self.rect);window.blit(wall_image,(self.rect.x+30,self.rect.y));window.blit(wall_image,(self.rect.x+60,self.rect.y))
        elif pl=='plxleft':plxleft.append(self.rect);window.blit(wall_image,self.rect);window.blit(wall_image,(self.rect.x+30,self.rect.y));window.blit(wall_image,(self.rect.x+60,self.rect.y))
        elif pl=='plydown':plydown.append(self.rect);window.blit(wall_image,self.rect);window.blit(wall_image,(self.rect.x+30,self.rect.y));window.blit(wall_image,(self.rect.x+60,self.rect.y))
        elif pl=='plyup':plyup.append(self.rect);window.blit(wall_image,self.rect);window.blit(wall_image,(self.rect.x+30,self.rect.y));window.blit(wall_image,(self.rect.x+60,self.rect.y))

class Animation():
    def __init__(self,posx,posy,image,angle):
        self.angle=angle
        self.rotimage=pygame.transform.rotate(image,angle)
        self.rect=self.rotimage.get_rect(center=(posx,posy))
        #pygame.draw.rect(window,RED,self.rect)
        window.blit(self.rotimage,self.rect)
        
    def ret(self,body=None):#,angle,time):
        if self.angle<0:self.angle=360+self.angle
        if self.angle>360:self.angle=self.angle-360
        if body==None:
            if 0<=self.angle<=90:return self.rect.bottomright[0]-4, self.rect.bottomright[1]-4
            elif 90<self.angle<=180:return self.rect.topright[0]-4, self.rect.topright[1]+4
            elif 180<self.angle<=270:return self.rect.topleft[0]+4, self.rect.topleft[1]+4
            elif 270<self.angle<=360:return self.rect.bottomleft[0]+4, self.rect.bottomleft[1]-4
        elif body!=None:
            if body=='bl':return self.rect.bottomleft[0]+4, self.rect.bottomleft[1]-4
            elif body=='br':return self.rect.bottomright[0]-4, self.rect.bottomright[1]-4
            elif body=='tl':return self.rect.topleft[0]+4, self.rect.topleft[1]+4
            elif body=='tr':return self.rect.topright[0]-4, self.rect.topright[1]+4
            elif body=='mt':return self.rect.midtop
    def get_mid(self):
        return self.rect.center
    
def wall(folder,room):
    file=open('resources/'+folder+'/'+room+'.txt')
    for l in file:
        xisdone=False
        bposx=bposy=str()
        if l!='':
            for u in l:
                if u=='\n':break
                if xisdone==True:bposy+=u
                if u==' ':xisdone=True
                if xisdone==False:bposx+=u
            try:w.block(int(bposx)+globalx,int(bposy)+globaly,30,30)
            except ValueError:pass
    file.close()

def platform(folder,room):
    file=open('resources/'+folder+'/'+room+'.txt')
    for l in file:
        xisdone=False
        bposx=bposy=str()
        if l!='':
            for u in l:
                if u=='\n':break
                if xisdone==True:bposy+=u
                if u==' ':xisdone=True
                if xisdone==False:bposx+=u
            try:p.block(int(bposx)+globalx,int(bposy)+globaly,30,30)
            
            except ValueError:pass
    file.close()
def moving_platform_xright(folder,room):
    file=open('resources/'+folder+'/'+room+'.txt')
    for l in file:
        xisdone=False
        bposx=bposy=str()
        if l!='':
            for u in l:
                if u=='\n':break
                if xisdone==True:bposy+=u
                if u==' ':xisdone=True
                if xisdone==False:bposx+=u
            try:p.block(int(bposx)+globalx+pl_movex,int(bposy)+globaly,90,30,pl='plxright')
            except ValueError:pass
    file.close()
def moving_platform_xleft(folder,room):
    global plr_movey,plr_movex
    file=open('resources/'+folder+'/'+room+'.txt')
    for l in file:
        xisdone=False
        bposx=bposy=str()
        if l!='':
            for u in l:
                if u=='\n':break
                if xisdone==True:bposy+=u
                if u==' ':xisdone=True
                if xisdone==False:bposx+=u
            try:p.block(int(bposx)+globalx+plr_movex,int(bposy)+globaly,90,30,pl='plxleft')
            except ValueError:pass
    file.close()
def moving_platform_ydown(folder,room):
    global pl_movey,pl_movex
    file=open('resources/'+folder+'/'+room+'.txt')
    for l in file:
        xisdone=False
        bposx=bposy=str()
        if l!='':
            for u in l:
                if u=='\n':break
                if xisdone==True:bposy+=u
                if u==' ':xisdone=True
                if xisdone==False:bposx+=u
            try:p.block(int(bposx)+globalx,int(bposy)+globaly+pl_movey,90,30,pl='plydown')
            except ValueError:pass
    file.close()
def moving_platform_yup(folder,room):
    global plr_movey,plr_movex
    file=open('resources/'+folder+'/'+room+'.txt')
    for l in file:
        xisdone=False
        bposx=bposy=str()
        if l!='':
            for u in l:
                if u=='\n':break
                if xisdone==True:bposy+=u
                if u==' ':xisdone=True
                if xisdone==False:bposx+=u
            try:p.block(int(bposx)+globalx,int(bposy)+globaly+plr_movey,90,30,pl='plyup')
            except ValueError:pass
    file.close()
def set_platform(level,room):
    position=str(mousex-round(globalx))+' '+str(mousey-round(globaly))
    try:
        file=open('resources/'+level+'/'+room+'.txt')
        old_data=file.read()
        file.close()
        file=open('resources/'+level+'/'+room+'.txt','w')
        if old_data=='':file.write(position)
        elif old_data!='':file.write(old_data+'\n'+position)
        file.close()
    except PermissionError:pass

basic_enemies=[]
enemies_hb=[]
class Enemy():
    def __init__(self,posx,posy,enemy_type, speed=1, distance=None, direction='right', health=10, firerate=100, difficulty='medium'):
        global globalx, globaly
        self.move_k=0
        self.image=pygame.image.load('resources/'+enemy_type+'.png')
        self.direction=direction
        self.speed=speed
        self.enemy_type=enemy_type
        self.posx=posx
        self.posy=posy
        self.rect=self.image.get_rect(topleft=(posx,posy))
        self.health=health
        self.firerate=firerate
        if self.direction=='left':self.image=pygame.transform.flip(self.image,True,False)
        if enemy_type=='turret':
            if difficulty=='medium':
                self.distance=600
                self.speed=2.5
                self.firerate=250
            if difficulty=='low':
                self.distance=600
                self.speed=2.5
                self.firerate=400
            if difficulty=='high':
                self.distance=600
                self.speed=4
                self.firerate=100
        if distance!=None:self.distance=distance
        if enemy_type=='low_enemy':
            self.speed=self.speed*2
    def bad(self):
        global plats
        if self.enemy_type=='basic_enemy':
            if self.direction=='right':
                self.rect.topleft=self.posx+self.move_k+globalx,self.posy-self.rect.height+globaly
            elif self.direction=='left':
                self.rect.topleft=self.posx-self.move_k+globalx,self.posy-self.rect.height+globaly
            window.blit(self.image,self.rect)
            self.move_k+=self.speed
            if self.move_k>self.distance:self.speed=-self.speed;self.image=pygame.transform.flip(self.image,True,False)
            elif self.move_k<0:self.speed=-self.speed;self.image=pygame.transform.flip(self.image,True,False)
            
        elif self.enemy_type=='low_enemy':
            if self.direction=='right':
                self.rect.topleft=self.posx+self.move_k+globalx,self.posy-self.rect.height+globaly
            elif self.direction=='left':
                self.rect.topleft=self.posx-self.move_k+globalx,self.posy-self.rect.height+globaly
            window.blit(self.image,self.rect)
            self.move_k+=self.speed
            if self.move_k>self.distance:self.speed=-self.speed;self.image=pygame.transform.flip(self.image,True,False)
            elif self.move_k<0:self.speed=-self.speed;self.image=pygame.transform.flip(self.image,True,False)
        elif self.enemy_type=='turret':
            if self.direction=='right':
                self.rect.topleft=self.posx+globalx,self.posy-self.rect.height+globaly
                self.move_k+=self.speed
                window.blit(self.image,self.rect)
                if self.move_k>self.firerate:
                    bullet_objects.append(Bullet(self.rect.topright[0]-globalx+5,self.rect.topright[1]-globaly+3,'right',speed=self.speed, distance=self.distance))
                    self.move_k=0
            elif self.direction=='left':
                self.rect.topleft=self.posx+globalx,self.posy-self.rect.height+globaly
                self.move_k+=self.speed
                window.blit(self.image,self.rect)
                if self.move_k>self.firerate:
                    bullet_objects.append(Bullet(self.rect.topright[0]-globalx-5-self.rect.width,self.rect.topright[1]+3-globaly,'left',speed=self.speed, distance=self.distance))
                    self.move_k=0
    def get_rect(self):
        return self.rect
    def do_damage(self, damage):
        self.health-=damage
        if self.health<=0:return True

bullet_objects=[]
class Bullet():
    def __init__(self,posx, posy, direction, speed=1, distance=300):
        self.posx=posx
        self.posy=posy
        self.speed=speed
        self.rect=pygame.Rect(0,0,6,6)
        self.rect.center=self.posx+globalx,self.posy+globaly
        self.move_k=0
        self.distance=distance
        self.direction=direction
        self.ret=False
    def shoot(self):
        if self.direction=='right':
            self.rect.center=self.posx+self.move_k+globalx,self.posy+globaly
            pygame.draw.rect(window, WHITE, self.rect)
            self.move_k+=self.speed
            if self.move_k>=self.distance:self.ret=True
        if self.direction=='left':
            self.rect.center=self.posx+self.move_k+globalx,self.posy+globaly
            pygame.draw.rect(window, WHITE, self.rect)
            self.move_k-=self.speed
            if self.move_k<=-self.distance:self.ret=True
        return self.ret
    def get_rect(self):
        return self.rect

hit_objects=[]
class Hit():
    def __init__(self,posx,posy,size=None):
        self.rects=[]
        self.speed=1
        for i in range(4):
            self.u=pygame.Rect(0,0,4,4)
            self.u.center=posx,posy
            self.rects.append(self.u)
        self.k=0
    def hits(self):
##        self.rects[0].x+=self.speed*2
##        self.rects[1].x-=self.speed*2
##        self.rects[2].y+=self.speed*2
##        self.rects[3].y-=self.speed*2
        self.rects[0].x+=self.speed;self.rects[0].y+=self.speed
        self.rects[1].x-=self.speed;self.rects[1].y-=self.speed
        self.rects[2].x+=self.speed;self.rects[2].y-=self.speed
        self.rects[3].x-=self.speed;self.rects[3].y+=self.speed
        for i in self.rects:
            pygame.draw.rect(window, RED, i)
        self.k+=1
        return self.k

def lvl1Enemies():
    global box_objects, basic_enemies
    basic_enemies=[]
    box_objects=[]
    box_objects.append(Box(-710, 454,'heart','right'))
    box_objects.append(Box(-405, 454,'heart','right'))
    box_objects.append(Box(-740, -1166,'heart','right'))
    box_objects.append(Box(-190, -1526,'heart','right'))
    box_objects.append(Box(1510, -2636,'heart','right'))
    box_objects.append(Box(-760, -3356,'heart','right'))
    box_objects.append(Box(2320, 484,'heart','right'))
    box_objects.append(Box(700, -146,'heart','right',hidden=True))

    box_objects.append(Box(1520, -1106,'turret','left', difficulty='high'))
    box_objects.append(Box(40, -2816,'turret','right', difficulty='high'))
    box_objects.append(Box(40, -4946,'turret','right', difficulty='medium', distance=440))

    basic_enemies.append(Enemy(710, -4196,'basic_enemy',distance=400, direction='left'))
    basic_enemies.append(Enemy(520, -4946,'basic_enemy',distance=190, direction='right'))
    basic_enemies.append(Enemy(220, -3356,'basic_enemy',distance=490, direction='right'))
    basic_enemies.append(Enemy(40, -146,'basic_enemy',distance=310, direction='right'))
    basic_enemies.append(Enemy(870, -1106,'basic_enemy',distance=550, direction='right'))
    basic_enemies.append(Enemy(710, -1316,'basic_enemy',distance=270, direction='left'))
    basic_enemies.append(Enemy(710, -3716,'basic_enemy',distance=130, direction='left'))
    basic_enemies.append(Enemy(310, -4196,'basic_enemy',distance=400, direction='right'))
    basic_enemies.append(Enemy(1450, -2606,'basic_enemy',distance=590, direction='left'))
    basic_enemies.append(Enemy(40, -5516,'basic_enemy',distance=190, direction='right'))
    basic_enemies.append(Enemy(560, -5216,'basic_enemy',distance=190, direction='left'))
    basic_enemies.append(Enemy(190, -5786,'basic_enemy',distance=190, direction='right'))

    basic_enemies.append(Enemy(-700, -1106,'low_enemy',distance=580, direction='right'))
    basic_enemies.append(Enemy(100, -1496,'low_enemy',distance=360, direction='right'))
    basic_enemies.append(Enemy(460, -1496,'low_enemy',distance=360, direction='left'))
    basic_enemies.append(Enemy(250, -2217,'low_enemy',distance=250, direction='right'))
    basic_enemies.append(Enemy(100, -2816,'low_enemy',distance=310, direction='right'))
    basic_enemies.append(Enemy(410, -2816,'low_enemy',distance=310, direction='left'))
    basic_enemies.append(Enemy(460, -2966,'low_enemy',distance=100, direction='right'))
    basic_enemies.append(Enemy(-700, -3326,'low_enemy',distance=580, direction='right'))
    basic_enemies.append(Enemy(190, -4406,'low_enemy',distance=120, direction='right'))

    basic_enemies.append(Enemy(730, -446,'turret', direction='left', difficulty='low'))
    basic_enemies.append(Enemy(40, -596,'turret', direction='right', difficulty='medium'))
    basic_enemies.append(Enemy(40, -956,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(40, -3956,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(40, -1316,'turret', direction='right', difficulty='medium'))
    basic_enemies.append(Enemy(40, -1526,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(40, -1976,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(40, -1886,'turret', direction='right', difficulty='medium'))
    basic_enemies.append(Enemy(40, -2277,'turret', direction='right', difficulty='medium'))
    basic_enemies.append(Enemy(40, -2996,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(40, -3146,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(40, -3536,'turret', direction='right', difficulty='low'))
    basic_enemies.append(Enemy(730, -5516,'turret', direction='left', difficulty='low', distance=440))
    basic_enemies.append(Enemy(730, -3536,'turret', direction='left', difficulty='low'))


w=Wall()
p=Plat()

speed=2
choosen_level='level1'
room='room1_1'
falling=False
jumping=False
staying=True
appeared=False
changing_speed=True
slowing_start=False
jumped=False
activate_delay=False
direction='right'
jump_k=0;jump_height=34;speed=2;speed_changer=0.1;speed_changer_k=1
jump_delay=20;land_k=0
stay_k=0;stay_reverse=False
anim_rhand1=0;anim_rhand2=0
anim_lhand1=0;anim_lhand2=0
anim_rleg1=0;anim_rleg2=0
anim_lleg1=0;anim_lleg2=0
anim_bodyy=0;anim_bodyangl=0
anim_sword=0
jump_reverse=False;animjump_k=2;in_air=False
walking=False;walk_k=0;walk_reverse=False
sword_attack=False;sword_k=0;sword_reverse=False;sword_movement=True; sword_points=[];stop_sword_damage=False

globalx=-1600
globaly=1000

pl_movex=pl_movey=0
plr_movex=plr_movey=0

#def setMap():
#    global walls, plats, plxright, plydown, plxleft, plyup
#    walls=plats=plxright=plydown=plxleft=plyup=[]
wall('level1','room1_1')
platform('level1','plats')
moving_platform_xright('level1','plxright')
moving_platform_ydown('level1','plydown')
moving_platform_xleft('level1','plxleft')
moving_platform_yup('level1','plyup')
#setMap()

platform_type='wall'
pl_reverse=False
plr_reverse=False
platform_speed=1
left_speed=0
right_speed=0
down_speed=0
up_speed=0
crouching=hero_body_crouch=False
falling_time=0
stop_platforms=False
assassination=False;anim_ass_fall=True
stop_shooting=False
shooting_k=0
shooting_delay=25
screen_shaking=False;screen_shake_time=20;sc_shake_k=0;shk_strength=5
push_k=0;push_direction='right';damage_push=False
damage_resistance=False; resistance_k=0
cam_mode='game'
barR=pygame.Rect(0,0,screenX,50)
win=False
congrats=False
play_bg_sound=False
running=True
while running:
    game_intro()
    key=pygame.key.get_pressed()
    if stop_platforms!=True:
        if pl_reverse==False:
            pl_movex+=platform_speed
            for i in plxright:i.x+=platform_speed
            for i in plxleft:i.x-=platform_speed
            for i in plydown: i.y+=platform_speed
            for i in plyup: i.y-=platform_speed
        if pl_movex>=250:pl_reverse=True;plr_reverse=False
        if pl_reverse==True:
            pl_movex-=platform_speed
            for i in plxright:i.x-=platform_speed
            for i in plxleft:i.x+=platform_speed
            for i in plydown: i.y-=platform_speed
            for i in plyup: i.y+=platform_speed
        if pl_movex<=-1:pl_reverse=False;plr_reverse=True
        
    
    window.fill(BLACK) 
    mousex,mousey=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if dev_mode==True:
        if platform_type=='wall':mrect=pygame.Rect(mousex,mousey,30,30);pygame.draw.rect(window,GREEN, mrect)
        if platform_type=='plxright':mrect=pygame.Rect(mousex,mousey,90+250,30);pygame.draw.rect(window,ROSE, mrect)
        if platform_type=='plydown':mrect=pygame.Rect(mousex,mousey,90,30+250);pygame.draw.rect(window,GREEN, mrect)
        if platform_type=='plxleft':mrect=pygame.Rect(mousex+90,mousey,-250-90,30);pygame.draw.rect(window,RED, mrect)
        if platform_type=='plyup':mrect=pygame.Rect(mousex,mousey+30,90,-250-30);pygame.draw.rect(window,BLUE, mrect)
        if platform_type=='plat':mrect=pygame.Rect(mousex,mousey,30,30);pygame.draw.rect(window,PURPLE, mrect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if dev_mode==True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:platform_type='plxright'
                if event.key == pygame.K_y:platform_type='plydown'
                if event.key == pygame.K_r:platform_type='wall'
                if event.key == pygame.K_g:platform_type='plyup'
                if event.key == pygame.K_h:platform_type='plxleft'
                if event.key == pygame.K_f:platform_type='plat'                
                if event.key == pygame.K_LEFT:globalx+=30
                if event.key == pygame.K_RIGHT:globalx-=30
                if event.key == pygame.K_UP:globaly+=30
                if event.key == pygame.K_DOWN:globaly-=30

                if event.key == pygame.K_p:
                    if platform_type=='wall':set_platform('level1','room1_1');walls=[];wall('level1','room1_1')
                    if platform_type=='plxright':set_platform('level1','plxright');plxright=[];moving_platform_xright('level1','plxright')
                    if platform_type=='plydown':set_platform('level1','plydown');plydown=[];moving_platform_ydown('level1','plydown')
                    if platform_type=='plxleft':set_platform('level1','plxleft');plxleft=[];moving_platform_xleft('level1','plxleft')
                    if platform_type=='plyup':set_platform('level1','plyup');plyup=[];moving_platform_yup('level1','plyup')
                    if platform_type=='plat':set_platform('level1','plats');plats=[];platform('level1','plats')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k and assassination==False:sword_attack=True
            if event.key == pygame.K_ESCAPE:pause()
            #if event.key == pygame.K_b:dev_mode=True
            #if event.key == pygame.K_n:dev_mode=False
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_l and assassination==False:shooting_k=shooting_delay-10

    if falling==True and dev_mode==False:
        falling_time+=1
        staying=False
        in_air=True
        if changing_speed==True:speed_changer_k+=1
        if speed_changer_k>15:changing_speed=False
        down_speed=speedy
        cam_speedy=down_speed
    if jumping==False:
        falling=True

    if damage_push==True:
        if push_k<1:
            for i in basic_enemies:
                hit_rect=i.get_rect()
                if hb_left.colliderect(hit_rect):
                    push_direction='right'
                elif hb_right.colliderect(hit_rect):
                    push_direction='left'
        push_k+=1
        if push_direction=='left':
            left_speed=-speedx
            if push_k>=10:damage_push=False;push_k=0
        if push_direction=='right':
            left_speed=speedx
            if push_k>=10:damage_push=False;push_k=0

    
    crouching=False
    for i in walls:
        if hb_left.colliderect(i):
            left_speed=0
        if hb_top.colliderect(i):
            if dev_mode==False:jumping=False;jumped=True;jump_k=0;slowing_start=False;speed_changer_k=1
            jumped=True
            land_k=0
        if hb_right.colliderect(i):
            right_speed=0
        if hb_bottom.colliderect(i):
            if dev_mode==False:
                if intro!=False:intro=False
                if play_bg_sound==False:
                    main_theme.play(loops=-1)
                    play_bg_sound=True
                assassination=False
                stop_platforms=False
                falling_time=0
                if key[pygame.K_LCTRL]:crouching=True
                falling_time=0
                activate_delay=True
                down_speed=0
                jumped=False
                hero.bottom=i.top
                falling=False
                speed_changer_k=1
                changing_speed=True
                in_air=False

    for i in plats:
        if hb_left.colliderect(i):
            left_speed=0
            if hb_top.colliderect(i):right_speed=1
        if hb_top.colliderect(i):
            if dev_mode==False:jumping=False;jumped=True;jump_k=0;slowing_start=False;speed_changer_k=1
            jumped=True
            land_k=0
        if hb_right.colliderect(i):
            right_speed=0
            if hb_top.colliderect(i):left_speed=1
        if hb_bottom.colliderect(i):
            if dev_mode==False:
                assassination=False
                stop_platforms=False
                activate_delay=True
                falling_time=0
                hero.bottom=i.top
                if key[pygame.K_LCTRL]:crouching=True
                down_speed=0
                jumped=False
                hero.bottom=i.top
                falling=False
                speed_changer_k=1
                changing_speed=True
                in_air=False
      
    for i in plydown:
        for d in walls:
            if hb_top.colliderect(i) and hb_bottom.colliderect(d):
                stop_platforms=True
        for d in plats:
            if hb_top.colliderect(i) and hb_bottom.colliderect(d):
                stop_platforms=True
        if hb_left.colliderect(i):
            left_speed=0
            if hb_bottom.colliderect(i):right_speed=1
        if hb_top.colliderect(i):
            if dev_mode==False:jumping=False;jumped=True;jump_k=0;slowing_start=False;speed_changer_k=1
            up_speed=0
            jumped=True
            land_k=0
        if hb_right.colliderect(i):
            right_speed=0
            if hb_bottom.colliderect(i):left_speed=-1
        if hb_bottom.colliderect(i):
            if dev_mode==False:
                assassination=False
                stop_platforms=False
                activate_delay=True
                falling_time=0
                if key[pygame.K_LCTRL]:crouching=True
                jumped=False
                hero.bottom=i.top
                if jumping==False:
                    if pl_reverse==True:
                        for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:
                            i.y+=platform_speed
                        globaly+=platform_speed
                if pl_reverse==False:
                    for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:
                        i.y-=platform_speed
                    globaly-=platform_speed
                falling=False
                speed_changer_k=1
                changing_speed=True
                in_air=False
        
    for i in plyup:
        for d in walls:
            if hb_top.colliderect(i) and hb_bottom.colliderect(d):
                stop_platforms=True
        for d in plats:
            if hb_top.colliderect(i) and hb_bottom.colliderect(d):
                stop_platforms=True
        if hb_left.colliderect(i):
            left_speed=0
            if hb_bottom.colliderect(i):right_speed=1
        if hb_top.colliderect(i):
            if dev_mode==False:jumping=False;jumped=True;jump_k=0;slowing_start=False;speed_changer_k=1
            up_speed=0
            land_k=0
        if hb_right.colliderect(i):
            right_speed=0
            if hb_bottom.colliderect(i):left_speed=-1
        if hb_bottom.colliderect(i):
            if dev_mode==False:
                assassination=False
                stop_platforms=False
                falling_time=0
                activate_delay=True
                if key[pygame.K_LCTRL]:crouching=True
                jumped=False
                hero.bottom=i.top
                if jumping==False:
                    if plr_reverse==True:
                        for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:
                            i.y+=platform_speed
                        globaly+=platform_speed
                if plr_reverse==False:
                    for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:
                        i.y-=platform_speed
                    globaly-=platform_speed
                falling=False
                speed_changer_k=1
                changing_speed=True
                in_air=False
    
    for i in plxright:
        for d in plxleft:
            if hb_right.colliderect(d) and hb_left.colliderect(i):
                stop_platforms=True
                down_speed+=2
        if hb_left.colliderect(i):
            if pl_reverse==False:right_speed=platform_speed; left_speed=0
            if pl_reverse==True:left_speed=0
        if hb_top.colliderect(i):
            if dev_mode==False:jumping=False;jumped=True;jump_k=0;slowing_start=False;speed_changer_k=1
            up_speed=0
            jumped=True
            land_k=0
        if hb_right.colliderect(i):
            if pl_reverse==False: right_speed=0
            if pl_reverse==True:left_speed=-platform_speed;right_speed=0
        if hb_bottom.colliderect(i):
            if dev_mode==False:
                assassination=False
                stop_platforms=False
                falling_time=0
                activate_delay=True
                if key[pygame.K_LCTRL]:crouching=True
                if pl_reverse==False:right_speed+=platform_speed
                if pl_reverse==True:left_speed+=-platform_speed
                hero.bottom=i.top
                jumped=False
                falling=False
                speed_changer_k=1
                changing_speed=True
                in_air=False
                
    for i in plxleft:
        for d in plxright:
            if hb_right.colliderect(i) and hb_left.colliderect(d):
                stop_platforms=True
        if hb_left.colliderect(i):
            if plr_reverse==False:right_speed=platform_speed; left_speed=0
            if plr_reverse==True:left_speed=0
        if hb_top.colliderect(i):
            if dev_mode==False:jumping=False;jumped=True;jump_k=0;slowing_start=False;speed_changer_k=1
            up_speed=0
            jumped=True
            land_k=0
        if hb_right.colliderect(i):
            if plr_reverse==False: right_speed=0
            if plr_reverse==True:left_speed=-platform_speed;right_speed=0
        if hb_bottom.colliderect(i):
            if dev_mode==False:
                assassination=False
                stop_platforms=False
                falling_time=0
                activate_delay=True
                if key[pygame.K_LCTRL]:crouching=True
                if plr_reverse==False:right_speed+=platform_speed
                if plr_reverse==True:left_speed+=-platform_speed
                hero.bottom=i.top
                jumped=False
                falling=False
                speed_changer_k=1
                changing_speed=True
                in_air=False


    if dev_mode==True:
        if hero.centerx<390:
            hero.x-=left_speed
            globalx-=left_speed
            for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:i.x-=left_speed
             
        if hero.centerx>screenX-390:
            hero.x-=right_speed
            globalx-=right_speed
            for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:i.x-=right_speed
        if hero.centery<280:
            hero.y-=up_speed
            globaly-=up_speed
            for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:i.y-=up_speed
        if hero.centery>screenY-280:
            hero.y-=down_speed
            globaly-=down_speed
            for i in  topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:i.y-=down_speed
            
    if dev_mode==False:
        if hero.centerx<0:
            if cam_mode=='game':
                hero.x-=-800
                globalx-=-800
                for i in topleft_points + topright_points +walls+ plats + plxleft + plxright + plydown +plyup:i.x-=-800
        if hero.centerx>screenX:
            if cam_mode=='game':
                hero.x-=800
                globalx-=800
                for i in topleft_points + topright_points + walls + plats + plxleft + plxright + plydown +plyup:i.x-=800
        if hero.centery<280:
            hero.y-=up_speed
            globaly-=up_speed
            for i in topleft_points + topright_points +walls + plats + plxleft + plxright + plydown +plyup:i.y+=-up_speed
        if hero.centery>screenY-280:
            hero.y-=down_speed
            globaly-=down_speed
            for i in topleft_points + topright_points +walls + plats + plxleft + plxright + plydown +plyup:i.y-=down_speed
    if screen_shaking==True:
        sc_shake_k+=1
        if shk_strength<0:shk_strength=5
        elif shk_strength>0:shk_strength=-5
        hero.y+=shk_strength
        globaly+=shk_strength
        if sc_shake_k>=screen_shake_time:screen_shaking=False;sc_shake_k=0
    
    hero.x+=left_speed+right_speed
    hero.y+=up_speed+down_speed
    
    hb_top.bottom=hero.top
    hb_top.centerx=hero.centerx
    hb_bottom.top=hero.bottom-5
    hb_bottom.centerx=hero.centerx
    hb_left.right=hero.left
    hb_left.centery=hero.centery-1
    hb_right.left=hero.right
    hb_right.centery=hero.centery-1
    hb_left.height=hero.height-1
    hb_right.height=hero.height-1
    hb_hero.bottom=hero.bottom
    hb_hero.centerx=hero.centerx

    if choosen_level=='level1':
        for i in range(0,4):
            secret_block(10,-1646+(30*i),30,30)
        for i in range(-1,5):
            secret_block(10,-2547+(30*i),30,30)

        message_to_screen('Good luck!',PURPLE,globaly,'medium',x_displace=globalx+800)
        message_to_screen('Somewhere far away...',GREEN,globaly-300,'medium',x_displace=globalx+1600)
        
##      ASSASSINATION

    if falling_time>30 and key[pygame.K_k]:
        for i in basic_enemies:
            rec=i.get_rect()
            if hb_bottom.colliderect(rec):damage_resistance=True
            for d in range(200):
                if rec.collidepoint(hero.centerx,hero.midbottom[1]+d):
                    assassination=True
                    break
    if assassination==True:
        anim_ass_fall=True
        for i in basic_enemies:
            rec=i.get_rect()
            if rec.collidepoint(sdw_points[0],sdw_points[1]):
                damage_resistance=True
                dam=i.do_damage(100)
                hit_objects.append(Hit(sdw_points[0],sdw_points[1]))
                if dam==True:basic_enemies.remove(i)
                assassination=False
                break

    for i in hit_objects:# hitmarkers update
        ggg=i.hits()
        if ggg>=10:hit_objects.remove(i)
    
    for i in box_objects:
        i.the_box()

    for i in basic_enemies:
        i.bad()

    for i in heart_objects:
        i.heart()

    for i in bullet_objects:
            boo=i.shoot()
            if boo==True:bullet_objects.remove(i)

    
    for i in basic_enemies:# damage by pistol
        re=i.get_rect()
        if -50<re.x<screenX+50 and -50<re.y<screenY+50:
            for d in bullet_objects:
                bre=d.get_rect()
                if re.colliderect(bre):
                    dam=i.do_damage(2) # pistol damage
                    sword_hit.play()
                    bullet_objects.remove(d)
                    hit_objects.append(Hit(bre.centerx,bre.centery))
                    if dam==True: basic_enemies.remove(i);SCORE+=100;break

    for i in basic_enemies:# damage by sword
        hit_rect=i.get_rect()
        if -50<hit_rect.x<screenX+50 and -50<hit_rect.y<screenY+50:
            for d in sword_points:
                if hit_rect.collidepoint(d):
                    dam=i.do_damage(10) # sword damage
                    sword_hit.play()
                    stop_sword_damage=True
                    hit_objects.append(Hit(d[0],d[1]))
                    if dam==True:basic_enemies.remove(i);SCORE+=150;break
                    break

    for i in box_objects:
        rec=i.get_rect()
        if -50<rec.x<screenX+50 and -50<rec.y<screenY+50:
            for d in sword_points:
                if rec.collidepoint(d):
                    i.open_box()
                    box_objects.remove(i)
                    break
    for i in box_objects:
        rec=i.get_rect()
        if -50<rec.x<screenX+50 and -50<rec.y<screenY+50:
            for d in bullet_objects:
                if rec.colliderect(d):
                    i.open_box()
                    box_objects.remove(i)
                    bullet_objects.remove(d)
                    break

    for i in heart_objects:
        rec=i.get_rect()
        if -50<rec.x<screenX+50 and -50<rec.y<screenY+50:
            if hero.colliderect(rec):
                heart_objects.remove(i)
                HEALTH+=1
                SCORE-=50
                powerup.play()
                break

    for i in bullet_objects:
        rec=i.get_rect()
        if -50<rec.x<screenX+50 and -50<rec.y<screenY+50:
            for d in walls:
                if rec.colliderect(d):
                    bullet_objects.remove(i)
                    break

    if dev_mode==False:
        if damage_resistance==False and assassination==False:
            for i in bullet_objects:
                bre=i.get_rect()
                if -50<bre.x<screenX+50 and -50<bre.y<screenY+50:
                    if hb_hero.colliderect(bre):
                        HEALTH-=1
                        got_damage.play()
                        bullet_objects.remove(i)
                        screen_shaking=True
                        damage_resistance=True

            for i in basic_enemies:
                hit_rect=i.get_rect()
                if -50<hit_rect.x<screenX+50 and -50<hit_rect.y<screenY+50:
                    if hero.colliderect(hit_rect):
                        HEALTH-=1
                        got_damage.play()
                        damage_push=True
                        damage_resistance=True
                        screen_shaking=True

    if damage_resistance==True:
        resistance_k+=1
        if resistance_k>=100:damage_resistance=False;resistance_k=0

    #walls
    for i in walls:
        if -50<i.centerx<screenX+50 and -50<i.centery<screenY+50:
            window.blit(wall_image,i)
        
    for i in plats:
        if -50<i.centerx<screenX+50 and -50<i.centery<screenY+50:
            window.blit(plat_image,i)
    for i in plxright:
        if -50<i.centerx<screenX+50 and -50<i.centery<screenY+50:
            window.blit(wall_image,i);window.blit(wall_image,(i.x+30, i.y));window.blit(wall_image,(i.x+60,i.y))
    for i in plxleft:
        if -50<i.centerx<screenX+50 and -50<i.centery<screenY+50:
            window.blit(wall_image,i);window.blit(wall_image,(i.x+30, i.y));window.blit(wall_image,(i.x+60,i.y))
    for i in plydown:
        if -50<i.centerx<screenX+50 and -50<i.centery<screenY+50:
            window.blit(wall_image,i);window.blit(wall_image,(i.x+30, i.y));window.blit(wall_image,(i.x+60,i.y))
    for i in plyup:
        if -50<i.centerx<screenX+50 and -50<i.centery<screenY+50:
            window.blit(wall_image,i);window.blit(wall_image,(i.x+30, i.y));window.blit(wall_image,(i.x+60,i.y))

        
    framerate=fpsClock.get_fps()

    # INFO_BAR
    if HEALTH>5:HEALTH=5
    if intro!=True:
        pygame.draw.rect(window, BLACK, barR)
        hmrect=message_to_screen('HEALTH:',WHITE,-275,'small',-300)
        for i in range(HEALTH):
            hmr=pygame.Rect(0,0,15,15)
            hmr.left=hmrect.right+5+(i*18)
            hmr.centery=hmrect.centery-2
            pygame.draw.rect(window,WHITE,hmr)
        screct=message_to_screen('SCORE:',WHITE,-275,'small',100)
        message_to_screen(str(SCORE),WHITE,-274,'small',xx=screct.topright[0]+50)
        
    if HEALTH<=0:death()
    
    #pygame.draw.rect(window, BLUE, hero)
##    for hb in hitboxes:
##        pygame.draw.rect(window, RED, hb)

    if staying==True or in_air==True:
        walking=False
        if stay_reverse==False:stay_k+=0.1
        if stay_reverse==True:stay_k+=-0.1
        if stay_k>6:stay_reverse=True
        if stay_k<0:stay_reverse=False
        anim_rhand1=35+stay_k
        anim_rhand2=40+stay_k*3
        anim_lhand1=stay_k
        anim_lhand2=stay_k*3
        anim_bodyy=5+stay_k/2
        anim_rleg1=anim_lleg1=stay_k*2
        anim_rleg2=anim_lleg2=-stay_k
        anim_sword=stay_k
    if staying==False:stay_k=0;stay_reverse=False

    if in_air==True:
        walking=False
        if jump_reverse==False:animjump_k+=0.1
        if jump_reverse==True:animjump_k+=-0.1
        if animjump_k>6:jump_reverse=True
        if animjump_k<2:jump_reverse=False
        anim_rhand1=anim_lhand1=animjump_k
        anim_rhand2=anim_lhand2=animjump_k*5
        anim_bodyy=animjump_k
        anim_rleg1=animjump_k*4
        anim_rleg2=animjump_k*4
        anim_lleg1=-animjump_k*2
        anim_lleg2=-animjump_k*3
        anim_sword=animjump_k
    if in_air==False:animjump_k=3;jump_reverse=False

    if assassination==True:
        anim_sword=-135
        anim_rhand1=50
        anim_rhand2=-40
        anim_lhand1=60
        anim_lhand2=30

    if walking==True:
        if walk_reverse==False:walk_k+=0.15
        if walk_reverse==True:walk_k+=-0.15
        if walk_k>2:walk_reverse=True
        if walk_k<-1:walk_reverse=False
        anim_bodyy=7+walk_k
        anim_lleg1=-walk_k*16
        anim_lleg2=-walk_k*18
        anim_rleg1=walk_k*16
        anim_rleg2=walk_k*22
        anim_rhand1=-walk_k*2+35
        anim_lhand1=-walk_k*2
        anim_rhand2=walk_k*5+40
        anim_lhand2=walk_k*5
        anim_sword=walk_k
    if walking==False:walk_k=0;walk_reverse=False

    #pygame.draw.rect(window, RED, hero)
    #pygame.draw.rect(window, GREEN, hb_hero)
    
    if crouching == True:
        anim_sword=0
        anim_bodyy=18;anim_lleg1=-20;anim_lleg2=-60
        anim_rleg1=60;anim_rleg2=10;anim_rhand1=10
        anim_rhand2=25;anim_lhand1=-20;anim_lhand2=0
        hb_hero.height=75
    else:hb_hero.height=90

    right_ledge_hb.x=hero.x+40+speedx;right_ledge_hb.y=hero.y-10
    left_ledge_hb.x=hero.x-speedx;left_ledge_hb.y=hero.y-10
    #pygame.draw.rect(window,GREEN,right_ledge_hb)
    #pygame.draw.rect(window,GREEN,left_ledge_hb)
    #for i in topleft_points:
    #    pygame.draw.rect(window, GREEN, i)
    hanging=False
    if dev_mode==False:
        if direction=='right':
            for i in topleft_points:
                if i.collidepoint(right_ledge_hb.center):
                    assassination=False
                    hanging=True;down_speed=0;jumping=False
                    jumped=False;falling=False;speed_changer_k=1
                    changing_speed=True;in_air=False;activate_delay=True
                    anim_bodyy=2
                    anim_rhand1=150
                    anim_rhand2=130
                    anim_lhand1=0
                    anim_lhand2=-40
                    anim_rleg1=0
                    anim_rleg2=0
                    anim_lleg1=0
                    anim_lleg2=0
                    
        if direction=='left':
            for i in topright_points:
                if i.collidepoint(left_ledge_hb.center):
                    assassination=False
                    hanging=True;down_speed=0;jumping=False
                    jumped=False;falling=False;speed_changer_k=1
                    changing_speed=True;in_air=False;activate_delay=True
                    anim_bodyy=2
                    anim_rhand1=150
                    anim_rhand2=130
                    anim_lhand1=-10
                    anim_lhand2=-45
                    anim_rleg1=0
                    anim_rleg2=0
                    anim_lleg1=0
                    anim_lleg2=0

    sword_points=[]
    if sword_attack==True and assassination==False and intro==False:
        if sword_reverse==False:
            if sword_movement==True:
                sword_k+=0.9
                anim_sword=-sword_k*10
                if sword_k>4:sword_movement=False;sword_k=0
            if sword_movement==False:
                sword_k+=0.5
                anim_sword=-8.1*5
                anim_lhand1=sword_k*30
                anim_lhand2=sword_k*10
                if sword_k>3:sword_reverse=True;#sword_k=0#;sword_attack=False
        if sword_reverse==True:
             if sword_movement==False:
                sword_k-=0.5
                anim_sword=-8.1*5
                anim_lhand1=sword_k*30
                anim_lhand2=sword_k*10
                if sword_k<=0:sword_k=4;sword_movement=True
             if sword_movement==True:
                sword_k-=0.9
                anim_sword=-sword_k*10
                if sword_k<=0:sword_reverse=False;sword_k=0;sword_attack=False;stop_sword_damage=False
        if stop_sword_damage==False and sword_reverse==False and sword_movement==False:
            poi1=sdw.ret()
            poi2=sdw.get_mid()
            sdwdiffx=poi2[0]-poi1[0]
            sdwdiffy=poi2[1]-poi1[1]
            sdwc=math.sqrt(sdwdiffx**2+sdwdiffy**2)
            sdwdx=sdwdiffx/sdwc
            sdwdy=sdwdiffy/sdwc
            for i in range(round(sdwc)):
                sdw_npx=i*sdwdx+poi1[0]
                sdw_npy=i*sdwdy+poi1[1]
                sword_points.append((sdw_npx,sdw_npy))
            
    
    if activate_delay==True:
        land_k+=1
        if land_k>=jump_delay:
            activate_delay=False

    if direction=='right':
        #body
        bod=Animation(hero.centerx,hero.centery-10+anim_bodyy,body,anim_bodyangl)
        body_bl=bod.ret('bl');body_br=bod.ret('br')
        body_tl=bod.ret('tl');body_tr=bod.ret('tr');head_point=bod.ret('mt')
        #head
        hd=Animation(head_point[0],head_point[1],pygame.transform.flip(head,True,False),0)
        #back leg
        l1=Animation(body_br[0],body_br[1],leg1,20+anim_rleg1)
        l2pos=l1.ret()
        l2=Animation(l2pos[0],l2pos[1],leg1,340+anim_rleg2)
        #back hand
        h1=Animation(body_tr[0],body_tr[1],leg1,10+anim_rhand1)
        h2pos=h1.ret()
        h2=Animation(h2pos[0],h2pos[1],leg1,35+anim_rhand2)
        # long-distance weapon
        if hanging==False and assassination==False and intro==False:
            weap=h2.ret()
            ldw=Animation(weap[0],weap[1],pistol,0)
        #body after back hand
        Animation(hero.centerx,hero.centery-10+anim_bodyy,body,anim_bodyangl)
        #front leg
        l1=Animation(body_bl[0],body_bl[1],leg1,10+anim_lleg1)
        l2pos=l1.ret()
        l2=Animation(l2pos[0],l2pos[1],leg1,340+anim_lleg2)
        #front hand
        h1=Animation(body_tl[0],body_tl[1],leg1,340+anim_lhand1)
        h2pos=h1.ret()
        h2=Animation(h2pos[0],h2pos[1],leg1,35+anim_lhand2)
        # short-distance weapon
        if hanging==False and intro==False:
            weap=h2.ret()
            sdw=Animation(weap[0],weap[1],sword,135+anim_sword)
            sdw_points=sdw.ret()
        # additional front hand
        Animation(h2pos[0],h2pos[1],leg1,35+anim_lhand2)

    if direction=='left':
        #body
        bod=Animation(hero.centerx,hero.centery-10+anim_bodyy,body,0)
        body_bl=bod.ret('bl');body_br=bod.ret('br')
        body_tl=bod.ret('tl');body_tr=bod.ret('tr');head_point=bod.ret('mt')
        #head
        hd=Animation(head_point[0],head_point[1],head,0)
        #back leg
        l1=Animation(body_bl[0],body_bl[1],leg1,340-anim_rleg1)
        l1pos=l1.ret()
        l2=Animation(l1pos[0],l1pos[1],leg1,20-anim_rleg2)
        #back hand
        h1=Animation(body_tl[0],body_tl[1],leg1,350-anim_rhand1)
        h2pos=h1.ret()
        h2=Animation(h2pos[0],h2pos[1],leg1,325-anim_rhand2)
        # long-distance weapon
        if hanging==False and assassination==False and intro==False:
            weap=h2.ret()
            ldw=Animation(weap[0],weap[1],pygame.transform.flip(pistol,True,False),0)
        #body after back hand
        Animation(hero.centerx,hero.centery-10+anim_bodyy,body,anim_bodyangl)
        #front leg
        l1=Animation(body_br[0],body_br[1],leg1,350-anim_lleg1)
        l2pos=l1.ret()
        l2=Animation(l2pos[0],l2pos[1],leg1,20-anim_lleg2)
        #front hand
        h1=Animation(body_tr[0],body_tr[1],leg1,10-anim_lhand1)
        h2pos=h1.ret()
        h2=Animation(h2pos[0],h2pos[1],leg1,325-anim_lhand2)
        # short-distance weapon
        if hanging==False and intro==False:
            weap=h2.ret()
            sdw=Animation(weap[0],weap[1],pygame.transform.flip(sword,True,False),-135-anim_sword)
            sdw_points=sdw.ret()
        # additional front hand
        Animation(h2pos[0],h2pos[1],leg1,325-anim_lhand2)

    if stop_shooting==True:
        shooting_k+=1
        if shooting_k>=shooting_delay:stop_shooting=False;shooting_k=0

        
    if hanging==False and intro==False:
        if direction=='right' and stop_shooting==False:
            if key[pygame.K_l] and assassination==False:
                pistol_shot.stop()
                pistol_shot.play()
                b_place=ldw.ret()
                bullet_objects.append(Bullet(b_place[0]-globalx+8,b_place[1]-globaly-12,'right',speed=15, distance=500))
                stop_shooting=True
        elif direction=='left' and stop_shooting==False:
            if key[pygame.K_l] and assassination==False:
                pistol_shot.stop()
                pistol_shot.play()
                b_place=ldw.ret()
                bullet_objects.append(Bullet(b_place[0]-globalx-40,b_place[1]-globaly-12,'left',speed=15, distance=400))
                stop_shooting=True

                
    if dev_mode==True:
        message_to_screen(str(round(framerate)),GREEN,-250,'medium')
        message_to_screen(str(HEALTH),PURPLE, -200, 'small')
        message_to_screen(str(round(mousex-globalx))+' '+str(round(mousey-globaly)),GREEN,250,'small')
    
    animation_k=0 #animation variables
    staying=True

    left_speed=0
    right_speed=0
    up_speed=0
    down_speed=0
    
    if key[pygame.K_a] and hanging==False and intro==False:
        direction='left'
        if crouching==False:
            staying=False
            walking=True
            left_speed=-speedx
        
    if key[pygame.K_d]and hanging==False and intro==False:
        direction='right'
        if crouching==False:
            staying=False
            walking=True
            right_speed=speedx

    if key[pygame.K_SPACE] or jumping==True:
        if activate_delay==False and jump_k<=jump_height and falling==False and jumped==False and crouching==False:
            jump_k+=1
            if jump_k>jump_height-15:slowing_start=True
            if slowing_start==True:speed_changer_k+=1;land_k=0
            falling=False
            jumping=True
            in_air=True
            staying=False
            up_speed=round(-speedy/speed_changer_k)
            if jump_k==jump_height:
                jumped=True
                slowing_start=False
                speed_changer_k=1
                falling=True
                jumping=False
                jump_k=0

    if dev_mode==True:
        if key[pygame.K_w]:
            up_speed=-speed
        if key[pygame.K_s]:
            down_speed=speed
    
    if win==False:
        if hero.bottom-globaly<=-6086:
            win=True
            congrats=True
            main_theme.stop()
            chan=victory1.play()
            chan.queue(victory2)
            for i in range(0,26):
                walls.append(pygame.Rect(10+(i*30)+globalx,-6086+globaly,30,30))

    if congrats==True:
        message_to_screen('Congratulations!',YELLOW,-6650+globaly,'medium',x_displace=globalx)
        message_to_screen('You have completed thit tower!',GREEN,-6600+globaly,'small',x_displace=globalx)

    fpsClock.tick(FPS)
    pygame.display.update()
