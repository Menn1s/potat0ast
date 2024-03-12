---
title: "Bit: Android Biometrics Bypass"
date: 2024-03-12T09:55:56-08:00
draft: false
tags:
  - mobile
  - android
---

This was performed around the same time as my reading into iOS biometric bypasses, but I just never really got a chance to dig into it. See {{<preview-link "/2023/11/28/bit_on_ios_biometrics_bypasses/" iOSBiometricBypasses>}} for some context.

Similar to iOS, Android provides a secure way to store data on the device. iOS uses the iOS keychain to securely store data such as keys, passwords, or anything else that is considered sensitive and needs to be stored on the device.

Please note the part about "needs to be stored". Unless offline computing needs to be done, or the application is meant to be used offline, there should not be sensitive data stored on the device. This should, in general, remain on the server side and the application memory while the application runs.

On Android, there is the Keystore. What is interesting about this, is that it provides very similar functionality to the iOS keychain, albeit with a key difference: The iOS keychain may contain a broad set of different types of sensitive data. The Keystore, on the other hand, does exactly what its name suggests. It stores keys which are released when the user authenticates, and those can then be used to decrypt data that could be stored within application directories.

The protection provided, however, is similar. Since the logic for authenticating the user's biometrics are not done by application code, they cannot be hooked by Frida. It is simply a question of whether a key comes back from the keystore or not. 

The issue exists when the API is used to check authorization status (rather than just retrieve the key), then to return a boolean value representing that status to be used by the application. Once the boolean is returned, it is used by the application for further logic (and at this point it exists in application space that Frida can hook into). Frida can than be used to modify the boolean while the app runs, so even if the OS returns that the user authentication failed, the value that is used by the application for other logic can be modified.

## Recommendations
Make sure sensitive data is protected with keys stored in the Android Keystore and make sure that the keys can only be retrieved with valid biometric information using `setUserAuthenticationRequired` and `setInvalidatedByBiometricEnrollment` to make sure that new biometrics will invalidate the keys (requiring re authentication to the application for new keys).

I will try to update this with more practical details, but that's the high-level for now!

