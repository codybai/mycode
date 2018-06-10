package com.tinydeer.android.fragment;

import android.content.Intent;
import android.graphics.Color;
import android.os.Message;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.activity.OKHttpActivity;
import com.tinydeer.activity.ShowUserListActivity;
import com.tinydeer.activity.UserInfoPageActivity;
import com.tinydeer.activity.UserInfoSendStoreActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.adapter.NoticeListViewAdapter;
import com.tinydeer.android.adapter.RecommFramAdapter;
import com.tinydeer.android.adapter.ShowPostListAdapter;
import com.tinydeer.android.base.BaseFragment;
import com.tinydeer.domain.NoticeBean;
import com.tinydeer.domain.UserData;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-01.
 */

public class CommonFrameFragment extends BaseFragment {
    private ViewPager viewPager;
    private ListView noticeListView;
    private LinearLayout ll_point_group;
    private ArrayList<ImageView> imageViews;
    private String[] notices = {"实习公告通知！","实习公告通知！","实习公告通知！","实习公告通知！","实习公告通知！","实习公告通知！"};
    private final int[] imageIds = {
            R.drawable.d_welcome,
            R.drawable.b_welcome,
            R.drawable.c_welcome
    };
    private final String[] imageDescriptions = {
            "不错不错!",
            "很好很好！",
            "哈哈哈哈!"
    };


    @Override
    protected View initView() {//创建绘图  页面显示的主要内容在这里初始化并且创建
        View view = View.inflate(mContext, R.layout.welcom_view_page, null);
        viewPager = (ViewPager) view.findViewById(R.id.viewpage_welcome);
        noticeListView = (ListView)view.findViewById(R.id.notice_listview);



        getNoticeInfo();

        return view;
    }

    @Override
    protected void initData() {
        super.initData();

        imageViews = new ArrayList<>();
        for (int i = 0; i < imageIds.length; i++) {
            ImageView imageView = new ImageView(mContext);
            imageView.setBackgroundResource(imageIds[i]);
            imageViews.add(imageView);

        }
        viewPager.setAdapter(new MyPageAdapter());


    }

    class MyPageAdapter extends PagerAdapter {

        @Override
        public int getCount() {
            return imageViews.size();
        }

        @Override
        public Object instantiateItem(ViewGroup container, int position) {
            ImageView imageView = imageViews.get(position);
            container.addView(imageView);
            return imageView;
        }

        @Override
        public void destroyItem(ViewGroup container, int position, Object object) {
            container.removeView((View) object);
        }

        @Override
        public boolean isViewFromObject(View view, Object object) {
            return view == object;
        }
    }

    //第一次点击我的联网获取信息
    public void getNoticeInfo() {
        String url = Util.URL_GET_ALL_NOTICE;;
        OkHttpUtils
                .post()
                .url(url)
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
            Log.e("onerror:",e.getMessage());

        }

        @Override
        public void onResponse(String response, int id) {

            Gson gson = new Gson();
            List<NoticeBean> list = gson.fromJson(response, new TypeToken<List<NoticeBean>>(){}.getType());
            NoticeListViewAdapter noticeListViewAdapter = new NoticeListViewAdapter(list,mContext);
            noticeListView.setAdapter(noticeListViewAdapter);

        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//                mProgressBar.setProgress((int) (100 * progress));

        }

    }

}
