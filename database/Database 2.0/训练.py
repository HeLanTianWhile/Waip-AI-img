from PIL import Image, ImageDraw
import os
import copy


def main():
    # 训练Waip AI
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, '训练data', input("请输入训练数据的文件夹名："))
    # 遍历数据库中的所有文件目录
    img_list = []
    width_list = []
    height_list = []
    
    # 第一步：收集所有图片的尺寸信息
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        img = Image.open(image_path)
        img = img.convert("RGBA")
        width, height = img.size
        width_list.append(width)
        height_list.append(height)
        img.close()
    
    # 计算最小尺寸
    min_width = min(width_list)
    min_height = min(height_list)
    print(f"所有图片的最小尺寸：{min_width}x{min_height}")
    
    # 第二步：将所有图片调整为最小尺寸
    resized_img_list = []
    for filename in os.listdir(path):
        image_path = os.path.join(path, filename)
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        # 使用PIL的resize方法调整图片尺寸
        resized_img = img.resize((min_width, min_height), Image.Resampling.LANCZOS)
        
        # 获取调整后的像素数据
        pixels = list(resized_img.getdata())
        # 将一维像素列表转换为二维列表
        resized_pixels = [pixels[i*min_width:(i+1)*min_width] for i in range(min_height)]
        resized_img_list.append(resized_pixels)
        
        img.close()
        resized_img.close()
        
        print(f"已将图片 {filename} 调整为 {min_width}x{min_height}")
    
    print(f"\n所有图片已成功调整为 {min_width}x{min_height}")
    print(f"共处理 {len(resized_img_list)} 张图片")
    
    # 正片开始！！！
    print('边缘检测开始')
    lk = []
    fm = 1
    mk = 100
    # 先遍历每张图片
    for h in resized_img_list:
        # 为当前图片创建一个二级列表
        img_pixels = {}
        # 再遍历图片的每个像素
        for k in range(min_height):
            for i in range(min_width):
                if k < fm or k > min_height-fm-1 or i < fm or i > min_width-fm-1:
                    continue
                for yu in range(100):
                    sz = 0
                    for yh in range(4):
                        ssz = 0
                        if ((h[k][i][yh] - h[k][i-fm][yh]) > mk) or ((h[k][i][yh] - h[k][i-fm][yh]) < -mk):
                            ssz += 1
                        if ((h[k][i][yh] - h[k][i+fm][yh]) > mk) or ((h[k][i][yh] - h[k][i+fm][yh]) < -mk):
                            ssz += 1
                        if ((h[k][i][yh] - h[k-fm][i][yh]) > mk) or ((h[k][i][yh] - h[k-fm][i][yh]) < -mk):
                            ssz += 1
                        if ((h[k][i][yh] - h[k+fm][i][yh]) > mk) or ((h[k][i][yh] - h[k+fm][i][yh]) < -mk): 
                            ssz += 1
                        if ssz >= 2:
                            sz += 1
                    if sz >= 3:
                        print(f'当前像素 {k, i} 是边缘像素')
                        img_pixels.append([k, i])
                    else:
                        print(f'当前像素 {k, i} 不是边缘像素')
                    mk -= 1
        # 将当前图片的结果添加到主列表
        lk.append(img_pixels)
    print('降噪开始')
    oiiaioiia = copy.deepcopy(lk)
    for ni in [4] * 4:
        for o in range(len(oiiaioiia)):
            print(f'当前图片 {o+1} 降噪开始')
            # 将列表转换为元组集合以便快速查找
            pixel_set = set(tuple(p) for p in oiiaioiia[o])
            for p in oiiaioiia[o]:
                cs = 0
                if (p[0]+1, p[1]) in pixel_set:
                    cs += 1
                if (p[0]-1, p[1]) in pixel_set:
                    cs += 1
                if (p[0], p[1]+1) in pixel_set:
                    cs += 1
                if (p[0], p[1]-1) in pixel_set:
                    cs += 1
                if cs <= ni:
                    oiiaioiia[o].remove(p)
    lk = copy.deepcopy(oiiaioiia)
    ec = []
    for iu in lk:
        ec.append([])
        for oi in height:
            pass
    print(lk)
    
    # 保存结果到临时文件夹
    def save_results():
        # 创建临时文件夹
        temp_folder = os.path.join(current_dir, '临时文件夹')
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            print(f"已创建临时文件夹: {temp_folder}")
        
        # 获取所有图片的路径
        image_paths = [os.path.join(path, filename) for filename in os.listdir(path)]
        
        # 处理每张图片
        for idx, (img_path, edge_pixels) in enumerate(zip(image_paths, lk)):
            # 打开并调整图片大小
            img = Image.open(img_path).convert("RGBA")
            resized_img = img.resize((min_width, min_height), Image.Resampling.LANCZOS)
            
            # 保存原图
            original_filename = f"原图_{idx+1}.png"
            original_path = os.path.join(temp_folder, original_filename)
            resized_img.save(original_path)
            
            # 创建带描边的图片
            draw_img = resized_img.copy()
            draw = ImageDraw.Draw(draw_img)
            
            # 标记边缘像素点（使用红色小点）
            for pixel in edge_pixels:
                x, y = pixel
                draw.ellipse((x-2, y-2, x+2, y+2), fill=(255, 0, 0, 255))
            
            # 保存带描边的图片
            edge_filename = f"描边_{idx+1}.png"
            edge_path = os.path.join(temp_folder, edge_filename)
            draw_img.save(edge_path)
            
            print(f"已保存图片 {idx+1}: {original_filename} 和 {edge_filename}")
            
            # 关闭图片
            img.close()
            resized_img.close()
            draw_img.close()
        
        print(f"\n所有结果已保存到临时文件夹: {temp_folder}")
    
    # 调用保存函数
    save_results()
    
main()
input("按下任意键结束")