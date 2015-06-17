# coding=utf-8

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__) 
#程序实例app是Flask类的对象
#Flask使用__name__这个变量来决定程序的根目录，以便能够找到相对于程序根目录的资源文件的位置
manager = Manager(app)
bootstrap = Bootstrap(app)

#修饰器是Python语言的标准特性，其作用是：可以使用不同的方式修改函数的行为
#在这里是使用修饰器把函数注册为事件的处理程序
#下例就是把index()函数注册为程序根地址的处理程序
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/user/<name>') #尖括号中的内容就是动态部分,任何能匹配静态部分的 URL 都会映射到这个路由上 
def user(name): #调用视图函数时,Flask会将动态部分作为参数传入函数 
	#render_template函数的第一个参数是模版的文件名
	#随后的参数都是键值对，表示模版变量对应的真实值
	#左边的name为模版中占位变量；右边的name为当前作用域中的变量
	return render_template('user.html', name=name)


if __name__ == '__main__':
	app.run(debug=True)
'''
__name__=='__main__' 是 Python 的惯常用法
在这里确保直接执行这个脚本时才启动开发Web服务器
如果这个脚本由其他脚本引入,程序假定父级脚本会启动不同的服务器,因此不会执行app.run()。 

'''