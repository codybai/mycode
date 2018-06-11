#include "workthread.h"
#include <QDebug>
#include <iomanip>
#include <iostream>
#include <QtMath>
WorkThread::WorkThread(QTcpSocket* socket,QString Msg)
{
    m_socket = socket;
    max_angle =0.0;

}
//多客户端与多进程处理
void WorkThread::run()
{
    connect(m_socket,SIGNAL(readyRead()),this,SLOT(readSlot()));
    qDebug()<<"thread:"<<m_socket->socketDescriptor();
    QString str = "正在为您服务的进程ID为："+QString::number(int(QThread::currentThreadId()))+",您已经成功连接服务器！";
    thID = QString::number(int(QThread::currentThreadId()));

    m_socket->write(str.toLocal8Bit());
    exec();
}



void WorkThread::readSlot()
{
    QByteArray array= m_socket->readAll();
    qDebug()<<"size:"<<array.size()<<"sum:"<<(unsigned char)(array[99]);

    RADAR_PACKET packet={0};
    RADAR_OBJECT Targets[15]={0};//物体信息  15个

    for(int i = 0; i < 99; i++)   //for和if语句新加的，判断校验字节
    {
        packet.check += array[i];
    }
    unsigned char check = (unsigned char)array[99];
    if(packet.check == check)
    {
    }
    //填充packet
    packet.rawinfo = array;
    packet.header = array.mid(0,2);
    packet.seq = (unsigned char)array[2];
    packet.reserved = (unsigned int)array[4];
    packet.count = array[8];


    for(int i = 0; i < packet.count; i++)
    {
        QByteArray obj = array.mid(i*6 + 9, 6);
        packet.object[i].y = (unsigned short)obj[0];
        packet.object[i].speed = (signed char)obj[2];
        packet.object[i].echo = obj[3];
        packet.object[i].x = (signed short)obj[4];

    }

    QString s = thID+":"+array.toHex()+"\nparse:";

    register double j;

    for(int i = 0;i<packet.count;i++)
    {
        j=0;
        s+="\n目标";
        s+=QString::number(i);
        s+="->(x,y)=(";
        s+=""+QString::number(packet.object[i].x*0.1);
        s+=",";
        s+=QString::number(packet.object[i].y*0.1);
        s+="),speed: ";
        s+=QString::number(packet.object[i].speed*0.1);
        s+=" echo_rate:";
        s+=QString::number(packet.object[i].echo);
        s+="packet.check:";
        s+=QString::number(packet.check);
        s+="check:";
        s+=QString::number(check);

    }
    qDebug()<<"最大角度为："<<qAtan(j);
    emit getMsg(s);
    emit signal_inf(packet);
}
WorkThread::~WorkThread()

{
}
