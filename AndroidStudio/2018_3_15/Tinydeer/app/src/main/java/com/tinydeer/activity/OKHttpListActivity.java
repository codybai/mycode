package com.tinydeer.activity;

import android.app.Activity;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Toast;

import com.tinydeer.android.R;
import com.tinydeer.android.adapter.OKHttplistAdapter;
import com.tinydeer.domain.DataBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-04.
 */

public class OKHttpListActivity extends Activity {
    private static final String TAG = OKHttpListActivity.class.getSimpleName();
    private ListView listView;
    private ListView nodatalistView;
    private ProgressBar progressBar;
    private OKHttplistAdapter adapter;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_okhttp_list);

        initView();
        getDataFromNet();

    }

    private void getDataFromNet() {
        String url = "http://www.zhiyun-tech.com/App/Rider-M/changelog-zh.txt";
        url = "http://api.m.mtime.cn/PageSubArea/TrailerList.api";
        OkHttpUtils
                .get()
                .url(url)
                .id(100)
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
//            tv_result.setText("onError:" + e.getMessage());
            nodatalistView.setVisibility(View.VISIBLE);
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e(TAG, "onResponse：complete");
//            tv_result.setText("onResponse:" + response);
            nodatalistView.setVisibility(View.GONE);

            switch (id) {
                case 100:
                    Toast.makeText(OKHttpListActivity.this, "http", Toast.LENGTH_SHORT).show();
                    break;
                case 101:
                    Toast.makeText(OKHttpListActivity.this, "https", Toast.LENGTH_SHORT).show();
                    break;
            }
            if (response != null) {
                //解析数据和显示数据
                //此时response是json数据集
                processData(response);
                // http://api.m.mtime.cn/PageSubArea/TrailerList.api

            }
        }

        @Override
        public void inProgress(float progress, long total, int id) {
            Log.e(TAG, "inProgress:" + progress);
            progressBar.setProgress((int) (100 * progress));
        }
    }

    private void processData(String json) {
        DataBean dataBean = processJson(json);
        List<DataBean.ItemData> datas = dataBean.getTrailers();
        if (datas != null && datas.size() > 0) {
            //有数据要显示
            nodatalistView.setVisibility(View.GONE);
            //显示适配器
            adapter = new OKHttplistAdapter(OKHttpListActivity.this, datas);
            listView.setAdapter(adapter);
        } else {
            nodatalistView.setVisibility(View.VISIBLE);
        }
        progressBar.setVisibility(View.GONE);
    }

    private DataBean processJson(String response) {
        DataBean dataBean = new DataBean();
        try {
            JSONObject jsonObject = new JSONObject(response);
            JSONArray jsonArray = jsonObject.optJSONArray("trailers");
            if (jsonArray != null && jsonArray.length() > 0) {
                List<DataBean.ItemData> trailers = new ArrayList<>();
                dataBean.setTrailers(trailers);
                for (int i = 0; i < jsonArray.length(); i++) {

                    JSONObject jsonObjectItem = (JSONObject) jsonArray.get(i);

                    if (jsonObjectItem != null) {

                        DataBean.ItemData mediaItem = new DataBean.ItemData();

                        String movieName = jsonObjectItem.optString("movieName");//name
                        mediaItem.setMovieName(movieName);

                        String videoTitle = jsonObjectItem.optString("videoTitle");//desc
                        mediaItem.setVideoTitle(videoTitle);

                        String imageUrl = jsonObjectItem.optString("coverImg");//imageUrl
                        mediaItem.setCoverImg(imageUrl);

                        String hightUrl = jsonObjectItem.optString("hightUrl");//data
                        mediaItem.setHightUrl(hightUrl);

                        //把数据添加到集合
                        trailers.add(mediaItem);
                    }
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }
        return dataBean;


    }

    private void initView() {
        listView = (ListView) findViewById(R.id.listview);
        nodatalistView = (ListView) findViewById(R.id.tv_nodata);
        progressBar = (ProgressBar) findViewById(R.id.progressbar);
    }


}
