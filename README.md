# runtogether
http请求的多端口转发以达到提速的目的

## Install
>> pip install runtogether

## Run in Project
>>from runtogether.handles import Referee
>>server = Referee(app=app, host='0.0.0.0', port=8899, workers=4)
>>server.run()

## Run in Teminal
### For Flask
创建wsgi文件,并引入create_app方法,创建一个app对象.如：
>>from your_project.app import create_app
>>wsgi = create_app()

### For Django
django自带wsgi文件，且内含可用的application对象.

在命令行输入
***rtg -ro <your_project path> -mo <your wsgi module>:<your application obj> -ho <Host> -po <Port> -w0 <Workers>***
Flask如:
***rtg -ro /MyProject/ -mo wsgi:application -ho 0.0.0.0 -po 8888 -wo 4***
django时, 命令行需要注意-ro和-mo部分. -ro部分比Flask时候少引入一层, 在-mo内以点(.)连接.如:
***rtg -ro MyProject -mo MainPackage.wsgi:application  -ho 0.0.0.0 -po 8888 -wo 4***