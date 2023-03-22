# write as a tf or pytorch data generator
from PIL import Image
from PIL.ImageDraw import ImageDraw
import random
import uuid
import pandas as pd
import numpy as np
from pandas import concat
level = Image.open("./images/empty_level.png").convert("RGBA")
level_with_RGBA = Image.new("RGBA", level.size)
# So monkey points north.
monkey = Image.open(
    "./images/dart_monkey_no_background.png").rotate(180, expand=True)

width_background, height_background = level.size
width_foreground, height_foreground = monkey.size
outputsize = (np.array([1920, 1080])/(120/40)).astype(np.int32)

inframe_x, inframe_y = width_background - \
    width_foreground, height_background - height_foreground
print(inframe_x, inframe_y)

df = pd.DataFrame(columns=["uuid", "rotation", "top_left_y",
                  "top_left_x", "bottom_right_x", "bottom_right_y", "class"])


for i in range(2000):

    id = uuid.uuid4().hex

    top_left_x, top_left_y = [random.randint(
        0, inframe_x), random.randint(0, inframe_y)]

    rotation = random.randint(0, 360)

    foreground_rotated = monkey.rotate(rotation, expand=True)

    bottom_right_x, bottom_right_y = np.array(
        [top_left_x, top_left_y]) + np.array(foreground_rotated.size)

    center_x = round(top_left_x + foreground_rotated.size[0]/2)
    center_y = round(top_left_y + foreground_rotated.size[1]/2)

    df2 = pd.DataFrame(
        {"uuid": id,
         "rotation": rotation,
         "top_left_y": top_left_y,
         "top_left_x": top_left_x,
         "bottom_right_x": bottom_right_x,
         "bottom_right_y": bottom_right_y,
         "center_x": center_x,
         "center_y": center_y,
         "class": "dart_monkey"
         }, index=["uuid"])

    df = concat([df, df2])

    df.to_csv("./images/data/lookup.csv", header=True, index=False)

    level_with_RGBA.paste(level, (0, 0), level)

    level_with_RGBA.paste(foreground_rotated, (top_left_x,
                          top_left_y), foreground_rotated)

    level_with_RGBA.resize(outputsize).convert("L").save(
        f"./images/data/{id}.png", optimize=True)
