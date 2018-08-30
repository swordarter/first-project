from socket import *
import os,time,sys,re
from signal import *

def do_historysave(word,name,time):
    with open('/home/tarena/vscode_project/dict_project/history.txt','a+') as f:
        f.write('\n'+'user:{} word:{} time:{}'.format(name,\
              word,time))

def do_history(connfd,c):    
        with open('/home/tarena/vscode_project/dict_project/history.txt','r') as f:
            if c == '1':
                data = f.read()
                connfd.send(data.encode())
                time.sleep(0.1)
            elif c == '2':
                list1 = []
                for line in f:
                    list1.append(line)
                list2 = list1[-1:-11:-1]
                for record in list2:
                    connfd.send(record.encode())
                    time.sleep(0.1)
            print('发送完毕')
            connfd.send(b'end')

def do_search(word,connfd):
    with open('/home/tarena/vscode_project/dict_project/dict.txt','r') as f:
        for line in f:
            idea = re.split('[ ]+',line)
            word_s,mean = idea[0],' '.join(idea[1:])
            if not line:
                connfd.send(b'notword')
                print('查无此词')
            if word_s == word:
                connfd.send(mean.encode())
                break


def do_register(name,passwd,connfd):
    with open('userinfo.txt','r+') as f:
        data = f.read()
        data = data.splitlines()
        print(data)
        isok = True
        for i in range(1,len(data)):
            name1 = data[i].split('  ')[0].split(':')[1]
            print(name1)
            if name == name1:
                connfd.send(b'fail')
                isok = False           
        if isok:
            f.write('\n'+'name:{}  password:{}'.format(name,passwd))
            connfd.send(b'ok')
            
            

def do_login(name,passwd,connfd):
    with open('userinfo.txt','r') as f:
        data = f.read()
        data = data.splitlines()
        pattern1 = r'^name:\w+'
        pattern2 = r'password:\w+'
        for i in range(1,len(data)):
            know = data[i]            
            Name = re.findall(pattern1,know)[0].split(':')[1]
            if Name == name:
                Passwd = re.findall(pattern2,know)[0].split(':')[1]    
                print(Passwd)
                if Passwd == passwd:
                    print('登录成功')
                    connfd.send(b'success')
                    break
                else:
                    print('密码错误，请重新登录')
                    connfd.send(b'wrong')
                    break
                      

def main():
    addr = ('0.0.0.0',9999)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(addr)
    s.listen(5)


    signal(SIGCHLD,SIG_IGN)

    while True:
        try:
            print('waitting...')
            connfd,addr = s.accept()
            print('connecting successful')
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器已关闭')
        except Exception as e:
            print(e)
            continue
        if connfd:
            pid = os.fork()
            if pid < 0:
                sys.exit('进程创建失败')
            elif pid == 0:
                while True:
                    msg = connfd.recv(1024).decode()
                    msg = msg.strip().split(' ')
                    if msg[0] == 'R':
                        do_register(msg[1],msg[2],connfd)
                    elif msg[0] == 'L':
                        do_login(msg[1],msg[2],connfd)
                    elif msg[0] == 'S':
                        do_historysave(msg[1],msg[2],time.ctime())
                        do_search(msg[1],connfd)
                    elif msg[0] == 'H':
                        if msg[1] == '3':
                            continue
                        do_history(connfd,msg[1])
                    else:
                        connfd.close()
                        break

                    
                

            else:
                s.close()
                break

if __name__ == '__main__':
    main()

