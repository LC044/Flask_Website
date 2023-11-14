from flask import Blueprint, request, abort, render_template
import hashlib
import time
# 用它可以访问http请求地址
import urllib.request as urllib2
import urllib
import json
import xmltodict
from . import data

WECHAT_TOKEN = 'zhou1316'
wechat = Blueprint('wechat', __name__)


@wechat.route("/", methods=['POST', 'GET'], strict_slashes=False)
def WeChat():
    """验证服务器地址的有效性"""
    # 开发者提交信息后，微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数:
    # signature:微信加密, signature结合了开发者填写的token参数和请求中的timestamp参数 nonce参数
    # timestamp:时间戳(chuo这是拼音)
    # nonce: 随机数
    # echostr: 随机字符串
    # 接收微信服务器发送参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    # 校验参数
    # 校验流程：
    # 将token、timestamp、nonce三个参数进行字典序排序
    # 将三个参数字符串拼接成一个字符串进行sha1加密
    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if not all([signature, timestamp, nonce]):
        # 抛出400错误
        abort(400)

    # 按照微信的流程计算签名
    li = [WECHAT_TOKEN, timestamp, nonce]
    # 排序
    li.sort()
    # 拼接字符串
    tmp_str = "".join(li)
    tmp_str = tmp_str.encode('utf-8')

    # 进行sha1加密, 得到正确的签名值
    sign = hashlib.sha1(tmp_str).hexdigest()

    # 将自己计算的签名值, 与请求的签名参数进行对比, 如果相同, 则证明请求来自微信
    if signature != sign:
        # 代表请求不是来自微信
        # 弹出报错信息, 身份有问题
        abort(403)
    else:
        # 表示是微信发送的请求
        if request.method == "GET":
            # 表示第一次接入微信服务器的验证
            echostr = request.args.get("echostr")
            # 校验echostr
            if not echostr:
                abort(400)
            return echostr

        elif request.method == "POST":
            # 表示微信服务器转发消息过来
            # 拿去xml的请求数据
            xml_str = request.data

            # 当xml_str为空时
            if not xml_str:
                abort(400)

            # 对xml字符串进行解析成字典
            xml_dict = xmltodict.parse(xml_str)

            xml_dict = xml_dict.get("xml")
            print('接收到的数据\n', xml_dict)
            # MsgType是消息类型 这里是提取消息类型
            msg_type = xml_dict.get("MsgType")

            if msg_type == "text":
                # 表示发送文本消息
                # 够造返回值, 经由微信服务器回复给用户的消息内容
                # 回复消息
                # ToUsername: (必须传) 接收方账号(收到的OpenID)
                # FromUserName: (必须传) 开发者微信号
                # CreateTime: (必须传) 消息创建时间(整形)
                # MsgType: (必须传) 消息类型
                # Content: (必须传) 回复消息的内容(换行:在Content中能够换行, 微信客户端就支持换行显示)
                resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": xml_dict.get("Content")
                    }
                }
                pasered_data = data.parser_text(resp_dict)
            elif msg_type == 'image':
                resp_dict = {
                    "xml": xml_dict
                }
                pasered_data = data.img(resp_dict)
            else:
                pasered_data = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": "别闹了，我看不懂啊！"
                    }
                }
            # 将字典转换为xml字符串
            resp_xml_str = xmltodict.unparse(pasered_data)
            # 返回消息数据给微信服务器
            return resp_xml_str
