package com.tinydeer.activity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.tinydeer.Utils.Util;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import okhttp3.Call;
import okhttp3.Request;

public class ShowBoardActivity extends Activity {
    private TextView Title;
    private TextView Content;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_board);
        Title   = (TextView)findViewById(R.id.notice_title);
        Content = (TextView)findViewById(R.id.notice_content);
//        getNoticeFromNet();
    }


    //保存数据到数据库
    public void getNoticeFromNet() {
        String url = "";
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid", getIntent().getStringExtra("NoticeID"))
                .build()
                .execute(new MyStringCallback());

    }



    public class MyStringCallback extends StringCallback {
        @Override
        public void onBefore(Request request, int id) {

        }

        @Override
        public void onAfter(int id) {

        }

        @Override
        public void onError(Call call, Exception e, int id) {
            e.printStackTrace();

        }

        @Override
        public void onResponse(String response, int id) {

            Log.e("Click Notice:", response);
            //此处解析并且显示Notice
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//            mProgressBar.setProgress((int) (100 * progress));

        }
    }

}
