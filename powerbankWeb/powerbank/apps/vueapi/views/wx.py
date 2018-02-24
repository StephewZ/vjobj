#coding=utf8
import time
import urllib

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
        return  self.arrayToXml(self.parameters)

    def getPrepayId(self):
        """获取prepay_id"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        prepay_id = self.result["prepay_id"]
        return prepay_id

@csrf_exempt
def paydetail(request):
	re_url = "http://weixin.gzncloud.com/get-weixin-code.html?appid={0}&scope=snsapi_base&state=STATE&redirect_uri={1}"
	into_url = "http://powerbank.gzncloud.com/pay/paying/"
	return HttpResponseRedirect(re_url.format(WxPayConf_pub.APPID, into_url))

def pay(request):
	code = request.GET.get('code')  
	fp = urllib.request.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+WxPayConf_pub.APPID+"&secret="+WxPayConf_pub.APPSECRET+"&code="+code+"&grant_type=authorization_code")  
	token = fp.read().decode('utf-8')  
	tokenjson = json.loads(token)  
	openid = tokenjson['openid']