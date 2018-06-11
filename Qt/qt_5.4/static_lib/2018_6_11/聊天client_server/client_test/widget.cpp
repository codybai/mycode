#include "widget.h"
#include "ui_widget.h"
#include <QHostAddress>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
        ui->pushButton->setEnabled(false);


}

Widget::~Widget()
{
    delete ui;
}
void Widget::initButtn()
{
    ui->pushButton->setEnabled(false);
    ui->pushButton_2->setEnabled(true);
}
void Widget::on_pushButton_clicked()
{
    QString msg = ui->sendMsgTextEdit->toPlainText();
//    m_socket->write(msg.toLocal8Bit());
    m_socket->write(msg.toLocal8Bit());

}

void Widget::on_pushButton_2_clicked()
{

    m_socket = new QTcpSocket();
    m_socket->connectToHost(QHostAddress("127.0.0.1"),9999);
    if(!m_socket->isOpen())
    {
        return;
    }
    connect(m_socket,&QTcpSocket::disconnected,this,&Widget::disconnectSlot);
    connect(m_socket,&QTcpSocket::readyRead,this,&Widget::readMsgSlot);
    connect(m_socket,SIGNAL(disconnected()),this,SLOT(initButtn()));
    connect(m_socket,&QTcpSocket::connected,this,&Widget::connectStatSlot);
    ui->pushButton_2->setEnabled(false);
    ui->pushButton->setEnabled(true);
}
void Widget::connectStatSlot()
{
     ui->ShowtextEdit->append("服务器连接成功！");
}
void Widget::disconnectSlot()
{
    ui->ShowtextEdit->append("服务器断开连接！");
}
void Widget::readMsgSlot()
{
    ui->ShowtextEdit->append(QString::fromLocal8Bit(m_socket->readAll()));
}

