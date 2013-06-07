# --*-- coding:utf-8 --*--
__author__ = 'Administrator'
import random
import Image
import ImageDraw
import ImageFilter
import ImageFont

__author__ = 'Administrator'
def createValidateCode(size=(100,25),mode='RGB',font_size=18,length=4):
    '''
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''
    width,height = size
    def getRandColor(x,y):
        if x>255:
            x =255
        if y>255:
            y = 255
        r = x + random.randint(0,y-x)
        g = x + random.randint(0,y-x)
        b = x + random.randint(0,y-x)
        return (r,g,b)
    chars = 'ab1cd2ef3gh4ij5kl6mn7op8qr9st0uvwxyz'.upper()
    image = Image.new(mode,size,getRandColor(200,250))
    draw = ImageDraw.Draw(image)
    def get_chars():
        return random.sample(chars,length)
    def createLines():
        for x in xrange(50):
            w = random.randint(0,width)
            h = random.randint(0,height)
            offx = random.randint(0,12)
            offy = random.randint(0,12)
            draw.line([(w,h),(w+offx,h+offy)],fill=getRandColor(160,200))
    def createStrs():
        c_chars = get_chars()
        #font = ImageFont.load_default()
        font = ImageFont.truetype('ARIAL.TTF',font_size)
        i = 0
        for x in c_chars:
            dw,dh = font.getsize(x)
            draw.text((20*i+3,(height-dh)/3),x,font=font,fill=(40+random.randint(0,10),120+random.randint(0,10),170+random.randint(0,10)))
            i +=1
        return ''.join(c_chars)
    createLines()
    strs = createStrs()

    params = [1-float(random.randint(1,2))/100,
              0,
              0,
              0,
              1-float(random.randint(1,10))/100,
              float(random.randint(1,2))/500,
              0.001,
              float(random.randint(1,2))/500]
    image = image.transform(size,Image.PERSPECTIVE,params)
    #image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image,strs