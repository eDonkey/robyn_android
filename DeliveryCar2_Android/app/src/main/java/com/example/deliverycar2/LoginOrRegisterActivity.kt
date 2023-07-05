package com.example.deliverycar2

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import java.*

class LoginOrRegisterActivity : AppCompatActivity(), View.OnClickListener {
    private lateinit var loginButton: Button
    private lateinit var registerButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login_or_register)

        loginButton = findViewById(R.id.loginButton)
        registerButton = findViewById(R.id.registerButton)

        loginButton.setOnClickListener(this)
        registerButton.setOnClickListener(this)
    }

    override fun onClick(view: View) {
        when (view.id) {
            R.id.loginButton -> {
                // Start the LoginActivity to handle login process
                startActivity(Intent(this, LoginActivity::class.java))
            }
            R.id.registerButton -> {
                // Start the RegisterActivity to handle registration process
                startActivity(Intent(this, RegisterActivity::class.java))
            }
        }
    }
}
