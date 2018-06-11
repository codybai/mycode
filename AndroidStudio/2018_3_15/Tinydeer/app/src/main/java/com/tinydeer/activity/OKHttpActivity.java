//看到第二集
package com.tinydeer.activity;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.tinydeer.android.R;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.BitmapCallback;
import com.zhy.http.okhttp.callback.FileCallBack;
import com.zhy.http.okhttp.callback.StringCallback;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import okhttp3.Call;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by baicol on 2018-03-03.
 */

public class OKHttpActivity extends Activity implements View.OnClickListener {
    public static final MediaType JSON
            = MediaType.parse("application/json; charset=utf-8");
    private static final int GET = 1;
    private static final int POST = 2;
    private static final String TAG = OKHttpActivity.class.getSimpleName();
    private Button btn_get_post;
    private Button btn_okhttputil;
    private Button btn_okhttputil_post;
    private Button btn_download;
    private TextView tv_result;
    private ProgressBar progressBar;
    private Button getBtn_okhttputil_uploadFile;
    private Button btn_getimg;
    private ImageView img_view;
    private Button btn_getImgList;

    //get请求用到
    private OkHttpClient client = new OkHttpClient();
    private Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what) {
                case GET:
                    //获取数据
                    tv_result.setText((String) msg.obj);
                    break;
                case POST:
                    tv_result.setText((String) msg.obj);
                    downloadFile();
                    break;
            }
        }
    };


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_okhttp);

        btn_get_post = (Button) findViewById(R.id.btn_get_post);
        tv_result = (TextView) findViewById(R.id.tv_result);
        progressBar = (ProgressBar) findViewById(R.id.tv_bar);
        progressBar.setMax(100);
        btn_okhttputil = (Button) findViewById(R.id.btn_okhttputils_get);
        btn_okhttputil_post = (Button) findViewById(R.id.btn_okhttputils_post);
        btn_download = (Button) findViewById(R.id.btn_okhttputil_downFile);
        getBtn_okhttputil_uploadFile = (Button) findViewById(R.id.btn_okhttputil_uploadFile);
        btn_getimg = (Button) findViewById(R.id.btn_getImg);
        img_view = (ImageView) findViewById(R.id.show_img);
        btn_getImgList = (Button) findViewById(R.id.btn_getImg_bylist);


        //设置点击事件
        btn_get_post.setOnClickListener(this);//为什么不用匿名内部类
        btn_okhttputil.setOnClickListener(this);
        btn_okhttputil_post.setOnClickListener(this);
        btn_download.setOnClickListener(this);
        getBtn_okhttputil_uploadFile.setOnClickListener(this);
        btn_getimg.setOnClickListener(this);
        btn_getImgList.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_get_post://使用原生的okhttp请求网络数据get 和post
