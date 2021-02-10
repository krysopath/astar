import numpy as np
import noise
from PIL import Image


def linmap(t, a, b, c, d):
    return c + ((d - c) / (b - a)) * (t - a)


def noise3(point, scale, persistence=.5, lacunarity=2, octaves=2):
    x, y, z = point
    scalex, scaley, scalez = scale
    return noise.snoise3(
        x / scalex, y / scaley, z / scalez,
        persistence=persistence,
        lacunarity=lacunarity,
        octaves=octaves
    )


def make_pixel(location, offset_x=0, offset_y=0, offset_z=0, time_scale=1, **kwargs):
    x, y, z = location
    noise_value = noise3(
        (x+offset_x, y+offset_y, time_scale*z+offset_z),
        **kwargs
    )
    uint8 = linmap(noise_value, -1, 1, 0, 255)
    return uint8/4, uint8/2, uint8


def save_graph(graph, path="noise.png"):
    array = np.array(graph.as_pixels(), dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save(path)


