from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from reportlab.graphics.shapes import Path
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing
import pytesseract
from PIL import Image


class ReportLabPen(BasePen):
    """A pen for drawing onto a reportlab.graphics.shapes.Path object."""

    def __init__(self, glyph_set, path=None):
        BasePen.__init__(self, glyph_set)
        if path is None:
            path = Path()
        self.path = path

    def _moveTo(self, p):
        (x, y) = p
        self.path.moveTo(x, y)

    def _lineTo(self, p):
        (x, y) = p
        self.path.lineTo(x, y)

    def _curveToOne(self, p1, p2, p3):
        (x1, y1) = p1
        (x2, y2) = p2
        (x3, y3) = p3
        self.path.curveTo(x1, y1, x2, y2, x3, y3)

    def _closePath(self):
        self.path.closePath()


def schedule(a, b, c):
    # a:已经下载的数据块
    # b:数据块的大小
    # c:远程文件的大小
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def ttf_to_image(font_path, image_path, fmt="png"):
    # 图片列表
    images = []

    # ttf文件
    font = TTFont(font_path)
    # 图集
    glyph_set = font.getGlyphSet()
    # 图名
    glyph_names = font.getGlyphNames()

    # 编号，用于记录程序进度
    n = 0
    # 处理每张图
    for i in glyph_names:
        n += 1

        # 跳过'.notdef', '.null'
        if i[0] == '.':
            continue

        # 图
        glyph = glyph_set[i]
        # 笔
        pen = ReportLabPen(glyph_set, Path(fillColor=colors.black, strokeWidth=5))
        # 图路径
        glyph.draw(pen)

        # 大小
        w, h = glyph.width, glyph.width
        glyph = Group(pen.path)
        glyph.translate(500, 600)
        glyph.scale(0.5, 0.5)

        # 画图
        drawer = Drawing(w, h)
        drawer.add(glyph)
        # 保存图片
        image_file = image_path + "/" + i + ".png"
        # renderPM.drawToFile(drawer, image_file, fmt)

        # 转换成PIL.Image.Image
        image = renderPM.drawToPIL(drawer)

        # 调整图片大小，并保持比例不变
        # 给定一个基本宽度
        base_width = 50
        # 基本宽度与原图宽度的比例
        w_percent = base_width / float(image.size[0])
        # 计算比例不变的条件下新图的长度
        h_size = int(float(image.size[1]) * float(w_percent))
        # 重新设置大小
        image = image.resize((base_width, h_size), Image.ANTIALIAS)

        # image.save(image_file, fmt)

        # 将图片加载到列表中
        images.append(image)

        # 显示进度
        schedule(n, 1, len(glyph_names))

    return images


def image_to_text(images):
    # 文字列表
    texts = []

    # image转text
    for j in images:
        text = pytesseract.image_to_string(j, lang='chi_sim', config='-psm 10')
        texts.append(text)

    return texts


if __name__ == '__main__':

    # .ttf路径
    my_font_path = '../../../../data/mouth_spider/mouth_data/01cjv944pg68rk2d9p6wr00000.ttf'
    # 保存图片路径
    my_image_path = '../../../../data/mouth_spider/picture'

    # .ttf转image
    my_images = ttf_to_image(font_path=my_font_path, image_path=my_image_path)

    # image转text
    my_texts = image_to_text(my_images)
    print(my_texts)
