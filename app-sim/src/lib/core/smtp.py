#!/bin/evn python
#coding:utf-8
'''
#=============================================================================
#     FileName: smtp.py
#         Desc: send email,can't use!!
#       Author: Crow@ZPT
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 0.0.1
#   LastChange: 2016-10-18 11:53:02
#      History:
#=============================================================================
'''

import smtplib  
from email.mime.text import MIMEText  

mailto_list=["rentaox.liang@intel.com"] 
mail_host="OutlookSH.intel.com"  
mail_user="rentaox.liang"    
mail_pass="123?intel"   
mail_postfix="intel.com"  

def send_mail(to_list,sub,content):  
  me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
  msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
  msg['Subject'] = sub  
  msg['From'] = me  
  msg['To'] = ";".join(to_list)  
  #try:  
  server = smtplib.SMTP()  
  server.connect(mail_host)  
  server.login(mail_user,mail_pass)  
  server.sendmail(me, to_list, msg.as_string())  
  server.close()  
  return True  
  #except Exception, e:  
      #print str(e)  
      #return False  


if __name__ == '__main__':  
  if send_mail(mailto_list,"hello","hello world！"):  
      print "发送成功"  
  else:  
      print "发送失败" 

