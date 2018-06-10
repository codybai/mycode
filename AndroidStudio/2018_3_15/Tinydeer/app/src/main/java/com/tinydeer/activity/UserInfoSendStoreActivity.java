package com.tinydeer.activity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.ProgressBar;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.adapter.ShowPostListAdapter;
import com.tinydeer.domain.PostBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;

import okhttp3.Call;
import okhttp3.Request;
//用于显示我发表的帖子
//我收藏的帖子
public class UserInfoSendStoreActivity extends Activity {

    private ListView mListView;

    private ShowPostListAdapter mshowPostListAdapter;
    private ProgressBar mProgressBar;
    private Button back_btn;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_send_store_post);
        mListView = (ListView) findViewById(R.id.show_focus_list);
        mProgressBar = (ProgressBar)findViewById(R.id.progressbar);
        back_btn = (Button)findViewById(R.id.focus_back);
        back_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        getPost();
    }

    public void getPost() {
        String url =getIntent().getStringExtra("url");
//        String url = Util.URL_QUERY_ALL_POST;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username", MainActivity.getUsername())
                .build()
                .execute(new MyStringCallback());
    }

    private class MyStringCallback extends StringCallback {
        @Override
        public void onBefore(Request request, int id) {
            mProgressBar.setVisibility(View.VISIBLE);
        }

        @Override
        public void onAfter(int id) {
            mProgressBar.setVisibility(View.INVISIBLE);
        }

        @Override
        public void onError(Call call, Exception e, int id) {
            e.printStackTrace();
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("我发表/收藏的文章：", response);
            Gson gson = new Gson();
            List<PostBean> post_list  = gson.fromJson(response, new TypeToken<List<PostBean>>() {
            }.getType());
            mshowPostListAdapter = new ShowPostListAdapter(UserInfoSendStoreActivity.this, post_list);
            mListView.setAdapter(mshowPostListAdapter);
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//                mProgressBar.setProgress((int) (100 * progress));
        }
    }
}
