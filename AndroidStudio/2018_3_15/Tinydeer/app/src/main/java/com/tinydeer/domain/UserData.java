package com.tinydeer.domain;

import java.io.Serializable;

/**
 * Created by baicol on 2018-03-11.
 */

public class UserData implements Serializable {

    /**
     * mail : 123456@qq.com
     * phone : 123456
     * Smajor : 软件工程
     * Saddr : 山东省青岛市胶州市西交青岛研究院
     * Sdept : 软件学院
     * photo : 123456
     * password : admin
     * username : admin
     * level : 500
     * words : 精勤求学,敦笃励志,果毅力行,忠恕任事
     * age : 20
     * Ssex : 女
     * points : 10
     * Sedu : 博士
     * Sname : 李四
     */

    private String mail;
    private String phone;
    private String Smajor;
    private String Saddr;
    private String Sdept;
    private String photo;
    private String password;
    private String username;
    private int level;
    private String words;
    private int age;
    private String Ssex;
    private int points;
    private String Sedu;
    private String Sname;

    public String getMail() {
        return mail;
    }

    public void setMail(String mail) {
        this.mail = mail;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getSmajor() {
        return Smajor;
    }

    public void setSmajor(String Smajor) {
        this.Smajor = Smajor;
    }

    public String getSaddr() {
        return Saddr;
    }

    public void setSaddr(String Saddr) {
        this.Saddr = Saddr;
    }

    public String getSdept() {
        return Sdept;
    }

    public void setSdept(String Sdept) {
        this.Sdept = Sdept;
    }

    public String getPhoto() {
        return photo;
    }

    public void setPhoto(String photo) {
        this.photo = photo;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public String getWords() {
        return words;
    }

    public void setWords(String words) {
        this.words = words;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getSsex() {
        return Ssex;
    }

    public void setSsex(String Ssex) {
        this.Ssex = Ssex;
    }

    public int getPoints() {
        return points;
    }

    public void setPoints(int points) {
        this.points = points;
    }

    public String getSedu() {
        return Sedu;
    }

    public void setSedu(String Sedu) {
        this.Sedu = Sedu;
    }

    public String getSname() {
        return Sname;
    }

    public void setSname(String Sname) {
        this.Sname = Sname;
    }
}
