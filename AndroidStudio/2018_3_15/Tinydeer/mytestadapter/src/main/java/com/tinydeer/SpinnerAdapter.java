package com.tinydeer;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.tinydeer.mytestadapter.R;

/**
 * Created by baicol on 2018-03-10.
 */

public class SpinnerAdapter extends BaseAdapter {
    public SpinnerAdapter(String[] datas, Context mcontext) {
        this.datas = datas;
        this.mcontext = mcontext;
    }

    private String[] datas;
    private Context mcontext;

    @Override
    public int getCount() {
        return datas.length;
    }

    @Override
    public Object getItem(int position) {
        return datas[position];
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
//        TextView textView = View.inflate(mcontext, R.layout.activity_main,null).findViewById(R.id.)
        return convertView;
    }
}
