from flask import Flask, render_template, request

# 创建flask对象
app = Flask(__name__, static_url_path='')



@app.route("/")
def index():
    """
    返回html页面数据
    :return:
    """
    # return "<h1>我是个人主页</h1>"
    return render_template("index.html")


@app.route('/api/start', methods=['POST'], strict_slashes=False)
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
    app.run(host = '127.0.0.1')
    # app.run(host='192.168.1.100', port=7788)
