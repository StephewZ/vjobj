#coding=utf8
import time
import urllib
import json
import hashlib
import random
import threading
import pycurl
import requests
import io
import xml.etree.ElementTree as ET

from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render_to_response, redirect, render
from django.views.decorators.csrf import csrf_exempt

class WxPayConf_pub(object):
    """配置账号信息"""

    #=======【基本信息设置】=====================================
    #微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    APPID = "wx15286249fc2de8b6"
    #JSAPI接口中获取openid，审核后在公众平台开启开发模式后可查看
    APPSECRET = "5e19880e71db23d9aca81530cb3843ee"
    #接口配置token
    TOKEN = "brain"
    #受理商ID，身份标识
    MCHID = "1428287802"
    #商户支付密钥Key。审核通过后，在微信发送的邮件中查看
    KEY = "ReY4xPjF3OYVS3AJmZ2tH7t9VmiD2fZJ"
   

    #=======【异步通知url设置】===================================
    #异步通知url，商户根据实际开发过程设定
    NOTIFY_URL = "powerbank.gzncloud.com/pay/payback_url"

    #=======【证书路径设置】=====================================
    #证书路径,注意应该填写绝对路径
    SSLCERT_PATH = "/******/cacert/apiclient_cert.pem"
    SSLKEY_PATH = "/******/cacert/apiclient_key.pem"

    #=======【curl超时设置】===================================
    CURL_TIMEOUT = 30

    #=======【HTTP客户端设置】===================================
    HTTP_CLIENT = "CURL"  # ("URLLIB", "CURL", "REQUESTS")

class BaseHttpClient(object):
    include_ssl = False

    def get(self, url, second=30):
        if self.include_ssl:
            return self.postXmlSSL(None, url, second, False, False)
        else:
            return self.postXml(None, url, second)

    def postXml(self, xml, url, second=30):
        if self.include_ssl:
            return self.postXmlSSL(xml, url, second, cert=False)
        else:
            raise NotImplementedError("please implement postXML")

    def postXmlSSL(self, xml, url, second=30, cert=True, post=True):
        raise NotImplementedError("please implement postXMLSSL")

class Singleton(object):
    """可配置单例模式"""

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    impl = cls.configure() if hasattr(cls, "configure") else cls
                    instance = super(Singleton, cls).__new__(impl, *args, **kwargs)
                    if not isinstance(instance, cls):
                        instance.__init__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance

class UrllibClient(BaseHttpClient):
    """使用urlib2发送请求"""
    def postXml(self, xml, url, second=30):
        """不使用证书"""
        data = urllib.request.urlopen(url, xml, timeout=second).read()
        return data

class CurlClient(BaseHttpClient):
    """使用Curl发送请求"""
    include_ssl = True

    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.SSL_VERIFYHOST, False)
        self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
        #设置不输出header
        self.curl.setopt(pycurl.HEADER, False)

    def postXmlSSL(self, xml, url, second=30, cert=False, post=True):
        """使用证书"""
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.TIMEOUT, second)
        #设置证书
        #使用证书：cert 与 key 分别属于两个.pem文件
        #默认格式为PEM，可以注释
        if cert:
            self.curl.setopt(pycurl.SSLKEYTYPE, "PEM")
            self.curl.setopt(pycurl.SSLKEY, WxPayConf_pub.SSLKEY_PATH)
            self.curl.setopt(pycurl.SSLCERTTYPE, "PEM")
            self.curl.setopt(pycurl.SSLCERT, WxPayConf_pub.SSLCERT_PATH)
        #post提交方式
        if post:
            self.curl.setopt(pycurl.POST, True)
            self.curl.setopt(pycurl.POSTFIELDS, xml.encode("utf-8"))
        buff = io.BytesIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buff.write)

        self.curl.perform()
        return buff.getvalue()

