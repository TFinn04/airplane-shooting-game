from enemy import Enemy
from constants import *

import random


def new_formation(score):
    x = random.randint(1, 3)
    if x == 1:
        return formation1(score)
    if x == 2:
        return formation2(score)
    if x == 3:
        return formation3(score)
    

def formation1(score):
    formation = []
    x = random.randint(screen_width // 4, (screen_width // 4) * 3)
    y = random.randint(2, max(2,score//50))
    pos = 0

    layers = random.randint(0, 3)
    for i in range(y):
        for layer in range(layers):
            if pos == 0:
                formation.append(
                    Enemy(
                        x, -(enemy_height * (i + 1) // 1.75) - layer * enemy_height, 1
                    )
                )

            else:

                formation.append(
                    Enemy(
                        x + pos,
                        -((enemy_height * (i + 1)) // 1.75) - layer * enemy_height,
                        1,
                    )
                )
                formation.append(
                    Enemy(
                        x - pos,
                        -((enemy_height * (i + 1)) // 1.75) - layer * enemy_height,
                        1,
                    )
                )
        pos += enemy_width

    return formation


def formation2(score):
    formation = []
    x = 0
    y = random.randint(0, 100)
    layers = random.randint(0, 3)

    for i in range(random.randint(1, max(1,score//20))):
        for layer in range(layers):
            formation.append(
                Enemy(
                    x - (enemy_width * i),
                    y - (enemy_height * i) // 1.75 - layer * enemy_height,
                    2,
                )
            )
            formation.append(
                Enemy(
                    screen_width + enemy_width * i,
                    y - (enemy_height * i) // 1.75 - layer * enemy_height,
                    -2,
                )
            )
    return formation


def formation3(score):
    formation = []
    x = 0

    layers = random.randint(100, 400)

    for i in range(random.randint(score//50, score//25)):
        for layer in range(0, layers, enemy_height * 2):
            formation.append(Enemy(-enemy_width * i, layer, 3))
            formation.append(
                Enemy(screen_width + enemy_width * i, layer + enemy_height, -3)
            )
    return formation
