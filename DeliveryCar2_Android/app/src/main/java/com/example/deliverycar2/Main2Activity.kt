package com.example.deliverycar2

import android.content.Intent
import android.os.Bundle
import android.view.inputmethod.InputMethodManager
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import org.json.JSONObject
import java.io.IOException

class Main2Activity : AppCompatActivity() {
    private val client = OkHttpClient()
    private lateinit var origenEditText: EditText
    private lateinit var destinoEditText: EditText
    private lateinit var requestButton: Button
    private lateinit var responseTextView: TextView
    private lateinit var continueButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)

        origenEditText = findViewById(R.id.origenEditText)
        destinoEditText = findViewById(R.id.destinoEditText)
        requestButton = findViewById(R.id.requestButton)
        responseTextView = findViewById(R.id.responseTextView)
        continueButton = findViewById(R.id.continueButton)
        continueButton.isEnabled = false

        requestButton.setOnClickListener {
            val origen = origenEditText.text.toString()
            val destino = destinoEditText.text.toString()
            runRESTAPI("https://kooltheoutsider.pythonanywhere.com/reqDist", origen, destino)

            // Hide the keyboard
            val inputMethodManager = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
            inputMethodManager.hideSoftInputFromWindow(currentFocus?.windowToken, 0)
        }

        continueButton.setOnClickListener {
            val intent = Intent(this, LoginOrRegisterActivity::class.java)
            intent.putExtra("destino", responseTextView.text.toString())
            startActivity(intent)
        }
    }

    private fun runRESTAPI(url: String, origen: String, destino: String) {
        val formBody = FormBody.Builder()
            .add("add_from", origen)
            .add("add_to", destino)
            .add("source", "android")
            .build()
        val request = Request.Builder()
            .url(url)
            .post(formBody)
            .build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    responseTextView.text = "Request Failed"
                    continueButton.isEnabled = false
                }
            }

            override fun onResponse(call: Call, response: Response) {
                val responseBody = response.body?.string()
                val jsonResponse = JSONObject(responseBody)

                if (jsonResponse.has("data")) {
                    val data = jsonResponse.getJSONArray("data")

                    runOnUiThread {
                        if (data.length() > 0) {
                            val firstDataObject = data.getJSONObject(0)
                            val destinoArray = firstDataObject.getJSONArray("destino")
                            val origenArray = firstDataObject.getJSONArray("origen")
                            val distancia = firstDataObject.getString("distancia")
                            val precio = firstDataObject.getString("precio")

                            val destino = destinoArray.getString(0)
                            val origen = origenArray.getString(0)
                            responseTextView.text =
                                "Destno: $destino\n" +
                                        "Origen: $origen\n" +
                                        "Distancia: $distancia\n" +
                                        "Precio: $precio"

                            continueButton.isEnabled = true
                        } else {
                            responseTextView.text = "No data found"
                            continueButton.isEnabled = false
                        }
                    }
                } else {
                    runOnUiThread {
                        responseTextView.text = "Invalid response format"
                        continueButton.isEnabled = false
                    }
                }
            }
        })
    }
}
