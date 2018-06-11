#ifndef MYTCPSERVER_H
#define MYTCPSERVER_H
#include <QTcpServer>
#include <QMap>
#include "radar_object.h"

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
    int cnt_client;
    QMap<qintptr,QTcpSocket*> * clientsList;
    QMetaObject::Connection dis;
signals:
    void msgSingal(QString);
    void SendMsgSignal(QString);
    void signal_inf(RADAR_PACKET);//
public slots:
    void slotSingal_inf(RADAR_PACKET packet);//
    void msgSlot(QString s);
    void ListCountSlot(int i);

};

#endif // MYTCPSERVER_H
