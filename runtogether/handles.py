import sys
import socket
import threading
import select
import time
import psutil
from datetime import datetime
from runtogether.process import CBaseProcess
from runtogether.utils import WorkerBaseQueue


PROXY_PORTS = []


def get_port(workers, queue=None):
    '''
        获取端口
    :param workers: 工作进程数
    :param queue:   通信管道对象
    :return:        [(pid, 端口), (pid, 端口)...]
    '''
    queue = queue if queue else WorkerBaseQueue(workers)
    ports = []
    # nodes = []
    for i in range(workers):
        # node = queue.get()
        # ports.append(list(node.values())[0])
        ports.append(queue.get())
    return ports


def proxy_socket(client, addr):
    '''
        socket代理
    :param client:
    :param addr:
    :return:
    '''
    inputs = [client]
    outputs = []
    remote_socket = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    live = True
    while live:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, None)
        try:
            for s in readable:
                if s is client:
                    request_header = s.recv(4096)
                    if remote_socket is 0:
                        headers = request_header.decode()
                        host_addr = headers.split("\r\n")[1].split(":")
                        interface = headers.split("\r\n")[0]
                        name, host, port = map(lambda x: x.strip(), host_addr)
                        port = PROXY_PORTS.pop(0)
                        PROXY_PORTS.append(port)
                        sock.connect((host, port))
                        remote_socket = sock
                        inputs.append(sock)
                        print('%s server port: %s-->%s : %s' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(port), "client connent:{0}:{1}".format(addr[0], addr[1]), interface))
                    remote_socket.sendall(request_header)
                else:
                    while True:
                        resp = s.recv(512)
                        if len(resp):
                            client.sendall(resp)
                        else:
                            live = False
                            break
        except Exception as e:
            print("http socket error {0}".format(e))


class Referee(object):

    def __init__(self, app, workers, host, port):
        '''
        :param app:     application 对象.
        :param workers: 工作进程数
        :param host:    主进程运行host
        :param port:    主进程运行端口
        :param process: 工作进程对象列表
        :param p:       工作进程元组列表
        '''

        self.app = app
        self.workers = workers
        self.host = host
        self.port = port
        self.process = []
        self.p = []

    def add_process(self):
        '''
            添加工作进程
        :return:
        '''
        p = CBaseProcess(self.app, self.workers)
        self.process.append(p)
        p.start()

    def handle_process(self):
        '''
            控制工作进程
        :return:
        '''
        for i in range(self.workers):
            self.add_process()

    def handle_check(self):
        '''
            子进程健康检查及重建对应端口的进程
        :return:
        '''
        time.sleep(10)
        while True:
            # print('health checking!')
            pop_idx = []
            # print(self.p)
            for i, p in enumerate(self.p):
                if not psutil.pid_exists(p[0]) or psutil.Process(p[0]).status() not in ['running', 'sleeping']:
                    print(psutil.Process(p[0]).status())
                    print('pid:[%s] is dead!' % str(p[0]))
                    pop_idx.append(i)
                    np = CBaseProcess(self.app, 1, port=p[1])
                    np.start()
                    print(np.pid)
                    self.p.append((np.pid, np.port))
                    print('new process[%s] is start!' % str(np.pid))
            [self.p.pop(i) for i in pop_idx]
            time.sleep(5)

    def run(self):
        '''
            主方法
        :return:
        '''
        self.handle_process()
        self.p = get_port(self.workers)
        [PROXY_PORTS.append(p[1]) for p in self.p]
        threading.Thread(target=self.handle_check, args=()).start()
        http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # print(type(self.port))
            http_server.bind((self.host, self.port))
        except Exception as e:
            sys.exit("python proxy bind error [%s]" % str(e))

        print("python proxy start")
        print("* Server Running on http://{}:{}. Proxy Ports {}".format(self.host, str(self.port), str(PROXY_PORTS)))

        http_server.listen(1024)

        while True:
            conn, addr = http_server.accept()
            http_thread = threading.Thread(target=proxy_socket, args=(conn, addr))
            http_thread.start()


if __name__ == '__main__':
    import importlib
    sys.path.append('/home/chengsy/CUS-C/')
    app = getattr(importlib.import_module('wsgi'), 'wsgi')
    server = Referee(app=app, workers=4, host='0.0.0.0', port=8888)
    server.run()