from flask import Flask
import nginx_log


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello worle'

@app.route('/log')
nginx_log.nginx()


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=666,debug=True)
