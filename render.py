import multiprocessing as mp

from multiprocessing.managers import SyncManager
from queue import PriorityQueue


class PipelineManager(SyncManager):
    pass


PipelineManager.register("PriorityQueue", PriorityQueue)  # Register a shared PriorityQueue


def Manager():
    m = PipelineManager()
    m.register("PriorityQueue", PriorityQueue)
    m.start()
    return m


def from_pixels(q_in: mp.Queue, q_out: PriorityQueue):
    c = 0
    while True:
        c += 1
        priority, data = q_in.get()
        if data:
            world, values = data
            if (world == 'DONE'):
                print("count: ", c)
                break

            pixels = world.as_pixels(**values)

            try:
                q_out.put((priority, pixels), block=True)
            except Exception as e:
                print(len(pixels), len(pixels[1]))
                print(e, priority, values)
                print("damn failure\n", e.__traceback__)


def create_render_workers(count: int = 2):
    q_man = Manager()
    q_in, q_out = mp.Queue(), q_man.Queue(maxsize=4 * count)

    procs = {}

    for i in range(count):
        procs[i] = mp.Process(target=from_pixels, args=(q_in, q_out))
        procs[i].daemon = True
        procs[i].start()

    return q_in, q_out, procs