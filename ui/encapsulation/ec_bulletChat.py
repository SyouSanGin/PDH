# -!- coding: utf-8 -!-
import requests
import re
import pandas as pd
import string
import jieba
import os

def __get_data(cid):
    # 分析网页，并获取网页文件
    url = 'https://comment.bilibili.com/{}.xml'.format(cid)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/80.0.3987.163Safari/537.36"
    }
    response = requests.get(url, headers=headers).content.decode('utf-8')
    return response


def __parse_html(W_response):
    # 解读网页文件，获取关键信息
    # soup = bs4.BeautifulSoup(response)
    # lst = [soup.find_all(name='d')]
    # danmuku = [i.text for i in lst]

    W_pattern = re.compile(r'<d p=".*?">(.*?)</d>')
    W_danmuku = re.findall(W_pattern, W_response)
    return W_danmuku


def __save_data(W_danmuku, W_cid):
    # 保存数据
    W_Dict = {
        'danmuku': W_danmuku
    }
    pd_data = pd.DataFrame(W_Dict)
    W_cid = str(W_cid)
    W_name = W_cid + 'bulletChatData.csv'
    
    # W_path = r'C:\Users\86183\Desktop\程序设计大作业\{}'.format(W_name)

    """
     这里我也改了一下
    """
    W_path = f"./savedData/{W_name}"

    # 防止文件夹不存在产生报错
    if not os.path.exists("./savedData"):
        os.mkdir("./savedData")

    """
    改utf-8-sig 为 utf-8
    """
    pd_data.to_csv(W_path, index=False, header=False,
                   mode='w', encoding='utf-8')


def __data_preprocess(danmuku, cid):
    cid = str(cid)
    name = cid + 'bulletChatData.csv'

    """
    WZL你坑我是不是。。。
    重新写了保存的目录，到时候就会直接保存在主程序目录下的savedData文件夹下面
    差点C盘被霍霍了（楽
    """
    # path = r'C:\Users\86183\Desktop\程序设计大作业\{}'.format(name)
    path = f"./savedData/{name}"

    with open(path, mode='r', encoding='utf-8') as f:
        # 加载用户自定义字典
        #jieba.load_userdict(r'D:\爬虫\userdict')
        reader = f.read().replace('\n', '')
        # 加载停用词词表
        stopwords = []  # line.strip() for line in
        #open(r'D:\爬虫\stop_wordslst', encoding='gbk').readlines()]
        # 去标点，去数字，去空白
        pun_num = string.punctuation + string.digits
        table = str.maketrans('', '', pun_num)
        reader = reader.translate(table)
        seg_list = jieba.cut(reader, cut_all=False)
        sentence = ''
        for word in seg_list:
            if word not in stopwords and word.isspace() == False:
                sentence += word
                sentence += ','
        sentence = sentence[:-1]
        return sentence


def __count_words(txt, cid):
    cid = str(cid)
    # name = cid + u'countForBulletChat.csv'
    name = cid + u'countForBulletChat'
    """
    为了适应我之前的修改，这里我也进行了修改
    同时为了让两个文件在一个文件夹下面，我把open()中的文件名也做了些修改
    """

    #path = 'D:\爬虫\{}'.format(name)
    aDict = {}
    words = txt.split(',')
    for word in words:
        aDict[word] = aDict.get(word, 0) + 1
    #pd_count = pd.DataFrame(aDict, index=['times']).T.sort_values('times', ascending=False)
    #pd_count.to_csv(path,encoding='utf-8')

    """
    我把编码改成了utf_8,之前也是以这个保存的
    """
    with open("./savedData/"+name + '.csv', mode='w', encoding='utf_8') as f:
        d_order = sorted(aDict.items(), key=lambda x: x[1], reverse=True)
        #print(d_order)
        for i in d_order:
            for j in i:
                try:
                    f.write(str(j))
                    #print(str(j))
                    f.write(' ')
                except:
                    break
            f.write('\n')

def execute(cid, lw):
    lw.log.append("开始获取弹幕数据")
    lw.redraw = True
    resp = __get_data(cid)
    bcData = __parse_html(resp)
    __save_data(bcData,cid)
    sentence = __data_preprocess(bcData, cid)
    __count_words(sentence, cid)


