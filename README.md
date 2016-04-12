# app
one python app for zoomeye

第一次使用，没有zoomeye api的key，需要登录，登录以后就不再需要登录，也可以选择再次登录，以便更改key

python main.py zoomeye -u yourname -p yourpasswd --type host --query cms --facets os,app --page 1

使用说明：
  main.py为框架，第一个参数zoomeye为要执行的模块，后续的参数为zoomeye需要的。
  其他app的使用可以参考zoomeye的例子，放在app路径下。
  
  
  zoomeye api需要先登录zoomeye，使用-u yourname -p yourpasswd。
  登录之后key会保存在zoomeye同级的access_token.txt文件中，第二次使用则无须用户名和密码：
  python main.py zoomeye --type host --query cms --facets os,app --page 1
  
  zoomeye api有三个参query，facets，page；都是可选参数（官方文档位置：https://www.zoomeye.org/api/doc）
  type指定俩值，分为host和web，省去写url的过程而已。
  

-----------------------------------------------------------------------------------------------------
# changeLog

  2016年4月12日 17:11:44
    将从zoomeye api的结果永久保存在文件中，MetInfo攻击模块从文件中加载结果，进行攻击测试
    下一步优化：1.保存文件；2.动态加载攻击模块；main.py框架对进程的管理。
    
  2016年4月8日 17:10:07 结合zoomeye api 和seebug的poc。
    增加了基《于MetInfo5.3 最新版本SQL注射》的自动化sql注入小例子，出处http://www.wooyun.org/bugs/wooyun-2015-0119166
    Poc是从网上抄的，出处：http://blog.evalbug.com/2016/01/27/poc_coding_3/
    说明：利用zoomeye api查询MetInfo，将结果输入到poc中，进行注入测试。目前还不能动态加载模块，只是写死，后续优化
    
  2016-04-05 23时30分50秒 目前只打印了搜索到的ip，其他信息没有打印，没有保存。
    后续将所有搜索到的信息进一步保存，并加载其他测试模块
    


