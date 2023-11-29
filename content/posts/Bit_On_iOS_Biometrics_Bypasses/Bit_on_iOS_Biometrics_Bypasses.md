---
title: "Bit: iOS Biometrics Bypasses"
date: 2023-11-28T21:33:56-08:00
draft: false
tags: 
- mobile
- ios
- frida
---

## Introduction
So I was looking at biometric bypasses on iOS and found myself not understanding why certain applications/app logic could be bypassed with a simple Frida script while others were nothing but trouble.

##  Setup
{{<preview-link>}}
I did some reading. {{<preview-link "https://github.com/sensepost/objection/wiki/Understanding-the-iOS-Biometrics-Bypass" test>}} was super helpful, combined with some Googling and Bard/ChatGPT to help me figure out very basic Obj-C syntax.

Long story short, one function (the safer one) reaches out to an iOS API that handles keychain items and requests auth from the user. Once authenticated, a key is released to decrypt a particular keychain item (So all of those checks are handled outside the app and the app can do what it needs with the now decrypted keychain item).

The other function requests user auth, and based on whether the success boolean is true or false, application logic will execute. Since all of those callback blocks and the logic handling is in the app's context, it can be hooked and modified by Frida. 

I think. Tell me if I got something wildly wrong xD @M3nn1s for now.

also. Test image 
![Test123.png](/posts/Bit_On_iOS_Biometrics_Bypasses/Test123.png)

