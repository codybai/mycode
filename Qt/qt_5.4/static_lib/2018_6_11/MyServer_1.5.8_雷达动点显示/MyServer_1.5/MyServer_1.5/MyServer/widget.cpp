#include "widget.h"
#include "ui_widget.h"
#include "QHostAddress"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{

    ui->setupUi(this);
    ui->pushButton_2->setEnabled(false);
    ui->pushButton_3->setEnabled(false);
    ui->pushButton_4->setEnabled(false);
}

Widget::~Widget()
{
    delete ui;
}

void Widget::pickConnectionSlot()
{
    connect(socket,SIGNAL(readyRead()),this,SLOT(readMsgSlot()));
}

void Widget::countTime()
{
}


void Widget::on_pushButton_clicked()
{

    server = new MyTcpServer();
    server->listen(QHostAddress::Any,4001);
    starttime = QDateTime::currentDateTime();
    timer = new QTimer();
    connect(timer,&QTimer::timeout,this,&Widget::countTime);
    connect(server,SIGNAL(msgSingal(QString)),this,SLOT(msgToWidget(QString)));
    connect(server,SIGNAL(signal_inf(RADAR_PACKET)),ui->widget,SLOT(slotGetInf(RADAR_PACKET)));//参数
    connect(this,SIGNAL(clearPointsSignals()),ui->widget,SLOT(slotClearPoints()));
    timer->start(1090);
    ui->pushButton_2->setEnabled(true);
    ui->pushButton_3->setEnabled(true);
    ui->pushButton_4->setEnabled(true);
    ui->pushButton->setEnabled(false);
}

void Widget::msgToWidget(QString s)
{
    ui->textEdit->append(s);

}

void Widget::on_pushButton_3_clicked()
{

    this->close();
}

void Widget::on_pushButton_4_clicked()
{
//    点击群发功能代码
    if(server->clientsList->isEmpty())
    {
        qDebug()<<"no client";
        return;
    }
    server->sentToAllClient(ui->sentToClientEditLine->text());
}

void Widget::on_pushButton_2_clicked()
{
    ui->textEdit->clear();
}

void Widget::on_textEdit_destroyed()
{
}

void Widget::on_clearPoints_clicked()
{
    emit clearPointsSignals();
}
