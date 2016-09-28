# app

python的多进程框架，LINUX版，功能包括：
1.系统后台，前台运行
2.通过配置，可以便捷的自定义函数（app）转换成进程调用
3.主框架对进程有监控功能，如子进程异常退出，主框架可将其再次拉起

结构说明：
父进程------子进程（app）------- 孙进程（函数）
        |                |----孙进程（函数）
        |--子进程（app）-------孙进程（函数）
                         |----孙进程（函数）
                         
以此类推。
