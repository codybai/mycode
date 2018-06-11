#ifndef STRUCT_OBJECT
#define STRUCT_OBJECT
typedef struct mypacket
{
    QByteArray header;
    QByteArray seq_frame;
    QByteArray keep;
    QByteArray num_aim;
    QByteArray a1;
    QByteArray a2;
    QByteArray a3;
    QByteArray a4;
    QByteArray a5;
    QByteArray a6;
    QByteArray a7;
    QByteArray a8;
    QByteArray a9;
    QByteArray a10;
    QByteArray a11;
    QByteArray a12;
    QByteArray a13;
    QByteArray a14;
    QByteArray a15;
    QByteArray check;
}mypacket;

typedef struct Object
{
    QByteArray x;//有符号数
    QByteArray y;//无符号数
    QByteArray speed; //有符号数
    QByteArray echo_rate; //无符号数
    double intx;   //所在x
    double inty;    //所在y
}Object;
#endif // STRUCT_OBJECT

