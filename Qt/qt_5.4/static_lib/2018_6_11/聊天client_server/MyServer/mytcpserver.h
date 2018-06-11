#ifndef MYTCPSERVER_H
#define MYTCPSERVER_H
#include <QTcpServer>
#include <QMap>

class MyTcpServer : public QTcpServer
{
    Q_OBJECT
public:
    MyTcpServer();
    ~MyTcpServer();
public:
    virtual void incomingConnection(qintptr socketID);
    void sentToAllClient(QString);
public:
    QMap<qintptr,QTcpSocket*> * clientsList;
    QMetaObject::Connection dis;
signals:
    void msgSingal(QString);
    void SendMsgSignal(QString);
public slots:
    void msgSlot(QString s);
    void ListCountSlot(int i);

};

#endif // MYTCPSERVER_H
