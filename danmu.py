# -!- coding: utf-8 -!-
import requests
import re
import pandas as pd
import string
import jieba


def get_data(cid):
    # 分析网页，并获取网页文件
    url = 'https://comment.bilibili.com/{}.xml'.format(cid)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/80.0.3987.163Safari/537.36"
    }
    response = requests.get(url, headers=headers).content.decode('utf-8')
    return response

def parse_html(W_response):
    # 解读网页文件，获取关键信息
    # soup = bs4.BeautifulSoup(response)
    # lst = [soup.find_all(name='d')]
    # danmuku = [i.text for i in lst]

    W_pattern = re.compile(r'<d p=".*?">(.*?)</d>')
    W_danmuku = re.findall(W_pattern, W_response)
    return W_danmuku


def save_data(W_danmuku, W_cid):
    # 保存数据
    W_Dict = {
        'danmuku': W_danmuku
    }
    pd_data = pd.DataFrame(W_Dict)
    W_cid = str(W_cid)
    W_name = W_cid + '弹幕文件.csv'
    W_path = r'C:\Users\86183\Desktop\程序设计大作业\{}'.format(W_name)
    pd_data.to_csv(W_path, index=False, header=False, mode='w', encoding='utf-8-sig')


def data_preprocess(danmuku, cid):
    cid = str(cid)
    name = cid + '弹幕文件.csv'
    path = r'C:\Users\86183\Desktop\程序设计大作业\{}'.format(name)
    with open(path , mode='r', encoding='utf-8') as f:
        # 加载用户自定义字典
        #jieba.load_userdict(r'D:\爬虫\userdict')
        reader = f.read().replace('\n', '')
        # 加载停用词词表
        stopwords = []#line.strip() for line in
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


def count_words(txt, cid):
    cid = str(cid)
    name = cid + '弹幕词汇数统计.csv'
    #path = 'D:\爬虫\{}'.format(name)
    aDict = {}
    words = txt.split(',')
    for word in words:
        aDict[word] = aDict.get(word, 0) + 1
    #pd_count = pd.DataFrame(aDict, index=['times']).T.sort_values('times', ascending=False)
    #pd_count.to_csv(path,encoding='utf-8')
    with open(name + '.csv',mode = 'w',encoding='gbk') as f:
        d_order=sorted(aDict.items(),key=lambda x:x[1],reverse=True)
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


def Main():
    import PySimpleGUI as sg
    import sys
    layout = [
        [sg.T('请输入cid')],
        [sg.Input('')],
        [sg.B('确认'), sg.B('取消')]
    ]

    window = sg.Window('自定义网址界面', layout)
    flag = 0
    while True:
        event, values = window.read()
        if event == None:
            break
        if event == '取消':
            break
        if event == '确认':
            flag = 1
            break

    window.close()
    if flag == 0:
        sys.exit()

    W_cid = values[0]
    #cid = int(input('请输入你想查询的视频CID号：'))
    W_response = get_data(W_cid)
    W_danmuku = parse_html(W_response)
    save_data(W_danmuku, W_cid)
    W_sentence = data_preprocess(W_danmuku, W_cid)
    count_words(W_sentence, W_cid)