# import matplotlib.pyplot as plt
# coding=utf-8
from __future__ import print_function
import numpy as np
import numpy.linalg as LA
from numpy import pi
import sys
import socket
import time
import commands

import socket  # socket模块
import datetime
import time
import ENN


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
# s.bind((HOST, PORT))  # 套接字绑定的IP与端口
# s.listen(1)  # 开始TCP监听

# from scipy import optimize
# from scipy import io as spio

def StateWrite():
    file_string = "State.txt"
    f1 = open(file_string, "w+")
    f1.write("1")
    f1.close()
    time.sleep(0.1)
    f1 = open(file_string, "w+")
    f1.write("0")
    f1.close()



def huan(e, E, J):
    J1 = np.linalg.pinv(J)
    u = np.dot(J1, (0.4 * e))
    return u


def Read_file(D):
    # file_string = "/home/jyd/vision/CameraORBTrackingDBSCANframe_bino/Pic/mydataset1.txt"
    file_string = "../KukaSiamFC-tf-master/BiasData.txt"
    f = open(file_string, "r")
    list_arr = f.readlines()
    lists = []
    for index, x in enumerate(list_arr):
        x = x.strip()
        x = x.strip('[]')
        x = x.split(" ")
        lists.append(x)
    lists.append(x)
    a = np.array(lists)
    a = a.astype('Float64')
    e0 = a[0][0]
    e1 = a[0][1]
    myindex = a[0][4]
    f.close()

    indextmp = myindex
    while (myindex == indextmp):
        f = open(file_string, "r")
        list_arr = f.readlines()
        lists = []
        for index, x in enumerate(list_arr):
            x = x.strip()
            x = x.strip('[]')
            x = x.split(" ")
            lists.append(x)
        lists.append(x)
        a = np.array(lists)
        a = a.astype('Float64')
        e0 = a[0][0]
        e1 = a[0][1]
        e2 = a[0][2]
        e3 = a[0][3]
        indextmp = a[0][4]
        f.close()

    if D == 2:
        e00 = np.array([e0, e1])
        return e00
    if D == 3:
        e003 = np.array([e0, e1, e2])
        return e003
    if D == 4:
        e004 = np.array([e0, e1, e2, e3])
        return e004
    if D == 5:
        e005 = np.array([e2, e3])
        return e005


elman = ENN.ELMAN_RNN(input_num=4, hidden_num=20, output_num=12, learning_rate=0.1)
# Read ICP msg
f_icp = open("../SideICP/TransformArray.txt", "r")
list_arr_icp = f_icp.readlines()
list_icp = []

for index, x in enumerate(list_arr_icp):
    x = x.strip()
    x = x.strip('[]')
    x = x.split(" ")
    list_icp.append(x)
list_icp.append(x)
a = np.array(list_icp)
a = a.astype('Float64')
a = a.reshape(8, 4)
# print (a)
f_icp.close()

Trans = a[0:4, 0:4]
# print(T21)
Trans[0:3, 3] = 1000 * Trans[0:3, 3]
# 1379.41,-1970.77,1008.51,138.77,26.33,-160.69,
Euler1 = np.array([137.71, 25.95, -160.85])

T1 = np.array([1389.98, -1988.74, 1100.01])
myep = np.array([Trans[2, 3], Trans[0, 3]])
myOutput = T1
tmp = np.array([(myep[0], (-1.1 * myep[1]), 0)])
myOutput = myOutput + tmp
print("Init Location")
print(myOutput)

# 开启服务器
HOST = ''
PORT = 59152
x00 = myOutput[0][0]
y00 = myOutput[0][1]
z00 = myOutput[0][2]
a00 = Euler1[0]
b00 = Euler1[1]
c00 = Euler1[2]

