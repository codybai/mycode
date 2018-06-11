package com.tinydeer.android.adapter;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.activity.DetailActivity;
import com.tinydeer.activity.UserInfoSendStoreActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.fragment.HomeFrameFragment;
import com.tinydeer.domain.PostBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;

import java.util.List;
import java.util.Map;
import java.util.Objects;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-05.
 */

public class ShowPostListAdapter extends BaseAdapter {
    private Context mcontext;
    private List<PostBean> datas;


    public ShowPostListAdapter(Context context, List<PostBean> datas) {
        this.mcontext = context;
        this.datas = datas;
    }

    @Override
    public int getCount() {
        return datas.size();
    }

    @Override
    public Object getItem(int position) {
        return datas.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        final ViewHolder viewhold;
        if (null == convertView) {
            viewhold = new ViewHolder();
            convertView = View.inflate(mcontext, R.layout.item_post_list, null);
            viewhold.item_ico = (TextView) convertView.findViewById(R.id.item_ico);  //头像
            viewhold.item_name = (TextView) convertView.findViewById(R.id.item_name);//昵称
            viewhold.item_post_title = (TextView)convertView.findViewById(R.id.item_post_title);//文章标题
            viewhold.item_post_content  = (TextView) convertView.findViewById(R.id.item_post_content);//文章内容
            viewhold.mItemReadCount = (TextView) convertView.findViewById(R.id.item_post_read_counts);//浏览数

            viewhold.mStoreTextIco=(TextView)convertView.findViewById(R.id.item_make_fouce_ico);
            viewhold.mUpTimesTextIco=(TextView)convertView.findViewById(R.id.item_up_times_ico);




            viewhold.item_post_content.setOnClickListener(new View.OnClickListener() {//点击内容打开帖子
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(mcontext,new DetailActivity().getClass());
                    intent.putExtra("Pid",viewhold.Pid);
                    mcontext.startActivity(intent);
                }
            });
            viewhold.item_post_title.setOnClickListener(new View.OnClickListener() {//点击标题打开帖子
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(mcontext,new DetailActivity().getClass());
                    intent.putExtra("Pid",viewhold.Pid);
                    mcontext.startActivity(intent);
                }
            });

            convertView.setTag(viewhold); //相当于登记在案
        } else {
            viewhold = (ViewHolder)convertView.getTag();//请求放出  决定创建还是废物利用
        }

        final PostBean postBean=datas.get(position);
        //根据点赞与否初始化图标
        if(postBean.getLovesign().equals("loved")){//点过赞
            viewhold.mUpTimesTextIco.setBackgroundResource(R.drawable.up_press);
        }else {//未点赞
            viewhold.mUpTimesTextIco.setBackgroundResource(R.drawable.up);
        }

        //根据点赞与否初始化图标
        if(postBean.getCollectionsign().equals("collected")){//收藏过
            viewhold.mStoreTextIco.setBackgroundResource(R.drawable.focus_ico);
//            viewhold.mStoreText.setText("已收藏");
        }else {//未收藏过
            viewhold.mStoreTextIco.setBackgroundResource(R.drawable.to_store_ico);
//            viewhold.mStoreText.setText("点击收藏");
        }



        //重新绑定变量
        viewhold.item_up_times = (TextView)convertView.findViewById(R.id.item_up_times);//赞的人数
        viewhold.mStoreText = (TextView)convertView.findViewById(R.id.item_make_store);//收藏数
        viewhold.item_name = (TextView)convertView.findViewById(R.id.item_name);

        //点赞响应事件
        viewhold.mUpTimesTextIco.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if(postBean.getLovesign().equals("unloved")){//未点过赞可以点赞
                    int count = postBean.getLovenum()+1;
                    datas.get(position).setLovenum(count);//关键一步！！！！！！ ，点赞同时同步userBean,然后连接后台修改数据
                    datas.get(position).setLovesign("loved");//同步userBean标志
                    viewhold.item_up_times.setText(String.valueOf(count));//修改界面
                    tellServerPlusUpTime(String.valueOf(datas.get(position).getPid()));//同步后台数据
                    //点完赞更新界面图标
                    viewhold.mUpTimesTextIco.setBackgroundResource(R.drawable.up_press);
                    Log.e("赞：","1223");
                }

            }
        });
        //收藏响应事件
        viewhold.mStoreTextIco.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(postBean.getCollectionsign().equals("uncollected")){//未收藏可以收藏
                    int count = postBean.getFollownum()+1;
                    datas.get(position).setFollownum(count);//关键一步！！！！！！ ，点赞同时同步userBean,然后连接后台修改数据
                    datas.get(position).setCollectionsign("collected");//同步userBean标志
//                    viewhold.mStoreText.setText("已收藏");//修改界面
                    tellServerStorePost(String.valueOf(datas.get(position).getPid()));//同步后台数据
                    //点完赞更新界面图标
                    viewhold.mStoreTextIco.setBackgroundResource(R.drawable.focus_ico);
                    Log.e("赞：","1223");
                }
            }
        });

        viewhold.item_name.setText(postBean.getUsername());//用户名
        viewhold.item_post_title.setText(postBean.getTitle());//文章题目
        viewhold.item_post_content.setText(postBean.getPcontent());//内容
        viewhold.item_up_times.setText(String.valueOf(postBean.getLovenum()));//赞
        viewhold.mItemReadCount.setText(String.valueOf(postBean.getBrowsernum()));//浏览数
        viewhold.mStoreText.setText(String.valueOf(postBean.getFollownum()));//收藏与否
        viewhold.Pid = String.valueOf(postBean.getPid());


        return convertView;
    }
    static class ViewHolder{
        TextView item_ico;
        TextView item_name ;
        TextView  item_post_title;
        TextView item_post_content ;
        TextView  item_up_times ;
        TextView mUpTimesTextIco;
        TextView  mStoreText ;//
        TextView  mStoreTextIco;
        String Pid;
        TextView mItemReadCount;


    }
public void tellServerStorePost(String Pid){
        String url = Util.URL_CLICK_STORE_PLUS;
    OkHttpUtils
            .post()
            .url(url)
            .addParams("Pid", Pid)
            .addParams("username",MainActivity.getUsername())
            .build()
            .execute(new MyStringCallback());

    }
    public void tellServerPlusUpTime(String Pid) {
        String url = Util.URL_TELL_SERVER_UPTIMES_PLUS;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid", Pid)
                .addParams("username",MainActivity.getUsername())
                .build()
                .execute(new MyStringCallback());
    }

    private class MyStringCallback extends StringCallback {
        @Override
        public void onBefore(Request request, int id) {
//            mProgressBar.setVisibility(View.VISIBLE);
        }

        @Override
        public void onAfter(int id) {
//            mProgressBar.setVisibility(View.INVISIBLE);
        }

        @Override
        public void onError(Call call, Exception e, int id) {
            e.printStackTrace();
        }

        @Override
        public void onResponse(String response, int id) {

        }

        @Override
        public void inProgress(float progress, long total, int id) {
//                mProgressBar.setProgress((int) (100 * progress));
        }
    }


}
