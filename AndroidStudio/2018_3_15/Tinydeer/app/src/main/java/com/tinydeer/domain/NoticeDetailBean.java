package com.tinydeer.domain;

/**
 * Created by baicol on 2018-03-13.
 */

public class NoticeDetailBean {

    /**
     * content :
     编辑：
     星 火
     * time : 2018-03-14
     * title : 西安交大师生关注两会 热议政府工作报告
     * browsernum : 0
     * Pid : 2
     */

    private String content;
    private String time;
    private String title;
    private int browsernum;
    private int Pid;

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public int getBrowsernum() {
        return browsernum;
    }

    public void setBrowsernum(int browsernum) {
        this.browsernum = browsernum;
    }

    public int getPid() {
        return Pid;
    }

    public void setPid(int Pid) {
        this.Pid = Pid;
    }
}
