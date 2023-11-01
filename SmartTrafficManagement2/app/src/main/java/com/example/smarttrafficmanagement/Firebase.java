package com.example.smarttrafficmanagement;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class Firebase extends AppCompatActivity {

    private DatabaseReference sensorDataRef,sensorDataRef1;

    private TextView textViewDistance;
    private TextView textViewDistance2;

    private TextView status,status1;

    private TextView airQualityTextView;
private ImageView img1,img2;
    @SuppressLint("CutPasteId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_firebase);

        // Initialize Firebase
        FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();
        sensorDataRef = firebaseDatabase.getReference("TrafficLightStatus1");
        sensorDataRef1 = firebaseDatabase.getReference("TrafficLightStatus2");
        // Get references to GaugeView widgets in your layout
        textViewDistance=findViewById(R.id.textViewDistance);
        textViewDistance2=findViewById(R.id.textViewDistance2);
        status=findViewById(R.id.textViewStatus);
        status1=findViewById(R.id.textViewStatus2);
        img1=findViewById(R.id.trafficLightImage);
        img2=findViewById(R.id.trafficLightImage2);



        sensorDataRef.addValueEventListener(new ValueEventListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if (dataSnapshot.exists()) {
                    // Retrieve values from the dataSnapshot
                    Double Distance = dataSnapshot.child("Distance1").getValue(Double.class);
                    Integer redstatus = dataSnapshot.child("Red").getValue(Integer.class);
                    Integer yelstatus = dataSnapshot.child("Yellow").getValue(Integer.class);
                    Integer grnstatus = dataSnapshot.child("Green").getValue(Integer.class);


                    textViewDistance.setText("Length of the Vehicle in Signal 1 :"+String.valueOf(Distance)+"CM");

                    if(redstatus==1)
                    {
                        status.setText("RED LIGHT ON");
                        img1.setBackgroundResource(R.drawable.red_circle);

                    }
                    if(yelstatus==1)
                    {
                        status.setText("YELLOW LIGHT ON");
                        img1.setBackgroundResource(R.drawable.yellow_circle);

                    }
                    if(grnstatus==1)
                    {
                        status.setText("Green LIGHT ON");
                        img1.setBackgroundResource(R.drawable.green_circle);
                    }



                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                // Handle database error
            }
        });
        sensorDataRef1.addValueEventListener(new ValueEventListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if (dataSnapshot.exists()) {
                    // Retrieve values from the dataSnapshot
                    Double Distance = dataSnapshot.child("Distance2").getValue(Double.class);
                    Integer redstatus1 = dataSnapshot.child("Red").getValue(Integer.class);
                    Integer yelstatus1 = dataSnapshot.child("Yellow").getValue(Integer.class);
                    Integer grnstatus1 = dataSnapshot.child("Green").getValue(Integer.class);


                    textViewDistance2.setText("Length of the Vehicle in Signal 2 :"+String.valueOf(Distance)+"CM");

                    if(redstatus1==1)
                    {
                        status1.setText("RED LIGHT ON");
                        img2.setBackgroundResource(R.drawable.red_circle);

                    }
                    if(yelstatus1==1)
                    {
                        status1.setText("YELLOW LIGHT ON");
                        img2.setBackgroundResource(R.drawable.yellow_circle);

                    }
                    if(grnstatus1==1)
                    {
                        status1.setText("Green LIGHT ON");
                        img2.setBackgroundResource(R.drawable.green_circle);
                    }



                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                // Handle database error
            }
        });
    }
}
