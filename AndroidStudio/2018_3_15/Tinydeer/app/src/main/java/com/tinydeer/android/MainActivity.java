package com.tinydeer.android;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.annotation.IdRes;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.RadioGroup;
import android.widget.Toast;

import com.tinydeer.activity.DetailActivity;
import com.tinydeer.activity.SendPostActivity;
import com.tinydeer.android.base.BaseFragment;
import com.tinydeer.android.fragment.ClassifyFrameFragment;
import com.tinydeer.android.fragment.CommonFrameFragment;
import com.tinydeer.android.fragment.HomeFrameFragment;
import com.tinydeer.android.fragment.ProfileFrameFragment;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by baicol on 2018-02-28.
 */

public class MainActivity extends FragmentActivity {
    /*
        上次切换的Fragment
     */
    private static String username;
    private static String password;


    static private Fragment mContent;
    private RadioGroup mRg_main;
    private List<BaseFragment> mBaseFragment;
    private int position;
    private Button btn_send;
    public static Handler handler;
    private static Button menu_btn;
    public static DetailActivity detailActivity;
    private Button quit_btn;
    public static String getUsername(){return username;}
    public static String getPassword(){return password;}
    public static DetailActivity getDetailActivity() {
        return detailActivity;
    }
    public static void clearUserInfo(){username="";password="";}
    public static Button getMenu_btn() {
        return menu_btn;
    }  //侧拉兰监听

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        detailActivity = new DetailActivity();
//        初始化view

        username = getIntent().getStringExtra("username");
        password=getIntent().getStringExtra("password");
        Log.e("ceshi",password+username);

        handler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {
                switch (msg.what){
                    case 1:
                        finish();
                        break;
                    default:
                        break;
                }
                return true;
            }
        });
        setContentView(R.layout.activity_main);
        mRg_main = (RadioGroup) findViewById(R.id.rg_main);
        btn_send = (Button) findViewById(R.id.rb_send);
        btn_send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, new SendPostActivity().getClass());
                startActivity(intent);
            }
        });
        menu_btn = (Button) findViewById(R.id.open_menu);//侧拉栏弹出按钮
        //设置默认选中
//        mRg_main.check(R.id.rb_recomm);

        //初始化fragment
//        homeFrameFragment=;

        mBaseFragment = new ArrayList<>();
        mBaseFragment.add(new CommonFrameFragment());//推荐
        mBaseFragment.add(new HomeFrameFragment());//分类
        mBaseFragment.add(new ClassifyFrameFragment());//社区
        mBaseFragment.add( new ProfileFrameFragment());//我的



        //设置RadioGroup的监听
        mRg_main.setOnCheckedChangeListener(new MyOnCheckChangeListener());
        //设置默认选中
        mRg_main.check(R.id.rb_recomm);
    }

    //    private void switchFragment(BaseFragment fragment) {   //用得到的页面替换当前屏幕fl_content下的内容 replace实现
//        //得到FragmentManger
//        FragmentManager fm = getSupportFragmentManager();  //得到一个管理替换页面的管理对象
//        //开启事务
//        FragmentTransaction transaction = fm.beginTransaction();   //开启事务，这个事务类似一个线程，通过事务才能替换，这个事务是由管理器返回的
//        //替换
//        transaction.replace(R.id.fl_content,fragment);
//        //提交事务
//        transaction.commit();
//    }
    //from：目前显示的页面
    //to:即将切换到的页面；
    private void switchFragment(Fragment from, Fragment to) {   //用得到的页面替换当前屏幕fl_content下的内容 add实现，优化重复联网初始化情况
        if (from != to) {
            mContent = to;
            FragmentTransaction ft = getSupportFragmentManager().beginTransaction();//开启一个事务
            //切换
            //判断有没有被添加
            if (!to.isAdded()) {
                //没有被添加
                //from隐藏
                if (from != null) {
                    ft.hide(from);
                }
                //添加to
                if (to != null) {
                    ft.add(R.id.fl_content, to).commit();//第一次add不需要show
                }
            } else {
//                已经被添加
                //from隐藏
                // show to
                if (from != null) {
                    ft.hide(from);
                }
                //添加to
                if (to != null) {
                    ft.show(to).commit();//已经add需要用show来显示
                }
            }

        }
    }


    private BaseFragment getFragment(int position) {
        BaseFragment fragment = mBaseFragment.get(position);
        return fragment;

    }

    private class MyOnCheckChangeListener implements RadioGroup.OnCheckedChangeListener {
        @Override
        public void onCheckedChanged(RadioGroup group, @IdRes int checkedId) {
            switch (checkedId) {
                case R.id.rb_recomm://tuijian
                    menu_btn.setVisibility(View.INVISIBLE);
                    position = 0;
                    break;
                case R.id.rb_classify://tuijian
                    menu_btn.setVisibility(View.VISIBLE);
                    position = 1;
                    break;
                case R.id.rb_home://tuijian
                    menu_btn.setVisibility(View.INVISIBLE);
                    position = 2;
                    break;
                case R.id.rb_profile://tuijian
                    menu_btn.setVisibility(View.INVISIBLE);
                    position = 3;
                    break;
                default:
                    position = 0;
                    break;
            }

            //根据位置得到对应的flagment
            BaseFragment to = getFragment(position);
            //替换
//                    switchFragment(fragment);  //自定义替换函数
            switchFragment(mContent, to);
        }
    }
}
