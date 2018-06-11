package com.tinydeer.activity;

import android.app.Activity;
import android.os.Bundle;
import android.os.Message;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.adapter.DetailLeftWordAdapter;
import com.tinydeer.domain.LeftWordsBean;
import com.tinydeer.domain.PostDetailBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-12.
 */

public class WriteReplyActivity extends Activity {
    private Button button;
    private EditText write_reply_text;
    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.write_reply);
        write_reply_text= (EditText)findViewById(R.id.write_reply_text);
        button = (Button)findViewById(R.id.write_submit);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                submitReply();
            }
        });

    }
    public void submitReply() {
        String url = Util.URL_BUTTON_WRITE_REPLY;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid",getIntent().getStringExtra("Pid"))
                .addParams("username", MainActivity.getUsername())
                .addParams("content",write_reply_text.getText().toString())
                .addParams("author",getIntent().getStringExtra("author"))
                .build()
                .execute(new MyStringCallback());
    }

    private class MyStringCallback extends StringCallback {
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
            if(response.equals("publish_success")){
                Log.e("sdf",response);
                Message msg = new Message();
                msg.what=1;
                DetailActivity.handler.sendMessage(msg);
                finish();
            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
        }
    }

}
