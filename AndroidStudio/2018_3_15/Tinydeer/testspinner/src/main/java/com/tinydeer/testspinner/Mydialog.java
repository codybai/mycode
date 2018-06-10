package com.tinydeer.testspinner;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.annotation.StyleRes;
import android.view.WindowManager;

/**
 * Created by baicol on 2018-03-12.
 */

public class Mydialog extends Dialog {
    private Context context;
    public Mydialog(@NonNull Context context) {
        super(context);
    }

    public Mydialog(@NonNull Context context, @StyleRes int themeResId) {
        super(context, themeResId);
    }

    protected Mydialog(@NonNull Context context, boolean cancelable, @Nullable OnCancelListener cancelListener) {
        super(context, cancelable, cancelListener);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WindowManager m =getWindow().getWindowManager();
//        m.getDefaultDisplay()
    }
}
