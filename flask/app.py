from flask import Flask, jsonify, request, Response
from flask_cors import *
from flask import render_template #引入模板插件
 
app = Flask(__name__,
static_folder='../vue/static',  #设置静态文件夹目录
template_folder = "../vue")  #设置vue编译输出目录dist文件夹，为Flask模板文件目录
# 跨域解决方案
CORS(app, supports_credentials=True)

@app.route('/')
@app.route('/login')
def index():
    return render_template('index.html',name='index') #使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。


"""
login 的后端api
""" 
@app.route("/checklogin", methods=['POST'])
def login():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        data = request.form.to_dict()
        username = data.get("username")
        password = data.get("password")
        return Response("1")
    else:
        return Response("0")

if __name__ == '__main__':
    app.run(debug=True)