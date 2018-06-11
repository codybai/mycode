package com.tinydeer.android.adapter;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.tinydeer.android.R;
import com.tinydeer.domain.LeftWordsBean;
import com.tinydeer.domain.PostDetailBean;

import java.util.List;

/**
 * Created by baicol on 2018-03-11.
 */

public class DetailLeftWordAdapter extends BaseAdapter {
    public DetailLeftWordAdapter(List<LeftWordsBean> datas, Context mContext) {
        this.datas = datas;
        this.mContext = mContext;
    }

    private List<LeftWordsBean> datas;
    private Context mContext;
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
    public View getView(int position, View convertView, ViewGroup parent) {
        ViewHolder viewHolder;
        if(null == convertView){
            viewHolder = new ViewHolder();
            convertView = View.inflate(mContext,R.layout.item_show_left_words,null);
            viewHolder.username = (TextView)convertView.findViewById(R.id.left_word_user_name);
            viewHolder.content = (TextView)convertView.findViewById(R.id.left_words_content);


            convertView.setTag(viewHolder);
        }else{
            viewHolder= (ViewHolder) convertView.getTag();
        }
        viewHolder.username.setText(datas.get(position).getUsername());
        viewHolder.content.setText(datas.get(position).getCcontent());

        return convertView;
    }
    static class ViewHolder{
        TextView username;
        TextView content;
    }
}
