import pew

pew.init()

screen = pew.Pix()
screen.box(2)

points = [
    (1, 4),
    (2, 3),
    (2, 5),
    (3, 4),
    (5, 5),
    (6, 3),
]
buttons = [
    pew.K_LEFT,
    pew.K_UP,
    pew.K_DOWN,
    pew.K_RIGHT,
    pew.K_X,
    pew.K_O,
]

for point in points:
    screen.pixel(point[0], point[1], 3)

while True:
    pew.show(screen)
    keys = pew.keys()
    for point, button in zip(points, buttons):
        if keys & button:
            screen.pixel(point[0], point[1], 0)
    pew.tick(1/8)