data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
print("Send data:" + data1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
s.bind((HOST, PORT))  # 套接字绑定的IP与端口
s.listen(1)  # 开始TCP监听

E = np.array([0, 0, 0, 0])

R1 = np.eye(12)*0.5
R2 = np.eye(4)*0.5

I12 = 2 * R1
P = 10 ** 5 * I12
u = np.array([0, 0, 0])
y1 = np.array([300, 4, 300, 4])
I4 = np.eye(4)
i = 0
conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址


print
'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)
print("Recive data  " + data)
conn.sendall(data1)

print("Wait for moving")
data = conn.recv(100)  # 把接收的数据实例化
print(data)
StateWrite()

e00 = Read_file(4)
x0 = elman.feed_forward(e00)
x1 = x0[0][:]
J = np.array([(x1[0], x1[1], x1[2]), (x1[3], x1[4], x1[5]), (x1[6], x1[7], x1[8]), (x1[9], x1[10], x1[11])])
dis = 100000
txtname = "record.txt"

mytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
f1 = file(txtname, "a+")  # 初始化距离参数
f1.write("Start to Record" + mytime + "\n")

e01tmp = np.array([0, 0])
eflag1 = e00
eflag = Read_file(2)
eflag5 = Read_file(5)
print("   \n")
print("XYPhi dias data:")
print(eflag1)
# conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
# print'Connected by', addr  # 输出客户端的IP地址
# data = conn.recv(100)
# conn.sendall(data1)

dis = 100000
while LA.norm(eflag5, 2) > 6 or LA.norm(eflag, 2) > 6:
    # conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
    # print'Connected by', addr  # 输出客户端的IP地址
    # data = conn.recv(100)  # 把接收的数据实例化
    # print(data)
    eflag1 = Read_file(4)
    print("  \n")
    print("XY dias data:")
    print(eflag1)

    conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
    print
    'Connected by', addr  # 输出客户端的IP地址
    data = conn.recv(100)  # 把接收的数据实例化
    # time.sleep(2)
    e01 = Read_file(4)
    if LA.norm(e01, 2) > 500:
        print("continue from 1, Too far from pixel")
        conn.sendall(data1)
        eflag1 = Read_file(4)
        continue
    x0 = elman.feed_forward(e01)
    x1 = x0[0][:]
    J = np.array([(x1[0], x1[1], x1[2]), (x1[3], x1[4], x1[5]), (x1[6], x1[7], x1[8]), (x1[9], x1[10], x1[11])])

    x1 = np.array(
        [J[0, 0], J[0, 1], J[0, 2], J[1, 0], J[1, 1], J[1, 2], J[2, 0], J[2, 1], J[2, 2], J[3, 0], J[3, 1], J[3, 2]])
    y1 = e00 - e01
    e00 = e01
    a1 = u[0]
    b1 = u[1]
    c1 = u[2]
    C = np.array([(a1, b1, c1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                  (0, 0, 0, a1, b1, c1, 0, 0, 0, 0, 0, 0),
                  (0, 0, 0, 0, 0, 0, a1, b1, c1, 0, 0, 0),
                  (0, 0, 0, 0, 0, 0, 0, 0, 0, a1, b1, c1)])
    Q = P + R1
    k = np.dot(np.dot(C, Q), C.T) + R2
    K = np.dot(np.dot(Q, C.T), np.linalg.inv(k))
    P = np.dot((I12 - np.dot(K, C)), Q)
    X = y1 - np.dot(C, x1)
    x1 = x1 + np.dot(K, X)
    elman.training(e00, x1)
    J = np.array([(x1[0], x1[1], x1[2]), (x1[3], x1[4], x1[5]), (x1[6], x1[7], x1[8]), (x1[9], x1[10], x1[11])])
    E = E + e00
    u = huan(e00, E, J)
    print("Controling Data:")
    print("%f,%f,%f" % (u[0], u[1], u[2]))
    print("Right J")
    print(J)
    e01tmp = e01
    x00 = x00 + u[0]
    y00 = y00 + u[1]
    a00 = a00 + u[2]
    data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
    conn.sendall(data1)
    context = str(e00[0]) + " " + str(e00[1]) + " " + str(u[0]) + " " + str(u[1]) + " " + str(x00) + " " + str(
        y00) + '\n'
    f1.write(context)
    print("Wait for moving")
    data = conn.recv(100)  # 把接收的数据实例化
    print(data)
    eflag1 = Read_file(4)
    eflag = Read_file(2)
    eflag5 = Read_file(5)
    # conn.sendall(data1)

mytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
f1.write("End of Record" + mytime + "\n")
f1.close()
conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
ENN.printmatrix(elman)
'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)  # 把接收的数据实例化
print(data)

Judge_Data = Read_file(4)
print("Judge Data:")
print(Judge_Data)

print("Prepare to down\n")

y01 = y00 - 20
data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y01, z00, a00, b00, c00)
conn.sendall(data1)

conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
print
'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)  # 把接收的数据实例化
print(data)

# Final Pose
data1 = "%.2f,%.2f,1008.51,%.2f,%.2f,%.2f,\r\n" % (x00, y00, a00, b00, c00)
print("Final Pose")
print(data)
txtname = "recordFinalPose.txt"
mytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
f1 = file(txtname, "a+")  # 初始化距离参数
f1.write(mytime + "  ")
f1.write(data1)
f1.close()

conn.sendall(data1)

conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
print
'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)  # 把接收的数据实例化
print(data)
# conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
# print'Connected by', addr  # 输出客户端的IP地址
# data = conn.recv(100)  # 把接收的数据实例化
# print(data)
c00 = 1
# data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
# conn.sendall(data1)
# conn.close()  # 关闭连接
while 1:
    asd1231 = 1
