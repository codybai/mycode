#ifndef MYTCPSOCKET_H
#define MYTCPSOCKET_H
#include <QTcpSocket>

class MyTcpSocket : public QTcpSocket
{
    Q_OBJECT
public:
    MyTcpSocket();
    ~MyTcpSocket();
public:

signals:
    void MyDisconnetc(int id);
public slots:
    void sentToClientSlot(QString s);

    void ToEmit();
};

#endif // MYTCPSOCKET_H
