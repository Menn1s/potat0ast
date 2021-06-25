---
title: "T-Beam Alarm Clock (with NTP!)"
date: 2021-05-24T21:33:56-08:00
draft: false
tags: 
- wifi
- arduino
- t-beam
- esp32
---

## Introduction
SKIP if you just want the *How to*.
Microcontrollers can be fairly difficult to get into. For the most part, if I had any project, I would head straight for github and grab either some code to push through the Arduino IDE or something that could be flashed (with some more magical GUI software). 
Then, my friend shared with me a project called (Meshtastic)[https://meshtastic.org/] where, using a combination of LORA 915Mhz communication and GPS, you could have an open source device that would let you keep in touch with your party in the great outdoors (without wifi, LTE, or any other more stationary networking resource). I was amazed by what it could do, and I saw that there was just more software to be flashed. So I put in an order for two TTGO T-Beams and waited for them to come in from overseas. 
Finally they arrived... but I ordered the wrong ones with no OLED screens. I could probably work with them without the screens, but I was there for an easy ride. So I ordered another 2 (at this point I'm pushing a hundred bucks for some side project I don't know will even work).
Those show up, I flash them and..... GPS does not connect. Needless to say, I did a bit of Googling but couldn't find much, so they started to sit there.
Anyway, I needed an alarm because I didn't want an excuse to keep my phone near my bed (since it is the current alarm in use). That thing is an adult pacifier and probably the most appealing thing next to staring at the ceiling. So instead of buying 
![19319ca1ecebdab7b1d394774de2f5dc.png](/posts/T-Beam_Alarm_Clock/19319ca1ecebdab7b1d394774de2f5dc.png)

I opted to at least make some use of the hundred dollars spent (wasted).

##  Setup
So here are some prerequisites we will need before starting:
- Drivers
    - https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers for Windows and Mac. From Silabs. Guess we just have to trust it and click next on the install prompts very quickly so the viruses can't multiply.
    - If you're running Linux, I imagine you already know what to do
- Arduino IDE https://www.arduino.cc/en/software
- VS Code (not required but it's nice to have) 
- Arduino Libraries 
    - ESP8266 and ESP32 OLED driver for SSD1306 displays (yeah it's a mouthful). This gets the little screen to work.
    - WiFi for the esp32 should be built in
    - NTPClient (so time isn't completely off)

First download the driver and install it so your usb port can communicate with the UART channels on your board.
![Screenshot_of_Install_CP210x_VCP_Driver.png](/posts/T-Beam_Alarm_Clock/Screenshot_of_Install_CP210x_VCP_Driver.png)
Unzip the downloaded file, double click on the dmg, double click on the driver installation app, and follow the on-screen prompts to install it.

Once that is installed, also install the Arduino IDE if you haven't already. Then open it up and you should be greeted with something like this
![adc139963d398d86b12ac76d9fe7f7c8.png](/posts/T-Beam_Alarm_Clock/adc139963d398d86b12ac76d9fe7f7c8.png)
If you've never used an Arduino board before, this is just some template code for the board. Anything in the {} after setup() will be run only once. Anything in between the {} after loop() will be run repeatedly... like in a loop.

In order to get the code onto the T-beam board, we will need to add the particular board type into our Arduino installation. To do this, first head to the preferences or settings for the IDE and look for the field called "Additional Boards Manager URLs".
![Screenshot_of_Arduino.png](/posts/T-Beam_Alarm_Clock/Screenshot_of_Arduino.png)
Add the following URL: https://dl.espressif.com/dl/package_esp32_index.json and open the Boards Manager.

![Screenshot_of_Arduino.png](/posts/T-Beam_Alarm_Clock/Screenshot_of_Arduino.png)
Search for the esp32 (by Espressif Systems) and install it.
![Screenshot_of_Arduino.png](/posts/T-Beam_Alarm_Clock/Screenshot_of_Arduino.png)
Go back to Tools -> Board -> ESP32 and select the T-Beam.
Now, we have essentially configured everything we need to begin communicating with the T-Beam. You can plug in your T-Beam and begin coding and flashing code to your board. However, for more advanced functionality, it is likely that you would install libraries so you don't need to learn how to write code to communicate with a specific OLED screen or how to communicate with a networking chip. 

![Screenshot_of_Arduino.png](/posts/T-Beam_Alarm_Clock/Screenshot_of_Arduino.png)
Under the Sketch tab, go to "Include Library" and select "Manage Libraries..."
The first library we will install is Timelib so that managing time is easier. 
![3a9daaf1dbea6e8f5d5be8410e41aab8.png](/posts/T-Beam_Alarm_Clock/3a9daaf1dbea6e8f5d5be8410e41aab8.png)
Go to the search bar and search "time" or "timelib" until you find the library shown above. The install button will be in the bottom right if you haven't already installed the library. Proceed to install all of the following libraries as well:
- esp8266 and esp32 OLED driver for ssd1306 displays: It's a pretty self explanatory library name, but it basically makes it easier to use the small displays that are used on arduino boards. For example, you can print text to the screen or draw shapes to the screen.
- NTPClient: Contains the code that allows the board to communicate using the network time protocol and get accurate, current time/date.
- WiFi: Contains code to communicate with common WiFi protocols. Should be installed by default.

That is all for the libraries we'll be needing. Now here is the code. I will try to comment everything as clearly as possible. Otherwise it should just work once you change the wifi details to suit your access point.

```cpp
#include "SSD1306Wire.h"
#include <WiFi.h>
#include <NTPClient.h>
#include <TimeLib.h>
#include "pitches.h" // see pitches.h file below. It is another file in the same project


// set wifi variables
const char* ssid     = "SSID";
const char* password = "PASSWORD";

// set the display
SSD1306Wire display(0x3c, SDA, SCL); 

// Define NTP client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

// Variables to save date and time
String formattedDate;
String dayStamp;
String timeStamp;

// connect to WiFi function
void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  // set wifi to station mode (client mode)
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  int attempt = 0;
  // while loop that adds a dot for each second that the status is not connected yet
  while(WiFi.status() != WL_CONNECTED){
    Serial.print("."); // print a dot to serial
    display.drawString(attempt, 0, "."); // draw a dot next to the last one.
    display.display(); // refresh the display so what was drawn actually shows
    attempt++; // increase the attempt counter (acts as x axis for dots being printed)
    delay(1000);
  }
}

// utility function for digital clock display: prints leading 0
String twoDigits(int digits){
  if(digits < 10) {
    String i = '0'+String(digits);
    return i;
  }
  else {
    return String(digits);
  }
}


// plays a tone from a particular pin for a set amount of time
void tone(byte pin, int freq, int length) {
  ledcSetup(0, 2000, 8); // setup beeper
  ledcAttachPin(pin, 0); // attach beeper
  ledcWriteTone(0, freq); // play tone

  delay(length); // play for as long as specified
  ledcWriteTone(0, 0); // then turn off
}

void playMelody() {
  // notes in the melody:
  int melody[] = {
    NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
  };

  // note durations: 4 = quarter note, 8 = eighth note, etc.:
  int noteDurations[] = {
    4, 8, 8, 4, 4, 4, 4, 4
  };
  // loop to play the melody specified
  for (int thisNote = 0; thisNote < sizeof(melody)/sizeof(melody[0]); thisNote++) {
    tone(14, melody[thisNote], 1000/noteDurations[thisNote]);
  }
}

void setup() {
  // set the baud rate and print newlines to serial
  Serial.begin(9600);
  Serial.println();
  Serial.println();
  
  // initialize the display and set font
  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  
  connectToWiFi();

  // set pin 14 for output
  pinMode(14, OUTPUT);
    
  playMelody();

  display.drawString(0, 0, "hello");
  display.display();
  delay(3000);

  display.clear();

  // show the mac address in serial and on the screen
  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());
  display.drawString(0, 10, "ESP Board MAC Address: ");
  display.drawString(0, 20, WiFi.macAddress());
  display.display();

  // show the IP address on screen
  display.drawString(0, 40, "ESP Board IP Address: ");
  display.drawString(0, 50, WiFi.localIP().toString());
  display.display();

  // start the time client and set timezone GMT -8
  timeClient.begin();
  timeClient.setTimeOffset(-25200); delay(5000);

  // get the datetime
  while(!timeClient.update()) {
    timeClient.forceUpdate();
  }

  // Extract Date and Time
  formattedDate = timeClient.getFormattedTime();
  int epochTime = timeClient.getEpochTime();
  setTime(epochTime);
  Serial.println(formattedDate);

  // Extract date
  int splitT = formattedDate.indexOf("T");
  dayStamp = formattedDate.substring(0,splitT);

  display.drawString(0, 0, "TIME: " + dayStamp);
  display.display();

  // save some power
  WiFi.mode(WIFI_OFF);

}

void loop() {
  // clear the screen and update the time  
  display.clear();
  display.setFont(ArialMT_Plain_16);
  display.drawString(0,0, String(hour()) + ":" + twoDigits(minute()) + ":" + twoDigits(second()));
  display.display();

  // The alarm. This is for 6:25 am. 1430 for 2:30 pm
  if (String(hour()) + String(minute()) == "625") {
    playMelody();
  }
  // update the time every so often. In milliseconds
  delay(1000);

}
```

```cpp
// contains note definitions so you don't need to know specific frequencies. Just a bit of music theory
#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978
```
