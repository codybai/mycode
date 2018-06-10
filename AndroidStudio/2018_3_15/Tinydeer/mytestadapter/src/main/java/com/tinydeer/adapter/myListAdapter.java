package com.tinydeer.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.tinydeer.mytestadapter.R;

import java.util.List;
import java.util.Map;

/**
 * Created by baicol on 2018-03-06.
 */

public class myListAdapter extends BaseAdapter {

    private Context context;
    private List<Map<String,Object>> list;
    public myListAdapter(Context context, List<Map<String, Object>> list) {
        this.context = context;
        this.list = list;
    }

    @Override
    public int getCount() {
        return list.size();
    }

    @Override
    public Object getItem(int position) {
        return list.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ViewHolder viewHolder;
        if(null ==convertView){


            viewHolder = new ViewHolder();
            convertView= View.inflate(context,R.layout.item_list,null);
            viewHolder.text_1 = (TextView)convertView.findViewById(R.id.text_1);
            viewHolder.text_2 = (TextView)convertView.findViewById(R.id.text_2);
            viewHolder.text_3 = (TextView)convertView.findViewById(R.id.text_3);
            viewHolder.text_4 = (TextView)convertView.findViewById(R.id.text_4);

            convertView.setTag(viewHolder);
        }else{
            viewHolder= (ViewHolder) convertView.getTag();
        }
        Map<String,Object> map = list.get(position);
        viewHolder.text_1.setText(map.get("text_1").toString());
        viewHolder.text_2.setText(map.get("text_2").toString());
        viewHolder.text_3.setText( map.get("text_3").toString());
        viewHolder.text_4.setText( map.get("text_4").toString());

        return convertView;
    }
    static class ViewHolder{
        TextView text_1;
        TextView text_2;
        TextView text_3;
        TextView text_4;
    }
}
