#include "mywidget.h"
#include "radar_object.h"
#include <QDebug>
#include <QTimer>
#include <QBrush>
MyWidget::MyWidget(QWidget *parent) : QWidget(parent),m_x({0}),m_y({0})
{
    pList = new QList<Points>();
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
void MyWidget::slotGetInf(RADAR_PACKET packet) //参数
{
    Points p = {0};
    for(int i = 0; i < packet.count; i++)
    {
       p.m_y[i] = packet.object[i].y*0.1;
       p.m_x[i] = packet.object[i].x*0.1;
    }
    pList->append(p);
}
void MyWidget::slotClearPoints(){
    pList->clear();
}

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


    painter->drawLine(-3000,210,3000,210);
    painter->drawLine(-3000,180,3000,180);
    painter->drawLine(-3000,150,3000,150);

    painter->setBrush(QBrush(Qt::red,Qt::SolidPattern));
    painter->setPen(QPen(Qt::red,height()/600));


    for(int j = 0;j<pList->length();j++){
        for(int i=0;i<15;i++)
        {
            if(pList->at(j).m_x[i] !=0&&pList->at(j).m_y[i]!=0)//
    //        if(m_speed[i]!=0)
            {
                painter->drawEllipse(0-pList->at(j).m_x[i]*10-5,pList->at(j).m_y[i]*10-5,10,10);//-4是为了让实心圆中心对准原点坐标
            }
        }

    }


    delete(painter);
    painter=NULL;

}

