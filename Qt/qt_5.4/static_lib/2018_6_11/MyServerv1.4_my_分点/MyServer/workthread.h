#ifndef WORKTHREAD_H
#define WORKTHREAD_H
#include <QTcpServer>
#include <QThread>
#include <QString>
#include "mytcpsocket.h"
#include "struct_object.h"
class WorkThread : public QThread
{
    Q_OBJECT
public:
    WorkThread(QTcpSocket* socket,QString Msg);
    ~WorkThread();
protected://线程处理函数
    virtual void run();
QTcpSocket* m_socket;
QString Msg;
signals:
    void getMsg(QString);
    void dissocketID(qintptr);
    void signal_inf(QByteArray);
    void send_angle(double);

public slots:
    void readSlot();
public:
    QString thID ;
    double max_angle;
};

#endif // WORKTHREAD_H
