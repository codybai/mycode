package com.tinydeer.android.fragment;

import android.content.Intent;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.gson.Gson;
import com.tinydeer.Utils.Util;
import com.tinydeer.activity.ShowUserListActivity;
import com.tinydeer.activity.UserInfoSendStoreActivity;
import com.tinydeer.activity.UserInfoPageActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.base.BaseFragment;
import com.tinydeer.domain.UserData;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-01.
 */

public class ProfileFrameFragment extends BaseFragment implements View.OnClickListener {
    private static final String TAG = ProfileFrameFragment.class.getSimpleName();//"CommonFrameFragment"
    public   Button btn_quit;
    private UserData userData;
    private TextView setUserIco;
    //用户个人的信息获取
    private String   user_ico;//头像
    private TextView user_name;//用户昵称
    private TextView user_words;//用户签名
    private TextView user_level;//用户等级
    private TextView user_score;//用户积分
    private TextView user_mypage;//我的主页
    private TextView user_myfocus;//我的关注
    private TextView user_mypost;//我的帖子
    private TextView user_mystar;//我的收藏


    @Override
    protected View initView() {//创建绘图

        View view = View.inflate(mContext, R.layout.activity_user_profile, null);

        btn_quit     = (Button)   view.findViewById(R.id.user_quit_btn);
        setUserIco   = (TextView) view.findViewById(R.id.user_ico);
        user_name    = (TextView) view.findViewById(R.id.user_name);
        user_words   = (TextView) view.findViewById(R.id.user_words);
        user_level   = (TextView) view.findViewById(R.id.user_level);
        user_score   = (TextView) view.findViewById(R.id.user_score);
        user_mypage  = (TextView) view.findViewById(R.id.user_mypage);
        user_myfocus = (TextView) view.findViewById(R.id.user_myfocus);
        user_mypost  = (TextView) view.findViewById(R.id.user_mypost);
        user_mystar  = (TextView) view.findViewById(R.id.user_mystar);
        user_name.setText(MainActivity.getUsername());
        btn_quit.setOnClickListener(this);

        user_mypage.setOnClickListener(this);
        user_myfocus.setOnClickListener(this);
        user_mypost.setOnClickListener(this);
        user_mystar.setOnClickListener(this);
        return view;
    }


    @Override
    protected void initData() {
        super.initData();

        getUserInfo();

    }

    //第一次点击我的联网获取信息
    public void getUserInfo() {
        String url = Util.URL_GET_USERBEAN_BY_CLICK_MY;;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username", MainActivity.getUsername())
                .build()
                .execute(new MyStringCallback());
    }

    //处理各种点击事件
    @Override
    public void onClick(View v) {
        if(MainActivity.getUsername().equals("")||MainActivity.getPassword().equals("")){//未登录不响应
            return;
        }
        switch (v.getId()){
            case R.id.user_mypage:
                Intent intent = new Intent(mContext, UserInfoPageActivity.class);
                intent.putExtra("userData",userData);
                startActivity(intent);
                break;
            case R.id.user_myfocus://我关注的用户显示
                Intent intent_foucus = new Intent(mContext, ShowUserListActivity.class);
                startActivity(intent_foucus);
                break;
            case R.id.user_mypost://我发表的文章
                Intent intent_post = new Intent(mContext, UserInfoSendStoreActivity.class);
                intent_post.putExtra("url",Util.URL_GET_MY_PUBLISHED_POST_BY_USERID);  //不能删除
                startActivity(intent_post);
                break;
            case R.id.user_mystar://我收藏的文章
                Intent intent_star = new Intent(mContext, UserInfoSendStoreActivity.class);
                intent_star.putExtra("url",Util.URL_GET_MY_STORED_POST_BY_USERID);//不能删除
                startActivity(intent_star);
                break;
            case R.id.user_quit_btn:
                Log.e("quit","btn");
                Message msg = new Message();
                msg.what=1;
                MainActivity.handler.sendMessage(msg);
                break;
            default:
                break;
        }
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
            Log.e("onerror:",e.getMessage());

        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("接受完毕：", response);
            //处理返回信息
            //设置用户的各个属性  其中设计到json的解析
            Gson gson = new Gson();
            userData  = gson.fromJson(response,UserData.class);
            user_name.setText(userData.getSname());
            user_words.setText(userData.getWords());
            user_level.setText(String.valueOf(userData.getLevel()));
            user_score.setText(String.valueOf(userData.getPoints()));


        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//                mProgressBar.setProgress((int) (100 * progress));

        }

    }
}
