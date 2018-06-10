package com.tinydeer.android.fragment;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.widget.DrawerLayout;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.activity.DetailActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.adapter.ShowPostListAdapter;
import com.tinydeer.android.base.BaseFragment;
import com.tinydeer.domain.PostBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.zip.Inflater;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-01.
 */

public class HomeFrameFragment extends BaseFragment implements AdapterView.OnItemClickListener {
    private ShowPostListAdapter showPostListAdapter;
    private static final String TAG = HomeFrameFragment.class.getSimpleName();//"CommonFrameFragment"
    private List<Map<String, Object>> list = new ArrayList<>();
    private DrawerLayout drawerLayout;
    private ListView mlistView;
    private ListView mLv;
    private Button menu_btn;
    private Boolean isOpen;
    private Handler mhander;



    @Override
    protected View initView() {//创建绘图

        View view = View.inflate(mContext, R.layout.activity_show_post_list, null);

        mlistView = (ListView) view.findViewById(R.id.post_list_view);
        drawerLayout = (DrawerLayout) view.findViewById(R.id.id_drawerlayout);
        mLv = (ListView) drawerLayout.findViewById(R.id.id_lv);

        menu_btn = MainActivity.getMenu_btn();



        mhander= new Handler(){
            @Override
            public void handleMessage(Message msg) {
                switch (msg.what){
                    case 1:
                        mlistView.setAdapter(null);
                        String type = msg.getData().getString("type");
                        if(type.equals("全部")){
                            getPostList();
                        }else{
                            getPostByType(type);
                        }

                        break;
                    default:
                        break;
                }
            }
        };

        return view;
    }

    @Override
    protected void initData() {
        super.initData();
        isOpen = false;

        /************************************显示所有文章**************************************/
        getPostList();//联网请求文章数据

        /************************************侧栏分页**************************************/

        String[] str = new String[]{"学习", "就业", "生活", "情感", "交友", "市场", "旅游", "全部"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(mContext, android.R.layout.simple_list_item_1, str);
        mLv.setAdapter(adapter);
        mLv.setOnItemClickListener(this);    //点击侧栏显示
        menu_btn.setOnClickListener(new View.OnClickListener() {    //打开侧栏
            @Override

            public void onClick(View v) {
                if (isOpen) {
                    drawerLayout.closeDrawer(Gravity.LEFT);
                    isOpen = false;
                } else {
                    drawerLayout.openDrawer(Gravity.LEFT);
                    isOpen = true;
                }

            }
        });


    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        switch (view.getId()) {
            case android.R.id.text1:
                String str = ((TextView) view.findViewById(android.R.id.text1)).getText().toString();
                Toast.makeText(mContext, str, Toast.LENGTH_SHORT).show();

                drawerLayout.closeDrawer(Gravity.LEFT);
                Message msg = new Message();
                Bundle bundle = new Bundle();
                bundle.putString("type", str);
                msg.what = 1;
                msg.setData(bundle);
                mhander.sendMessage(msg);
                break;
        }

    }


    public  void getPostByType(String type){
        String url = Util.URL_GET_POST_BY_TYPE;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Ptype",type)
                .addParams("username",MainActivity.getUsername())
                .build()
                .execute(new MyStringCallback());
    }
    //查询所有的帖子
    public void getPostList() {
        String url = Util.URL_QUERY_ALL_POST;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username",MainActivity.getUsername())
                .build()
                .execute(new MyStringCallback());
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
        }

        @Override
        public void onResponse(String response, int id) {
            Log.e("HomeframeFragment接受完毕：", response);
            if (response.equals("get_post_failed")) {
                return;
            }
            List<PostBean> list = new Gson().fromJson(response, new TypeToken<List<PostBean>>() {
            }.getType());
            showPostListAdapter = new ShowPostListAdapter(mContext, list);
            mlistView.setAdapter(showPostListAdapter);
            //处理返回信息
            //设置用户的各个属性  其中设计到json的解析
        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//                mProgressBar.setProgress((int) (100 * progress));

        }

    }
}
