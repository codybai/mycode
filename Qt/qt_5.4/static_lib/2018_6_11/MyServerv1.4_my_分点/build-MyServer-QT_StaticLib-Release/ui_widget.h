/********************************************************************************
** Form generated from reading UI file 'widget.ui'
**
** Created by: Qt User Interface Compiler version 5.4.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_WIDGET_H
#define UI_WIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include <mywidget.h>

QT_BEGIN_NAMESPACE

class Ui_Widget
{
public:
    QVBoxLayout *verticalLayout_2;
    MyWidget *widget;
    QTextEdit *textEdit;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_3;
    QLabel *label_onlinenum;
    QLabel *label_max_angle;
    QHBoxLayout *horizontalLayout_2;
    QLineEdit *sentToClientEditLine;
    QPushButton *pushButton_4;
    QHBoxLayout *horizontalLayout;
    QPushButton *pushButton;
    QPushButton *pushButton_2;
    QPushButton *pushButton_3;

    void setupUi(QWidget *Widget)
    {
        if (Widget->objectName().isEmpty())
            Widget->setObjectName(QStringLiteral("Widget"));
        Widget->resize(1139, 661);
        verticalLayout_2 = new QVBoxLayout(Widget);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        widget = new MyWidget(Widget);
        widget->setObjectName(QStringLiteral("widget"));
        widget->setMinimumSize(QSize(761, 391));

        verticalLayout_2->addWidget(widget);

        textEdit = new QTextEdit(Widget);
        textEdit->setObjectName(QStringLiteral("textEdit"));

        verticalLayout_2->addWidget(textEdit);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setSpacing(6);
        horizontalLayout_3->setObjectName(QStringLiteral("horizontalLayout_3"));
        label_onlinenum = new QLabel(Widget);
        label_onlinenum->setObjectName(QStringLiteral("label_onlinenum"));
        label_onlinenum->setMinimumSize(QSize(0, 31));
        label_onlinenum->setMaximumSize(QSize(16777215, 31));

        horizontalLayout_3->addWidget(label_onlinenum);

        label_max_angle = new QLabel(Widget);
        label_max_angle->setObjectName(QStringLiteral("label_max_angle"));

        horizontalLayout_3->addWidget(label_max_angle);


        verticalLayout->addLayout(horizontalLayout_3);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        sentToClientEditLine = new QLineEdit(Widget);
        sentToClientEditLine->setObjectName(QStringLiteral("sentToClientEditLine"));

        horizontalLayout_2->addWidget(sentToClientEditLine);

        pushButton_4 = new QPushButton(Widget);
        pushButton_4->setObjectName(QStringLiteral("pushButton_4"));
        pushButton_4->setMinimumSize(QSize(91, 31));
        pushButton_4->setMaximumSize(QSize(91, 31));

        horizontalLayout_2->addWidget(pushButton_4);


        verticalLayout->addLayout(horizontalLayout_2);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        pushButton = new QPushButton(Widget);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setMinimumSize(QSize(91, 31));
        pushButton->setMaximumSize(QSize(91, 31));

        horizontalLayout->addWidget(pushButton);

        pushButton_2 = new QPushButton(Widget);
        pushButton_2->setObjectName(QStringLiteral("pushButton_2"));
        pushButton_2->setMinimumSize(QSize(91, 31));
        pushButton_2->setMaximumSize(QSize(91, 31));

        horizontalLayout->addWidget(pushButton_2);

        pushButton_3 = new QPushButton(Widget);
        pushButton_3->setObjectName(QStringLiteral("pushButton_3"));
        pushButton_3->setMinimumSize(QSize(91, 31));
        pushButton_3->setMaximumSize(QSize(91, 31));

        horizontalLayout->addWidget(pushButton_3);


        verticalLayout->addLayout(horizontalLayout);


        verticalLayout_2->addLayout(verticalLayout);


        retranslateUi(Widget);

        QMetaObject::connectSlotsByName(Widget);
    } // setupUi

    void retranslateUi(QWidget *Widget)
    {
        Widget->setWindowTitle(QApplication::translate("Widget", "\346\234\215\345\212\241\345\231\250", 0));
        label_onlinenum->setText(QApplication::translate("Widget", "FA01XX(XX:32-c8,\345\200\274\350\266\212\344\275\216\345\217\221\347\216\260\347\211\251\344\275\223\346\246\202\347\216\207\350\266\212\351\253\230) FA02XX(XX:32-c8,\345\200\274\350\266\212\344\275\216\345\217\221\347\216\260\347\211\251\344\275\223\346\246\202\347\216\207\350\266\212\351\253\230) FA07XX(XX:02\344\273\243\350\241\250\346\243\200\346\265\2130.2\347\261\263/s\344\273\245\344\270\212\351\200\237\345\272\246)", 0));
        label_max_angle->setText(QString());
        pushButton_4->setText(QApplication::translate("Widget", "\345\217\221\351\200\201\345\221\275\344\273\244", 0));
        pushButton->setText(QApplication::translate("Widget", "\345\274\200\345\220\257\346\234\215\345\212\241\345\231\250", 0));
        pushButton_2->setText(QApplication::translate("Widget", "\346\270\205\347\251\272\344\277\241\346\201\257", 0));
        pushButton_3->setText(QApplication::translate("Widget", "\345\205\263\351\227\255\346\234\215\345\212\241\345\231\250", 0));
    } // retranslateUi

};

namespace Ui {
    class Widget: public Ui_Widget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_WIDGET_H
