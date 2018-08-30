from socket import *
import sys,time,re

def do_search(sockfd,name):
    while True:
        word = input('请输入想要查询的单词:')
        if not word:
            print('警告:非法输入!')
            continue
        elif word == '#':
            print('结束查询')
            break
        sockfd.send('S {} {}'.format(word,name).encode())
        mean = sockfd.recv(1024).decode()
        if mean == 'notword':
            print('对不起,无法查询到该单词')
        else:
            print('word: {}'.format(mean))         

def do_history(sockfd):
    while True:
        print('++++++++++++++++++')
        print('(1)查看所有记录　　　')
        print('(2)查看前十记录　　　')
        print('(3)退出　　　　　　　')
        print('++++++++++++++++++')
        try:
            choice = int(input('请选择命令选项:'))
            if choice == 3:
                break
        except Exception as e:
            print('非法输入')
            continue
            if choice not in [1,2,3]:
                print('无用指令')
                continue
        sockfd.send('H {}'.format(choice).encode())
        while True:
            record = sockfd.recv(1024).decode()
            if record == 'end':
                break
            print(record)

def do_dictionary(sockfd,name):
    while True:
        print('+++++++++++++++++++++')
        print('      search         ')
        print('      history        ')
        print('       quit          ')
        print('+++++++++++++++++++++')
        choice = input('请需要执行的操作:')
        if not choice:
            print('请输入有效操作')
            continue
        elif choice == 'search':
            do_search(sockfd,name)
        elif choice == 'history':
            do_history(sockfd)
        else:
            print('用户已注销')
            return '##'

def main():
    if len(sys.argv) < 3:
        sys.exit('地址格式输入错误')

    HOST = sys.argv[1]
    ADDR = int(sys.argv[2])
    addr = (HOST,ADDR)
    print(addr)

    s = socket()
    s.connect(addr)
    print('succeed')
    while True:
        print('+++++++++++++++++++++++++++')
        print('+++welcome to dictionary+++')
        print('+login+++++++++++++++++++++')
        print('+register++++++++++++++++++')
        print('+quit++++++++++++++++++++++')
        print('+++++++++++++++++++++++++++')
        choice = input('请选择需要执行的操作:')
        if choice == 'register':
            while True:
                name = input('请输入新用户姓名：')
                passwd = input('请输入密码')
                if  name and passwd:
                    break                         
            s.send('R {} {}'.format(name,passwd).encode())
            reply = s.recv(1024)
            print(reply)
            if reply == b'fail':
                print('用户名已被注册')
                continue
            else:
                print ('恭喜你,注册成功')

        if choice == 'login':
            while True:
                name = input('请输入账号姓名:')
                if not name:
                    print('请输入正确用户名')
                    continue
                passwd = input('请输入密码：')
                s.send('L {} {}'.format(name,passwd).encode())
                reply = s.recv(1024).decode()
                if reply == 'success':
                    get_r = do_dictionary(s,name)
                    if get_r == '##':
                        break
                elif reply == 'wrong':
                    print('密码错误，请重新登录')
                    continue
                else:
                    print('该用户不存在，请重新登录')
                    continue
        if choice == 'quit':
            print('客户端已退出')
            s.send(b'exit')
            s.close() 
            sys.exit(0)
        
       

if  __name__ == '__main__':
    main()


                

