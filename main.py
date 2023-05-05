import pygame
import random
from random import randint
import pygame_menu

import cv2
import mediapipe as mp


pygame.init()

canvas_x = 720
canvas_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
gray = pygame.Color(248, 248, 255)
blue = (80, 80, 155)

snake_color = pygame.Color(0, 0, 0)
r = randint(0, 255)
g = randint(0, 255)
b = randint(0, 255)
random_fruit_color = pygame.Color(r, g, b)

r2 = randint(0, 255)
g2 = randint(0, 255)
b2 = randint(0, 255)
while r == r2 and g == g2 and b == b2:
    r2 = randint(0, 255)
    g2 = randint(0, 255)
    b2 = randint(0, 255)

random_fruit_color = pygame.Color(r, g, b)
random_fruit_color2 = pygame.Color(r2, g2, b2)


pygame.display.set_caption('Snake Game')
game_canvas = pygame.display.set_mode((canvas_x, canvas_y))


snake_position = [100, 100]

snake = [[100, 100],
         [90, 100],
         [80, 100],
         [70, 100]
         ]


mushroom_position = [random.randrange(1, (canvas_x//10)) * 10,
                     random.randrange(1, (canvas_y//10)) * 10]

fruit_position = [random.randrange(1, (canvas_x//10)) * 10,
                  random.randrange(1, (canvas_y//10)) * 10]

fruit_position2 = [random.randrange(1, (canvas_x//10)) * 10,
                   random.randrange(1, (canvas_y//10)) * 10]

while mushroom_position[0] == fruit_position[0] and mushroom_position[1] == fruit_position[1]:
    fruit_position = [random.randrange(1, (canvas_x//10)) * 10,
                      random.randrange(1, (canvas_y//10)) * 10]

while (fruit_position2[0] == mushroom_position[0] and fruit_position2[1] == mushroom_position[1]) or (fruit_position[0] == fruit_position2[0] and fruit_position[1] == fruit_position2[1]):
    fruit_position2 = [random.randrange(1, (canvas_x//10)) * 10,
                       random.randrange(1, (canvas_y//10)) * 10]

is_fruit = True
is_fruit2 = True

score = 0
x_change = 0
y_change = 0


def display_score():
    score_font = pygame.font.SysFont("Arial", 16)
    score_rend = score_font.render('Score : ' + str(score), True, blue)
    score_rect = score_rend.get_rect()
    game_canvas.blit(score_rend, score_rect)


def orientation(coordinate_landmark_0, coordinate_landmark_9):
    x0 = coordinate_landmark_0[0]
    y0 = coordinate_landmark_0[1]

    x9 = coordinate_landmark_9[0]
    y9 = coordinate_landmark_9[1]

    if abs(x9 - x0) < 0.05:
        m = 1000000000
    else:
        m = abs((y9 - y0)/(x9 - x0))

    if m >= 0 and m <= 1:
        if x9 > x0:
            return "Right"
        else:
            return "Left"
    if m > 1:
        if y9 < y0:
            return "Up"
        else:
            return "Down"


def game_over(game_score):
    end_menu = pygame_menu.Menu(width=canvas_x, height=canvas_y,
                                title='Game Over', theme=pygame_menu.themes.THEME_BLUE)
    end_menu.add.label("Your Score:" + str(game_score))
    end_menu.add.button("Quit Game", pygame_menu.events.EXIT)
    end_menu.mainloop(game_canvas)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    x, y, c = frame.shape

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, None, fx=0.43, fy=0.43,
                       interpolation=cv2.INTER_AREA)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    movement = ''

    if result.multi_hand_landmarks:

        for hand_no, hand_landmarks in enumerate(result.multi_hand_landmarks):
            tuple1 = hand_landmarks.landmark[mp_hands.HandLandmark(
                0).WRIST].x, hand_landmarks.landmark[mp_hands.HandLandmark(0).WRIST].y,
            tuple2 = hand_landmarks.landmark[mp_hands.HandLandmark(
                0).MIDDLE_FINGER_MCP].x, hand_landmarks.landmark[mp_hands.HandLandmark(0).MIDDLE_FINGER_MCP].y,
            movement = orientation(tuple1, tuple2)

            if movement == 'Up':
                movement = 'Up'
                y_change = -10
                x_change = 0
            elif movement == 'Down':
                movement = 'Down'
                y_change = 10
                x_change = 0
            elif movement == 'Right':
                movement = 'Right'
                x_change = 10
                y_change = 0
            elif movement == 'Left':
                movement = 'Left'
                x_change = -10
                y_change = 0
            else:
                pass

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over(score)

        snake_position[1] += y_change
        snake_position[0] += x_change

        snake.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            is_fruit = False
            snake_color = random_fruit_color
        elif snake_position[0] == fruit_position2[0] and snake_position[1] == fruit_position2[1]:
            score += 10
            is_fruit2 = False
            snake_color = random_fruit_color2
        elif mushroom_position[0] <= snake_position[0] and snake_position[0] <= mushroom_position[0]+20 and mushroom_position[1] <= snake_position[1] and snake_position[1] <= mushroom_position[1]+20:
            game_over(score)
        else:
            snake.pop()

        if not is_fruit:
            fruit_position = [random.randrange(1, (canvas_x//10)) * 10,
                              random.randrange(1, (canvas_y//10)) * 10]
            while mushroom_position[0] == fruit_position[0] and mushroom_position[1] == fruit_position[1]:
                fruit_position = [random.randrange(1, (canvas_x//10)) * 10,
                                  random.randrange(1, (canvas_y//10)) * 10]

            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            random_fruit_color = pygame.Color(r, g, b)

        if not is_fruit2:
            fruit_position2 = [random.randrange(1, (canvas_x//10)) * 10,
                               random.randrange(1, (canvas_y//10)) * 10]
            while (fruit_position2[0] == mushroom_position[0] and fruit_position2[1] == mushroom_position[1]) or (fruit_position[0] == fruit_position2[0] and fruit_position[1] == fruit_position2[1]):
                fruit_position2 = [random.randrange(1, (canvas_x//10)) * 10,
                                   random.randrange(1, (canvas_y//10)) * 10]
            r2 = randint(0, 255)
            g2 = randint(0, 255)
            b2 = randint(0, 255)
            while r == r2 and g == g2 and b == b2:
                r2 = randint(0, 255)
                g2 = randint(0, 255)
                b2 = randint(0, 255)
            random_fruit_color2 = pygame.Color(r2, g2, b2)

        is_fruit = True
        is_fruit2 = True
        game_canvas.fill(gray)

        for p in snake:
            pygame.draw.rect(game_canvas, snake_color,
                             pygame.Rect(p[0], p[1], 10, 10))

        pygame.draw.rect(game_canvas, random_fruit_color, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))
        pygame.draw.rect(game_canvas, random_fruit_color2, pygame.Rect(
            fruit_position2[0], fruit_position2[1], 10, 10))
        pygame.draw.circle(game_canvas, red,
                           (mushroom_position[0], mushroom_position[1]), 20)
        pygame.draw.circle(game_canvas, white,
                           (mushroom_position[0]-10, mushroom_position[1]-10), 5)
        pygame.draw.circle(game_canvas, white,
                           (mushroom_position[0]-10, mushroom_position[1]+10), 5)
        pygame.draw.circle(game_canvas, white,
                           (mushroom_position[0]+10, mushroom_position[1]+10), 5)
        pygame.draw.circle(game_canvas, white,
                           (mushroom_position[0]+10, mushroom_position[1]-10), 5)

        if snake_position[0] < 0 or snake_position[0] > canvas_x-10:
            if snake_position[0] < 0:
                snake_position[0] = canvas_x-10
            elif snake_position[0] > canvas_x-10:
                snake_position[0] = 0
        if snake_position[1] < 0 or snake_position[1] > canvas_y-10:
            if snake_position[1] < 0:
                snake_position[1] = canvas_y-10
            elif snake_position[1] > canvas_y-10:
                snake_position[1] = 0

        display_score()
        pygame.display.update()
        cv2.imshow('Hand', frame)
