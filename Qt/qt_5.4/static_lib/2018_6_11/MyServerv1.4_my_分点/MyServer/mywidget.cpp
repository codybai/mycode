#include "mywidget.h"
#include "struct_object.h"
#include <QDebug>
#include "struct_object.h"
#include <QTimer>
#include <QBrush>
MyWidget::MyWidget(QWidget *parent) : QWidget(parent),m_w({0}),m_h({0})
{
    t= new QTimer;
    t->start();

    connect(t,SIGNAL(timeout()),this,SLOT(slotPaint()));
}

MyWidget::~MyWidget()
{

}
void MyWidget::slotPaint()
{
    this->update();
}
void MyWidget::slotGetInf(QByteArray array)
{
    mypacket packet={0};
    Object Targets[15]={0};//物体信息  15个
    //填充packet
    packet.header = array.mid(0,2);
    packet.seq_frame = array.mid(2,2);
    packet.keep = array.mid(4,4);
    packet.num_aim = array.mid(8,1);
    packet.a1 = array.mid(9,6);
    Targets[0].x = packet.a1.mid(4,2);
    Targets[0].y = packet.a1.mid(0,2);
    Targets[0].speed = packet.a1.mid(2,1);
    Targets[0].echo_rate = packet.a1.mid(3,1);
    packet.a2 = array.mid(15,6);
    Targets[1].x = packet.a2.mid(4,2);
    Targets[1].y = packet.a2.mid(0,2);
    Targets[1].speed = packet.a2.mid(2,1);
    Targets[1].echo_rate = packet.a2.mid(3,1);
    packet.a3 = array.mid(21,6);
    Targets[2].x = packet.a3.mid(4,2);
    Targets[2].y = packet.a3.mid(0,2);
    Targets[2].speed = packet.a3.mid(2,1);
    Targets[2].echo_rate = packet.a3.mid(3,1);
    packet.a4 = array.mid(27,6);
    Targets[3].x = packet.a4.mid(4,2);
    Targets[3].y = packet.a4.mid(0,2);
    Targets[3].speed = packet.a4.mid(2,1);
    Targets[3].echo_rate = packet.a4.mid(3,1);
    packet.a5 = array.mid(33,6);
    Targets[4].x = packet.a5.mid(4,2);
    Targets[4].y = packet.a5.mid(0,2);
    Targets[4].speed = packet.a5.mid(2,1);
    Targets[4].echo_rate = packet.a5.mid(3,1);
    packet.a6 = array.mid(39,6);
    Targets[5].x = packet.a6.mid(4,2);
    Targets[5].y = packet.a6.mid(0,2);
    Targets[5].speed = packet.a6.mid(2,1);
    Targets[5].echo_rate = packet.a6.mid(3,1);
    packet.a7 = array.mid(45,6);
    Targets[6].x = packet.a7.mid(4,2);
    Targets[6].y = packet.a7.mid(0,2);
    Targets[6].speed = packet.a7.mid(2,1);
    Targets[6].echo_rate = packet.a7.mid(3,1);
    packet.a8 = array.mid(51,6);
    Targets[7].x = packet.a8.mid(4,2);
    Targets[7].y = packet.a8.mid(0,2);
    Targets[7].speed = packet.a8.mid(2,1);
    Targets[7].echo_rate = packet.a8.mid(3,1);
    packet.a9 = array.mid(57,6);
    Targets[8].x = packet.a9.mid(4,2);
    Targets[8].y = packet.a9.mid(0,2);
    Targets[8].speed = packet.a9.mid(2,1);
    Targets[8].echo_rate = packet.a9.mid(3,1);
    packet.a10 = array.mid(63,6);
    Targets[9].x = packet.a10.mid(4,2);
    Targets[9].y = packet.a10.mid(0,2);
    Targets[9].speed = packet.a10.mid(2,1);
    Targets[9].echo_rate = packet.a10.mid(3,1);
    packet.a11 = array.mid(69,6);
    Targets[10].x = packet.a11.mid(4,2);
    Targets[10].y = packet.a11.mid(0,2);
    Targets[10].speed = packet.a11.mid(2,1);
    Targets[10].echo_rate = packet.a11.mid(3,1);
    packet.a12 = array.mid(75,6);
    Targets[11].x = packet.a12.mid(4,2);
    Targets[11].y = packet.a12.mid(0,2);
    Targets[11].speed = packet.a12.mid(2,1);
    Targets[11].echo_rate = packet.a12.mid(3,1);
    packet.a13 = array.mid(81,6);
    Targets[12].x = packet.a13.mid(4,2);
    Targets[12].y = packet.a13.mid(0,2);
    Targets[12].speed = packet.a13.mid(2,1);
    Targets[12].echo_rate = packet.a13.mid(3,1);
    packet.a14 = array.mid(87,6);
    Targets[13].x = packet.a14.mid(4,2);
    Targets[13].y = packet.a14.mid(0,2);
    Targets[13].speed = packet.a14.mid(2,1);
    Targets[13].echo_rate = packet.a14.mid(3,1);
    packet.a15 = array.mid(93,6);
    Targets[14].x = packet.a15.mid(4,2);
    Targets[14].y = packet.a15.mid(0,2);
    Targets[14].speed = packet.a15.mid(2,1);
    Targets[14].echo_rate = packet.a15.mid(3,1);
    packet.check =array.mid(99,1);

    QString s = array.toHex()+"\nparse:";

    for(int i = 0;i<15;i++)
    {
        //转换字节序
        QByteArray a =Targets[i].x.mid(0,1);   //低字节
        QByteArray b= Targets[i].x.mid(1,1);   //高字节
        b.append(a);
        Targets[i].x = b;
        QByteArray c=Targets[i].y.mid(0,1);   //低字节
        QByteArray d=Targets[i].y.mid(1,1);   //高字节
        d.append(c);
        Targets[i].y = d;
        Targets[i].intx = (short)Targets[i].x.toHex().toInt(0,16)*0.1;
        Targets[i].inty = (unsigned short)Targets[i].y.toHex().toInt(0,16)*0.1;

        if(Targets[i].speed!=0)
        {
            this->m_w[i]=Targets[i].intx;
            this->m_h[i]=Targets[i].inty;
        }
    }
}
//放大版本
//void MyWidget::paintEvent(QPaintEvent *)
//{
//    int side  = qMin(width(),height());
//    painter = new QPainter(this);
//    painter->setRenderHint(QPainter::Antialiasing,true);
//    painter->translate(width()/2,height()/1.1);//把原点移到窗口中心
//    painter->scale(side/1500.0,side/1500.0);//坐标变换比例，随窗口缩放
//    painter->scale(1,-1);//Y轴向上反转，成为正常的平面直角坐标系
//    painter->setPen(QPen(Qt::black,height()/600));

