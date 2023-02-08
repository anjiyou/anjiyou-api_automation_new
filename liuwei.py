import pytesseract
from PIL import Image


class MapAnalyse(object):
    current_time = None
    current_coordinate = None
    average_speed = None
    distance_next = None
    next_guiding = None

    def __init__(self, current_time,current_coordinate,average_speed,distance_next,next_guiding,image):
        self.current_time = current_time
        self.current_coordinate = current_coordinate
        self.average_speed = average_speed
        self.distance_next = distance_next
        self.next_guiding = next_guiding
        self.image = image

    def get_color(self, x, y):
        """返回单个像素的颜色值"""
        return

    def get_width_height(self):
        image = Image.open(self.image)
        image = image.convert("RGB")
        width = image.size[0]
        height = image.size[1]
        return width, height

    def get_text(self, x_start: int, y_start: int, x_end: int, y_end: int):
        """"返回由x和y坐标定义的文本内"""
        image = Image.open(self.image)
        cropped = image.crop((x_start, y_start, x_end, y_end))
        picture_name = f"{x_start}_{y_start}_{x_end}_{y_end}.png"
        cropped.save(picture_name)
        image = Image.open(picture_name)
        text = pytesseract.image_to_string(image)
        return text

    def match_image(self, x_start, y_start, x_end, y_end, img_src):
        """如通过 x 和 y 坐标定义的矩形与 img_src 中的图像文件集匹配，则返回 false"""
        return


if __name__ == '__main__':
    map_analyser = MapAnalyse(r"D:\anjiyou-api_automation_new\map.png")
    width,height = map_analyser.get_width_height()
    text= map_analyser.get_text(0,0,int(width/2),int(height/2))
    print(text)