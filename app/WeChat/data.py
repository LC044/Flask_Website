import time

AppSecret = '718080b0db31a654b0a3c8e0a763b1b8'


def parser_text(resp_data):
    data = resp_data['xml']
    print(data)
    return {
        'xml': data
    }


def img(resp_data):
    xml_dict = resp_data['xml']
    print(xml_dict)
    resp_dict = {
        "xml": {
            "ToUserName": xml_dict.get("FromUserName"),
            "FromUserName": xml_dict.get("ToUserName"),
            "CreateTime": int(time.time()),
            "MsgType": "image",
            'PicUrl': xml_dict.get("PicUrl"),
            'MediaId': xml_dict.get("MediaId")
        }
    }
    print(resp_dict)
    return resp_dict
