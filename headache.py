from time import sleep
from graphics_and_games_klassen import *
from intern.zeichenfenster import Zeichenfenster
from random import randint, choice

class Ball(Kreis):
    def moveUp(self, length = 10):
        self.Verschieben(0, -length)
    def moveDown(self, length = 10):
        self.Verschieben(0, length)
    def moveRight(self, length = 10):
        self.Verschieben(length, 0)
    def moveLeft(self, length = 10):
        self.Verschieben(-length, 0)
    def move(self, x, y):
        self.Verschieben(x, -y)


print("Prepare yourself for 'Kopfschemrzen'!")

ball_colors = ["weiss", "rot", "blau", "gruen", "schwarz", "gelb"]
balls = []


for i in range(100):
    x = randint(100, 500)
    y = randint(100, 500)
    ball_obj = Ball(x, -y)
    ball_obj.FarbeSetzen(choice(ball_colors))
    balls.append(ball_obj)

waiting_time = 0.1 #0.000000000000000000000000000000000000000000001

while True:
    for ball in balls:
        start_radius = ball.radius
        sleep(waiting_time)
        ball.moveRight()
        ball.FarbeSetzen(choice(ball_colors))
        ball.radius += 1
        
        sleep(waiting_time)
        ball.moveDown()
        ball.FarbeSetzen(choice(ball_colors))
        ball.radius += 1
        
        sleep(waiting_time)
        ball.moveLeft()
        ball.FarbeSetzen(choice(ball_colors))
        ball.radius += 1
        
        sleep(waiting_time)
        ball.moveUp()
        ball.FarbeSetzen(choice(ball_colors))
        ball.radius += 1
        
        end_radius = ball.radius
        radius_difference = end_radius - start_radius
        
        ball.move(radius_difference, -radius_difference)
