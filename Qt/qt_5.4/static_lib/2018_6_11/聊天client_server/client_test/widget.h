#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QTcpSocket>
namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();
public slots:
    void connectStatSlot();
    void disconnectSlot();
    void readMsgSlot();
    void initButtn();
private:
    Ui::Widget *ui;
public:
    QTcpSocket* m_socket;
};

#endif // WIDGET_H
