package com.example.deliverycar2

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

class Step2 : AppCompatActivity() {
    private lateinit var goBackButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_step2)
        goBackButton = findViewById(R.id.goBackButton)
        goBackButton.setOnClickListener {
            // Finish the current activity and go back to the previous screen
            finish()
        }
    }
}