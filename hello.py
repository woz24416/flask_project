#coding=utf-8

from flask import Flask
app = Flask(__name__) #程序实例是Flask类的对象
#Flask使用__name__这个变量来决定程序的根目录，以便能够找到相对于程序根目录的资源文件的位置

#修饰器是Python语言的标准特性，其作用是：可以使用不同的方式修改函数的行为
#在这里是使用修饰器把函数注册为事件的处理程序
#下例就是把index()函数注册为程序根地址的处理程序
@app.route('/')
def index():
	return '<h1>Hello World!</h1>'

if __name__ == '__main__':
	app.run(debug=True)