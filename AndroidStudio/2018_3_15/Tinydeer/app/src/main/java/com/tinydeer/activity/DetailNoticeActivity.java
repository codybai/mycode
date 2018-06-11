package com.tinydeer.activity;

import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.android.R;
import com.tinydeer.android.adapter.NoticeListViewAdapter;
import com.tinydeer.android.fragment.CommonFrameFragment;
import com.tinydeer.domain.NoticeBean;
import com.tinydeer.domain.NoticeDetailBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;

import okhttp3.Call;
import okhttp3.Request;

public class DetailNoticeActivity extends Activity {
    private NoticeDetailBean noticeDetailBean;
    private TextView noticeTitle;
    private TextView noticeContent;
    private TextView noticeTime;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail_notice);
        noticeContent = (TextView) findViewById(R.id.show_notice_content);
        noticeTime = (TextView) findViewById(R.id.show_notice_time);
        noticeTitle = (TextView) findViewById(R.id.show_notice_title);

        getNoticeContent();
    }


    //第一次点击我的联网获取信息
    public void getNoticeContent() {
        String url = Util.URL_GET_DETAIL_NOTICE_BY_ONE;
        ;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid",getIntent().getStringExtra("noticeID"))
                .build()
                .execute(new MyStringCallback());
    }

    private class MyStringCallback extends StringCallback {
        @Override
        public void onBefore(Request request, int id) {
//                setTitle("loading...");
        }

        @Override
        public void onAfter(int id) {
//                setTitle("Sample-okHttp");
        }

        @Override
        public void onError(Call call, Exception e, int id) {
            e.printStackTrace();
            Log.e("onerror:", e.getMessage());

        }

        @Override
        public void onResponse(String response, int id) {
                Log.e("notice_detail:",response);
            Gson gson = new Gson();
            noticeDetailBean = gson.fromJson(response, NoticeDetailBean.class);
            noticeTitle.setText(noticeDetailBean.getTitle());
            noticeTime.setText(noticeDetailBean.getTime());
            noticeContent.setText(noticeDetailBean.getContent());
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//                mProgressBar.setProgress((int) (100 * progress));

        }

    }

}
