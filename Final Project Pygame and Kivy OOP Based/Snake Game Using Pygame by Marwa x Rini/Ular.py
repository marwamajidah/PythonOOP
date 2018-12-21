import sys,os,pygame,random,math

pygame.init()
pygame.display.set_caption("Moi Snake MarwaxRini")

pygame.font.init()
random.seed()

#--- Globals ---
SPEED = 0.3
#segmentsize
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE
WALL_SIZE = SNAKE_SIZE
#margin between segment
SEPARATION = 10
#screen size
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
#frame rate per second
FPS = 25
KEY = {"UP":1,"DOWN":2,"LEFT":3,"RIGHT":4}

#Screen initialization
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.HWSURFACE)

#Resources
game_over_font = pygame.font.Font(None,46)
play_again_font = pygame.font.Font(None,38)
background_color = pygame.Color(0, 0, 0)
black = pygame.Color(0,0,0)
yellow = (255,255,0)
gameClock = pygame.time.Clock()

#winicon
icon = pygame.image.load("snakelogomarwarini.png")
pygame.display.set_icon(icon)
        
class Segment:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = pygame.color.Color("white")
        
class Apple:
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("red")
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,APPLE_SIZE,APPLE_SIZE),0)
        
class Snake:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = []
        
        self.stack.append(self)
        
        blackBox = Segment(self.x,self.y + SEPARATION)
        blackBox.direction = KEY["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)

    def move(self):
        last_element = len(self.stack)-1
        while(last_element != 0):
            self.stack[last_element].direction = self.stack[last_element-1].direction
            self.stack[last_element].x = self.stack[last_element-1].x 
            self.stack[last_element].y = self.stack[last_element-1].y 
            last_element-=1
        if(len(self.stack)<2):
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if(self.stack[0].direction ==KEY["UP"]):
            last_segment.y = self.stack[0].y - (SPEED * FPS)
            
        elif(self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y + (SPEED * FPS)
            
        elif(self.stack[0].direction ==KEY["LEFT"]):
            last_segment.x = self.stack[0].x - (SPEED * FPS)
            
        elif(self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x + (SPEED * FPS)
        self.stack.insert(0,last_segment)

    def getHead(self):
        return(self.stack[0])
    
    def grow(self):
        last_element = len(self.stack)-1
        self.stack[last_element].direction = self.stack[last_element].direction
        if(self.stack[last_element].direction == KEY["UP"]):
            newSegment = Segment(self.stack[last_element].x,self.stack[last_element].y-SNAKE_SIZE)
            blackBox = Segment(newSegment.x,newSegment.y-SEPARATION)
            
        elif(self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = Segment(self.stack[last_element].x,self.stack[last_element].y+SNAKE_SIZE)
            blackBox = Segment(newSegment.x,newSegment.y+SEPARATION)
            
        elif(self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = Segment(self.stack[last_element].x-SNAKE_SIZE,self.stack[last_element].y)
            blackBox = Segment(newSegment.x-SEPARATION,newSegment.y)
            
        elif(self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = Segment(self.stack[last_element].x+SNAKE_SIZE,self.stack[last_element].y)
            blackBox = Segment(newSegment.x+SEPARATION,newSegment.y)
            
        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)
    
    def setDirection(self,direction):
        if(self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY["LEFT"] and direction == KEY["RIGHT"]):
            pass
        elif(self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["DOWN"] and direction == KEY["UP"]):
            pass
        else:
            self.direction = direction

    def draw(self,screen):
        pygame.draw.rect(screen,pygame.color.Color("green"),(self.stack[0].x,self.stack[0].y,SNAKE_SIZE,SNAKE_SIZE),0)
        counter = 1
        while(counter < len(self.stack)):
            if(self.stack[counter].color == "NULL"):
                counter+=1
                continue
            pygame.draw.rect(screen,pygame.color.Color("white"),(self.stack[counter].x,self.stack[counter].y,SNAKE_SIZE,SNAKE_SIZE),0)
            counter+=1

class Wall:
    def createWall(self):
        global boundry
        self.boundry=[]
        for i in range(0,SCREEN_WIDTH):
            self.boundry.append((i,0))
            self.boundry.append((i,SCREEN_HEIGHT-7))
        for i in range(0,SCREEN_HEIGHT):
            self.boundry.append((0,i))
            self.boundry.append((SCREEN_WIDTH-7,i))
    def drawWall(self):
        for each in self.boundry:
            self.wallRect = pygame.Rect(each[0],each[1], WALL_SIZE-2, WALL_SIZE-2)
            pygame.draw.rect(screen, yellow, self.wallRect)

    def checkCollision2(self,snake):
        self.bumper_x = SCREEN_WIDTH - WALL_SIZE
        self.bumper_y = SCREEN_HEIGHT - WALL_SIZE
        if(
            snake.x < WALL_SIZE or
            snake.y < WALL_SIZE or
            snake.x + SNAKE_SIZE > self.bumper_x or
            snake.y + SNAKE_SIZE > self.bumper_y):
            endGame()
            return True
        else:
            return False

#collision apple
def checkCollision(posA,As,posB,Bs):
    #As size of a | Bs size of b
    if(posA.x   < posB.x+Bs and posA.x+As > posB.x and posA.y < posB.y + Bs and posA.y+As > posB.y):
        return True
    return False

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()

def respawnApple(apples,index,sx,sy):
    radius = math.sqrt((SCREEN_WIDTH/2*SCREEN_WIDTH/2  + SCREEN_HEIGHT/2*SCREEN_HEIGHT/2))/2
    angle = 999
    while(angle > radius):
        angle = random.uniform(0,800)*math.pi*2
        x = SCREEN_WIDTH/2 + radius * math.cos(angle)
        y = SCREEN_HEIGHT/2 + radius * math.sin(angle)
        if(x == sx and y == sy):
            continue
    newApple = Apple(x,y,1)
    apples[index] = newApple
        
def respawnApples(apples,quantity,sx,sy):
    counter = 0
    del apples[:]
    radius = math.sqrt((SCREEN_WIDTH/2*SCREEN_WIDTH/2  + SCREEN_HEIGHT/2*SCREEN_HEIGHT/2))/2
    angle = 999
    while(counter < quantity):
        while(angle > radius):
            angle = random.uniform(0,800)*math.pi*2
            x = SCREEN_WIDTH/2 + radius * math.cos(angle)
            y = SCREEN_HEIGHT/2 + radius * math.sin(angle)
            if( (x-APPLE_SIZE == sx or x+APPLE_SIZE == sx)
                and (y-APPLE_SIZE == sy or y+APPLE_SIZE == sy) or radius - angle <= 10):
                continue
        apples.append(Apple(x,y,1))
        angle = 999
        counter+=1
        
def endGame():
    message = game_over_font.render("Game Over",1,pygame.Color("white"))
    message_play_again = play_again_font.render("Play Again? Y/N",1,pygame.Color("green"))
    screen.blit(message,(320,240))
    screen.blit(message_play_again,(320+12,240+40))
        
    pygame.display.flip()
    pygame.display.update()
    
    myKey = getKey()
    while(myKey != "exit"):
        if(myKey == "yes"):
            main()
        elif(myKey == "no"):
            break
        myKey = getKey()
    pygame.quit()
    sys.exit()
    
    
def main():
    score = 0

    myWall=Wall()
    #Snake initialization
    mySnake = Snake(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    mySnake.setDirection(KEY["UP"])
    mySnake.move()
    start_segments=3
    while(start_segments>0):
        mySnake.grow()
        mySnake.move() 
        start_segments-=1

    #Apples
    max_apples = 1
    eaten_apple = False
    apples = [Apple(random.randint(60,SCREEN_WIDTH),random.randint(60,SCREEN_HEIGHT),1)]
    respawnApples(apples,max_apples,mySnake.x,mySnake.y)
    endgame = 0
    
    while(endgame!=1):
        gameClock.tick(FPS)

        #Input
        keyPress = getKey()
        if keyPress == "exit":
            endgame = 1

        #Collision to wall
        myWall.checkCollision2(mySnake)
            
        for myApple in apples:
            if(myApple.state == 1):
                if(checkCollision(mySnake.getHead(),SNAKE_SIZE,myApple,APPLE_SIZE)==True):
                    mySnake.grow()
                    myApple.state = 0
                    eaten_apple=True
            

        #Position Update
        if(keyPress):
            mySnake.setDirection(keyPress)    
        mySnake.move()
        
        #Respawning apples
        if(eaten_apple == True):
            eaten_apple = False
            respawnApple(apples,0,mySnake.getHead().x,mySnake.getHead().y)

        #Drawing
        screen.fill(background_color)
        for myApple in apples:
            if(myApple.state == 1):
                myApple.draw(screen)
        
        myWall.createWall()
        myWall.drawWall()    
        mySnake.draw(screen)

        #Flip screen
        pygame.display.flip()
        pygame.display.update()
            
main()
