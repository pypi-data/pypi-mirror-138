## **NETRA**
A python based script which takes IPs as stdin and scans for open ports and vulnerabilities using [`shodan-internetdb`](https://internetdb.shodan.io/)

<br>

> **Note:** _I made it just to check if I implement [`https://gitlab.com/shodan-public/nrich`](https://gitlab.com/shodan-public/nrich) in python or not._

<br>

#### **InternetDB**
The InternetDB API provides a fast way to see the open ports for an IP address. It gives a quick, at-a-glance view of the type of device that is running behind an IP address to help you make decisions based on the open ports.

<br>

#### **Installation**
<br>

```bash
$ pip3 install snetra
```

#### **Usage**
<br>

```bash
$ cat ip.list | snetra
```

```bash
$ cat ip.list | snetra

TARGET: 149.202.182.140
PORTS: 21 80 111 443
HOSTNAMES: ftptech1.pcsoft.fr
CPES: cpe:/a:apache:http_server:2.4.25 cpe:/a:proftpd:proftpd:1.3.5b
TAGS: Not Found
VULNS: CVE-2017-9788 CVE-2018-11763 CVE-2019-0220 CVE-2019-0196 CVE-2019-12815 CVE-2017-3167 CVE-2017-15710 CVE-2017-9798 CVE-2018-17199 CVE-2017-7659 CVE-2017-3169 CVE-2019-0211 CVE-2017-15715 CVE-2019-0197 CVE-2018-1333 CVE-2017-7679 CVE-2018-1312 CVE-2017-7668 CVE-2018-1283
```

**Inspired from:** [`https://gitlab.com/shodan-public/nrich`](https://gitlab.com/shodan-public/nrich)


<br>

---