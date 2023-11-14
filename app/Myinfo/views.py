from flask import Blueprint, request, render_template

Myinfo=Blueprint('Myinfo', __name__)

@Myinfo.route("/")
def index():
    """
    返回html页面数据
    :return:
    """
    # return "<h1>我是个人主页</h1>"
    return render_template("index.html")

@Myinfo.route("/firework")
def index2():
    """
    返回html页面数据
    :return:
    """
    # return "<h1>我是个人主页</h1>"
    return render_template("firework.html")


@Myinfo.route("/firework/code")
def fireworkCode():
    f = open('./templates/firework.txt', 'r')
    html = f.read()
    f.close()
    return html


@Myinfo.route('/api/start', methods=['POST'], strict_slashes=False)
def api_predict():
    CLASSIFY_REST_API_URL = 'http://xxx.xxx.xxx.xxx:5000/predict'
    headers = {'Content-Type': 'application/json'}
    fname = request.form
    print(fname)
    # return "已发送"
    with open('data.txt', 'a', encoding='utf-8') as f:
        f.write(fname['name'] + ',')
        f.write(fname['email'] + ',')
        f.write(fname['subject'] + ',')
        f.write(fname['text'] + '\n')
    return "已发送"


if __name__ == '__main__':
    Myinfo.run(host='192.168.1.6', port=7788)
