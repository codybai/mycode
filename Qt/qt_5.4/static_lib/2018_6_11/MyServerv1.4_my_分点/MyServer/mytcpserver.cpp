#include "mytcpserver.h"
#include <QDebug>
#include <QThread>
#include "mytcpsocket.h"
#include "workthread.h"
MyTcpServer::MyTcpServer()
{
    clientsList = new QMap<int,QTcpSocket*>;
}

void MyTcpServer::incomingConnection(qintptr socketID)
{
    MyTcpSocket* socket = new MyTcpSocket;
//    QThread * thread = new QThread(socket);//把线程的父类设为连接的，防止内存泄漏
    //可以信号连接信号的，我要捕捉线程ID就独立出来函数了，使用中还是直接连接信号效率应该有优势
    socket->setSocketDescriptor(socketID);
    clientsList->insert(socketID,socket);
    cnt_client++;
//    qDebug()<<"incoming:"<<socket->socketDescriptor();
    WorkThread* th = new WorkThread(socket," 欢迎访问服务器！");
    connect(th,SIGNAL(getMsg(QString)),this,SLOT(msgSlot(QString)));
    connect(th,SIGNAL(signal_inf(QByteArray)),this,SLOT(slotSingal_inf(QByteArray)));
    connect(socket,SIGNAL(MyDisconnetc(int)),this,SLOT(ListCountSlot(int)));/////////??????

   dis =connect(socket,SIGNAL(disconnected()),th,SLOT(quit()));//链接断开则对应线程结束
   connect(this,SIGNAL(SendMsgSignal(QString)),socket,SLOT(sentToClientSlot(QString)));//群发消息

    socket->moveToThread(th);
    th->start();
}
void MyTcpServer::msgSlot(QString s )
{
    emit msgSingal(s);
}
MyTcpServer::~MyTcpServer()
{

}

void MyTcpServer::ListCountSlot(int id)
{
//    qDebug()<<clientsList->count();
//    qDebug()<<"dis soketID:"<<id;
//    qDebug()<<clientsList;
//    qDebug()<<clientsList->remove(id);
//    qDebug()<<clientsList->count();
}
void MyTcpServer::sentToAllClient(QString msg)
{
    qDebug()<<"emit signal to send to client";
    emit SendMsgSignal(msg);
}
void MyTcpServer::slotSingal_inf(QByteArray array)
{
    emit signal_inf(array);
}