class RequestsClient(BaseHttpClient):
    include_ssl = True

    def postXmlSSL(self, xml, url, second=30, cert=True, post=True):
        if cert:
            cert_config = (WxPayConf_pub.SSLCERT_PATH, WxPayConf_pub.SSLKEY_PATH)
        else:
            cert_config = None
        if post:
            res = requests.post(url, data=xml, second=30, cert=cert_config)
        else:
            res = requests.get(url, timeout=second, cert=cert_config)
        return res.content

class HttpClient(Singleton, BaseHttpClient):
    @classmethod
    def configure(cls):
        config_client =  WxPayConf_pub.HTTP_CLIENT
        client_cls = {"urllib": UrllibClient,
                      "curl": CurlClient,
                      "requests": RequestsClient}.get(config_client.lower(), None)
        if client_cls:
            return client_cls

        if pycurl is not None:
            print("HTTP_CLIENT config error, Use 'CURL'")
            return CurlClient
        if requests is not None:
            print("HTTP_CLIENT config error, Use 'REQUESTS'")
            return RequestsClient
        else:
            print("HTTP_CLIENT config error, Use 'URLLIB'")
            return UrllibClient

class WeixinHelper(object):
    @classmethod
    def checkSignature(cls, signature, timestamp, nonce):
        """微信对接签名校验"""
        tmp = [WxPayConf_pub.TOKEN, timestamp, nonce]
        tmp.sort()
        code = hashlib.sha1("".join(tmp)).hexdigest()
        return code == signature

    @classmethod
    def nonceStr(cls, length):
        """随机数"""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @classmethod
    def xmlToArray(cls, xml):
        """将xml转为array"""
        return dict((child.tag, child.text) for child in ET.fromstring(xml))

    @classmethod
    def oauth2(cls, redirect_uri, scope="snsapi_userinfo", state="STATE"):
        """网页授权获取用户信息
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """
        #_OAUTH_URL = "http://weixin.gzncloud.com/get-weixin-code.html?appid={0}&scope=snsapi_base&state=STATE&redirect_uri={1}"
        _OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope={2}&state={3}#wechat_redirect"
        return _OAUTH_URL.format(WxPayConf_pub.APPID, urllib.parse.quote(redirect_uri), scope, state)

    @classmethod
    def getAccessToken(cls):
        """获取access_token
        需要缓存access_token,由于缓存方式各种各样，不在此提供
        http://mp.weixin.qq.com/wiki/11/0e4b294685f817b95cbed85ba5e82b8f.html
        """
        _ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
        return HttpClient().get(_ACCESS_URL.format(WxPayConf_pub.APPID, WxPayConf_pub.APPSECRET))


    @classmethod
    def getUserInfo(cls, access_token, openid, lang="zh_CN"):
        """获取用户基本信息
        http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        """
        _USER_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang={2}"
        return HttpClient().get(_USER_URL.format(access_token, openid, lang))

    @classmethod
    def getAccessTokenByCode(cls, code):
        """通过code换取网页授权access_token, 该access_token与getAccessToken()返回是不一样的
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """
        _CODEACCESS_URL = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
        return HttpClient().get(_CODEACCESS_URL.format(WxPayConf_pub.APPID, WxPayConf_pub.APPSECRET, code))

    @classmethod
    def refreshAccessToken(cls, refresh_token):
        """刷新access_token, 使用getAccessTokenByCode()返回的refresh_token刷新access_token，可获得较长时间有效期
        http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        """
        _REFRESHTOKRN_URL = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={0}&grant_type=refresh_token&refresh_token={1}"
        return HttpClient().get(_REFRESHTOKRN_URL.format(WxPayConf_pub.APPID, refresh_token))


    @classmethod
    def getSnsapiUserInfo(cls, access_token, openid, lang="zh_CN"):
        """拉取用户信息(通过网页授权)
        """
        _SNSUSER_URL = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang={2}"
        return HttpClient().get(_SNSUSER_URL.format(access_token, openid, lang))

    @classmethod
    def send(cls, data, access_token):
        """发送客服消息
        http://mp.weixin.qq.com/wiki/1/70a29afed17f56d537c833f89be979c9.html
        """
        _SEND_URL ="https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}"
        data = json.dumps(data, ensure_ascii=False)
        return HttpClient().postXml(data, _SEND_URL.format(access_token))

    @classmethod
    def sendTextMessage(cls, openid, message, access_token):
        """发送文本消息
        """
        data = {
            "touser": openid,
            "msgtype":"text",
            "text":
            {
                "content": message
            }
        }
        return cls.send(data, access_token)

    @classmethod
    def getJsapiTicket(cls, access_token):
        """获取jsapi_tocket
        """
        _JSAPI_URL = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi"
        return HttpClient().get(_JSAPI_URL.format(access_token))


    @classmethod
    def jsapiSign(cls, jsapi_ticket, url):
        """jsapi_ticket 签名"""
        sign = {
            'nonceStr': cls.nonceStr(15),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': int(time.time()),
            'url': url
        }
        signature = '&'.join(['%s=%s' % (key.lower(), sign[key]) for key in sorted(sign)])
        sign["signature"] = hashlib.sha1(signature).hexdigest()
        return sign

