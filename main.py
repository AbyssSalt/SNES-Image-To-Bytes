import math
import os
from PIL import Image

directory = "Active Sprites"
f = open("C:\\Users\\trues\\Downloads\\Snes Development\\sprite.bin", mode="wb")

bpp = 4
addresses_per_row = 128
off = 0
def RowToHex(byte_list):
    bits = {
        1: [0] * 8,
        2: [0] * 8,
        4: [0] * 8,
        8: [0] * 8
    }
    for e, char in enumerate(byte_list):
        num = int(char, 16)

        while num > 0:
            print(2 ** math.floor(math.log2(num)), e)
            bits[2 ** math.floor(math.log2(num))][e] = 1
            num -= 2 ** math.floor(math.log2(num))
    bytes = [0, 0, 0, 0]
    for k in bits.keys():
        code = hex(int("".join(str(a) for a in bits[k]), 2))[2::]
        if len(code) < 2:
            code = "0" + code

        bytes[int(math.log2(k))] = code

    return bytes

color_palette = [(0, 0, 0, 0)]
for c, file in enumerate(os.listdir(directory)):
    image = Image.open("Active Sprites\\" + file.split("\\")[-1])

    for count, color in image.getcolors():
        if color not in color_palette:
            color_palette.append(color)

    color_hexcodes = []
    for color in color_palette:
        r = bin(color[0] // 8)[2::].rjust(5, "0")
        g = bin(color[1] // 8)[2::].rjust(5, "0")
        b = bin(color[2] // 8)[2::].rjust(5, "0")

        full = "0" + b + g + r

        addr = [full[8::], full[0:8]]
        for h in addr:
            color_hexcodes.append(int(h, 2))

    for y_chunk in range(c * 4, image.height // 8 + c * 4):
        Address = int(str((y_chunk - c * 4) * 200), 16) + int(str(c * 40), 16)
        f.write(bytes([((addresses_per_row + 16) * (y_chunk + 1)) // 256]))
        f.write(bytes([((addresses_per_row + 16) * (y_chunk + 1)) % 256]))
        f.write(bytes([((addresses_per_row + 16) * (y_chunk + 1) - 1) // 256]))
        f.write(bytes([((addresses_per_row + 16) * (y_chunk + 1) - 1) % 256]))
        f.write(bytes([Address // 256]))
        f.write(bytes([Address % 256]))
        f.write(bytes([((addresses_per_row + 16) * y_chunk + 16) // 256]))
        f.write(bytes([((addresses_per_row + 16) * y_chunk + 16) % 256]))
        if y_chunk == 0:
            f.write(bytes([(max(image.height//8, image.width//8) - 2) // 2]))

            f.write(b'\x00' * 7)
        else:
            f.write(b'\x00' * 8)

        for x_chunk in range(image.width // 8):
            hex_array = [[], []]
            for y in range(8):
                byte_list = ""
                for x in range(8):
                    byte_list += str(hex(color_palette.index(image.getpixel((x + x_chunk * 8, y + (y_chunk - c * 4) * 8)))))[2::]
                print(byte_list)
                byte_array = RowToHex(byte_list)
                hex_array[0].append(str(byte_array[0]))
                hex_array[0].append(str(byte_array[1]))
                hex_array[1].append(str(byte_array[2]))
                hex_array[1].append(str(byte_array[3]))
            f.write(bytes(int(a, 16) for a in hex_array[0]))
            f.write(bytes(int(a, 16) for a in hex_array[1]))

f.write(bytes([0, 0]))
f.write(bytes([((addresses_per_row + 16) * (4 * (c + 1)) + 16 + len(color_hexcodes)) // 256]))
f.write(bytes([((addresses_per_row + 16) * (4 * (c + 1)) + 16 + len(color_hexcodes)) % 256]))
f.write(bytes([0, 128]))
f.write(bytes([((addresses_per_row + 16) * (4 * (c + 1)) + 16) // 256]))
f.write(bytes([((addresses_per_row + 16) * (4 * (c + 1)) + 16) % 256]))

f.write(b'\x00')
f.write(b'\x01')
f.write(b'\x00' * 6)

for color in color_hexcodes:
    f.write(bytes([color]))

f.write(b'\x00' * 16)
f.close()
