import urllib.request
import http.cookiejar
import hashlib
import log
import config
import json
from betelgeuse import Betelgeuse

options = config.options
logger = log.logger()


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
		'Cookie': 'pgv_pvi=3125944320; pgv_si=s3699565568; fts=1440563200; sid=639eso63; LIVE_BUVID=c9d691d803f02630e8f080d527aa6716; LIVE_BUVID__ckMd5=6c1f0b546d46cc6f; DedeUserID=252152; DedeUserID__ckMd5=f1c32e768f29d468; SESSDATA=0d9059a5%2C1456986269%2Cf7299ccc; IESESSION=alive; user_face=http%3A%2F%2Fi1.hdslb.com%2Fuser%2F2521%2F252152%2Fmyface.jpg; LIVE_LOGIN_DATA=3f0dc76243fc4135b10ad5d76a9c7f8345962cce; LIVE_LOGIN_DATA__ckMd5=65a5291e167a8111; DedeID=3180622; rlc_time=1456823609703; _cnt_dyn=null; _cnt_pm=0; _cnt_notify=4; uTZ=-480; CNZZDATA2724999=cnzz_eid%3D1046512906-1440563100-null%26ntime%3D1456828381'
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

	def search(self, keyword, page=1, order="default", pagesize=20):
		params = {}
		params['keyword'] = keyword
		params['order'] = order
		params['pagesize'] = pagesize
		params['page'] = page

		sign = self.get_sign(params)
		logger.info("get: " + self.__urls["search"] + "?" + sign)
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

	def build_url(self, avid, api="h5", page=1):
		return self.__urls["cloudmoe"] + ("?api={0}&id={1}&page={2}".format(api, avid, page))

	def build_h5_url(self, avid, page=1):
		return self.build_url(avid=avid, api="h5", page=1)

	def build_h5_hd_url(self, avid, page=1):
		return self.build_url(avid=avid, api="h5_hd", page=1)

	def build_h5_low_url(self, avid, page=1):
		return self.build_url(avid=avid, api="h5_low", page=1)

	def sort_params(params):
		data = "";
		paras = params;
		for para in paras:
			if data != "":
					data += "&";
			data += para + "=" + str(params[para]);
		return data

	def build_download_url(self, cid, page=1, overseas=False, type="mp4"):
		url_get_media = self.__urls["playurl"] if not overseas else self.__urls["playurl"]

		media_args = {'otype': 'json', 'cid': cid, 'type': 'mp4', 'quality': 4, 'appkey': self.appkey}
		url = url_get_media + "?" +Bellatrix.sort_params(media_args)
		logger.info("get: " + url)
		res = self.opener.open(url).read()
		result = json.loads(res.decode())
		if result["result"] == "error":
			return ''
		return  result['durl'][0]['url']

	def view(self, avid, page=1):
		params = {'id': avid,'page': page}
		sign = self.get_sign(params)

		logger.info("get: " + self.__urls["view"] + "?" + sign)
		print("get: " + self.__urls["view"] + "?" + sign)
		res = self.opener.open(self.__urls["view"] + "?" + sign).read()
		print("view: ")
		print(json.loads(res.decode()))
		return Subject(json.loads(res.decode()))