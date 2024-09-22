# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO
from pdf2image import convert_from_bytes


def convert_image_to_bw_old(image, threshold):
    fn = lambda x : 255 if x > threshold else 0
    return image.convert('L').point(fn, mode='1') # convert to black and white


def convert_image_to_bw(image, threshold):
    # Convert the image to RGB mode if it's not already
    rgb_image = image.convert('RGB')

    # Split the image into its RGB components
    r, g, b = rgb_image.split()

    def bwr_convert(r, g, b):
        r, g, b = r.point(lambda x: x), g.point(lambda x: x), b.point(lambda x: x)
        result = Image.new('RGB', r.size)
        for x in range(r.width):
            for y in range(r.height):
                r_val, g_val, b_val = r.getpixel((x, y)), g.getpixel((x, y)), b.getpixel((x, y))
                luminance = (0.299 * r_val + 0.587 * g_val + 0.114 * b_val)

                if r_val > threshold and r_val > g_val * 1.5 and r_val > b_val * 1.5:
                    # If red is dominant and above threshold, keep it red
                    result.putpixel((x, y), (255, 0, 0))
                elif luminance > threshold:
                    # If bright enough, convert to white
                    result.putpixel((x, y), (255, 255, 255))
                else:
                    # Otherwise, convert to black
                    result.putpixel((x, y), (0, 0, 0))
        return result

    # Apply the conversion
    bwr_image = bwr_convert(r, g, b)

    return bwr_image

def convert_image_to_grayscale(image):
    fn = lambda x : 255 if x > threshold else 0
    return image.convert('L') # convert to greyscale


def imgfile_to_image(file):
    s = BytesIO()
    file.save(s)
    im = Image.open(s)
    return im


def pdffile_to_image(file, dpi):
    s = BytesIO()
    file.save(s)
    s.seek(0)
    im = convert_from_bytes(
        s.read(),
        dpi = dpi
    )[0]
    return im


def image_to_png_bytes(im):
    image_buffer = BytesIO()
    im.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer.read()
