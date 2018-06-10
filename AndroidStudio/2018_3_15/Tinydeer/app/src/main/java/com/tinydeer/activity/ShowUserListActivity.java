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
import com.tinydeer.android.adapter.ShowMyFocusAdapter;
import com.tinydeer.android.adapter.ShowPostListAdapter;
import com.tinydeer.domain.PostBean;
import com.tinydeer.domain.UserData;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;

import okhttp3.Call;
import okhttp3.Request;

//用以显示我关注的用户
public class ShowUserListActivity extends Activity {
    private ListView mlistview;
    private ProgressBar mProgressBar;
    private List<UserData> focus_users_list;
    private ShowMyFocusAdapter mshowUserListAdapter;
    private Button backBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_user_list);
        mlistview = (ListView) findViewById(R.id.show_user_list_view);
        mProgressBar = (ProgressBar) findViewById(R.id.show_user_list_laod_progressBar);
        backBtn = (Button) findViewById(R.id.show_user_list_back_button);

        //返回
        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        //页面点开进行联网拉数据
        getFocusUserFromNet();

    }


    public void getFocusUserFromNet() {
        String url = Util.URL_GET_FOCUS_USER_BY_USERID;
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
            Log.e("我的关注：", response);
            Gson gson = new Gson();
            focus_users_list = gson.fromJson(response, new TypeToken<List<UserData>>() {
            }.getType());
            mshowUserListAdapter = new ShowMyFocusAdapter(ShowUserListActivity.this, focus_users_list);
            mlistview.setAdapter(mshowUserListAdapter);
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//                mProgressBar.setProgress((int) (100 * progress));
        }
    }


}
