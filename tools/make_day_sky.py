"""Cloudless equirectangular display/ambient map; direct sun is authored in Blender.

This entry point changes only sky_day.jpg, keeping approved material maps and night.
"""
from pathlib import Path
import numpy as np
from PIL import Image


def make_day_sky(destination):
    width, height = 2048, 1024
    elevation = np.linspace(np.pi / 2, -np.pi / 2, height)
    haze = np.clip(np.sin(elevation), 0, 1) ** .45
    zenith = np.array([48, 118, 190])
    horizon = np.array([187, 219, 237])
    upper = horizon + haze[:, None] * (zenith - horizon)
    ground = np.array([81, 88, 71])
    rows = np.where((elevation >= 0)[:, None], upper, ground)
    pixels = np.broadcast_to(rows[:, None, :], (height, width, 3))
    Image.fromarray(np.uint8(np.clip(pixels, 0, 255))).save(destination, quality=95)


if __name__ == '__main__':
    destination = Path(__file__).resolve().parents[1] / 'blender/textures/sky_day.jpg'
    make_day_sky(destination)
    print('CLEAR_DAY_SKY', destination)
