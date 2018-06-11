package com.tinydeer.android;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.tinydeer.Utils.Util;
import com.tinydeer.android.R;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import okhttp3.Call;
import okhttp3.Request;

public class RegisterActivity extends Activity {
    private TextView register_show_result;
    private Button register;
    private TextView usrname;
    private TextView password;
    private TextView phone;
    private TextView email;
    private String usr;
    private String pwd;
    private Button register_back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        register = (Button) findViewById(R.id.regist_btn);
        usrname = (TextView) findViewById(R.id.regist_usr_name);
        password = (TextView) findViewById(R.id.regist_usr_pwd);
        phone = (TextView) findViewById(R.id.regist_phone_text);
        email = (TextView) findViewById(R.id.regist_email_text);
        register_show_result = (TextView) findViewById(R.id.regist_show_result);
        register_back = (Button)findViewById(R.id.back_register);
        register_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                usr = usrname.getText().toString();
                pwd = password.getText().toString();
                register(usr,
                        pwd,
                        phone.getText().toString(),
                        email.getText().toString());
            }
        });
    }


    //登陆验证函数
    public void register(String usr, String password, String phone, String email) {
        String url =Util.URL_REGISTER_ACCESS;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username", usr)
                .addParams("userpass", password)
                .addParams("phone", phone)
                .addParams("email", email)
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
//            mTv.setText("onError:" + e.getMessage());
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("接受结果：", response);
            if (response.equals("register_true")) {
                register_show_result.setText("注册成功！");
                Intent intent = new Intent(RegisterActivity.this, MainActivity.class);
                intent.putExtra("username", usr);
                intent.putExtra("password", pwd);
                startActivity(intent);
                finish();
            } else if (response.equals("register_failed")) {
                register_show_result.setText("用户名重复!");
            } else if (response.equals("register_error")) {
                register_show_result.setText("格式输入错误!");
            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//            mProgressBar.setProgress((int) (100 * progress));

        }
    }
}
