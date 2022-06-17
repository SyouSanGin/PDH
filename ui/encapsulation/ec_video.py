import json
import os
import re
import requests
from random import choice
from lxml import etree
import datetime

"""
添加了一些适配ui的功能
"""
"""
删除了一些无用的import
"""


__headers = {

    'Accept': '*/*',

    'Accept-Language': 'en-US,en;q=0.5',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'

}


def __get_user_agent():
  '''获取随机用户代理'''

  W_user_agents = [

      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",

      "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

      "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",

      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",

      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",

      "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",

      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",

      "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",

      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",

      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",

      "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",

      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",

      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",

      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",

      "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",

      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",

      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",

      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",

      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",

      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",

      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",

      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",

      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",

      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",

      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",

      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",

      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",

      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",

      "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",

      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",

      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",

      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",

      "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",

      "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",

      "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",

      "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",

      "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",

      "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",

      "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"

  ]

  # 在user_agent列表中随机产生一个代理，作为模拟的浏览器

  W_user_agent = choice(W_user_agents)

  return W_user_agent


def __re_video_info(W_text, W_pattern, lw):

    W_match = re.search(W_pattern, W_text)

    lw.log.append(W_match.group(1))
    lw.redraw = True

    return json.loads(W_match.group(1))


def __single_download(W_aid, W_acc_quality, lw):

    # 请求视频链接，获取信息

    W_origin_video_url = W_aid

    W_res = requests.get(W_origin_video_url, headers=__headers)

    W_html = etree.HTML(W_res.text)

    # W_title = W_html.xpath('//*[@id="viewbox_report"]/h1/span/text()')[0]


    """
    修改了title的生成方式
    """
    W_title = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + \
        str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + \
        str(datetime.datetime.now().second)
    lw.log.append('您当前正在下载：'+ str( W_title))
    lw.redraw = True
    W_video_info_temp = __re_video_info(
        W_res.text, '__playinfo__=(.*?)</script><script>',lw)

    W_video_info = {}

    # 获取视频质量

    W_quality = W_video_info_temp['data']['accept_description'][W_acc_quality]

    # 获取视频时长

    W_video_info['duration'] = W_video_info_temp['data']['dash']['duration']

    # 获取视频链接

    W_video_url = W_video_info_temp['data']['dash']['video'][W_acc_quality]['baseUrl']

    # 获取音频链接

    W_audio_url = W_video_info_temp['data']['dash']['audio'][W_acc_quality]['baseUrl']

    # 计算视频时长

    W_video_time = int(W_video_info.get('duration', 0))

    W_video_minute = W_video_time // 60

    W_video_second = W_video_time % 60

    lw.log.append('当前视频清晰度为{}，时长{}分{}秒'.format(
        W_quality, W_video_minute, W_video_second))
    lw.redraw = True

    __download_video_single(
        W_origin_video_url, W_video_url, W_audio_url, W_title,lw)


def __download_video_single(W_referer_url, W_video_url, W_audio_url, W_video_name, lw):
    '''单个视频下载'''

    """
    添加储存文件夹的检测，免得到时候又双叒叕TMD报错
    """
    if not os.path.exists("./savedData"):
        os.mkdir("./savedData")

    # 更新请求头

    __headers.update({"Referer": W_referer_url})

    lw.log.append("视频下载开始：%s" % W_video_name)
    lw.redraw = True

    # 下载并保存视频

    W_video_content = requests.get(W_video_url, headers=__headers)


    """
    这里修改了一下保存的路径
    """
    pathPrefix = "./savedData/"
    lw.log.append(f"{W_video_name}\t视频大小： {str(round(int(W_video_content.headers.get('content-length', 0)) / 1024 / 1024, 2))}"+'\tMB')
    lw.redraw = True

    received_video = 0

    with open(pathPrefix+'%s_video.mp4' % W_video_name, 'ab') as output:

        __headers['Range'] = 'bytes=' + str(received_video) + '-'

        response = requests.get(W_video_url, headers=__headers)

        output.write(response.content)

    # 下载并保存音频

    audio_content = requests.get(W_audio_url, headers=__headers)

    lw.log.append(f"{ W_video_name}\t音频大小：{round(int(audio_content.headers.get('content-length', 0)) / 1024 / 1024, 2)}" + '\tMB')
    lw.redraw = True

    received_audio = 0

    with open(pathPrefix+'%s_audio.mp3' % W_video_name, 'ab') as output:

        __headers['Range'] = 'bytes=' + str(received_audio) + '-'

        response = requests.get(W_audio_url, headers=__headers)

        output.write(response.content)

        received_audio += len(response.content)

    lw.log.append("视频下载结束：%s" % W_video_name)
    lw.redraw = True

    __video_audio_merge_single(W_video_name,lw)


def __video_audio_merge_single(W_video_name, lw):

    #'''使用ffmpeg单个视频音频合并'''
    lw.log.append("视频合成开始：%s" % W_video_name)
    lw.redraw = True
    import subprocess

    """
    修改了一下保存的路径
    """
    W_command = 'ffmpeg -i ./savedData/%s_video.mp4 -i ./savedData/%s_audio.mp3 -c copy ./savedData/%s.mp4 -y -loglevel quiet' % (
        W_video_name, W_video_name, W_video_name)

    subprocess.Popen(W_command, shell=True)

    lw.log.append("视频合成结束：%s" % W_video_name)
    lw.redraw = True

def execute(url, lw):
    """
    这里提供了一个可调用的部分
    """
    lw.log.append("视频下载启动")
    __single_download(url, 0, lw)

