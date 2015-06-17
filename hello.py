# coding=utf-8

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__) 
#程序实例app是Flask类的对象
#Flask使用__name__这个变量来决定程序的根目录，以便能够找到相对于程序根目录的资源文件的位置
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
#app.config字典可用来存储配置变量；除了明文外，还可以从环境中导入配置值
app.config['SECRET_KEY'] = 'just do it'

#每个web表单都由一个继承自Formd的类表示
class NameForm(Form):
	#每个字段都是一个对象，是一个相应字段类型的对象
	#validators是一个由验证函数组成的列表
	name = StringField('What is your name?', validators=[Required()]) #字段对象可附属一个或多个验证函数，
	#字段构造函数的第一个参数是把表单渲染成HTML时使用的标号
	submimt = SubmitField('Submit')
	#表单类中的字段是可调用的，在模版中调用后会渲染成HTML
	#在视图函数中通过参数将表单对象传入模版	

#修饰器是Python语言的标准特性，其作用是：可以使用不同的方式修改函数的行为
#在这里是使用修饰器把函数注册为事件的处理程序
#下例就是把index()函数注册为程序根地址的处理程序
@app.route('/', methods=['GET', 'POST']) #如果没有指定methods参数的话，flask就只会把视图函数注册为GET请求的处理程序
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name)

@app.route('/user/<name>') #尖括号中的内容就是动态部分,任何能匹配静态部分的 URL 都会映射到这个路由上 
def user(name): #调用视图函数时,Flask会将动态部分作为参数传入函数 
	#render_template函数的第一个参数是模版的文件名
	#随后的参数都是键值对，表示模版变量对应的真实值
	#左边的name为模版中占位变量；右边的name为当前作用域中的变量
	return render_template('user.html', name=name)

#Flask允许程序使用基于模版的自定义错误页面
#最常见的错误有两个：404客户端请求位置页面；500处理异常
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

'''
Flask使用url_for()函数生成URL，它的第一个参数是视图函数的名称
第二个可选参数 _external=True的话，返回的是绝对地址。一般在生成浏览器之外的链接时使用，例如邮件
在生成动态地址时，动态部分作为关键字参数传入:url_for('index', name='mark', page=2 )返回的结果是:/mark/?page=2
'''
'''
静态文件多为JS和图片，一般存放在static的子目录中。如有需要可再设置更深一层子目录
url_for('static', filename='css/style.css')得到的结果是：static/css/style.css
在模版中存放图片路径链接为：href=" {{url_for('static', filename='img/favicon.ico')}} "
'''

if __name__ == '__main__':
	app.run(debug=True)
'''
__name__=='__main__' 是 Python 的惯常用法
在这里确保直接执行这个脚本时才启动开发Web服务器
如果这个脚本由其他脚本引入,程序假定父级脚本会启动不同的服务器,因此不会执行app.run()。 

'''