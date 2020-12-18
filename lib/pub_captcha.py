#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LETTER_CASES = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除容易造成干扰的i，l，o，z
UPPER_CASES = LETTER_CASES.upper()  # 大写字母
NUMBERS = ''.join(map(str, range(3, 10)))  # 数字，去除容易造成干扰的0，1
CHARS_POOL = ''.join((LETTER_CASES, NUMBERS, UPPER_CASES))
fontTypeList = ["lib/captcha_font/AlgerianD.ttf", "lib/captcha_font/Lubalin_Graph.otf",
                "lib/captcha_font/leikesasi.ttf", "lib/captcha_font/tanhuagui.ttf",
                "lib/captcha_font/type_writter.ttf", "lib/captcha_font/yegenyou_xingshu.ttf"]

MOVE_INTERVAL = [80, 90, 100]
# STAY_INTERVAL = [800, 1000, 1500]
STAY_INTERVAL = [4000, 5000, 7500]


def _create_strs(draw, chars, chars_length, font_size, fg_color, width, height):
    """
    绘制验证码字符
    :param chars:
    :param draw:
    :param font_size:
    :param fg_color:
    :param width:
    :param height:
    :return:
    """
    c_chars = random.sample(chars, chars_length)
    strs = ' %s  ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

    font = ImageFont.truetype(fontTypeList[random.randint(0, 5)], font_size)
    font_width, font_height = font.getsize(strs)

    draw.text(((width - font_width) / 3, (height - font_height) / 3),
              strs, font=font, fill=fg_color)

    return ''.join(c_chars)


def create_validate_code(size: tuple = (150, 50),
                         chars_pool: str = CHARS_POOL,
                         chars_length: int = 4,
                         mode: str = "RGB",
                         bg_color: tuple = (26, 31, 34),
                         fg_color: tuple = (255, 255, 255),
                         font_size: int = 28,
                         draw_lines: bool = True,
                         n_line: tuple = (1, 2),
                         draw_points: bool = True,
                         point_chance: int = 2) -> tuple:
    """
    生成验证码图片
    :param size: 验证码图片的尺寸，格式（宽，高）
    :param chars_pool: 待选字符集合
    :param chars_length: 验证码字符串长度
    :param mode: 图片色彩模式
    :param bg_color: 背景色，6位16进制表示法
    :param fg_color: 前景色，6位16进制表示法
    :param font_size: 验证码字体大小
    :param draw_lines: 是否划干扰线
    :param n_line: 干扰线的条数范围，仅有draw_lines为True时有效
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现的概率，大小范围[0, 100]
    :return PIL Image实例，验证码图片中的字符串
    """
    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    if draw_lines:
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))
    if draw_points:
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))
    strs = _create_strs(draw, chars_pool.lower(), chars_length, font_size, fg_color, width, height)

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs


def get_static_captcha():
    """
    获取静态验证码
    :return: 验证码图片字节流，验证码字符
    """
    img, text = create_validate_code()

    bytes = io.BytesIO()

    # see http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#saving
    img.save(bytes, format="png")
    return bytes, text


def get_gif_captcha():
    """
    获取动态验证码
    :return: 验证码图片字节流，验证码字符
    """
    duration_intervals = [random.choice(MOVE_INTERVAL) for _ in range(4)]
    duration_intervals.append(random.choice(STAY_INTERVAL))

    imgs = []
    text = ""
    for _ in range(5):
        img, text = create_validate_code()
        imgs.append(img)

    bytes = io.BytesIO()

    # see http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#saving
    imgs[0].save(bytes, format="gif", save_all=True, append_images=imgs[1:], duration=duration_intervals, loop=0)
    return bytes.getvalue(), text


if __name__ == "__main__":
    # code_img = create_validate_code()
    # code_img[0].save("validate.gif", "GIF")
    #
    # print(code_img[1])
    pass
