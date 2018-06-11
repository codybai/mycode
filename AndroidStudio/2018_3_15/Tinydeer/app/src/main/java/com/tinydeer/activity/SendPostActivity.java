package com.tinydeer.activity;


import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

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

public class SendPostActivity extends Activity {
    private Button btn_back;
    private TextView post_content;
    private TextView post_title;
    private Spinner sp;
    private Button btn_publish;
    private String postYype;
    private TextView show_result;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_post);
        btn_back = (Button) findViewById(R.id.send_post_back);
        sp = (Spinner) findViewById(R.id.tobe_post_type);
        post_content = (TextView) findViewById(R.id.tobe_post_content);
        post_title = (TextView) findViewById(R.id.tobe_post_title);
        btn_publish = (Button)findViewById(R.id.publish_post);
        show_result  = (TextView)findViewById(R.id.publish_result_show);
        btn_publish.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //联网发送信息
                publishPostToServer();

//                Log.e("post:",postYype);
//                Log.e("post:",MainActivity.getUsername());
//                Log.e("post:",post_content.getText().toString());
//                Log.e("post:",postYype);
            }
        });
        btn_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        sp.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                postYype = sp.getSelectedItem().toString();
                Log.e("OnItemSelected：spinner：",postYype);//文章类型
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });

    }
    public void publishPostToServer() {
        String url = Util.URL_PUBLISH_POST_TO_SERVER;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username", MainActivity.getUsername())
                .addParams("Ptitle",post_title.getText().toString())
                .addParams("Pcontent",post_content.getText().toString())
                .addParams("Ptype",postYype)
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
        }

        @Override
        public void onError(Call call, Exception e, int id) {
            Log.e("发布帖子：",e.getMessage());
            e.printStackTrace();
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("发布帖子：",response);
            if(response.equals("publish_success")){
                show_result.setText("发布成功！");
            }
            if(response.equals("publish_failed")){
                show_result.setText("发布失败！");
            }

        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//                mProgressBar.setProgress((int) (100 * progress));
        }
    }
}
