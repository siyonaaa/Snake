import os
import random

PATH = os.getcwd()

#assigning global variables
ROW_WIDTH = 30
COL_WIDTH = 30
RESOLUTION_W = 600
RESOLUTION_H = 600
#so that it becomes adjustable
NUM_ROWS = int(RESOLUTION_H / ROW_WIDTH)
NUM_COLS = int(RESOLUTION_W / COL_WIDTH)

#class reflecting the overall game
class Game:
    #when Game class is called the reset method is initialized which reinitializes all the attributes to restart the game
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.snake = Snake()
        self.direction = RIGHT
        self.last_dir = RIGHT
        self.fruits = Fruits()
        self.fruits.choose_place(self.snake)
        #score is initialized by 0 at the beginning of the game
        self.score = 0
        #no collision happens when the game starts
        self.collided = False
        #player cannot win just when the game starts
        self.win = False
        self.last_x = self.snake[-1].row
        self.last_y = self.snake[-1].col
    
    #method to check both types of collisions
    def check_collision(self):
        
        #checks collision of the snake with the walls of the canvas
        if (self.snake.head_row < 0 or self.snake.head_row >= NUM_ROWS or self.snake.head_col < 0 or self.snake.head_col >= NUM_COLS):
            print("Wall collision detected") 
            self.collided = True
            return                   
        
        #checks collision of the snake with itself                                 
        for segment in self.snake[1:]:  #loops over each segment of the snake except for the head
            if segment.row == self.snake.head_row and segment.col == self.snake.head_col:
                print("Snake collided with itself") #debug line
                self.collided = True
                return
        
    def display(self):
 
        #if the player loses or wins, skip the display method
        if self.collided or self.win:
            return   
    
        #condition to check for a win
        if len(self.snake) == NUM_ROWS * NUM_COLS:
            self.win = True
            return

        # check if snake eats fruit                    
        if self.snake.head_row == self.fruits.row and self.snake.head_col == self.fruits.col:
            #append the correct colored segment based on the fruit type
            if self.fruits.choice == 0:
                self.snake.append(Element(self.last_x, self.last_y, 'red'))
            elif self.fruits.choice == 1:
                self.snake.append(Element(self.last_x, self.last_y, 'yellow'))
            
        #increase score by 1 pt for every fruit that is eaten    
            self.score += 1
        #generate a new fruit at a new location
            self.fruits.choose_place(self.snake)
    
    #set x and y coordinates for the head image placement 
        head_x = self.snake.head_col * COL_WIDTH
        head_y = self.snake.head_row * ROW_WIDTH
    
    #enable the appearance of fruits
        self.fruits.display()
    
    #render each segment except the head
        for segment in self.snake[1:]:
            segment.display()
    
    #render the head image based on the direction
        if self.direction == RIGHT:
            image(self.snake.head_left, head_x, head_y, 30, 30, 30, 30, 0, 0)
            self.move_right()
        elif self.direction == LEFT:
            image(self.snake.head_left, head_x, head_y, 30, 30)
            self.move_left()
        elif self.direction == UP:
            image(self.snake.head_up, head_x, head_y, 30, 30)
            self.move_up()
        elif self.direction == DOWN:
            image(self.snake.head_up, head_x, head_y, 30, 30, 30, 30, 0, 0)
            self.move_down()
    
    #update last body coordinates
        self.last_x = self.snake[-1].row
        self.last_y = self.snake[-1].col   

    #check for wall or self-collision
        self.check_collision()
        
    #for moving the snake to the right    
    def move_right(self):
        #first check for collission        
        if self.snake.head_col + 1 >= NUM_COLS:
            self.collided = True
            return        
        #updates body grid positions
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].row = self.snake[i - 1].row
            self.snake[i].col = self.snake[i - 1].col
        #moves head in the grid
        self.snake.head_col += 1
        self.snake[0].col = self.snake.head_col  #updates head position in grid        
                
    #for moving the snake to the left        
    def move_left(self):        
        if self.snake.head_col - 1 < 0:
            self.collided = True
            return        
        #updates body grid positions
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].row = self.snake[i - 1].row
            self.snake[i].col = self.snake[i - 1].col
        #moves head in the grid
        self.snake.head_col -= 1
        self.snake[0].col = self.snake.head_col  
    
    #for moving the snake up                
    def move_up(self):        
        if self.snake.head_row - 1 < 0:
            self.collided = True
            return    
        #updates body grid positions
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].row = self.snake[i - 1].row
            self.snake[i].col = self.snake[i - 1].col
        #moves head in the grid
        self.snake.head_row -= 1
        self.snake[0].row = self.snake.head_row  
    
    #for moving the snake down
    def move_down(self):
        if self.snake.head_row + 1 >= NUM_ROWS:
            self.collided = True
            return        
        #updates body grid positions
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].row = self.snake[i - 1].row
            self.snake[i].col = self.snake[i - 1].col
        #moves head in the grid
        self.snake.head_row += 1
        self.snake[0].row = self.snake.head_row            
     
