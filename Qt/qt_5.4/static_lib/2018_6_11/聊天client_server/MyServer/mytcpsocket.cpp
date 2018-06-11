#include "mytcpsocket.h"

MyTcpSocket::MyTcpSocket()
{
    connect(this,SIGNAL(disconnected()),this,SLOT(ToEmit()));
}

MyTcpSocket::~MyTcpSocket()
{

}
void MyTcpSocket::sentToClientSlot(QString s)
{
    qDebug()<<"send to client:"<<s;
    s="来自服务器的消息："+s;
    this->write(s.toLocal8Bit());
}
void MyTcpSocket::ToEmit()
{
    qDebug()<<"ToEmit："<<this->socketDescriptor();
    emit MyDisconnetc(this->socketDescriptor());
}
