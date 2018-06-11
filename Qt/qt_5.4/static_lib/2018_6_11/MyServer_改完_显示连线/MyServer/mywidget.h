#ifndef MYWIDGET_H
#define MYWIDGET_H
#include "radar_object.h"
#include <QWidget>
#include <QPainter>
class MyWidget : public QWidget
{
    Q_OBJECT
public:
    explicit MyWidget(QWidget *parent = 0);
    ~MyWidget();
protected:
    void paintEvent(QPaintEvent *);

signals:

public slots:
    void slotGetInf(RADAR_PACKET);
    void slotPaint();
public:
    QPainter *painter;
    int m_w[15];
    int m_h[15];
    QTimer *t ;
};

#endif // MYWIDGET_H
