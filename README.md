# app
one python app for zoomeye

第一次使用，没有zoomeye api的key，需要登录，登录以后就不再需要登录，也可以选择再次登录，以便更改key

python main.py -u yourname -p yourpasswd --type host --query cms --facets os,app --page 1

使用说明：
  zoomeye api需要先登录zoomeye，使用-u yourname -p yourpasswd。
  登录之后key会保存在zoomeye同级的access_token.txt文件中，第二次使用则无须用户名和密码：
  python main.py --type host --query cms --facets os,app --page 1
  
  zoomeye api有三个参query，facets，page；都是可选参数（官方文档位置：https://www.zoomeye.org/api/doc）
  type指定俩值，分为host和web，省去写url的过程而已。
  
  为什么这个zoomeye api 没有放在bin下，而是放在src/app/zoomeye下？
  main.py还能做哪些事？You can you up,can you?  :)
-----------------------------------------------------------------------------------------------------
changeLog
  2016-04-05 23时30分50秒 目前只打印了搜索到的ip，其他信息没有打印，没有保存。
    后续将所有搜索到的信息进一步保存，并加载其他测试模块
