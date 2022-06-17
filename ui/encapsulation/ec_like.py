import requests


def __get_info(av):
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/vidio/av' + av,
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/78.0.3904.108 ' +
            'Safari/537.36'
    }
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + av
    info_rsp = requests.get(url=url, headers=headers)
    info_json = info_rsp.json()
    information = {
        'view': "播放",
        'danmaku': "弹幕",
        'favorite': "收藏",
        'coin': "投币",
        'share': "分享",
        'like': "点赞"
    }

    """
    这里我对保存的目录进行了一定的修改
    """
    with open("./savedData/"+av + '_information.txt', 'w', encoding='utf-8') as fp:
        for i in information:
            try:
                fp.write("{}：{}\n".format(
                    information[i], info_json['data'][i]))
            except TypeError:
                fp.write('Cannot find av' + av)
                break
            except:
                fp.write('Error!')
                break


def __get_info_bv(bv):
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/vidio/' + bv,
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/78.0.3904.108 ' +
            'Safari/537.36'
    }
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + bv
    info_rsp = requests.get(url=url, headers=headers)
    info_json = info_rsp.json()
    information = {
        'view': "播放",
        'danmaku': "弹幕",
        'favorite': "收藏",
        'coin': "投币",
        'share': "分享",
        'like': "点赞"
    }

    """
    这里我对保存的目录进行了一定的修改
    """
    with open("./savedData/"+bv + '_information.txt', 'w', encoding='utf-8') as fp:
        for i in information:
            try:
                fp.write("{}：{}\n".format(
                    information[i], info_json['data'][i]))
            except TypeError:
                fp.write('Cannot find av' + bv)
                break
            except:
                fp.write('Error!')
                break

def execute_av(av):
    __get_info(av)

def execute_bv(bv):
    __get_info_bv(bv)

def execute_bv_notSave(bv):
    """
    这个方法是我重新写的一个获取点赞数等信息的方法
    这个方法不会保存数据到磁盘里面去
    但是通过返回值的类型把数据返回
    """
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/vidio/' + bv,
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/78.0.3904.108 ' +
            'Safari/537.36'
    }
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid=' + bv
    info_rsp = requests.get(url=url, headers=headers)
    info_json = info_rsp.json()
    information = {
        'view': "播放",
        'danmaku': "弹幕",
        'favorite': "收藏",
        'coin': "投币",
        'share': "分享",
        'like': "点赞"
    }

    """
    注意返回的json的有效信息都是在 data 这个tag下的
    下方是一段示例返回值
    {
        'code': 0,
        'message': '0', 
        'ttl': 1, 
        'data': {
            'aid': 597544224, 
            'bvid': 'BV1eB4y1S7u8', 
            'view': 58463, 
            'danmaku': 185, 
            'reply': 290, 
            'favorite': 1727, 
            'coin': 2952, 
            'share': 310, 
            'like': 4923, 
            'now_rank': 0, 
            'his_rank': 0, 
            'no_reprint': 1, 
            'copyright': 1, 
            'argue_msg': '', 
            'evaluation': ''
            }
    }
    """

    """
    这里我生成一个字典，用来返回我需要的数据
    """
    rtDic = {
        "view":info_json["data"]["view"],
        "danmaku": info_json["data"]["danmaku"],
        "favorite": info_json["data"]["favorite"],
        "coin": info_json["data"]["coin"],
        "share": info_json["data"]["share"],
        "like": info_json["data"]["like"],
        }

    return rtDic