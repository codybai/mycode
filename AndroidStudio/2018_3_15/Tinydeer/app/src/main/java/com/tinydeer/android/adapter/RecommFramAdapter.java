package com.tinydeer.android.adapter;

import android.content.Context;
import android.graphics.Color;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

/**
 * Created by baicol on 2018-03-03.
 */

public class RecommFramAdapter extends BaseAdapter {
    private final Context mContext;
    private final String[] mDatas;

    public RecommFramAdapter(Context context,String[] datas) {
        this.mContext = context;
        this.mDatas = datas;
        
    }

    @Override
    public int getCount() {
        return mDatas.length;
    }

    @Override
    public Object getItem(int position) {
        return null;
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {//对于每一个position位置的进行设置item的函数
        TextView textview = new TextView(mContext);
        textview.setTextColor(Color.BLACK);
        textview.setTextSize(20);
        textview.setPadding(40,40,0,40);
        textview.setText(mDatas[position]);

        return textview;
    }

}