//                getDataFromGet();
                tv_result.setText("");
                getDataFromPost();
                break;
            case R.id.btn_okhttputils_get:
                tv_result.setText("");
                getHtml(null);
                break;
            case R.id.btn_okhttputils_post:
                tv_result.setText("");
                PostRequest(null);
                break;
            case R.id.btn_okhttputil_downFile:
                Log.e(TAG, "click download:");
                tv_result.setText("");
                downloadFile();
                break;
            case R.id.btn_okhttputil_uploadFile:
                tv_result.setText("");
                uploadFile(null);
                break;
            case R.id.btn_getImg:
                getImage(null);
                break;
            case R.id.btn_getImg_bylist:
                Intent intent = new Intent(OKHttpActivity.this, OKHttpListActivity.class);
                startActivity(intent);
                break;


        }
    }

    private void getDataFromGet() {
        new Thread() {
            @Override
            public void run() {
                super.run();
                try {
                    String result = get("http://api.m.mtime.cn/PageSubArea/TrailerList.api");
                    Log.e("TAG", result);
                    Message msg = Message.obtain();
                    msg.what = GET;
                    msg.obj = result;
                    handler.sendMessage(msg);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();

    }

    private void getDataFromPost() {
        new Thread() {
            @Override
            public void run() {
                super.run();
                try {
                    String result = post("http://api.m.mtime.cn/PageSubArea/TrailerList.api", "");
                    Log.e("TAG", result);
                    Message msg = Message.obtain();
                    msg.what = POST;
                    msg.obj = result;
                    handler.sendMessage(msg);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();

    }


    //get请求
    private String get(String url) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .build();

        Response response = client.newCall(request).execute();
        return response.body().string();


    }

    //OKHttpUtils提供的方法  get请求
    public void getHtml(View view) {
        String url = "http://www.zhiyun-tech.com/App/Rider-M/changelog-zh.txt";
        url = "http://www.391k.com/api/xapi.ashx/info.json?key=bd_hyrzjjfb4modhj&size=10&page=1";
        OkHttpUtils
                .get()
                .url(url)
                .id(100)
                .build()
                .execute(new MyStringCallback());
    }

    //OKHttpUtils提供的方法  post请求
    public void PostRequest(View view) {
        String url = "http://www.zhiyun-tech.com/App/Rider-M/changelog-zh.txt";
        url = "http://www.391k.com/api/xapi.ashx/info.json?key=bd_hyrzjjfb4modhj&size=10&page=1";
        OkHttpUtils
                .post()
                .url(url)
                .id(100)
                .build()
                .execute(new MyStringCallback());
    }


    //postqingqiu
    private String post(String url, String json) throws IOException {
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
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
            tv_result.setText("onError:" + e.getMessage());
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e(TAG, "onResponse：complete");
            tv_result.setText("onResponse:" + response);

            switch (id) {
                case 100:
                    Toast.makeText(OKHttpActivity.this, "http", Toast.LENGTH_SHORT).show();
                    break;
                case 101:
                    Toast.makeText(OKHttpActivity.this, "https", Toast.LENGTH_SHORT).show();
                    break;
            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
            Log.e(TAG, "inProgress:" + progress);
            progressBar.setProgress((int) (100 * progress));
        }
    }

    public void downloadFile() {
        tv_result.setText("download");
//        String url = "https://github.com/hongyangAndroid/okhttp-utils/blob/master/okhttputils-2_4_1.jar?raw=true";
        String url = "http://vfx.mtime.cn/Video/2018/02/22/mp4/180222094449582501.mp4";
        OkHttpUtils//
                .get()//
                .url(url)//
                .build()//
                .execute(new FileCallBack(Environment.getExternalStorageDirectory().getAbsolutePath(), "download.mp4")//
                {

                    @Override
                    public void onBefore(Request request, int id) {
                    }

                    @Override
                    public void inProgress(float progress, long total, int id) {
                        progressBar.setProgress((int) (100 * progress));
                        Log.e(TAG, "inProgress :" + (int) (100 * progress));
                    }

                    @Override
                    public void onError(Call call, Exception e, int id) {
                        Log.e(TAG, "onError :" + e.getMessage());
                    }

                    @Override
                    public void onResponse(File file, int id) {
                        Log.e(TAG, "onResponse :" + file.getAbsolutePath());
                    }
                });
    }

    //  这个怎么用
    public void uploadFile(View view) {

        File file = new File(Environment.getExternalStorageDirectory(), "download.mp4");
        if (!file.exists()) {
            Toast.makeText(OKHttpActivity.this, "文件不存在，请修改文件路径", Toast.LENGTH_SHORT).show();
            return;
        }
        Map<String, String> params = new HashMap<>();
        params.put("username", "张鸿洋");//不用用户名登陆的情况下不用删除此处也是没有问题滴
        params.put("password", "123");

        Map<String, String> headers = new HashMap<>();
        headers.put("APP-Key", "APP-Secret222");
        headers.put("APP-Secret", "APP-Secret111");

//        String url = mBaseUrl + "user!uploadFile";

        String url = "http://192.168.3.24:8080/tinydeer/upLoadFileServlet";
        OkHttpUtils.post()//
                .addFile("mFile", "download.mp4", file)//
                .url(url)//
                .params(params)//
                .headers(headers)//
                .build()//
                .execute(new MyStringCallback());
    }

    public void getImage(View view) {
        tv_result.setText("");
        String url = "http://img5.mtime.cn/mg/2018/03/02/105243.57232710_120X90X4.jpg";
        OkHttpUtils
                .get()//
                .url(url)//
                .tag(this)//
                .build()//
                .connTimeOut(20000)
                .readTimeOut(20000)
                .writeTimeOut(20000)
                .execute(new BitmapCallback() {
                    @Override
                    public void onError(Call call, Exception e, int id) {
                        tv_result.setText("onError:" + e.getMessage());
                    }

                    @Override
                    public void onResponse(Bitmap bitmap, int id) {
                        Log.e("TAG", "onResponse：complete");
                        img_view.setImageBitmap(bitmap);
                    }
                });
    }


}
