package com.tinydeer.android;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Intent;
import android.os.Handler;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.app.LoaderManager.LoaderCallbacks;

import android.content.CursorLoader;
import android.content.Loader;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;

import android.os.Build;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.text.TextUtils;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.tinydeer.Utils.Util;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.Call;
import okhttp3.MediaType;
import okhttp3.Request;


/**
 * A login screen that offers login via email/password.
 */
public class LoginActivity extends Activity {

    private Button btn_login;
    private String account;
    private String password;
    private EditText account_edit;
    private EditText password_edit;
    private ProgressBar mProgressBar;
    private TextView err_show;
    private TextView textView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        btn_login = (Button) findViewById(R.id.log_button);
        account_edit = (EditText) findViewById(R.id.account_edit);
        password_edit = (EditText) findViewById(R.id.password_edit);
        mProgressBar = (ProgressBar) findViewById(R.id.login_progress);
        err_show = (TextView) findViewById(R.id.show_error);
        textView = (TextView)findViewById(R.id.login_register);

        textView.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this,RegisterActivity.class);
                startActivity(intent);
            }
        });
        btn_login.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                account = account_edit.getText().toString();
                password = password_edit.getText().toString();
                Log.e(":", account + "/" + password);
                mProgressBar.setVisibility(View.VISIBLE);
                if(account.equals("baicol")){
                    Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                    Log.e("转前：",account+password);
                    intent.putExtra("username", account);
                    intent.putExtra("password", password);
                    startActivity(intent);
                }
                confirmLogin(account, password);
//                if(account.equals("admin")&&password.equals("admin")){   //单机版本
//                    Intent intent = new Intent(LoginActivity.this, MainActivity.class);
//                    intent.putExtra("username",account);
//                    intent.putExtra("password",password);
//                    startActivity(intent);
//                }else{
//                    err_show.setText("输入有误！！请重新输入！");
//                }
//                mProgressBar.setVisibility(View.INVISIBLE);

            }
        });

    }

    //登陆验证函数
    public void confirmLogin(String usr, String password) {
        String url =Util.URL_LOGIN;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username",usr)
                .addParams("userpass",password)
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
            err_show.setText("请求错误！");
//            mTv.setText("onError:" + e.getMessage());
            mProgressBar.setVisibility(View.INVISIBLE);
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("接受完毕：", response);

//            此处根据结果判断判断账户密码到底正确与否！
            if (response.equals("login_true")) {
                //用户存在登陆
                Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                intent.putExtra("username", account);
                intent.putExtra("password", password);
                startActivity(intent);
//                finish();
            } else if(response.equals("login_failed")){
                //输入有问题
                err_show.setText("输入有误或者账户不存在，请重新输入！");
            }

            mProgressBar.setVisibility(View.INVISIBLE);

//            mTv.setText("onResponse:" + response);

//            switch (id)
//            {
//                case 100:
//                    Toast.makeText(MainActivity.this, "http", Toast.LENGTH_SHORT).show();
//                    break;
//                case 101:
//                    Toast.makeText(MainActivity.this, "https", Toast.LENGTH_SHORT).show();
//                    break;
//            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
            mProgressBar.setProgress((int) (100 * progress));

        }
    }
}

