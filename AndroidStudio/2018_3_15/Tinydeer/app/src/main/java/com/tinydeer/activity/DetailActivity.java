package com.tinydeer.activity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.adapter.DetailLeftWordAdapter;
import com.tinydeer.android.adapter.ShowPostListAdapter;
import com.tinydeer.domain.LeftWordsBean;
import com.tinydeer.domain.PostBean;
import com.tinydeer.domain.PostDetailBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;

import okhttp3.Call;
import okhttp3.Request;


public class DetailActivity extends Activity {
    private TextView back_label;
    private TextView post_title;
    private TextView post_content;
    private ListView post_left_word;
    private TextView post_time;
    private TextView post_author;
    private TextView detail_to_write;
    private DetailLeftWordAdapter mdetailLeftWordAdapter;
    private boolean isLoadingPost;
    private  String pid;
    public static Handler handler;


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);
        isLoadingPost = true;
        pid = getIntent().getStringExtra("Pid");
        back_label = (TextView) findViewById(R.id.back_ico);
        post_author = (TextView)findViewById(R.id.post_author_name_details);
        post_title = (TextView)findViewById(R.id.post_title_details);
        post_content = (TextView)findViewById(R.id.post_content);
        post_left_word=(ListView) findViewById(R.id.post_leftword_details);
        post_time = (TextView)findViewById(R.id.post_author_time_details);
        detail_to_write = (TextView)findViewById(R.id.detail_to_write_ico);
        handler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {
                switch (msg.what){
                    case 1:
                        showLeftWordsByPost();//联网请求文章
                        break;
                }
                return true;
            }

        });

        showPostByPid();//联网请求文章
            Log.e("testPid:",getIntent().getStringExtra("Pid"));
//            Log.e("pid:",getIntent().getStringExtra("Pid"));

        //进行评论
        detail_to_write.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                //点击发帖
                Intent intent =new Intent(DetailActivity.this,WriteReplyActivity.class);
                intent.putExtra("Pid",pid);
                intent.putExtra("author",post_author.getText());
                startActivity(intent);
                Log.e("openWrite:","sdf");
            }
        });


        back_label.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }

    public void showLeftWordsByPost(){
        String url = Util.URL_GET_CONMENT_BY_PID;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid",pid)
                .build()
                .execute(new MyStringCallback());
    }
    public void showPostByPid() {
        String url = Util.URL_GET_POST_DETAIL_BY_PID;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid",pid)
                .build()
                .execute(new MyStringCallback());
    }

    private class MyStringCallback extends StringCallback {
        @Override
        public void onBefore(Request request, int id) {
//                setTitle("loading...");
//            mProgressBar.setVisibility(View.VISIBLE);
        }

        @Override
        public void onAfter(int id) {
//                setTitle("Sample-okHttp");
//            mProgressBar.setVisibility(View.INVISIBLE);
            if(isLoadingPost){//刚处理完文章
                isLoadingPost =false;//设置为假，下次不执行，防止死循环
                showLeftWordsByPost();//文章加载完毕在加载评论
            }

        }

        @Override
        public void onError(Call call, Exception e, int id) {
            e.printStackTrace();
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("DetailActivity:", response);
            if(isLoadingPost){//isLoadingPost为真，处理文章
                //处理post
                Log.e("获取文章：",response);
                Gson gson = new Gson();
                final PostDetailBean pdb = gson.fromJson(response,PostDetailBean.class);
                post_author.setText(pdb.getUsername());
                post_title.setText(pdb.getTitle());
                post_content.setText(pdb.getPcontent());
                post_time.setText(pdb.getPtime());
                pid = String.valueOf(pdb.getPid());

            }else{//isLoadingPost 为假处理评论
//                //处理评论
                Log.e("获取评论：",response);
                Gson gson = new Gson();
                List<LeftWordsBean>  lwb = gson.fromJson(response,new TypeToken<List<LeftWordsBean>>(){}.getType());

                mdetailLeftWordAdapter = new DetailLeftWordAdapter(lwb,DetailActivity.this);
                post_left_word.setAdapter(mdetailLeftWordAdapter);

            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//                mProgressBar.setProgress((int) (100 * progress));
        }
    }


}
