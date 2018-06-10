package com.tinydeer.activity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.android.LoginActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.domain.UserData;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;

import okhttp3.Call;
import okhttp3.Request;
//用以设置用户的信息和修改信息
public class UserInfoPageActivity extends Activity {
    //用户的所有信息属性
    private EditText realName;
    private EditText age;
    private EditText sex;
    private EditText address;
    private EditText phone;
    private EditText school;
    private EditText major;
    private EditText email;
    private Button save_btn;
    private TextView show_result;
    private ProgressBar mProgressBar;
    private Button save_back;
    private UserData userData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_info_page);
        show_result = (TextView) findViewById(R.id.save_show_result);
        mProgressBar = (ProgressBar) findViewById(R.id.save_progressBar);
        save_back = (Button) findViewById(R.id.save_back);
        realName = (EditText) findViewById(R.id.save_realname);
        age = (EditText) findViewById(R.id.save_age);
        sex = (EditText) findViewById(R.id.save_sex);
        address = (EditText) findViewById(R.id.save_address);//未写
        phone = (EditText) findViewById(R.id.save_phone);
        school = (EditText) findViewById(R.id.save_school);
        major = (EditText) findViewById(R.id.save_major);
        email = (EditText) findViewById(R.id.save_email);
        save_btn = (Button) findViewById(R.id.save_submit);
        mProgressBar.setVisibility(View.INVISIBLE);

        //获取intent 里面的userData
        userData = (UserData) getIntent().getSerializableExtra("userData");
        //面板显示当前用户的信息
        realName.setText(userData.getSname());
        age.setText(String.valueOf(userData.getAge()));
        sex.setText(userData.getSsex());
        address.setText(userData.getSaddr());
        phone.setText(userData.getPhone());
        school.setText(userData.getSdept());
        major.setText(userData.getSmajor());
        email.setText(userData.getMail());

        //保存面板数据并且上传
        save_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                show_result.setText("");
                mProgressBar.setVisibility(View.VISIBLE);
                saveUserInfo();

            }
        });
        save_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                finish();
            }
        });

    }


    //保存数据到数据库
    public void saveUserInfo() {
        String url = Util.URL_SAVE_INFO_TO_SEVER;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username", MainActivity.getUsername())
                .addParams("Sname", realName.getText().toString())
                .addParams("Sage", age.getText().toString())
                .addParams("Ssex", sex.getText().toString())
                .addParams("Saddr", address.getText().toString())
                .addParams("phone", phone.getText().toString())
                .addParams("Sdept", school.getText().toString())
                .addParams("mail", email.getText().toString())
                .addParams("Smajor", major.getText().toString())
                .build()
                .execute(new MyStringCallback());

    }



    public class MyStringCallback extends StringCallback {
        @Override
        public void onBefore(Request request, int id) {
            setTitle("loading...");
        }

        @Override
        public void onAfter(int id) {
            setTitle("Sample-okHttp");
        }

        @Override
        public void onError(Call call, Exception e, int id) {
            e.printStackTrace();
            mProgressBar.setVisibility(View.INVISIBLE);
            Log.e("请求发生错误：", e.getMessage());

        }

        @Override
        public void onResponse(String response, int id) {

            Log.e("保存数据到服务端：：", response);
            mProgressBar.setVisibility(View.INVISIBLE);
            if (response.equals("update_success")) {//保存数据成功
                show_result.setText("更新资料成功,请重新登陆");
                //同步全局userBean操作在此处处理
//                Message msg = new Message();
//                msg.what=5;//同步全局userBean

            }
            if (response.equals("update_error")) {//保存数据成功
                show_result.setText("更新资料失败");
            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//            mProgressBar.setProgress((int) (100 * progress));

        }
    }
}
