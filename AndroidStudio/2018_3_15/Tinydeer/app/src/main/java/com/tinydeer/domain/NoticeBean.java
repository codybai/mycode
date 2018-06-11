package com.tinydeer.domain;

/**
 * Created by baicol on 2018-03-13.
 */

public class NoticeBean {


    /**
     * Pcontent :
     * title : 西安交大师生关注两会 热议政府工作报告
     * Ptime : 2018-03-14
     * Pid : 2
     */

    private String Pcontent;
    private String title;
    private String Ptime;
    private int Pid;

    public String getPcontent() {
        return Pcontent;
    }

    public void setPcontent(String Pcontent) {
        this.Pcontent = Pcontent;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getPtime() {
        return Ptime;
    }

    public void setPtime(String Ptime) {
        this.Ptime = Ptime;
    }

    public int getPid() {
        return Pid;
    }

    public void setPid(int Pid) {
        this.Pid = Pid;
    }
}
