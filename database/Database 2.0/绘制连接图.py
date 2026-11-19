import json
import os

from PIL import Image, ImageDraw


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(current_dir, '临时文件夹')
    out_dir = os.path.join(current_dir, '连接图')
    os.makedirs(out_dir, exist_ok=True)

    # 按图片序号排序，读取所有边缘数据 json
    filenames = sorted(
        (f for f in os.listdir(json_dir) if f.startswith('边缘数据_') and f.endswith('.json')),
        key=lambda f: int(f[len('边缘数据_'):-len('.json')]),
    )
    if not filenames:
        print(f'未找到边缘数据 json：{json_dir}')
        return

    for filename in filenames:
        json_path = os.path.join(json_dir, filename)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        width, height = data['图片尺寸']
        # 纯白底图，不叠加原图
        img = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # 边缘像素数据为 [行, 列]，绘制时转换为 (x, y)
        for row, col in data['边缘像素']:
            draw.point((col, row), fill=(180, 180, 180))

        # 连接数据为 [行1, 列1, 行2, 列2]
        for row1, col1, row2, col2 in data['连接']:
            draw.line((col1, row1, col2, row2), fill=(0, 0, 0), width=1)

        out_path = os.path.join(out_dir, f'连接图_{data["图片序号"]}.png')
        img.save(out_path)
        img.close()
        print(f'已生成连接图 {out_path}')
        print(f'  边缘像素 {len(data["边缘像素"])} 个，连接 {len(data["连接"])} 条')

    print(f'\n全部完成，结果保存在：{out_dir}')


main()
