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

//    ui->label_onlinenum->setText("在线人数："+QString::number(server->clientsList->count()));


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
//    QDateTime currenttime = QDateTime::currentDateTime();//
//    ui->label_onlinenum->setText("连接的客户端数："+QString::number(this->server->clientsList->count()));
//    ui->label_worktime->setText("服务端已运行："+QString::number(starttime.msecsTo(currenttime)/1000)+"秒");

}


void Widget::on_pushButton_clicked()
{

    server = new MyTcpServer();
    server->listen(QHostAddress::Any,4001);
    starttime = QDateTime::currentDateTime();
    timer = new QTimer();
    connect(timer,&QTimer::timeout,this,&Widget::countTime);
    connect(server,SIGNAL(msgSingal(QString)),this,SLOT(msgToWidget(QString)));
    connect(server,SIGNAL(signal_inf(QByteArray)),ui->widget,SLOT(slotGetInf(QByteArray)));
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

//    测试画图

}

void Widget::on_pushButton_2_clicked()
{
    ui->textEdit->clear();
}

void Widget::on_textEdit_destroyed()
{
//    ui->textEdit->clear();
}
