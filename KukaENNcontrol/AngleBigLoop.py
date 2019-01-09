# import matplotlib.pyplot as plt
# coding=utf-8
import numpy as np
import numpy.linalg as LA
from numpy import pi
import sys
import socket
import time

import socket  # socket模块

import time
import datetime

'''
1451.19	-2172.07	139.78
1451.19	-2172.07	139.78
'''


# ICP Init
def huan(e, E, J):
    J1 = np.linalg.pinv(J)  # 雅克比矩阵求逆
    u = np.dot(J1, (0.7 * e + 0.1 * E))
    return u


def huan3D(e, E, J):
    J1 = np.linalg.pinv(J)  # 雅克比矩阵求逆
    u = np.dot(J1, (0.8 * e))
    return u

def StateWrite():
    file_string = "State.txt"
    f1 = open(file_string, "w+")
    f1.write("1")
    f1.close()
    time.sleep(0.1)
    f1 = open(file_string, "w+")
    f1.write("0")
    f1.close()


def Read_file(D):
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
        a2 = a[0][2]
        e3 = a[0][3]
        indextmp = a[0][4]
        f.close()

    e2 = e3 / 121

    if D == 2:
        e00 = np.array([e0, e1])
        return e00
    if D == 3:
        e003 = np.array([e0, e1, e2])
        return e003
    if D == 4:
        e004 = np.array([e0, e1, a2, e3])
        return e004


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

T1 = np.array([1369.98, -1988.74, 1100.01])
myep = np.array([Trans[2, 3], Trans[0, 3]])
myOutput = T1
tmp = np.array([(myep[0], (-1.1 * myep[1]), 0)])
myOutput = myOutput + tmp
print("Init Location")
print(myOutput)

HOST = ''
PORT = 59152
x00 = myOutput[0, 0]
y00 = myOutput[0, 1]
z00 = myOutput[0, 2]
a00 = Euler1[0]
b00 = Euler1[1]
c00 = Euler1[2]
'''

x00 = 1389.98
y00 = -1988.74
z00 = 1100.01
a00 = 137.71
b00 = 25.95
c00 = -160.85

'''



