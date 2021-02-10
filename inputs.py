import pygame


def user_input(event, data):
    if event.key == pygame.K_UP:
        x, y, z = data["scale"]
        data["scale"] = x, y - 1, z
    elif event.key == pygame.K_DOWN:
        x, y, z = data["scale"]
        data["scale"] = x, y + 1, z
    elif event.key == pygame.K_LEFT:
        x, y, z = data["scale"]
        data["scale"] = x - 1, y, z
    elif event.key == pygame.K_RIGHT:
        x, y, z = data["scale"]
        data["scale"] = x + 1, y, z
    elif event.key == pygame.K_w:
        data["offset_y"] -= 1
    elif event.key == pygame.K_s:
        data["offset_y"] += 1
    elif event.key == pygame.K_a:
        data["offset_x"] -= 1
    elif event.key == pygame.K_d:
        data["offset_x"] += 1
    elif event.key == pygame.K_q:
        oc = data["octaves"]
        if oc > 1:
            data["octaves"] -= 1
    elif event.key == pygame.K_e:
        data["octaves"] += 1
    elif event.key == pygame.K_j:
        data["time_scale"] -= 2
    elif event.key == pygame.K_k:
        data["time_scale"] += 2

    return data


def check_pressed():
    global POINT
    mousex, mousey = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if click != (0, 0, 0):
        left, middle, right = click
        if left:
            POINT = (mousex, mousey)

    return mousex, mousey
