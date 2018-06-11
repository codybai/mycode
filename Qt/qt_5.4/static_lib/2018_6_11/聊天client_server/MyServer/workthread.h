#ifndef WORKTHREAD_H
#define WORKTHREAD_H
#include <QTcpServer>
#include <QThread>
#include <QString>
#include "mytcpsocket.h"
class WorkThread : public QThread
{
    Q_OBJECT
public:
    WorkThread(QTcpSocket* socket,QString Msg);
    ~WorkThread();
    virtual void run();
QTcpSocket* m_socket;
QString Msg;
signals:
    void getMsg(QString);
    void dissocketID(qintptr);

public slots:
    void readSlot();
public:
    QString thID ;
};

#endif // WORKTHREAD_H
