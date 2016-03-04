import urllib.request
import http.cookiejar
import hashlib
import log
import config
import json
from betelgeuse import Betelgeuse
from urllib.parse import urlparse, parse_qs

class Subject():
    def __init__(self, d):
        self.__dict__ = d

class Planet:

	def __init__(self):
		self.init_opener()

	def init_opener(self, head = {
		'Connection': 'Keep-Alive',
		'Accept': 'text/html, application/xhtml+xml, */*',
		'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Cookie': config.options.cookie
		}):
		self.head = head
		self.opener = urllib.request.build_opener()
		header = []
		for key, value in head.items():
				elem = (key, value)
				header.append(elem)
		self.opener.addheaders = header
		return self.opener


class Bellatrix(Planet):

	timeout = 100

	__urls = {
		"search": "http://api.bilibili.cn/search",
		"view": "http://api.bilibili.cn/view",
		"userinfo": "http://api.bilibili.cn/userinfo",
		"cloudmoe": 'http://bilibili.cloudmoe.com',
		"playurl": "http://interface.bilibili.com/playurl",
		"v_cdn_play": "http://interface.bilibili.com/v_cdn_play"
	}

	def __init__(self, appkey, appsecret=None):
		super(Bellatrix, self).__init__()
		self.appkey = appkey
		self.appsecret = appsecret


	def get_sign(self, params):
		"""
		获取新版API的签名，不然会返回-3错误
		"""
		params['appkey'] = self.appkey
		data = ""
		paras = sorted(params.keys())
		for para in paras:
				if data != "":
						data += "&"
				data += para + "=" + str(urllib.parse.quote(str(params[para])))
		if self.appsecret == None:
				return data
		m = hashlib.md5()
		m.update( (data+self.appsecret).encode('utf-8') )
		return data+'&sign='+m.hexdigest()

	def search(self, keyword, page=1, order="default", pagesize=100):
		params = {}
		params['keyword'] = keyword
		params['order'] = order
		params['pagesize'] = pagesize
		params['page'] = page

		sign = self.get_sign(params)
		log.logger().info("get: " + self.__urls["search"] + "?" + sign)
		res = self.opener.open(self.__urls["search"] + "?" + sign).read()
		res_json = json.loads(res.decode())
		if res_json["code"] == 0:
			return Subject({
					"is_done": res_json["code"] == 0,
					"pagesize": res_json["pagesize"],
					"page": res_json["page"],
					"total": res_json["total"],
					"result": res_json["result"]
				})
		else:
			return Subject({"is_done": res_json["code"] == 0})

	def sort_params(params):
		data = "";
		paras = params;
		for para in paras:
			if data != "":
					data += "&";
			data += para + "=" + str(params[para]);
		return data

	def build_download_url(self, cid, overseas=False, type="mp4"):
		url_get_media = self.__urls["playurl"] if not overseas else self.__urls["playurl"]

		media_args = {'otype': 'json', 'cid': cid, 'type': 'mp4', 'quality': 4, 'appkey': self.appkey}
		url = url_get_media + "?" +Bellatrix.sort_params(media_args)
		log.logger().info("get: " + url)
		res = self.opener.open(url).read()
		result = json.loads(res.decode())
		log.logger().info(result)
		if (result is None) or (result["result"] == "error"):
			return '', 0
		download_url = result['durl'][0]['url']
		params = parse_qs(urlparse(download_url).query)
		expires = 0
		if "expires" in params:
			expires = params["expires"][0]
		elif "wsTime" in params:
			expires = params["wsTime"][0]
		elif "tm" in params:
			expires = params["tm"][0]
		log.logger().info("download_url: {}, expires: {}".format(download_url, expires))
		return  download_url, expires

	def view(self, avid, page=1):
		params = {'id': avid,'page': page}
		sign = self.get_sign(params)

		log.logger().info("get: " + self.__urls["view"] + "?" + sign)
		res = self.opener.open(self.__urls["view"] + "?" + sign).read()
		return Subject(json.loads(res.decode()))

if __name__ == "__main__":
	options = config.options
	b = Bellatrix(options.appkey, options.appsecret)
	b.build_download_url(3439258)