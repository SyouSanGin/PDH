import requests


def get_info(av):
    headers = {
        'Host' : 'api.bilibili.com',
        'Referer' : 'https://www.bilibili.com/vidio/av' + av,
        'User-Agent' :
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/78.0.3904.108 ' +
            'Safari/537.36'
    }
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + av
    info_rsp = requests.get(url = url, headers = headers)
    info_json = info_rsp.json()
    information = {
        'view'     : "播放",
        'danmaku'  : "弹幕",
        'favorite' : "收藏",
        'coin'     : "投币",
        'share'    : "分享",
        'like'     : "点赞"
    }
    with open(av + '_information.txt', 'w', encoding = 'utf-8') as fp:
        for i in information:
            try:
                fp.write("{}：{}\n".format(information[i], info_json['data'][i]))
            except TypeError:
                fp.write('Cannot find av' + av)
                break
            except:
                fp.write('Error!')
                break


def main():
    while True:
        av = input('Please enter the av of the vidio: ')
        '''
        try:
            k = int(av)
            if 10000000 < k < 99999999:
                pass
            else:
                break
        except:
            break
        '''
        get_info(av)


if __name__ == '__main__':
    main()