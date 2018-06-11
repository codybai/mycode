package com.tinydeer.Utils;

/**
 * Created by baicol on 2018-03-10.
 */

public class Util {
    public static String Url                                  =       "http://192.168.1.6:8080/web";
    public static String URL_GET_FOCUS_USER_BY_USERID         = Url + "/QueryConcernByUser" ;        //根据用户id请求用户关注的用户
    public static String URL_GET_USERBEAN_BY_CLICK_MY         = Url + "/QueryStuByUserServlet";    //点击我的进行数据获取userBean
    public static String URL_REGISTER_ACCESS                  = Url + "/RegisterServlet";           //注册访问连接
    public static String URL_LOGIN                            = Url + "/loginServlet";              //登陆
    public static String URL_SAVE_INFO_TO_SEVER               = Url + "/UpdateStuServlet";          //保存数据到服务器
    public static String URL_GET_MY_PUBLISHED_POST_BY_USERID  = Url + "/QueryPostByUser";           //根据用户名获取发表的文章
    public static String URL_GET_MY_STORED_POST_BY_USERID     = Url + "/QueryCollectionByUser";    //根据用户名获取收藏的文章
    public static String URL_QUERY_ALL_POST                   = Url + "/QueryAllPostServlet";      //显示所有的帖子
    public static String URL_PUBLISH_POST_TO_SERVER           = Url + "/PublishPostServlet";
    public static String URL_GET_POST_BY_TYPE                 = Url + "/QueryPostByType";
    public static String URL_GET_POST_DETAIL_BY_PID           = Url + "/ViewPostServlet";
    public static String URL_GET_CONMENT_BY_PID               = Url + "/QueryCommentByPid";
    public static String URL_TELL_SERVER_UPTIMES_PLUS         = Url + "/LoveServlet";
    public static String URL_CLICK_STORE_PLUS                 = Url + "/CollectionServlet";
    public static String URL_BUTTON_WRITE_REPLY               = Url + "/PublishCommentServlet";
    public static String URL_GET_ALL_NOTICE                   = Url + "/QueryNoticeServlet" ;
    public static String URL_GET_DETAIL_NOTICE_BY_ONE         = Url + "/ViewNoticeServlet";
    public static String URL_GET_ALL_MY_MSG                   = Url + "/QueryMessageByUser";
    public static String URL_TELL_SERVER_READ_YET               = Url + "/ViewMessageServlet";

}
