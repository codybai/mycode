package com.tinydeer.android.adapter;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.Utils.Util;
import com.tinydeer.activity.DetailActivity;
import com.tinydeer.android.MainActivity;
import com.tinydeer.android.R;
import com.tinydeer.android.fragment.ClassifyFrameFragment;
import com.tinydeer.domain.MsgBean;
import com.tinydeer.domain.PostBean;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;
import com.zhy.http.okhttp.utils.L;
import com.zhy.http.okhttp.utils.Platform;

import java.util.List;
import java.util.Map;

import okhttp3.Call;
import okhttp3.Request;

/**
 * Created by baicol on 2018-03-08.
 */

public class ShowMsgAdapter extends BaseAdapter {
    private final Context mcontext;
    private final List<MsgBean> datas;

    public ShowMsgAdapter(Context mcontext, List<MsgBean> datas) {
        this.mcontext = mcontext;
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
        ViewHolder viewHolder;
        if (convertView == null) {
            viewHolder = new ViewHolder();
            convertView = View.inflate(mcontext, R.layout.item_my_msg, null);
            viewHolder.item_msg_content = (TextView)convertView.findViewById(R.id.item_msg_content);
            viewHolder.item_msg_owner =(TextView)convertView.findViewById(R.id.item_msg_owner);
            viewHolder.item_msg_time = (TextView)convertView.findViewById(R.id.item_msg_time);
            viewHolder.item_msg_warn_ico =(TextView)convertView.findViewById(R.id.item_msg_warn_ico);

            convertView.setTag(viewHolder);
        } else {
            viewHolder = (ViewHolder) convertView.getTag();
        }
        final MsgBean msg = datas.get(position);

        viewHolder.item_msg_content.setText("“"+msg.getContent()+"”");
        viewHolder.item_msg_time.setText(msg.getTime());
        viewHolder.item_msg_owner.setText("收到"+msg.getCname()+"的回复如下：");
        //根据内容选择加载消息图片
        if(msg.getNum()>0){
            viewHolder.item_msg_warn_ico.setBackgroundResource(R.drawable.has_msg);//
            viewHolder.item_msg_warn_ico.setText(String.valueOf(msg.getNum()));
        }else{
            viewHolder.item_msg_warn_ico.setBackgroundResource(0);//没有消息设置背景为纯白色
        }
        //点击事件
        convertView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.e("converView",String.valueOf(datas.get(position).getPid()));
                //通知服务器
                tellServerReadYet(String.valueOf(datas.get(position).getPid()));
                //修改界面
                datas.get(position).setNum(0);//修改缓存
                //打开有消息提示的页面
                Intent intent  = new Intent(mcontext, DetailActivity.class);
                intent.putExtra("Pid",String.valueOf(datas.get(position).getPid()));
                intent.putExtra("username",String.valueOf(datas.get(position).getPid()));
                mcontext.startActivity(intent);//跳转页面
            }
        });

        return convertView;
    }

    static class ViewHolder {
        TextView item_msg_owner;
        TextView item_msg_content;
        TextView item_msg_time;
        TextView item_msg_warn_ico;
    }

    //保存数据到数据库
    public void tellServerReadYet(String pid) {
        String url = Util.URL_TELL_SERVER_READ_YET;
        OkHttpUtils
                .post()
                .url(url)
                .addParams("Pid",pid)
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
            Log.e("msgclick:",response);

        }

        @Override
        public void inProgress(float progress, long total, int id) {
//            Log.e(TAG, "inProgress:" + progress);
//            mProgressBar.setProgress((int) (100 * progress));

        }
    }

}