//    painter->drawLine(-2000,0,2000,0);
//    painter->drawLine(0,1500,0,-1500);
//    painter->drawLine(-2000,150,2000,150);
//    painter->setBrush(QBrush(Qt::red,Qt::SolidPattern));
//    painter->setPen(QPen(Qt::red,height()/600));
//    for(int i=0;i<15;i++)
//    {
////        if(m_w[i] !=0&&m_h[i]!=0)
//        {
//        painter->drawEllipse(0-m_w[i]-20,m_h[i]-20,40,40);//-4是为了让实心圆中心对准原点坐标
////           qDebug()<<"j"+i;

//        }
//    }
//    delete(painter);
//    painter=NULL;


//}


void MyWidget::paintEvent(QPaintEvent *)
{
    int side  = qMin(width(),height());
    painter = new QPainter(this);
    painter->setRenderHint(QPainter::Antialiasing,true);
    painter->translate(width()/2,height()/1.1);//把原点移到窗口中心
    painter->scale(side/600.0,side/600.0);//坐标变换比例，随窗口缩放
    painter->scale(1,-1);//Y轴向上反转，成为正常的平面直角坐标系
    painter->setPen(QPen(Qt::black,height()/400));
    painter->drawLine(0,3000,0,-3000);
    painter->drawLine(-3000,0,3000,0);
    painter->setPen(QPen(Qt::blue,height()/2000));
//    painter->drawLine(-3000,480,3000,480);
//    painter->drawLine(-3000,450,3000,450);
//    painter->drawLine(-3000,420,3000,420);
//    painter->drawLine(-3000,390,3000,390);
//    painter->drawLine(-3000,360,3000,360);
//    painter->drawLine(-3000,330,3000,330);
//    painter->drawLine(-3000,300,3000,300);
//    painter->drawLine(-3000,270,3000,270);
//    painter->drawLine(-3000,240,3000,240);
    painter->drawLine(-3000,210,3000,210);
    painter->drawLine(-3000,180,3000,180);
    painter->drawLine(-3000,150,3000,150);
//    painter->drawLine(-3000,120,3000,120);
//    painter->drawLine(-3000,90,3000,90);
//    painter->drawLine(-3000,60,3000,60);
//    painter->drawLine(-3000,30,3000,30);

//    painter->drawLine(-2000,150,2000,150);
    painter->setBrush(QBrush(Qt::red,Qt::SolidPattern));
    painter->setPen(QPen(Qt::red,height()/600));
    for(int i=0;i<15;i++)
    {
        if(m_w[i] !=0&&m_h[i]!=0)//
        {
        painter->drawEllipse(0-m_w[i]*10-5,m_h[i]*10-5,10,10);//-4是为了让实心圆中心对准原点坐标
//           qDebug()<<"j"+i;

        }
    }
    delete(painter);
    painter=NULL;


}

