package com.example.deliverycar2

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.telephony.TelephonyManager
import android.util.Log
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.example.deliverycar2.Main2Activity
import com.example.deliverycar2.R
import java.util.*

class SplashActivity : AppCompatActivity() {
    private val splashDelay: Long = 5000 // 5 seconds

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        val loadingImageView: ImageView = findViewById(R.id.loadingImageView)
        Glide.with(this)
            .asGif()
            .load(R.drawable.loading)
            .into(loadingImageView)

        // Check if the user's country is Argentina
        if (isUserInArgentina()) {
            // User is in Argentina, proceed with launching the app
            Log.d("SplashActivity", "User is in Argentina")
            launchMainActivityWithDelay()
        } else {
            // User is not in Argentina, show an error message or exit the app
            Log.d("SplashActivity", "User is not in Argentina")
            // Add your desired logic here, such as showing an error dialog or exiting the app
            launchMainActivityWithDelay()
        }
    }

    private fun isUserInArgentina(): Boolean {
        val locale = Locale.getDefault()
        val countryCode = locale.country
        Log.d("SplashActivity", countryCode)
        return countryCode.equals("US", ignoreCase = true)
    }

    private fun launchMainActivityWithDelay() {
        Handler(Looper.getMainLooper()).postDelayed({
            val intent = Intent(this, Main2Activity::class.java)
            startActivity(intent)
            finish()
        }, splashDelay)
    }
}
