#ifndef _RADAR_OBJECT_
#define _RADAR_OBJECT_
#include <QByteArray>
typedef struct _RADAR_OBJECT
{
    short x;                //有符号数 //
    unsigned short y;       //无符号数//
    char speed;             //有符号数//
    unsigned char echo;     //无符号数//
}RADAR_OBJECT;

typedef struct _RADAR_PACKET //
{    
    QByteArray rawinfo;//
    QByteArray header;
    unsigned short seq;   //
    unsigned int reserved;//
    unsigned char count;  //
    RADAR_OBJECT object[15];//
    unsigned char check;   //
}RADAR_PACKET;//

#endif // _RADAR_OBJECT_

