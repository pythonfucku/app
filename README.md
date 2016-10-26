# app

python的多进程框架，LINUX版，功能包括：

        1.系统后台，前台运行

        2.通过配置，可以便捷的自定义函数（app）转换成进程调用

        3.主框架对进程有监控功能，如子进程异常退出，主框架可将其再次拉起


结构说明：


        python(4913)─┬─python(4914)─┬─python(4915)
                     │              └─python(4918)
                     └─python(4916)─┬─python(4917)
                                    └─python(4919)
                         
                         
以此类推。




CHANGE LOG：


        2016-10-26 10:31:142016-10-23 16:06:23   
                1.调整了框架退出的逻辑，对于抛出的自定异常类，框架直接退出，而不反复重启
                2.增加前台日志输出颜色
                3.增加shell命令接口，命令包括：bash任何命令，cp，mv，scp，rscp，rrscp，psdh
                1.增加强制退出方式，连续5次CTRL+C，将使用kill -9 杀掉app
                2.增加一个app：iostat，仅能获取本地的iostat，使用curses方式输出到屏幕
        
        2016-10-23 16:06:23   
                1.调整了框架退出的逻辑，对于抛出的自定异常类，框架直接退出，而不反复重启
                2.增加前台日志输出颜色
                3.增加shell命令接口，命令包括：bash任何命令，cp，mv，scp，rscp，rrscp，psdh
        
        2016年10月18日13:51:36   
                1.增加github模块
       
