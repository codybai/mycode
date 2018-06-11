package com.tinydeer.activity;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.Nullable;
import android.util.Log;
import android.widget.ListView;
import android.widget.TextView;

import com.tinydeer.android.R;
import com.tinydeer.android.adapter.ShowPostListAdapter;

/**
 * Created by baicol on 2018-03-05.
 */

public class ShowPostListActivity extends Activity {
    private ListView mlistView;
    private Context context;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_post_list);
        mlistView = (ListView) findViewById(R.id.post_list_view);

    }
}
