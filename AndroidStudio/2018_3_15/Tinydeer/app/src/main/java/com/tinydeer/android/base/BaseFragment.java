package com.tinydeer.android.base;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

/**
 * Created by baicol on 2018-03-01.
 * 基类  公共类  4个按钮的页面都要继承该类
 */

public abstract class BaseFragment extends Fragment {
    /*
    * 初始化视图
    * */
    protected Context mContext;
    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mContext = getActivity();
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return initView();
    }
//    强制子类重写，实现子类特有的ui
    protected abstract View initView() ;

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        initData();
    }
//当孩子需要初始化数据，或者要联网请求绑定数据或者展示数据的时候等等可以重写改方法
    protected void initData() {

    }
    //以上方法由系统调用
}
