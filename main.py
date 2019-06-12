
from PIL import Image

def get_bin_table(threshold=115):
    """
    获取灰度转二值映射table
    0：表示黑色，1：表示白色
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def sum_9_region_new(img, x, y):
    """
    确定噪点
    :param img:
    :param x:
    :param y:
    :return:
    """
    cur_pixel = img.getpixel((x, y)) # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1: # 如果当前点为白色区域，则不统计邻域值
        return 0

    # 因为当前图片四周有黑点，所以周围的黑点可以去掉
    if y < 3: # 去除前二行黑点
        return 1
    elif y > height - 3: # 去除最后2行黑点
        return 1
    else: # y不为边界
        if x < 3: # 去除前两列黑点
            return 1
        elif x > width - 3: # 去除最后两列黑点
            return 1
        else:
            sum = img.getpixel((x - 1, y - 1)) + img.getpixel((x - 1, y)) + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) + cur_pixel + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) + img.getpixel((x + 1, y)) + img.getpixel((x + 1, y + 1))
            return 9 - sum


def collect_noise_point(img):
    """
    收集所有噪点
    :param img:
    :return:
    """
    noise_point_list = []
    for x in range(img.width):
        for y in range(img.height):
            res = sum_9_region_new(img, x, y)
            if (0 < res < 3) and img.getpixel((x, y)) == 0: # 找到孤立的点
                pos = (x, y)
                noise_point_list.append(pos)
    return noise_point_list

def remove_noise_point(img, noise_point_list):
    """
    根据噪点信息，消除二值图片黑色噪点
    :param img:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)

def main():

    image = Image.open('./19051012183688.jpg')

    # print('image  mode: ', image.mode)
    # print(image.getpixel((0, 0)))
    # co = image.getcolors()
    # print(co)
    # print('-' * 40)

    # 彩色图片转为灰度图片
    imgry = image.convert('L')

    # print('image  mode: ', imgry.mode)
    # print(imgry.getpixel((0, 0)))
    # co = imgry.getcolors()
    # print(co)
    # print('-' * 40)

    table = get_bin_table()
    binary = imgry.point(table, '1')

    noise_point_list = collect_noise_point(binary)
    remove_noise_point(binary, noise_point_list)

    binary.save('./19051012183688_b.jpg')

    # print('image  mode: ', binary.mode)
    # print(binary.getpixel((0, 0)))
    # co = binary.getcolors()
    # print(co)
    # print(binary.size)

    # width, height = binary.size # width = 78 height=32
    #
    # lis = binary.getdata()  # 返回图片所有的像素值，要使用list()才能显示出具体数值
    # lis = list(lis)
    # start = 0
    # step = width
    # for i in range(height):
    #     for p in lis[start: start + step]:
    #         if p == 1:  # 将白色的点变成空格，方便人眼看
    #             p = ' '
    #         print(p, end=''),
    #     print()
    #     start += step

    # binary.save('./19051012183688_b.png')


if __name__ == '__main__':
    main()
