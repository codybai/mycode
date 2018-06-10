package com.tinydeer.android.adapter;

import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.tinydeer.android.R;
import com.tinydeer.domain.UserData;

import java.util.List;

/**
 * Created by baicol on 2018-03-11.
 */

public class ShowMyFocusAdapter extends BaseAdapter {
    private List<UserData> datas;
    private Context mContext;

    public ShowMyFocusAdapter( Context mContext,List<UserData> datas) {
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
    public View getView(int position, View convertView, ViewGroup parent) {
        ViewHolder viewHolder ;
        if(null==convertView){
            viewHolder=new ViewHolder();
            convertView = View.inflate(mContext, R.layout.item_show_user_list,null);
            viewHolder.itemIco  = (TextView)convertView.findViewById(R.id.item_show_user_list_ico);
            viewHolder.itemName= (TextView)convertView.findViewById(R.id.item_show_user_list_name);
            viewHolder.itemName.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
               //     Intent intent =new Intent(this,)//此处打开我关注的用户的具体信息
                }
            });

            convertView.setTag(viewHolder);
        }else{
            viewHolder=(ViewHolder)convertView.getTag();
        }
        UserData  userData = datas.get(position);
        viewHolder.itemName.setText(userData.getUsername());

        return convertView;
    }
    static class ViewHolder{
        TextView itemIco;
        TextView itemName;
    }

}
