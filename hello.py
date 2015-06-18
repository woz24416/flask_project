# coding=utf-8

from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length, NumberRange


app = Flask(__name__) 
#程序实例app是Flask类的对象
#Flask使用__name__这个变量来决定程序的根目录，以便能够找到相对于程序根目录的资源文件的位置
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
#app.config字典可用来存储配置变量；除了明文外，还可以从环境中导入配置值
app.config['SECRET_KEY'] = 'just do it'
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'mysql://root:65129377@127.0.0.1/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #每次请求结束后都会自动提交数据库中的变化
db = SQLAlchemy(app)

#每个web表单都由一个继承自Formd的类表示
class NameForm(Form):
	#每个字段都是一个对象，是一个相应字段类型的对象
	#validators是一个由验证函数组成的列表
	name = StringField('What is your name?', validators=[Required(), Length(min=4, max=25)]) #字段对象可附属一个或多个验证函数，
	number = IntegerField('Enter 4 to 25 numbers:', validators=[NumberRange(min=4, max=25)])
	#字段构造函数的第一个参数是把表单渲染成HTML时使用的标号
	submimt = SubmitField('Submit')
	#表单类中的字段是可调用的，在模版中调用后会渲染成HTML
	#在视图函数中通过参数将表单对象传入模版


#定义数据模型
class Role(db.Model):
	__tablename__ = 'roles' #SQLAlchemy使用的默认表名都是以单数形式进行命名约定的
	id = db.Column(db.Integer, primary_key=True)#模型的属性相当于表中的列
	name = db.Column(db.String(64), unique=True)#都是db.Column类的实例
	users = db.relationship('User', backref='role')#向User模型添加了一个role属性
	#这一属性可代替role_id访问Role模型，此时是作为模型对象而不是外健来获取使用
	def __repr__(self):
		return '<Role %r>' % self.name
class User(db.Model):
	__tablename__ = 'users' #因此最好自己定义表名
	id = db.Column(db.Integer, primary_key=True)#db.Column类的构造函数的第一个参数是数据库列(模型类属性)的类型
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #定义外键，就是这个外键建立起了关系
	def __repr__(self):
		return '<User %r>' % self.username
class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	bookname = db.Column(db.String(64), unique=True, nullable=False)
	def __repr__(self):
		return '<Book %r>' % self.bookname
'''
在insert数据是中文的时候，要确保数据库的database table column全部都是utf8的编码
'''

def make_shell_context(): #此函数以字典形式注册了程序实例，数据库实例以及模型
	return dict(app=app, db=db, User=User, Role=Role, Book=Book)
# 将这些对象导入到shell当中
manager.add_command("shell", Shell(make_context=make_shell_context))

#修饰器是Python语言的标准特性，其作用是：可以使用不同的方式修改函数的行为
#在这里是使用修饰器把函数注册为事件的处理程序
#下例就是把index()函数注册为程序根地址的处理程序
@app.route('/', methods=['GET', 'POST']) #如果没有指定methods参数的话，flask就只会把视图函数注册为GET请求的处理程序
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None: #如果数据库中没有表单输入的数据
			user = User(username=form.name.data) #将表单中的数据存入表中相应的字段
			db.session.add(user) #将数据先写入会话中
			#db.session.commit()  #提交会话，将数据写入数据库中
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data  #将表单中的数据写入session中便于用户跨页面调用
		session['number'] = form.number.data
		form.name.data = ''
		form.number.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form=form, current_time=datetime.utcnow(),
							name=session.get('name'), number=session.get('number'), known=session.get('known', False))


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
	manager.run()
'''
__name__=='__main__' 是 Python 的惯常用法
在这里确保直接执行这个脚本时才启动开发Web服务器
如果这个脚本由其他脚本引入,程序假定父级脚本会启动不同的服务器,因此不会执行app.run()。 

'''