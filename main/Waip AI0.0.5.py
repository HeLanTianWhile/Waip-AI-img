# 简单的图像生成
import json
import os
from PIL import Image
import random
 

def Waip_imgea(user_input):
    # 从数据库中查找相关提示词
    TF = False
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database','Database 1.0')
    # 遍历数据库中的所有文件目录
    for i in os.listdir(path):
        print(i)
        if i in user_input:
            TF = True
            path_user = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database','Database 1.0', i))
            xy = []
            # 存储所有图片的尺寸信息
            image_sizes = []
            
            for j in path_user:
                # 打开图片
                img = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database','Database 1.0', i, j)).convert('RGB')
                # 获取并打印图片尺寸
                width, height = img.size
                image_sizes.append((width, height))
                print(f"图片 {j} 尺寸: {width}x{height}")
                
                # 方法1：使用load()获取像素访问对象（更高效）
                pixels = img.load()
                pixel_matrix = [[pixels[x, y] for x in range(width)] for y in range(height)]
                xy.append(pixel_matrix)
            
            # 计算最小尺寸，确保不会越界访问
            min_width = min(s[0] for s in image_sizes) if image_sizes else 0
            min_height = min(s[1] for s in image_sizes) if image_sizes else 0
            print(f"所有图片的最小尺寸: {min_width}x{min_height}")
    if TF:
        pass
    else:
        return "没有找到相关提示词"
    # 使用计算出的最小尺寸创建图像的二维列表
    img_xy = []
    for k in range(min_height):
        img_xy.append([])
        for g in range(min_width):
            img_xy[k].append([0, 0, 0])  # 使用列表而不是元组，因为列表可以修改
    
    # 生成图片 - 直接使用最小尺寸，img_xy已经基于最小尺寸创建
    # 只处理所有图片都有的像素范围
    for h in range(min_height):
        for g in range(min_width):
            # 收集所有图片在该位置的RGB值
            r_values = []
            g_values = []
            b_values = []
            
            for img_data in xy:
                # 直接访问，因为我们已经确保不会越界
                pixel = img_data[h][g]
                r_values.append(pixel[0])
                g_values.append(pixel[1])
                b_values.append(pixel[2])
            
            # 决定颜色
            r_fs = ["跟风", -1, -1]
            g_fs = ["跟风", -1, -1]
            b_fs = ["跟风", -1, -1]

            for f in range(3):
                # 检测是要动什么颜色
                if f == 0:
                    # 红色
                    ys = r_values
                    ys2 = "red"
                elif f == 1:
                    # 绿色
                    ys = g_values
                    ys2 = "green"
                elif f == 2:
                    # 蓝色
                    ys = b_values
                    ys2 = "blue"
                # 检查是否有近似重复值
                TF = False
                for t in range(len(ys)):
                    d = ys[t]
                    for j in range(20):
                        if ys.count(d + (j-10)) > (round(len(ys) / 2) / 2):
                            TF = True
                            if ys2 == "red":
                                r_fs[0] = "判决"
                                r_fs[1] = d
                                r_fs[2] = t
                            elif ys2 == "green":
                                g_fs[0] = "判决"
                                g_fs[1] = d
                                g_fs[2] = t
                            elif ys2 == "blue":
                                b_fs[0] = "判决"
                                b_fs[1] = d
                                b_fs[2] = t
                        if TF:
                            break
                    if TF:
                        break
                if not TF:
                    if ys2 == "red":
                        r_fs[0] = "跟风"
                        r_fs[1] = -1
                        r_fs[2] = -1
                    elif ys2 == "green":
                        g_fs[0] = "跟风"
                        g_fs[1] = -1
                        g_fs[2] = -1
                    elif ys2 == "blue":
                        b_fs[0] = "跟风"
                        b_fs[1] = -1
                        b_fs[2] = -1
            
            gf = 0
            pj = 0
            for kh in range(3):
                if kh == 0:
                    if r_fs[0] == "判决":
                        pj += 1
                    else:
                        gf += 1
                elif kh == 1:
                    if g_fs[0] == "判决":
                        pj += 1
                    else:
                        gf += 1
                elif kh == 2:
                    if b_fs[0] == "判决":
                        pj += 1
                    else:
                        gf += 1
            
            if gf > pj:
                TF = False
                if h > 0 and g > 0:
                    pj_o = int((img_xy[h - 1][g][0] + img_xy[h - 1][g][1] + img_xy[h - 1][g][2]) / 3)
                    pj_n = int((img_xy[h][g - 1][0] + img_xy[h][g - 1][1] + img_xy[h][g - 1][2]) / 3)
                    wc = pj_n - pj_o
                    if wc > -10 and wc < 10 and h > 0 and g > 0:
                        r_ys = int((img_xy[h - 1][g][0] + img_xy[h][g - 1][0]) / 2)
                        g_ys = int((img_xy[h - 1][g][1] + img_xy[h][g - 1][1]) / 2)
                        b_ys = int((img_xy[h - 1][g][2] + img_xy[h][g - 1][2]) / 2)
                    else:
                        TF = True
                else:
                    TF = True
                
                if TF:
                    # 随机选择一个值
                    sjys = random.randint(0,len(r_values)-1)
                    r_ys = r_values[sjys]
                    g_ys = g_values[sjys]
                    b_ys = b_values[sjys]
            else:
                if r_fs[0] == "判决":
                    r_ys = r_fs[1]
                else:
                    r_ys = r_values[random.choice([g_fs[2], b_fs[2]])]
                if g_fs[0] == "判决":
                    g_ys = g_fs[1]
                else:
                    g_ys = g_values[random.choice([r_fs[2], b_fs[2]])]
                if b_fs[0] == "判决":
                    b_ys = b_fs[1]
                else:
                    b_ys = b_values[random.choice([r_fs[2], g_fs[2]])]

            # 修改列表中的值
            img_xy[h][g][0] = r_ys
            img_xy[h][g][1] = g_ys
            img_xy[h][g][2] = b_ys
    # 生成完毕
    # 返回图像数据和实际最小尺寸
    return img_xy, min_width, min_height

# 生成图像数据
img_data, actual_width, actual_height = Waip_imgea("猫")

# 在函数外部保存图像到PNG文件
# 创建新图像 - 直接使用实际的最小尺寸
result_image = Image.new('RGB', (actual_width, actual_height))

# 设置像素值 - 直接使用实际的最小尺寸
for y in range(actual_height):
    for x in range(actual_width):
        # 将列表转换为元组并设置像素
        pixel_value = tuple(img_data[y][x])
        result_image.putpixel((x, y), pixel_value)

# 保存图片
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'generated_image.png')
result_image.save(save_path)
print(f"图片已成功保存到: {save_path}")


