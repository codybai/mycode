#-------------------------------------------------
#
# Project created by QtCreator 2017-09-21T20:33:06
#
#-------------------------------------------------

QT       += core gui
QT       +=network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MyServer
TEMPLATE = app


SOURCES += main.cpp\
        widget.cpp \
    workthread.cpp \
    mytcpserver.cpp \
    mytcpsocket.cpp \
    mywidget.cpp

HEADERS  += widget.h \
    workthread.h \
    mytcpserver.h \
    mytcpsocket.h \
    mywidget.h \
    radar_object.h

FORMS    += widget.ui

RESOURCES += \
    res.qrc

RC_ICONS=nn.ico
