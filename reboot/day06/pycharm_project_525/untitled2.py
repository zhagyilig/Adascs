# coding=utf-8

# 系统模块:
from flask import Flask, request, render_template, redirect, session
import MySQLdb as mysql

# 自定模块:
import mem
import fileutil


conn= mysql.connect(    # 连接MySQL
        host='localhost',
        port = 9036,
        user='root',
        passwd='888888',
        db ='reboot12',
        unix_socket = '/tmp/mysql9036.sock',
        )

cur = conn.cursor()
# conn.autocommit(True)
# cur.execute("select * from flask_user")   # 测试连接库
# print(cur.fetchall())


fileutil.read_file()
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def hello_world():
    session['username'] = 'admin'
    return redirect('user_list')

@app.route('/logout')
def logout():
    session.pop('username')
    return  render_template('login.html')

def check_login(user,pwd):
    with open('user.txt') as f:
        user_list = f.read().split('\n')
        user_pwd = '%s:%s' %(user,pwd)

        if user_pwd in user_list and 'username' in session:
            return redirect('/user_list')
        else:
            return render_template("login.html",login_error="user or pwd is faild")

@app.route('/login')
def huoying():
    user =request.args.get('user')
    pwd = request.args.get('pwd')
    return  check_login(user,pwd)

@app.route('/user_list')
def user_list():
    cur.execute("select * from flask_user")
    if 'username' in session:
        # return  render_template('list.html',user_list=list(fileutil.file_dict.items()))
        return  render_template('list.html',user_list=cur.fetchall())
    return redirect('/')


@app.route('/del_user')
def del_user():
    user = request.args.get('user')
    fileutil.file_dict.pop(user)
    fileutil.wirte_file()
    return redirect('/user_list')

@app.route('/commit_user')
def commit_user():
    new_user = request.args.get('user')
    new_pwd  =request.args.get('pwd')
    # if new_user in fileutil.file_dict:
    #     return 'user is exist.'
    cur.execute('select * from flask_user')
    user_table = cur.fetchall()
    if new_user in user_table:
        return 'user is exist.'
    else:
        # fileutil.file_dict[new_user] = new_pwd
        # fileutil.wirte_file()
        insert_sql = 'insert into flask_user(user,pwd) values("%s","%s")' %(new_user,new_pwd)
        cur.execute(insert_sql)
        conn.commit()
        return redirect('/user_list')

@app.route('/add_user')
def add_user():
    return render_template("add_user.html")


@app.route('/change_user')
def change_user():
    change_use = request.args.get('user')
    change_pwd = fileutil.file_dict.get(change_use)
    # change_pwd = request.args.get('pwd')
    if change_use in fileutil.file_dict:
        return  render_template('change_user.html', user=change_use,pwd=change_pwd)

    else:
        return "This user isn't exist"

@app.route('/change_user_commit')
def change_user_commit():
    change_use = request.args.get('olduser')
    alter_new_user = request.args.get('alter_user')

    fileutil.file_dict[change_use] = alter_new_user
    return redirect('/user_list')

@app.route('/test_jquery')
def test_jquery():
    return render_template('jquery.html')

@app.route('/stu_js')
def stu_js():
    return  render_template('stu_js.html')


@app.route('/stu_jquery_ui')
def stu_jquery_ui():
    return render_template('stu_jquery_ui.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)
