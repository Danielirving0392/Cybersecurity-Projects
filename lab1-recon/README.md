# Footprinting, Reconnaissance, and Scanning

> CNS3005: Ethical Hacking | University of Technology, Jamaica
> Author: Daniel Irving (Student ID: 2005990)
> Lab 1

---

## Overview

This lab covers the foundational phase of any penetration test: information gathering. Before a single exploit is launched, a skilled attacker spends significant time understanding the target -- its infrastructure, exposed services, registered contacts, and publicly available data. This lab demonstrates both passive and active reconnaissance techniques using industry-standard tools available on Kali Linux and the web.

The lab is divided into four sections:

1. Passive Reconnaissance -- WHOIS, ICANN, Talos, and IP geolocation lookups on real domains
2. Active Reconnaissance -- Nmap scan types against local network targets
3. Google Dorking -- Using Google search operators to find sensitive exposed data
4. Website Footprinting -- theHarvester, Website Informer, Web Data Extractor, HTTrack, and CeWL

---

## Table of Contents

1. [Passive Reconnaissance](#1-passive-reconnaissance)
   - [Targets](#targets)
   - [WHOIS and Domain Lookup Tools](#whois-and-domain-lookup-tools)
   - [ICANN Lookup](#icann-lookup)
   - [Talos Intelligence Reputation Center](#talos-intelligence-reputation-center)
   - [IP Geolocation Verification](#ip-geolocation-verification)
2. [Active Reconnaissance with Nmap](#2-active-reconnaissance-with-nmap)
3. [Google Dorking (GHDB)](#3-google-dorking-ghdb)
4. [Website Footprinting](#4-website-footprinting)

---

## 1. Passive Reconnaissance

Passive reconnaissance involves gathering information about a target without directly interacting with its systems. All data is collected through publicly available sources -- WHOIS databases, DNS registries, IP reputation services, and geolocation providers. This phase leaves no trace on the target and is always the first step of any real-world engagement.

### Targets

The following domains were selected for passive information gathering:

| Domain | IP Address | Location | Contact | Phone |
|--------|-----------|----------|---------|-------|
| h4cker.org | 185.199.108.153 | San Francisco, California, USA | Omar Santos | +1.7204960020 |
| examcram.com | 168.146.67.181 | 200 Old Tappan Road, Old Tappan, New Jersey, USA | Pearson DataCert Engineers | +1.2017675000 |
| Rackspace Technology | 72.3.246.59 | Fanatical Place, Windcrest StatePro, TX USA | -- | +1-210-312-4000 |
| Rutgers.edu | 128.6.46.111 | Rutgers, The State University of New Jersey, Office of Information Technology, 96 Davidson Rd, NJ 08096, USA | -- | +1.8484457541 |
| secretcorp.org | 185.199.111.153 | -- | Omar Santos | -- |

---

### WHOIS and Domain Lookup Tools

WHOIS is a query and response protocol used to look up the registration records of domain names and IP addresses. It exposes registrant contact details, name servers, registration and expiry dates, and the registrar used. This data is valuable during reconnaissance because it identifies the people and organizations responsible for a target's infrastructure.

Tools used: whois.net, betterwhois.com, whois.domaintools.com

**h4cker.org and examcram.com -- WHOIS via domaintools:**

![WHOIS h4cker.org](screenshots/image36.png)
![WHOIS examcram.com](screenshots/image21.png)

**Additional domain lookups:**

![WHOIS lookup 3](screenshots/image66.png)
![WHOIS lookup 4](screenshots/image3.png)
![WHOIS lookup 5](screenshots/image47.png)
![WHOIS lookup 6](screenshots/image51.png)
![WHOIS lookup 7](screenshots/image57.png)
![WHOIS lookup 8](screenshots/image55.png)
![WHOIS lookup 9](screenshots/image6.png)
![WHOIS lookup 10](screenshots/image24.png)
![WHOIS lookup 11](screenshots/image61.png)

---

### ICANN Lookup

ICANN's lookup tool (https://lookup.icann.org) provides authoritative registration data directly from the domain registry. Unlike third-party WHOIS services, ICANN data is pulled from the source and includes registrar IANA ID, domain status codes, and RDAP compliance information.

![ICANN lookup 1](screenshots/image49.png)
![ICANN lookup 2](screenshots/image1.png)
![ICANN lookup 3](screenshots/image8.png)
![ICANN lookup 4](screenshots/image60.png)
![ICANN lookup 5](screenshots/image20.png)
![ICANN lookup 6](screenshots/image10.png)
![ICANN lookup 7](screenshots/image62.png)
![ICANN lookup 8](screenshots/image11.png)
![ICANN lookup 9](screenshots/image54.png)
![ICANN lookup 10](screenshots/image45.png)
![ICANN lookup 11](screenshots/image34.png)
![ICANN lookup 12](screenshots/image14.png)
![ICANN lookup 13](screenshots/image16.png)
![ICANN lookup 14](screenshots/image46.png)
![ICANN lookup 15](screenshots/image40.png)
![ICANN lookup 16](screenshots/image53.png)

---

### Talos Intelligence Reputation Center

Cisco Talos Intelligence (https://talosintelligence.com/reputation_center) provides threat intelligence and IP/domain reputation data sourced from Cisco's global sensor network. It is used during passive recon to determine whether a target IP has a known malicious history, what email volume it handles, and how it is categorized by threat intelligence feeds. This helps an attacker understand how monitored or hardened an organization is likely to be.

![Talos lookup 1](screenshots/image7.png)
![Talos lookup 2](screenshots/image19.png)
![Talos lookup 3](screenshots/image2.png)
![Talos lookup 4](screenshots/image38.png)
![Talos lookup 5](screenshots/image22.png)
![Talos lookup 6](screenshots/image59.png)

---

### IP Geolocation Verification

IP geolocation tools (https://ipinfo.io, https://www.maxmind.com) correlate an IP address to a physical location and organization. This is used to verify that the IP resolved from a domain actually belongs to the expected organization and is not pointing to a CDN, proxy, or cloud provider that would make direct scanning less useful.

**Commands used:**

```bash
ping h4cker.org
ping examcram.com
ping rackspace.com
ping rutgers.edu
ping secretcorp.org
```

![IPInfo geolocation 1](screenshots/image23.png)
![IPInfo geolocation 2](screenshots/image39.png)

---

## 2. Active Reconnaissance with Nmap

Active reconnaissance involves directly probing a target system. Unlike passive recon, this leaves evidence in network logs and may trigger intrusion detection systems. In a real engagement, active scanning is only performed after obtaining written authorization. In this lab, all scans were performed against local virtual machines within the test environment.

### Nmap Overview

Nmap (Network Mapper) is the most widely used tool for network discovery and security auditing. It supports dozens of scan types, each with different levels of visibility, speed, and protocol coverage.

**Reviewing available options:**

```bash
nmap -h
```

![nmap -h output](screenshots/image58.png)

---

### Scan Type Reference

| Scan Type | Flag | Description |
|-----------|------|-------------|
| Full Connect Scan | -sT | Completes the full TCP three-way handshake. Reliable but easily logged. |
| Stealth Scan | -sS | Sends SYN and does not complete the handshake. Less likely to appear in application logs. |
| UDP Scan | -sU | Probes UDP ports. Slower than TCP scans; important for discovering DNS, SNMP, and TFTP. |
| Fingerprint / OS Detection | -O | Analyzes TCP/IP stack responses to identify the operating system. |

**Full connect scan flag (-sT):**

![Full connect scan flag](screenshots/image29.png)

**Stealth scan flag (-sS):**

![Stealth scan flag](screenshots/image29.png)

**UDP scan flag (-sU):**

![UDP scan flag](screenshots/image30.png)

**Fingerprint scan flag (-O):**

![Fingerprint scan flag](screenshots/image27.png)

---

### Step 1 -- Full Connect Scan

```bash
nmap -sT <IP_Address>
```

![Full connect scan result](screenshots/image25.png)

The full connect scan completed the TCP three-way handshake on every probed port. All open ports were confirmed and the results were logged by the target system's connection table. This scan type is the most reliable for identifying open ports but is the most detectable.

---

### Step 2 -- Stealth Scan

```bash
nmap -sS <IP_Address>
```

![Stealth scan result](screenshots/image41.png)

The SYN scan (stealth scan) sent SYN packets and recorded responses without completing the handshake. Open ports responded with SYN-ACK; closed ports responded with RST. Because the connection was never fully established, this scan does not appear in most application-level logs, making it preferred for low-profile reconnaissance.

---

### Step 3 -- UDP Scan

```bash
nmap -sU <IP_Address>
```

![UDP scan result](screenshots/image33.png)

The UDP scan probed UDP ports on the target. UDP scanning is inherently slower than TCP because closed UDP ports respond with ICMP port-unreachable messages, which are often rate-limited by the OS. Open UDP ports frequently produce no response, requiring Nmap to infer their state. Services discovered through UDP scanning commonly include DNS (53), SNMP (161), and DHCP (67/68).

---

### Step 4 -- OS Fingerprint Scan

```bash
nmap -O <IP_Address>
```

![OS fingerprint scan result](screenshots/image35.png)

The OS fingerprint scan analyzed characteristics of the target's TCP/IP stack responses -- including TTL values, TCP window sizes, and IP options -- to identify the operating system. Nmap successfully identified the target system. OS detection is useful for tailoring exploits to the specific platform and version running on the target.

**Observation:** Nmap successfully identified the target operating system across all four scan types. The open ports returned were consistent with the services known to be running on the test machine, confirming the accuracy of each scan method.

---

## 3. Google Dorking (GHDB)

Google Dorking refers to using advanced Google search operators to surface information that is indexed by search engines but not intentionally exposed by the target organization. The Google Hacking Database (GHDB) at https://www.exploit-db.com/google-hacking-database maintains a curated list of tested dork queries organized by category.

### Common Search Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| site: | Restrict results to a domain | site:example.com |
| intitle: | Search within page titles | intitle:"index of" |
| filetype: | Search for specific file types | filetype:pdf |
| inurl: | Search within URLs | inurl:admin |
| "" (quotes) | Exact phrase match | "password" |
| - (minus) | Exclude terms | site:example.com -www |

---

### Exercise 1 -- Excel File Containing Usernames and Passwords

```
filetype:xlsx "username" "password"
```

![GHDB excel dork query](screenshots/image31.png)
![GHDB excel dork results](screenshots/image50.png)

Searching for Excel files containing credential-related keywords surfaced publicly indexed spreadsheets with username and password columns. These files are typically the result of misconfigured cloud storage, publicly shared Google Drive documents, or web servers with directory listing enabled.

---

### Exercise 2 -- Ethical Hacking Video on Google Drive

```
site:drive.google.com "ethical hacking"
```

This query targets Google Drive public shares indexable by Google Search. Content owners who set sharing to "Anyone with the link" without understanding that Google can index the file effectively make it publicly searchable.

---

### Exercise 3 -- IP Cameras with DVR

```
intitle:"DVR WebClient" OR inurl:"/view/viewer_index.shtml"
```

![GHDB IP camera dork query](screenshots/image43.png)
![GHDB IP camera results](screenshots/image18.png)

This dork exposed internet-facing DVR and IP camera management interfaces. Many are accessible without authentication due to default or blank credentials. This is one of the most well-known categories in the GHDB and illustrates how IoT devices with web interfaces are routinely left exposed.

---

### Exercise 4 -- Exposed Email Lists

```
filetype:txt "email" "list" site:.com
```

![GHDB email list dork query](screenshots/image9.png)
![GHDB email list results](screenshots/image52.png)

Exposed email list files indexed by Google can feed spam campaigns or targeted phishing attacks. The files surfaced through this dork include plain-text email dumps left on public web servers or in unprotected cloud buckets.

---

### Exercise 5 -- Exposed Directories

```
intitle:"index of" "parent directory"
```

![GHDB exposed directory dork query](screenshots/image64.png)
![GHDB exposed directory results](screenshots/image12.png)

Directory listing is enabled by default in older web server configurations. When Apache or Nginx serves a directory without an index.html file and directory listing is on, the entire contents of the folder are browsable. This dork finds those openly listed directories, which may contain configuration files, backups, source code, or credentials.

---

### Exercise 6 -- Exposed Database Files

```
filetype:sql "INSERT INTO" "password"
```

![GHDB database dork query](screenshots/image63.png)
![GHDB database dork results](screenshots/image13.png)

SQL dump files containing INSERT statements with plaintext or hashed passwords are occasionally uploaded to public repositories or web servers during migrations and left unprotected. This dork surfaces them directly from Google's index.

---

## 4. Website Footprinting

Website footprinting involves collecting detailed information about a target organization's web presence using a combination of active queries and passive analysis tools. The goal is to map the organization's digital footprint, understand its infrastructure, and identify entry points for further testing.

---

### Ping -- Basic Host Discovery and Latency

```bash
ping h4cker.org
```

![Ping output](screenshots/image68.png)

The ping command was used to resolve the target domain to its IP address and confirm the host was reachable. TTL values in the ping response can also hint at the operating system of the responding host (Linux systems typically return TTL 64; Windows systems return TTL 128).

---

### Website Informer -- Passive Web Intelligence

Website Informer aggregates publicly available data about a domain including hosting provider, IP neighborhood, DNS records, similar sites, and traffic estimates. It is a passive tool that provides a broad intelligence overview without sending any probes to the target.

![Website Informer result 1](screenshots/image5.png)
![Website Informer result 2](screenshots/image32.png)

---

### Web Data Extractor -- Structured Data Harvesting

Web Data Extractor crawls a target website and extracts structured data including email addresses, phone numbers, meta tags, URLs, and contact information. This automates what would otherwise be a time-consuming manual review of the site's HTML source code.

![Web Data Extractor result 1](screenshots/image65.png)
![Web Data Extractor result 2](screenshots/image15.png)
![Web Data Extractor result 3](screenshots/image42.png)

---

### HTTrack -- Website Mirroring

HTTrack Website Copier downloads a full local copy of a target website including all linked pages, images, scripts, and stylesheets. Having a local mirror allows an analyst to:

- Review the site's source code offline without generating further traffic
- Identify comments, hidden form fields, and internal path references in HTML
- Analyse JavaScript files for API endpoints or authentication logic

```bash
httrack "https://target.com" -O "/home/kali/mirror" "+*.target.com/*" -v
```

![HTTrack run 1](screenshots/image44.png)
![HTTrack run 2](screenshots/image17.png)
![HTTrack run 3](screenshots/image4.png)
![HTTrack run 4](screenshots/image67.png)

---

### CeWL -- Custom Wordlist Generation

CeWL (Custom Word List Generator) spiders a target website and builds a wordlist from the words found on the pages. The resulting wordlist is tailored to the vocabulary of the specific organization and is significantly more effective for password cracking against that target than a generic wordlist like rockyou.txt, because organizations tend to use company names, product names, and internal terminology in passwords.

```bash
cewl https://target.com -m 5 -w wordlist.txt
```

The `-m 5` flag sets the minimum word length to 5 characters, filtering out short common words.

![CeWL command](screenshots/image28.png)
![CeWL wordlist output](screenshots/image69.png)

---

## Key Takeaways

Passive reconnaissance alone surfaced registrant contact details, physical addresses, name servers, IP ranges, and threat reputation data for every target -- without sending a single packet to the target systems. When combined with active Nmap scanning, Google dorking, and website footprinting tools, an attacker has a comprehensive picture of the target's infrastructure before any exploitation begins.

The most actionable defensive lesson from this lab is that organizations have limited control over what passive sources reveal. WHOIS privacy services, careful management of public cloud storage permissions, and regular audits of what Google has indexed about your domain are among the few controls available.

---

## Disclaimer

This lab was performed in a controlled academic environment as part of CNS3005: Ethical Hacking at the University of Technology, Jamaica. All active scans were conducted against virtual machines within an isolated test network. All passive lookups were performed on publicly available information. The Google dorking exercises were conducted for educational purposes only. The techniques documented here must not be applied against any system or organization without explicit written authorization.

---

*University of Technology, Jamaica -- Faculty of Computing and Engineering*
*School of Computing and Information Technology*
