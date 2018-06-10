package com.tinydeer.mytestadapter;

import android.content.Intent;
import android.net.Uri;
import android.provider.ContactsContract;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.tinydeer.adapter.myListAdapter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    private ListView mLv;
    private DrawerLayout mDrawerLayout;
    private myListAdapter m_yListAdapter;
    private List<Map<String, Object>> list = new ArrayList<>();
    private DrawerLayout drawerLayout;
    private String str;
    private TextView textView;
    private Spinner sp;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        sp = (Spinner)findViewById(R.id.myspinner);

    }


}















