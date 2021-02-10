import pygame

from graphs import GridWithWeights
from inputs import user_input, check_pressed
from render import create_render_workers

N = 6
MAX_FPS = 25
screen_size = 1024, 768
#screen_size = 512, 384
#dimens = 512, 384
dimens = 256, 192

pygame.init()
screen = pygame.display.set_mode(screen_size)
done = False

world = GridWithWeights(*dimens)

POINT = screen_size[0]/2, screen_size[1]/2


def draw(mouse, surf, screen):
    pygame.transform.scale(surf, screen_size, screen)
    pygame.draw.circle(screen, (255, 0, 0), POINT, 5)
    pygame.draw.circle(screen, (255, 0, 0), mouse, 5)


def handle_events(data):
    global done

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            data = user_input(event, data)

    return data


def main():

    q_in, q_out, procs = create_render_workers(N)
    clock = pygame.time.Clock()

    data = {
        "scale": (100, 100, .01),
        "persistence": .5,
        "lacunarity": 2,
        "octaves": 1,
        "offset_x": 0,
        "offset_y": 0,
        "offset_z": 0,
        "time_scale": 1.1,
    }
    frame_id = 0

    try:
        while not done:
            frame_id = (frame_id + 1) % 10**4
            if q_in.qsize() < N:
                for _ in range(2*N):
                    q_in.put((frame_id, (world, data)))

            if frame_id % MAX_FPS == 0:
                print(round(clock.get_fps(), 1), q_in.qsize(), q_out.qsize(), data)

            data = handle_events(data)
            mouse = check_pressed()
            screen.fill((0, 0, 0))
            priority, data_rgb = q_out.get()
            surf = pygame.surfarray.make_surface(data_rgb)
            draw(mouse, surf, screen)

            pygame.display.flip()
            clock.tick(MAX_FPS)

    finally:
        for _ in procs.values():
            q_in.put(("DONE", (world, data)))
        for p in procs.values():
            p.join(timeout=1)

    for p in procs.values():
        p.terminate()


if __name__ == "__main__":
    main()
