package com.example.deliverycar2

//import android.app.AlertDialog
//import android.content.DialogInterface
//import android.content.Intent
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import org.json.JSONObject
import java.io.IOException
import java.util.regex.Pattern

class Step2 : AppCompatActivity() {
    private val client = OkHttpClient()



    override fun onCreate(savedInstanceState: Bundle?) {
        setContentView(R.layout.activity_step2)
        val firstNameEditText = findViewById<EditText>(R.id.firstNameEditText)
        val lastNameEditText = findViewById<EditText>(R.id.lastNameEditText)
        val emailEditText = findViewById<EditText>(R.id.emailEditText)
        val passwordEditText = findViewById<EditText>(R.id.passwordEditText)
        val confirmPasswordEditText = findViewById<EditText>(R.id.confirmPasswordEditText)
        val registerButton = findViewById<Button>(R.id.registerButton)
        super.onCreate(savedInstanceState)

        registerButton.setOnClickListener {
            val firstName = firstNameEditText.text.toString().trim()
            val lastName = lastNameEditText.text.toString().trim()
            val email = emailEditText.text.toString().trim()
            val password = passwordEditText.text.toString().trim()
            val confirmPassword = confirmPasswordEditText.text.toString().trim()

            if (validateInput(firstName, lastName, email, password, confirmPassword)) {
                val formBody = FormBody.Builder()
                    .add("nombre", firstName)
                    .add("apellido", lastName)
                    .add("email", email)
                    .add("password", password)
                    .add("confirm_password", password)
                    .build()

                val request = Request.Builder()
                    .url("https://kooltheoutsider.pythonanywhere.com/newUser")
                    .post(formBody)
                    .build()

                client.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        Log.e("API Call", "Registration request failed", e)
                        runOnUiThread {
                            Toast.makeText(this@Step2, "Registration Failed", Toast.LENGTH_SHORT).show()
                        }
                    }

                    override fun onResponse(call: Call, response: Response) {
                        val responseBody = response.body?.string()
                        val jsonObject = JSONObject(responseBody)
                        val status = jsonObject.getString("status")
                        if (status == "USER_REGISTRATION_SUCCESS") {
                            runOnUiThread {
                                Log.e("API Call", status)
                                Toast.makeText(this@Step2, "Registration Successful", Toast.LENGTH_SHORT).show()
                                // Proceed to the next screen or perform any necessary actions
                                startActivity(Intent(this@Step2, Success::class.java))
                            }
                        } else {
                            runOnUiThread {
                                Log.e("API Call", response.toString())
                                Toast.makeText(this@Step2, "Registration Failed", Toast.LENGTH_SHORT).show()
                            }
                        }
                    }
                })
            }
        }
    }
    private fun validateInput(
        firstName: String,
        lastName: String,
        email: String,
        password: String,
        confirmPassword: String
    ): Boolean {
        val namePattern = Pattern.compile("[a-zA-Z]+")
        val emailPattern = Pattern.compile("[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+")
        val passwordPattern = Pattern.compile("[a-zA-Z0-9]{8,}")
//
//        if (firstName.isEmpty() || !namePattern.matcher(firstName).matches()) {
//            firstNameEditText.error = "Invalid first name"
//            firstNameEditText.requestFocus()
//            return false
//        }
//
//        if (lastName.isEmpty() || !namePattern.matcher(lastName).matches()) {
//            lastNameEditText.error = "Invalid last name"
//            lastNameEditText.requestFocus()
//            return false
//        }
//
//        if (email.isEmpty() || !emailPattern.matcher(email).matches()) {
//            emailEditText.error = "Invalid email"
//            emailEditText.requestFocus()
//            return false
//        }
//
//        if (password.isEmpty() || !passwordPattern.matcher(password).matches()) {
//            passwordEditText.error = "Password must be at least 8 characters long"
//            passwordEditText.requestFocus()
//            return false
//        }
//
//        if (confirmPassword.isEmpty() || confirmPassword != password) {
//            confirmPasswordEditText.error = "Passwords do not match"
//            confirmPasswordEditText.requestFocus()
//            return false
//        }

        return true
    }
}
