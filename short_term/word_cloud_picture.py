import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from pymysql import *
import json

def get_address_img(targetImgSrc,resImgSrc):
    conn = connect(host='localhost', user='root', password='123456', database='hourses_data', port=3306)
    cursor = conn.cursor()
    sql = 'select address from hourse_info'
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for item in data:
        text += item[0]
    cursor.close()
    conn.close()

    cut = jieba.cut(text)
    string = ' '.join(cut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImgSrc,dpi=500)

def get_company_img(targetImgSrc,resImgSrc):
    conn = connect(host='localhost', user='root', password='123456', database='hourses_data', port=3306)
    cursor = conn.cursor()
    sql = 'select company from hourse_info'
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for item in data:
        text += item[0]
    cursor.close()
    conn.close()

    cut = jieba.cut(text)
    string = ' '.join(cut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImgSrc,dpi=500)

def get_tag_img(targetImgSrc,resImgSrc):
    conn = connect(host='localhost', user='root', password='123456', database='hourses_data', port=3306)
    cursor = conn.cursor()
    sql = 'select tags from hourse_info'
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for item in data:
        tags = json.loads(item[0])
        for tag in tags:
            text += tag
    cursor.close()
    conn.close()

    cut = jieba.cut(text)
    string = ' '.join(cut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImgSrc,dpi=500)


if __name__ == '__main__':
    # get_address_img('./static/1.jpg','./static/address_cloud.jpg')
    # get_company_img('./static/2.jpg','./static/company_cloud.jpg')
    get_tag_img('./static/3.jpg','./static/tag_cloud.jpg')