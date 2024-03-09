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
I did some reading.  [Understanding iOS biometric bypass](https://github.com/sensepost/objection/wiki/Understanding-the-iOS-Biometrics-Bypass) was super helpful, combined with some Googling and Bard/ChatGPT to help me figure out very basic Obj-C syntax.

Long story short, one function (the safer one) reaches out to an iOS API that handles keychain items and requests auth from the user. Once authenticated, a key is released to decrypt a particular keychain item (So all of those checks are handled outside the app and the app can do what it needs with the now decrypted keychain item).

The other function requests user auth, and based on whether the success boolean is true or false, application logic will execute. Since all of those callback blocks and the logic handling is in the app's context, it can be hooked and modified by Frida. 

I think. Tell me if I got something wildly wrong xD @M3nn1s for now.

So continued; I did some reading and the application I was working with essentially was only using the iOS biometrics functionality to return a boolean that would be used for further application logic.

The first step to fixing this issue would be to actually store the tokens into the iOS keychain. Once it is there, it can be additionally protected by several access control flags to prevent access when the fingerprint has not been authenticated (something that cannot be modified from user or application level privileges). These flags include `kSecAccessControlBiometryCurrentSet` (ensures information can only be retrieved after entering valid biometric information), `kSecAccessControlBiometryAny` (similar to before, but can also work with new biometrics), and `kSecAccessControlUserPresence` (allows either passcode or biometric authentication to access the information).


Test Image
![testImg213.png](/posts/Bit_On_iOS_Biometrics_Bypasses/testImg213.png)
