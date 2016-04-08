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
    
  2016年4月8日 17:10:07 结合zoomeye api 和seebug的poc。
    增加了基《于MetInfo5.3 最新版本SQL注射》的自动化sql注入小例子，出处http://www.wooyun.org/bugs/wooyun-2015-0119166
    
    Poc是从网上抄的，出处：http://blog.evalbug.com/2016/01/27/poc_coding_3/
    
    说明：利用zoomeye api查询MetInfo，将结果输入到poc中，进行注入测试。目前还不能动态加载模块，只是写死，后续优化
    
      python main.py  --type host --page 10 --query MetInfo   (省略用户名和密码）
      
      结果，手动验证好用：
      
      20160408170340,23985,INFO > find ip:60.251.212.90
      20160408170340,23985,INFO > find ip:42.96.165.119
      20160408170340,23985,INFO > find ip:42.120.9.203
      20160408170340,23985,INFO > find ip:223.26.54.73
      20160408170340,23985,INFO > find ip:221.204.12.99
      20160408170340,23985,INFO > find ip:220.135.199.36
      20160408170340,23985,INFO > find ip:42.96.165.119
      20160408170340,23985,INFO > find ip:211.155.86.148
      20160408170340,23985,INFO > find ip:103.243.131.241
      20160408170340,23985,INFO > find ip:198.57.202.135
      20160408170346,23985,INFO > find ip:60.251.212.90
      20160408170346,23985,INFO > find ip:42.96.165.119
      20160408170346,23985,INFO > find ip:42.120.9.203
      20160408170346,23985,INFO > find ip:223.26.54.73
      20160408170346,23985,INFO > find ip:221.204.12.99
      20160408170346,23985,INFO > find ip:220.135.199.36
      20160408170346,23985,INFO > find ip:42.96.165.119
      20160408170346,23985,INFO > find ip:211.155.86.148
      20160408170346,23985,INFO > find ip:103.243.131.241
      20160408170346,23985,INFO > find ip:198.57.202.135
      20160408170346,23985,INFO > account was break, excceeding the max limitations
      20160408170346,23985,ERROR > 'matches'
      42.96.165.119 is vulnerable!
      42.96.165.119 is vulnerable!
      42.96.165.119 is vulnerable!
      42.96.165.119 is vulnerable!
