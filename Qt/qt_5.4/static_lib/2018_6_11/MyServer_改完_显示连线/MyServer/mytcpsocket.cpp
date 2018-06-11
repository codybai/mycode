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
    s="来自服务器的消息："+s;
    this->write(s.toLocal8Bit());
}
void MyTcpSocket::ToEmit()
{
    emit MyDisconnetc(this->socketDescriptor());
}
