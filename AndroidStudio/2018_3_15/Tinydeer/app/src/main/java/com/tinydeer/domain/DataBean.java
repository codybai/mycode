package com.tinydeer.domain;

import java.util.List;

/**
 * Created by baicol on 2018-03-04.
 */

public class DataBean {


    private List<ItemData> trailers;

    public List<ItemData> getTrailers() {
        return trailers;
    }

    public void setTrailers(List<ItemData> trailers) {
        this.trailers = trailers;
    }

    public static class ItemData {
        /**
         * id : 69752
         * movieName : 《头号玩家》中国定档预告
         * coverImg : http://img5.mtime.cn/mg/2018/03/01/153733.13627283_120X90X4.jpg
         * movieId : 219107
         * url : http://vfx.mtime.cn/Video/2018/03/01/mp4/180301153522078172.mp4
         * hightUrl : http://vfx.mtime.cn/Video/2018/03/01/mp4/180301153522078172.mp4
         * videoTitle : 头号玩家 中国定档预告片
         * videoLength : 30
         * rating : -1
         * type : ["动作","冒险","科幻","惊悚"]
         * summary : 炫酷视效引发找梗狂潮
         */

        private int id;
        private String movieName;
        private String coverImg;
        private int movieId;
        private String url;
        private String hightUrl;
        private String videoTitle;
        private int videoLength;
        private int rating;
        private String summary;
        private List<String> type;

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public String getMovieName() {
            return movieName;
        }

        public void setMovieName(String movieName) {
            this.movieName = movieName;
        }

        public String getCoverImg() {
            return coverImg;
        }

        public void setCoverImg(String coverImg) {
            this.coverImg = coverImg;
        }

        public int getMovieId() {
            return movieId;
        }

        public void setMovieId(int movieId) {
            this.movieId = movieId;
        }

        public String getUrl() {
            return url;
        }

        public void setUrl(String url) {
            this.url = url;
        }

        public String getHightUrl() {
            return hightUrl;
        }

        public void setHightUrl(String hightUrl) {
            this.hightUrl = hightUrl;
        }

        public String getVideoTitle() {
            return videoTitle;
        }

        public void setVideoTitle(String videoTitle) {
            this.videoTitle = videoTitle;
        }

        public int getVideoLength() {
            return videoLength;
        }

        public void setVideoLength(int videoLength) {
            this.videoLength = videoLength;
        }

        public int getRating() {
            return rating;
        }

        public void setRating(int rating) {
            this.rating = rating;
        }

        public String getSummary() {
            return summary;
        }

        public void setSummary(String summary) {
            this.summary = summary;
        }

        public List<String> getType() {
            return type;
        }

        public void setType(List<String> type) {
            this.type = type;
        }
    }
}