#class reflecting the snake(which inherits from a list)
class Snake(list):
    def __init__(self):
        #loads the head images into memory
        self.head_left = loadImage(PATH + '/images/head_left.png')
        self.head_up = loadImage(PATH + '/images/head_up.png')
        
        #assigning the starting position in terms of the number of grid rows and columns
        self.head_row = NUM_ROWS // 2
        self.head_col = NUM_COLS // 2       
                
        #add initial body parts based on row/column grid positions
        self.append(Element(self.head_row, self.head_col, 'green'))
        self.append(Element(self.head_row, self.head_col - 1, 'green'))
        self.append(Element(self.head_row, self.head_col - 2, 'green'))
    
#class reflecting an element of the snake
class Element():
    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        
    def display(self):
        noStroke()
        #appending a green body segment
        if self.colour == 'green':
            fill(80, 152, 32)
        #appending a red body segment    
        elif self.colour == 'red':
            fill(172, 48, 32)
        #appending a yellow body segment    
        elif self.colour == 'yellow':
            fill(252, 226, 76)
        #generating the x and y center coordinates so that the ellipse's center is at the center of a cell    
        pixel_x = self.col * COL_WIDTH + 15
        pixel_y = self.row * ROW_WIDTH + 15
        #creating the ellipse (body segment)
        ellipse(pixel_x, pixel_y, 30, 30)
           
#class reflecting the food items
class Fruits:
    def __init__(self): 
        
        # loading the images of the fruits (apple and banana)       
        self.apple_img = loadImage(PATH + '/images/apple.png')
        self.banana_img = loadImage(PATH + '/images/banana.png')
        
        # simply initializing these variables here. I've assigned them random numbers because it is overwritten in the next method anyways.
        self.row = 1
        self.col = 1
        self.choice = 1
    
    def choose_place(self, snake):
        #randomly choose fruit type: 0 for apple; 1 for banana
        self.choice = random.randint(0,1)
        #creating a dictionary to track positions occupied by the snake's body parts
        occupied_positions = {}
        for element in snake:
            #mark each position occupied by the snake
            occupied_positions[(element.row, element.col)] = True
        if len(occupied_positions) >= NUM_ROWS * NUM_COLS:
            game.win = True
            return
        #generates a random position for the fruit, ensures it doesn't overlap with the snake
        while True:
            self.row = random.randint(0, NUM_ROWS - 1)
            self.col = random.randint(0, NUM_COLS - 1)
            #exits the loop if the chosen position for the fruit is unoccupied 
            if (self.row, self.col) not in occupied_positions:
                break                        
        
    def display(self):
        # to generate the x and y coordinate of the top left corner of the cell to place the image
        pixel_x = self.col * COL_WIDTH 
        pixel_y = self.row * ROW_WIDTH
        if self.choice == 0:
            image(self.apple_img, pixel_x, pixel_y, 30, 30)
        elif self.choice == 1:
            image(self.banana_img, pixel_x, pixel_y, 30, 30)       

#initially setting game_started to False until user clicks mouse button
game_started = False

#creating an instance of the Game class
game = Game()

def setup():
    size(RESOLUTION_W, RESOLUTION_H)
    #creating a grey background
    background(155, 155, 155)

def draw(): 
    
    #display message if player wins
    if game.win:
        fill(0)
        textSize(40)
        textAlign(CENTER, CENTER)
        text("YOU WIN!!!", RESOLUTION_W / 2, RESOLUTION_H / 2 - 20)
        text("Final Score: " + str(game.score), RESOLUTION_W / 2, RESOLUTION_H / 2 + 20)
       
    #display message if player loses    
    elif game.collided:
        fill(0)
        textSize(40)
        textAlign(CENTER, CENTER)
        text("GAME OVER!", RESOLUTION_W / 2, RESOLUTION_H / 2 - 20)
        text("Final Score: " + str(game.score), RESOLUTION_W / 2, RESOLUTION_H / 2 + 20)
        
    #keeps the game going if player does not lose/win and displays the score on the top right corner    
    elif game_started:
        if frameCount % 12 == 0:
            background(155, 155, 155)
            game.display()
            fill(0)
            textSize(20)
            text("Score:" + " " + str(game.score), RESOLUTION_W - 120, 30)
            #updates direction based on arrow key press
        if game.last_dir == RIGHT and game.direction != LEFT: #prevents reverse movement
            game.direction = RIGHT         
        elif game.last_dir == LEFT and game.direction != RIGHT:
            game.direction = LEFT
        elif game.last_dir == UP and game.direction != DOWN:
            game.direction = UP
        elif game.last_dir == DOWN and game.direction != UP:
            game.direction = DOWN
        
        #constantly checks if the snake has collided        
        game.check_collision()
        print("Collision status:", game.collided) #debug line

#to restart the game when the user clicks on the mouse
def mouseClicked():
    global game_started
    global game
    if not game_started:
        game_started = True
    elif game.collided or game.win:
        game = Game()
        game_started = True       
    
def keyPressed():
    game.last_dir = keyCode