data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
print("Send data:" + data1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
s.bind((HOST, PORT))  # 套接字绑定的IP与端口
s.listen(1)  # 开始TCP监听

E = np.array([0, 0])
Q = np.eye(4)
J = np.array([(-2.03376225, 0.54316436),
              (0.01525398, 4.36405703)])  # 试探性运动得到的初始雅克比矩阵
R1 = np.array([(0.5, 0, 0, 0), (0, 0.5, 0, 0), (0, 0, 0.5, 0), (0, 0, 0, 0.5)])  # 0.5×I4 状态噪声方差阵
R2 = np.array([(0.5, 0), (0, 0.5)])  # 0.5×I2 观测噪声方差阵
k = np.eye(2)
P = 10 ** 5 * np.array([(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)])  # P(0)为10^5×I4
u = np.array([0, 0])
y1 = np.array([300, 4])
I4 = np.array([(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)])
i = 0
K = np.array([0, 0, 0, 0, 0, 0, 0, 0]).reshape(4, 2)
X = np.array([0, 0])
# 读取txt中的图像坐标值
# 图像坐标
conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
print'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)
print("Recive data  " + data)
conn.sendall(data1)
StateWrite()

print("Wait for moving")
data = conn.recv(100)  # 把接收的数据实例化
print(data)
e00 = Read_file(2)

dis = 100000
txtname = "recordbigloop.txt"

mytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
f1 = file(txtname, "a+")  # 初始化距离参数
f1.write("Start to Record " + mytime + "\n")

e01tmp = np.array([0, 0])
eflag1 = e00

e003 = Read_file(3)

e013tmp = np.array([0, 0, 0])
eflag = e003
print("   \n")
print("XYPhi dias data:")
print(eflag)


while LA.norm(eflag, 2) > 8 or abs(eflag[2]) > 0.06:

    eflag1=Read_file(2)
    while LA.norm(eflag1, 2) > 7:
        print("  \n")
        print("XY dias data:")
        print(eflag1)
        conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
        print'Connected by', addr  # 输出客户端的IP地址
        data = conn.recv(100)  # 把接收的数据实例化
        # time.sleep(2)
        e01 = Read_file(2)
        if LA.norm(e01, 2) > 500:
            print("continue from 1, Too far from pixel")
            conn.sendall(data1)
            eflag1 = Read_file(2)
            continue
        x1 = np.array([J[0, 0], J[0, 1], J[1, 0], J[1, 1]])  # 将雅克比矩阵展开成向量
        y1 = e00 - e01  # 前后两次的图像坐标差值
        e000 = e00
        e00 = e01
        a1 = u[0]
        b1 = u[1]

        '''
        y1 = Cx1 + v;  v为观察噪声
        '''
        C = np.array([(a1, b1, 0, 0), (0, 0, a1, b1)])
        # 更新迭代过程
        Q00 = Q
        Q = P + R1
        k00 = k
        k = np.dot(np.dot(C, Q), C.T) + R2  # R1,R2噪声方差阵
        K00 = K
        K = np.dot(np.dot(Q, C.T), np.linalg.inv(k))
        P00 = P
        P = np.dot((I4 - np.dot(K, C)), Q)
        X00 = X
        X = y1 - np.dot(C, x1)
        # 迭代出新的x1向量
        x100 = x1
        x1 = x1 + np.dot(K, X)
        # 从x1得到新的雅克比矩阵
        J00 = J
        J = np.array([(x1[0], x1[1]), (x1[2], x1[3])])

        # 累计图像坐标差值，作为积分项
        E = E + e00
        # 代入函数生成下一周期的变换量
        u00 = u
        u = huan(e00, E, J)
        dis = LA.norm(u, 2)
        if dis > 60:
            e00 = e000
            Q = Q00
            k = k00
            K = K00
            P = P00
            X = X00
            x1 = x100
            J = J00
            E = E - e00
            print(u)
            u = u00

            print(J)
            print("continue from 2, too much controlling")
            conn.sendall(data1)
            eflag1 = Read_file(2)
            continue
        print("Controling Data:")
        print("%f,%f" % (u[0], u[1]))
        print("Right J")
        print(J)
        e01tmp = e01
        x00 = x00 + u[0]
        y00 = y00 + u[1]
        data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
        conn.sendall(data1)
        context = str(e00[0]) + " " + str(e00[1]) + " " + str(u[0]) + " " + str(u[1]) + " " + str(x00) + " " + str(
            y00) + '\n'
        f1.write(context)
        # 距离观测参数作为观测精度的计量
        # time.sleep(1)
        print("Wait for moving")
        data = conn.recv(100)  # 把接收的数据实例化
        print(data)
        eflag1 = Read_file(2)
    e013tmp = Read_file(3)
    print("   \n")
    print("Before XYPhi dias data:")
    print(e013tmp)
    print("Phi control")

    conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
    print'Connected by', addr  # 输出客户端的IP地址
    data = conn.recv(100)  # 把接收的数据实例化
    y00=y00 + 980 * np.sin(e013tmp[2] / 180 * pi)
    a00=a00 + e013tmp[2]
    data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
    context = str(x00) + " " + str(y00) + " " + str(a00) +'\n'
    f1.write(context)
    conn.sendall(data1)


    print("Wait for moving")
    data = conn.recv(100)  # 把接收的数据实例化
    print(data)
    eflag =  Read_file(3)
    print("   \n")
    print("After XYPhi dias data:")
    print(eflag)




mytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
f1.write("End of Record " + mytime + "\n")
f1.close()
# Down
conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
print'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)  # 把接收的数据实例化
print(data)

Judge_Data = Read_file(4)
print("Judge Data:")
print(Judge_Data)

print("Prepare to down\n")
time.sleep(2)

y01 = y00 - 20
data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y01, z00, a00, b00, c00)
conn.sendall(data1)

conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
print'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)  # 把接收的数据实例化
print(data)

# Final Pose
data1 = "%.2f,%.2f,1008.54,%.2f,%.2f,%.2f,\r\n" % (x00, y00, a00, b00, c00)
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
print'Connected by', addr  # 输出客户端的IP地址
data = conn.recv(100)  # 把接收的数据实例化
print(data)

c00 = 1  # 用于让机器人判断停止运动，退出循环
data1 = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,\r\n" % (x00, y00, z00, a00, b00, c00)
conn.sendall(data1)
#conn.close()  # 关闭连接
while 1:
    hold_on = 1