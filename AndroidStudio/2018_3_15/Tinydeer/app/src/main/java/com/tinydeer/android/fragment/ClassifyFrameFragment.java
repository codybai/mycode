package com.tinydeer.android.fragment;

import android.util.Log;
import android.view.View;
import android.widget.ListView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.activity.ShowBoardActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.adapter.ShowMsgAdapter;
import com.tinydeer.android.R;
import com.tinydeer.android.base.BaseFragment;
import com.tinydeer.domain.MsgBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-01.
 */

public class ClassifyFrameFragment extends BaseFragment {
    private static final  String TAG = ClassifyFrameFragment.class.getSimpleName();//"CommonFrameFragment"
    private ListView listView;
    private ShowMsgAdapter showMsgAdapter;
    private List<MsgBean> datas;
    @Override
    protected View initView() {//创建绘图
        View view = View.inflate(mContext,R.layout.activity_classify,null);
        listView = (ListView)view.findViewById(R.id.my_msg_listview);
//        造数据


        return view;
    }

    @Override
    protected void initData() {
        super.initData();

        getMesFromServer();
    }



    //保存数据到数据库
    public void getMesFromServer() {
        String url = Util.URL_GET_ALL_MY_MSG;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("username", MainActivity.getUsername())
                .build()
                .execute(new MyStringCallback());

    }



    public class MyStringCallback extends StringCallback {
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
            Log.e("msglist",response);
            Gson gson = new Gson();
            datas = gson.fromJson(response,new TypeToken<List<MsgBean>>(){}.getType());
            showMsgAdapter = new ShowMsgAdapter(mContext,datas);
            listView.setAdapter(showMsgAdapter);

        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//            mProgressBar.setProgress((int) (100 * progress));

        }
    }

}
