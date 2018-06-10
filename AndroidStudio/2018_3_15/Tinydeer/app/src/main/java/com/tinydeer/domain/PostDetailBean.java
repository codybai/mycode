package com.tinydeer.domain;

/**
 * Created by baicol on 2018-03-11.
 */
//文章详情页封装类
public class PostDetailBean {

    /**
     * Ptype : 学习
     * Pcontent : 4高考已经结束，亲爱的学弟学妹们是否已经开始向往大学生活了呢，想必大家对于报志愿选专业还有很多疑问吧~为此，光吧特别推出2018年高考招生咨询导航贴，由热心的吧友们为大家答疑解惑为了维护版面整洁，以及大家的问题都能得到及时回复，请大家在本贴或本贴所放的链接贴子中进行回复和咨询，单独开贴一律删除免责声明：本贴吧回复内容为热心吧友的友情帮助，不具有法律效力，不代表西安交通大学官方观点，回答仅供参考。西安交通大学本科招生办公室联系方式：
     * username : admin
     * title : 2018年高考招生咨询导航贴4
     * Ptime : 2018-03-10
     * lasttime : 2018-03-10
     * connum : 4
     * follownum : 4
     * lovenum : 4
     * browsernum : 4
     * Pid : 144
     * photo : ffff
     */

    private String Ptype;
    private String Pcontent;
    private String username;
    private String title;
    private String Ptime;
    private String lasttime;
    private int connum;
    private int follownum;
    private int lovenum;
    private int browsernum;
    private int Pid;
    private String photo;

    public String getPtype() {
        return Ptype;
    }

    public void setPtype(String Ptype) {
        this.Ptype = Ptype;
    }

    public String getPcontent() {
        return Pcontent;
    }

    public void setPcontent(String Pcontent) {
        this.Pcontent = Pcontent;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
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

    public String getLasttime() {
        return lasttime;
    }

    public void setLasttime(String lasttime) {
        this.lasttime = lasttime;
    }

    public int getConnum() {
        return connum;
    }

    public void setConnum(int connum) {
        this.connum = connum;
    }

    public int getFollownum() {
        return follownum;
    }

    public void setFollownum(int follownum) {
        this.follownum = follownum;
    }

    public int getLovenum() {
        return lovenum;
    }

    public void setLovenum(int lovenum) {
        this.lovenum = lovenum;
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

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }
}
