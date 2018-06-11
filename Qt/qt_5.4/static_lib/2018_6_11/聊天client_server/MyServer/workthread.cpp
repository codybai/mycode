#include "workthread.h"
#include <QDebug>
WorkThread::WorkThread(QTcpSocket* socket,QString Msg)
{
    m_socket = socket;
}

void WorkThread::run()
{
    connect(m_socket,SIGNAL(readyRead()),this,SLOT(readSlot()));
    qDebug()<<"thread:"<<m_socket->socketDescriptor();
    QString str = "正在为您服务的进程ID为："+QString::number(int(QThread::currentThreadId()))+",您已经成功连接服务器！";
    thID = QString::number(int(QThread::currentThreadId()));
    qDebug()<<Msg;
    m_socket->write(str.toLocal8Bit());
    exec();
}
void WorkThread::readSlot()
{
    QString s = thID+":"+m_socket->readAll();
    emit getMsg(s);
}
WorkThread::~WorkThread()
{
}
