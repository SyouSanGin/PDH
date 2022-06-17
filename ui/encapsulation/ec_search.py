import re
import requests


def search(word):
	url = "https://api.bilibili.com/x/web-interface/search/type?keyword=" + \
		word+"&search_type=video"
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"}
	data = requests.get(url=url, headers=headers).json()
	need = data["data"]["result"]
	next = list()
	for i in need:
		add = {}
		add["url"] = i["arcurl"]
		add["bvid"] = i["bvid"]
		add["title"] = i["title"]
		page = requests.get(url=add["url"], headers=headers).text
		cid = re.search("\"cid\":[0-9]+,", page)
		add["cid"] = cid.group()[6:-1]
		next.append(add)
	return next


if __name__ == "__main__":
	print(search("mmd"))