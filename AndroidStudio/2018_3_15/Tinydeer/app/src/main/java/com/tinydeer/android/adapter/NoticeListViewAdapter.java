package com.tinydeer.android.adapter;

import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.tinydeer.activity.DetailNoticeActivity;
import com.tinydeer.android.R;
import com.tinydeer.domain.NoticeBean;

import java.util.List;

/**
 * Created by baicol on 2018-03-13.
 */

public class NoticeListViewAdapter extends BaseAdapter {
    private List<NoticeBean> datas;
    private Context mContext;

    public NoticeListViewAdapter(List<NoticeBean> datas, Context mContext) {
        this.datas = datas;
        this.mContext = mContext;
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
        if(null == convertView){
            viewHolder = new ViewHolder();
            convertView = View.inflate(mContext, R.layout.item_notice_listview,null);
            viewHolder.noticeTitle = (TextView) convertView.findViewById(R.id.notice_id);
            viewHolder.noticeTime=(TextView)convertView.findViewById(R.id.notice_time);

            convertView.setTag(viewHolder);
        }else{
            viewHolder = (ViewHolder) convertView.getTag();
        }
        convertView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(mContext, DetailNoticeActivity.class);
                intent.putExtra("noticeID",String.valueOf(datas.get(position).getPid()));
                mContext.startActivity(intent);
            }
        });
        NoticeBean noticeBean = datas.get(position);
        viewHolder.noticeTitle.setText(noticeBean.getTitle());
        viewHolder.noticeTime.setText(noticeBean.getPtime());
        return convertView;
    }
    static class ViewHolder{
        TextView noticeTitle;
        TextView noticeTime;
    }
}
