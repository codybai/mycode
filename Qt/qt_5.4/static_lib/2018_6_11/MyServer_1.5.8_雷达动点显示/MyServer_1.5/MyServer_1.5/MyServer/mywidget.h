#ifndef MYWIDGET_H
#define MYWIDGET_H
#include "radar_object.h"
#include <QWidget>
#include <QPainter>
#include <QList>
typedef struct _Points{
    int m_x[15];
    int m_y[15];
}Points;
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
    void slotClearPoints();
    void slotGetInf(RADAR_PACKET);
    void slotPaint();
public:
    QPainter *painter;
    int m_x[15];
    int m_y[15];
    int m_speed[15];
    QTimer *t ;
    QList<Points> *pList;

};

#endif // MYWIDGET_H
