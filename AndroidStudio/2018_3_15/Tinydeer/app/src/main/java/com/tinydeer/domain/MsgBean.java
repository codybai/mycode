package com.tinydeer.domain;

/**
 * Created by baicol on 2018-03-13.
 */

public class MsgBean {

    /**
     * content : 是吗
     * Cname : admin
     * num : 1
     * time : 2018-03-13
     * Pid : 168
     */

    private String content;
    private String Cname;
    private int num;
    private String time;
    private int Pid;

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getCname() {
        return Cname;
    }

    public void setCname(String Cname) {
        this.Cname = Cname;
    }

    public int getNum() {
        return num;
    }

    public void setNum(int num) {
        this.num = num;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public int getPid() {
        return Pid;
    }

    public void setPid(int Pid) {
        this.Pid = Pid;
    }
}
