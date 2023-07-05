package com.example.deliverycar2

import android.app.AlertDialog
import android.content.DialogInterface
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class RegisterActivity : AppCompatActivity() {
    private lateinit var acceptButton: Button
    private lateinit var declineButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

//        acceptButton = findViewById(R.id.acceptButton)
//        declineButton = findViewById(R.id.declineButton)
//
//        acceptButton.setOnClickListener {
//            // Handle accept action
//            // For example, perform the registration process
//            // ...
//
//            // After successful registration, start the Step2Activity
//            startActivity(Intent(this, Step2::class.java))
//        }
//
//        declineButton.setOnClickListener {
//            // Handle decline action
//            // For example, go back to the previous screen
//            onBackPressed()
//        }

        showPromptDialog()
    }

    private fun showPromptDialog() {
        val alertDialogBuilder = AlertDialog.Builder(this)
        alertDialogBuilder.setTitle(getString(R.string.ToSConfirmationTitlePrompt))
        alertDialogBuilder.setMessage(getString(R.string.ToSConfirmationTextPrompt))
        alertDialogBuilder.setPositiveButton(getString(R.string.ToSConfirmationAcceptPrompt)) { _, _ ->
            // Handle accept action
            // For example, perform the registration process
            // ...

            // After successful registration, start the Step2Activity
            startActivity(Intent(this, Step2::class.java))
        }
        alertDialogBuilder.setNegativeButton(getString(R.string.ToSConfirmationDeclinePrompt)) { _, _ ->
            // Handle decline action
            // For example, go back to the previous screen
            onBackPressed()
        }
        alertDialogBuilder.setOnCancelListener(DialogInterface.OnCancelListener {
            // Handle dialog cancel action
            onBackPressed()
        })

        val alertDialog = alertDialogBuilder.create()
        alertDialog.setCancelable(false)
        alertDialog.show()
    }
}
