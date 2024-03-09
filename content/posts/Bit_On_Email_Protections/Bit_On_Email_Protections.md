---
title: Bit on Email Protections
date: 2024-03-09T21:55:56-08:00
draft: false
tags:
  - email
---


**SPF** - Record of IPs for a certain domain. 
1. Email is sent by sender. 
2. Receiver looks up the domain with DNS. Finds SPF record. Sees if the IP of the sender is a part of the record. 
3. If not, is evil. 

**DKIM** - Uses public keys to verify email hasn't been tampered. 
1. Sender signs a message with their private key (usually signing headers or the entire email body and headers). 
2. When the email client receives the message, it can look up the DKIM record with the public key and decrypt/verify the signed portions. 
3. From there, it can compare that to the plaintext.
4. If no match, is evil.

**DMARC** - Combo of the 2 above. Configured depending on how the domain administrator wants the email verified and whether they want information about the pass/fail of emails being sent.