class Common_util_pub(object):
    """所有接口的基类"""

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def createNoncestr(self, length = 32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        #签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        #签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String,WxPayConf_pub.KEY)
        #签名步骤三：MD5加密

        String = hashlib.md5(String.encode("utf-8")).hexdigest()
        #签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_

    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.items(): #pyhton2 iteritems
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xmlToArray(self, xml):
        """将xml转为array"""
        return WeixinHelper.xmlToArray(xml)

    def postXmlCurl(self, xml, url, second=30):
        """以post方式提交xml到对应的接口url"""
        return HttpClient().postXml(xml, url, second=second)

    def postXmlSSLCurl(self, xml, url, second=30):
        """使用证书，以post方式提交xml到对应的接口url"""
        return HttpClient().postXmlSSL(xml, url, second=second)

class JsApi_pub(Common_util_pub):
    """JSAPI支付——H5网页端调起支付接口"""
    code = None    #code码，用以获取openid
    openid = None  #用户的openid
    parameters = None  #jsapi参数，格式为json
    prepay_id = None #使用统一支付接口得到的预支付id
    curl_timeout = None #curl超时时间

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        self.curl_timeout = timeout

    def createOauthUrlForCode(self, redirectUrl):
        """生成可以获得code的url"""
        urlObj = {}
        urlObj["appid"] = WxPayConf_pub.APPID
        urlObj["redirect_uri"] = redirectUrl
        urlObj["response_type"] = "code"
        urlObj["scope"] = "snsapi_base"
        urlObj["state"] = "STATE#wechat_redirect"
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://open.weixin.qq.com/connect/oauth2/authorize?"+bizString

    def createOauthUrlForOpenid(self):
        """生成可以获得openid的url"""
        urlObj = {}
        urlObj["appid"] = WxPayConf_pub.APPID
        urlObj["secret"] = WxPayConf_pub.APPSECRET
        urlObj["code"] = self.code
        urlObj["grant_type"] = "authorization_code"
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://api.weixin.qq.com/sns/oauth2/access_token?"+bizString

    def getOpenid(self):
        """通过curl向微信提交code，以获取openid"""
        url = self.createOauthUrlForOpenid()
        data = HttpClient().get(url)
        self.openid = json.loads(data)["openid"]
        return self.openid
        
    
    def setPrepayId(self, prepayId):
        """设置prepay_id"""
        self.prepay_id = prepayId

    def setCode(self, code):
        """设置code"""
        self.code = code

    def  getParameters(self):
        """设置jsapi的参数"""
        jsApiObj = {}
        jsApiObj["appId"] = WxPayConf_pub.APPID
        timeStamp = int(time.time())
        jsApiObj["timeStamp"] = "{0}".format(timeStamp)
        jsApiObj["nonceStr"] = self.createNoncestr()
        jsApiObj["package"] = "prepay_id={0}".format(self.prepay_id)
        jsApiObj["signType"] = "MD5"
        jsApiObj["paySign"] = self.getSign(jsApiObj)
        self.parameters = json.dumps(jsApiObj)

        return self.parameters

class Wxpay_client_pub(Common_util_pub):
    """请求型接口的基类"""
    response = None  #微信返回的响应
    url = None       #接口链接
    curl_timeout = None #curl超时时间

    def __init__(self):
        self.parameters = {} #请求参数，类型为关联数组
        self.result = {}     #返回参数，类型为关联数组


    def setParameter(self, parameter, parameterValue):
        """设置请求参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """设置标配的请求参数，生成签名，生成接口参数xml"""
        self.parameters["appid"] = WxPayConf_pub.APPID   #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID   #商户号
        self.parameters["nonce_str"] = self.createNoncestr()   #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)   #签名
        return  self.arrayToXml(self.parameters)

    def postXml(self):
        """post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlCurl(xml, self.url, self.curl_timeout)
        return self.response

    def postXmlSSL(self):
        """使用证书post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlSSLCurl(xml, self.url, self.curl_timeout)
        return self.response

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        return self.result
        
class UnifiedOrder_pub(Wxpay_client_pub):
    """统一支付接口类"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(UnifiedOrder_pub, self).__init__()


    def createXml(self):
        """生成接口参数xml"""
        #检测必填参数

        if any(self.parameters[key] is None for key in ("out_trade_no", "body", "total_fee", "notify_url", "trade_type")):
            raise ValueError("missing parameter")
        if self.parameters["trade_type"] == "JSAPI" and self.parameters["openid"] is None:
            raise ValueError("JSAPI need openid parameters")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["spbill_create_ip"] = "127.0.0.1"  #终端ip      
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return self.arrayToXml(self.parameters)

    def getPrepayId(self):
        """获取prepay_id"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        prepay_id = self.result["prepay_id"]
        return prepay_id

@csrf_exempt
def paydetail(request):
	device = request.GET.get('device')
	re_url = "http://weixin.gzncloud.com/get-weixin-code.html?appid={0}&scope=snsapi_base&state=STATE&redirect_uri={1}"
	into_url = "http://powerbank.gzncloud.com/pay/paying/?device=" + device + "/"
	return HttpResponseRedirect(re_url.format(WxPayConf_pub.APPID, into_url))

@csrf_exempt
def pay(request):
	code = request.GET.get('code')
	fp = urllib.request.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+WxPayConf_pub.APPID+"&secret="+WxPayConf_pub.APPSECRET+"&code="+code+"&grant_type=authorization_code")  
	token = fp.read().decode('utf-8')  
	tokenjson = json.loads(token)
	openid = tokenjson['openid']
	money = 0.01
	money = int(float(money)*100)
	jsApi = JsApi_pub()
	unifiedOrder = UnifiedOrder_pub()
	unifiedOrder.setParameter("openid",openid) #商品描述
	unifiedOrder.setParameter("body","充值测试") #商品描述
	timeStamp = time.time()
	out_trade_no = "{0}{1}".format(WxPayConf_pub.APPID, int(timeStamp*100))
	unifiedOrder.setParameter("out_trade_no", out_trade_no) #商户订单号
	unifiedOrder.setParameter("total_fee", str(money)) #总金额
	unifiedOrder.setParameter("notify_url", WxPayConf_pub.NOTIFY_URL) #通知地址 
	unifiedOrder.setParameter("trade_type", "JSAPI") #交易类型
	unifiedOrder.setParameter("attach", "6666") #附件数据，可分辨不同商家(string(127))
	prepay_id = unifiedOrder.getPrepayId()
	jsApi.setPrepayId(prepay_id)
	jsApiParameters = jsApi.getParameters()
	return HttpResponse(jsApiParameters)