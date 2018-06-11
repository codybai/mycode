#ifndef WIDGET_H
#define WIDGET_H
#include<QTcpServer>
#include <QWidget>
#include <QTimer>
#include <QTcpSocket>
#include "mytcpserver.h"
#include <QDateTime>
namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();
public:
    MyTcpServer* server;
    QTcpSocket* socket;
    QTimer* timer;
    QDateTime currenttime;
    QDateTime starttime;

public slots:
//    void readMsgSlot();
    void pickConnectionSlot();
    void countTime();
 signals:
    void clearPointsSignals();
private slots:
    void on_pushButton_clicked();
    void msgToWidget(QString s);
    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void on_pushButton_2_clicked();

    void on_textEdit_destroyed();

    void on_clearPoints_clicked();

private:
    Ui::Widget *ui;
};

#endif // WIDGET_H
