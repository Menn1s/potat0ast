---
title: Golden And Silver Tickets
date: 2024-03-17T02:55:56-08:00
draft: false
tags:
  - windows
---
As a quick introduction, the concept behind Golden and Silver tickets (in the context of Kerberos and penetration testing) resurfaced when I was asked by a friend a couple weeks ago. I found that I either didn't have much of an answer or was stumbling to provide one. The following post hopefully explains some of it at a high level. I am hoping to bridge the gap between the very high level explanations I often see, and the very technical breakdowns that come from the amazing tool devs themselves.

For anyone not familiar with the terms Kerberos or penetration testing, both are terms that can be easily googled but I will summarize them here briefly. Kerberos is a network authentication protocol, and penetration testing is the practice of trying to hack into a system so that issues can be discovered proactively (this is in contrast to doing your best to plug all the security holes, only to find you missed something and an actual attacker/hacker has stolen all of the company's data).

## Silver Tickets
If you've made it this far, then you either know quite a bit about cyber security or you are quite curious at the very least. For a great explanation on Kerberos, see this great Computerphile video: https://www.youtube.com/watch?v=qW361k3-BtU.

1. Given the context of how tickets work in Kerberos, a user would normally have to use their user credentials (username and password) to request a TGT or a ticket granting ticket from the key distribution center's (KDC) authentication service. Remember, authentication is essentially making sure you are who you say you are.

2. This TGT that proves you are a certain user can then be used to request access to a service from the ticket granting server (TGS). The resulting ticket you get in response is called the service ticket, assuming you have permissions to the service you are requesting. This service ticket is authorization, where you are given permission based on the policies Kerberos can check (does this user have access to the service they are requesting?).

3. This  can then be used with the service to which you want access.

Here is a hyper-simplified diagram for the steps of Kerberos to authenticate to a service:

 ![kerberosAuth.png](/posts/Golden_And_Silver_Tickets/kerberosAuth.png)
_Super simplified Kerberos Authentication_

When communicating with the TGS, the service ticket that is given to the user is normally encrypted with the target service's credentials. This helps provide a variety of security benefits, but we are most concerned with two things:
1. Prevents the user from modifying the service ticket since only the TGS and the target service can decrypt the service ticket.
2. Proves that the user was authenticated by the Authentication Server and authorized by the TGS.

A Silver Ticket is a forged service ticket using the credentials of the service to sign the ticket, allowing an attacker to modify the service ticket and get access without proving they are who they say they are to the Authorization Server.

TL;DR, a Silver Ticket let's you claim to be anybody to a particular service. What you need to start forging Silver Tickets is just one thing:
1. The credentials for the service account

### Obtaining Service Account Credentials

So what are the common ways that these accounts can be compromised? The first way is through [Kerberoasting](https://posts.specterops.io/kerberoasting-revisited-d434351bd4d1), then attempting to crack the TGS (a portion of it anyway) for the service account's plaintext credentials.

Since the symmetric key (hash of the account) is derived from the plaintext of the service account's credentials (if none of that sentence made sense, do a quick google search for hashing or hash functions), an attacker with an encrypted service ticket could attempt to crack it offline. Cracking, in this case, is basically running through a decrypting algorithm repeatedly with a massive list of hashes (or plaintext credentials that are then converted to hashes before being fed into the decryption algorithm). The only limitation on this process is a computer's speed, hence password cracking rigs may be used for this to speed up the process.

Once one of the plaintext credentials or hashes manages to decrypt the service ticket, that means the attacker could use that password to create a Silver Ticket.

Another way to get credentials to start forging Silver Tickets is by harvesting them from the system on which the service is running itself. If local administrative credentials are recovered for the system or another method for executing code as System are found, an attacker could steal the NTLM hash from the Security Accounts Manager (SAM) on the system.

Finally, these credentials can also be recovered through phishing or poor storage of credentials. Sometimes these credentials can be recovered from places like SMB shares or Group Policy descriptions, custom fields, etc.

## Golden Ticket
So to summarize from a high level, the silver ticket is used to bypass the Ticket Granting Server in the KDC. By doing this, we can forge a ticket with any user for the service we have credentials for (For example, if you steal credentials for a SQL server, you can access it as Bob, Alice, or SQLAdmin if you wanted).

The Golden Ticket is when we have the NTLM hash for the Active Directory Key Distribution Service Account (KRBTGT). With this hash, you can start to mint TGTs (as compared to forging service tickets).

This lets you bypass the authentication server, essentially creating TGTs for any user. With the TGT for the domain administrator, you would have full control over the domain and any of its resources.

## Summary
So there you have it; two different ways to attack Kerberos by stealing credentials for either a specific service, or for the service that provides authentication itself.

I don't plan on doing a full technical dive into this since there is already amazing content on that, but let me know if anything is wrong or could use some clarification!

@M3nn1s
