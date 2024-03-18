---
title: Dalfox Quickest Start
date: 2024-03-17T01:55:56-08:00
draft: false
tags:
  - xss
  - automation
---
Dalfox is a powerful open-source tool that helps automate scanning for cross-site scripting (XSS) security vulnerabilities on a website. If you do not know what XSS is, or how to perform it, [PortSwigger Academy](https://portswigger.net/web-security) is a fantastic resource for learning about web vulnerabilities in detail. It is entirely free and includes free labs to practice what you learn!

## Starting: Gathering Endpoints and URLs
Given that there is a website or domain that you want to target, there are a couple of different ways to enumerate the possible endpoints and parameters that you can inject into. 

The most straightforward way is to use a tool like [GoSpider](https://github.com/jaeles-project/gospider) to performing spidering of the target site. GoSpider will attempt to find all the links in a given webpage and recursively try to find more links on the resulting pages. It can also do some other cool thing such as brute forcing endpoints or even getting URLs/Parameters from other sources.
To crawl a site with GoSpider use:

```bash
gospider -s "https://domain.com" -o gospider.out
```

That brings me to the tools [GAU](https://github.com/lc/gau) and [waybackurls](https://github.com/tomnomnom/waybackurls) that can go to resources such as the Wayback Machine (Internet Archive) or other databases containing endpoints or parameters to enumerate them there. This helps discover endpoints that may have existed before or have been used and archived, but are no longer directly linked anywhere on the public site.
To run waybackurls:

```bash
echo domain.com | waybackurls
```

## Scanning for XSS with Dalfox
After collecting different URLs into a list, use Dalfox to find XSS issues. Optionally, use `-b` to include a Burp Suite interceptor address for blind XSS testing. 
```bash
dalfox -b [burp.interceptor.address] file xss-urls.txt
```

That's all! Good luck!

@M3nn1s

