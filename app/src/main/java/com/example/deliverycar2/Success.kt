package com.example.deliverycar2

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class Success : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar?.hide()

        setContentView(R.layout.activity_success)

        // Additional setup for the success screen, if needed
    }
}
