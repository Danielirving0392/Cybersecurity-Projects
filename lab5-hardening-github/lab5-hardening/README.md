# Windows 10 System Hardening

> CNS3003: Security Testing and Detection | University of Technology, Jamaica
> Author: Daniel Irving (Student ID: 2005990)
> Lab 5

---

## Overview

This lab documents the systematic hardening of a Windows 10 workstation using built-in Windows security controls. System hardening is the process of reducing a machine's attack surface by eliminating unnecessary access, enforcing strong authentication policies, enabling audit logging, and activating protective features of the operating system.

The hardening process follows a structured sequence aligned with real-world baseline frameworks such as CIS Benchmarks for Windows 10 and NIST SP 800-123 (Guide to General Server Security). Each step is documented with the specific configuration applied and a screenshot confirming the change.

The lab covers six major hardening areas:

1. Password and account lockout policy (Local Security Policy)
2. Audit policy configuration and verification
3. User rights assignment
4. Security options -- account and logon settings
5. Windows Defender -- threat protection, malware scanning, ransomware protection, and core isolation
6. Firewall verification, application management, and UAC

---

## Table of Contents

1. [Password Policy Configuration](#1-password-policy-configuration)
2. [Account Lockout Policy](#2-account-lockout-policy)
3. [Audit Policy](#3-audit-policy)
4. [User Rights Assignment](#4-user-rights-assignment)
5. [Security Options -- Account Settings](#5-security-options----account-settings)
6. [Security Options -- Interactive Logon Settings](#6-security-options----interactive-logon-settings)
7. [Login Changes Verification](#7-login-changes-verification)
8. [Windows Defender -- Virus and Threat Protection](#8-windows-defender----virus-and-threat-protection)
9. [Windows Defender -- Ransomware Protection and Core Isolation](#9-windows-defender----ransomware-protection-and-core-isolation)
10. [Reputation-Based Protection](#10-reputation-based-protection)
11. [Firewall Verification](#11-firewall-verification)
12. [Disable Unused Applications](#12-disable-unused-applications)
13. [User Account Control (UAC)](#13-user-account-control-uac)

---

## 1. Password Policy Configuration

Password policy controls the strength and lifecycle requirements for all local account passwords. These settings are configured through Local Security Policy under `Security Settings > Account Policies > Password Policy`.

**Step 1 -- Baseline check: view current password policy via command line**

Before making changes, the existing policy was documented using `net accounts` to establish a baseline for comparison.

```cmd
net accounts
```

![net accounts baseline output](screenshots/image27.png)

The default Windows 10 configuration shows minimal password requirements, which is insufficient for a hardened workstation.

---

**Setting 1 -- Enforce password history**

Set to: 24 passwords remembered

Preventing password reuse stops users from cycling back to old credentials. A history of 24 is the CIS Benchmark Level 1 recommendation and ensures a user cannot rotate through a short list of familiar passwords.

![Enforce password history -- 24](screenshots/image21.png)

---

**Setting 2 -- Maximum password age**

Set to: 60 days

Forcing periodic password changes limits the window in which a compromised credential remains valid. 60 days balances security with usability.

![Maximum password age -- 60 days](screenshots/image15.png)

---

**Setting 3 -- Minimum password age**

Set to: 1 day (prevents immediate cycling to bypass history policy)

Without a minimum age, a user can change their password 24 times in rapid succession to return to their original password and bypass the history requirement entirely.

![Minimum password age](screenshots/image32.png)

---

**Settings 4 and 5 -- Minimum password length and complexity**

Minimum length set to: 14 characters
Complexity requirements: Enabled

Complexity enforcement requires passwords to contain characters from at least three of the following categories: uppercase letters, lowercase letters, digits, and symbols. Combined with a 14-character minimum, this significantly raises the cost of brute-force and dictionary attacks.

![Minimum length and complexity settings](screenshots/image17.png)

---

**Setting 6 -- Store passwords using reversible encryption**

Set to: Disabled

Reversible encryption is essentially plaintext storage. It exists only for legacy protocol compatibility and should always be disabled unless a specific application explicitly requires it. Disabling it ensures password hashes cannot be trivially reversed.

![Reversible encryption -- disabled](screenshots/image26.png)

---

## 2. Account Lockout Policy

Account lockout policy is configured under `Security Settings > Account Policies > Account Lockout Policy`. It prevents brute-force attacks by temporarily locking an account after a defined number of failed attempts.

**Settings applied:**

| Setting | Value | Rationale |
|---------|-------|-----------|
| Account Lockout Threshold | 10 invalid logon attempts | Blocks automated brute-force while allowing for genuine user mistakes |
| Account Lockout Duration | 15 minutes | Temporary lockout -- avoids permanent denial of service to legitimate users |
| Reset Account Lockout Counter After | 15 minutes | Resets the failed attempt counter after 15 minutes of inactivity |

![Account lockout policy settings](screenshots/image28.png)

With these settings active, an attacker attempting a brute-force attack would be locked out after 10 attempts. At 10 attempts per 15-minute window, testing a password list of 10,000 entries would take over 10 days -- far exceeding practical attack timelines for a local account.

---

## 3. Audit Policy

Audit policy enables Windows to write Security Event Log entries when specific actions occur. Without audit logging, there is no forensic trail -- attacks, privilege escalations, and policy changes go completely unrecorded.

All nine audit categories were enabled for both **Success** and **Failure** events:

- Audit account logon events
- Audit account management
- Audit directory service access
- Audit logon events
- Audit object access
- Audit policy change
- Audit privilege use
- Audit process tracking
- Audit system events

Auditing both success and failure is important: failed events reveal attack attempts; successful events reveal what an attacker actually accomplished.

![Audit policy settings configured](screenshots/image12.png)

**Testing the audit policy -- PowerShell process creation:**

A new PowerShell window was opened to generate a process creation event, then the Security event log was checked to confirm the audit policy was recording events correctly.

```powershell
# Open PowerShell -- this generates a process creation event under the audit policy
```

![PowerShell window opened for audit test](screenshots/image24.png)

Navigate to: `Event Viewer > Windows Logs > Security`

![Security event log showing process creation events](screenshots/image11.png)

![Process creation event confirming audit is active](screenshots/image38.png)

The Security log showed a Process Creation event corresponding to the PowerShell instance that was opened, confirming that the audit policy is actively logging events to the Security channel.

---

## 4. User Rights Assignment

User rights assignment controls which accounts and groups can perform specific privileged actions on the machine. These settings are found under `Local Policies > User Rights Assignment`.

**Setting 1 -- Access this computer from the network**

Action: Remove all users and groups listed

This right controls which accounts can connect to the machine over the network (e.g., via file shares or remote registry). Removing all entries prevents unauthenticated and authenticated remote access to local resources over SMB and similar protocols.

![Access from network -- all users removed](screenshots/image14.png)

---

**Setting 2 -- Allow log on locally**

Action: Remove the Guest account

The Guest account has no password by default. Removing it from the local logon right prevents an attacker with physical access from logging in as Guest and gaining a foothold on the machine.

![Allow log on locally -- Guest removed](screenshots/image5.png)

---

**Setting 3 -- Allow log on through Remote Desktop Services**

Action: Remove all users and groups listed

Unless remote desktop access is operationally required, removing all accounts from this right eliminates the RDP attack surface entirely. RDP is one of the most actively targeted services on internet-facing Windows machines.

![RDP logon right -- all users removed](screenshots/image6.png)

---

## 5. Security Options -- Account Settings

Security options are found under `Local Policies > Security Options`. These settings control a range of system-level behaviors.

**Setting 1 -- Rename the administrator account**

The built-in Administrator account is a high-value target because its name is universally known. Renaming it means an attacker must first discover the new name before attempting to authenticate, adding a layer of obscurity.

![Administrator account renamed](screenshots/image8.png)

---

**Setting 2 -- Rename the guest account**

The same principle applies to the Guest account. Renaming it removes the predictable target name from the attack surface.

![Guest account renamed](screenshots/image19.png)

---

## 6. Security Options -- Interactive Logon Settings

Interactive logon settings control what information is displayed at the Windows login screen and how user sessions are managed.

**Setting 1 -- Do not display user information when the session is locked**

Select: Do not display user information

Hiding the username on the lock screen prevents an attacker who gains physical access to a locked machine from immediately knowing which account is active.

![Lock screen user info -- do not display](screenshots/image30.png)

---

**Setting 2 -- Do not require CTRL+ALT+DEL**

Set to: Disabled (meaning CTRL+ALT+DEL will be required)

Requiring CTRL+ALT+DEL before login ensures the logon screen is invoked by the trusted Windows kernel path, not by a spoofed logon screen. This is a protection against credential-harvesting malware that mimics the Windows login UI.

![CTRL+ALT+DEL required -- enabled](screenshots/image31.png)

---

**Setting 3 -- Do not display last signed-in username**

Set to: Enabled

Hiding the last signed-in username prevents an attacker from learning a valid account name from the login screen.

![Do not display last signed-in -- enabled](screenshots/image25.png)

---

**Setting 4 -- Do not display username at sign-in**

Set to: Enabled

This prevents the username from appearing in the login UI even during active entry, providing an additional layer of information hiding at the logon interface.

![Do not display username at sign-in -- enabled](screenshots/image25.png)

---

**Setting 5 -- Machine inactivity limit**

Set to: 900 seconds (15 minutes)

Automatically locks the workstation after 15 minutes of inactivity, reducing the risk of an unattended logged-in session being exploited by someone with physical access.

![Machine inactivity limit -- 900 seconds](screenshots/image18.png)

---

**Setting 9 -- Message text for users attempting to log on**

A custom legal notice message was entered to warn unauthorized users that access is restricted and monitored. Legal banners are required in many compliance frameworks (PCI-DSS, HIPAA, government standards) because they establish notice before access and support legal action in the event of unauthorized use.

![Logon message text configured](screenshots/image22.png)

---

**Setting 10 -- Message title for users attempting to log on**

A custom title was added for the logon banner window.

![Logon message title configured](screenshots/image1.png)

---

**Setting 11 -- Prompt user to change password before expiration**

Users are prompted to change their password in advance of the expiration date, preventing unexpected lockouts that could disrupt productivity.

![Password expiration prompt configured](screenshots/image7.png)

---

## 7. Login Changes Verification

After applying all logon settings, the machine was locked and the login screen was tested to confirm each change took effect.

**Verified: CTRL+ALT+DEL required before login screen appears**

![CTRL+ALT+DEL required screen](screenshots/image34.png)

**Verified: Custom security message displayed before credentials are entered**

![Custom logon security message displayed](screenshots/image29.png)

**Verified: No previous username displayed -- manual username entry required**

![No username displayed at login](screenshots/image3.png)

All three logon hardening controls were confirmed active on the live system.

---

## 8. Windows Defender -- Virus and Threat Protection

**Step 1 -- Open Virus and Threat Protection in Windows Security**

![Windows Security -- Virus and Threat Protection](screenshots/image36.png)

**Step 2 -- Disable automatic sample submission**

Under Virus and threat protection settings, Automatic sample submission was turned off. In an enterprise environment, automatically sending file samples to Microsoft may not be appropriate for machines handling sensitive or classified data. Disabling this keeps sample data on-premises.

![Automatic sample submission -- off](screenshots/image16.png)

**Step 3 -- Remove malware exclusions**

Any existing malware scan exclusions were reviewed and removed.

![Malware exclusions removed](screenshots/image23.png)

Scan exclusions are a common persistence technique used by malware: if an attacker can write to the registry to add an exclusion for their payload's location, Windows Defender will silently skip that path during scans. Removing all unnecessary exclusions closes this bypass.

**Step 4 -- Run a full malware scan**

A malware scan was run to establish a clean baseline for the hardened system.

![Malware scan running](screenshots/image4.png)

---

## 9. Windows Defender -- Ransomware Protection and Core Isolation

**Enable ransomware protection (Controlled Folder Access)**

![Ransomware protection -- enabled](screenshots/image35.png)

Controlled Folder Access prevents unauthorized applications from writing to protected directories (Documents, Pictures, Desktop, etc.). Ransomware relies on the ability to enumerate and encrypt files in these locations. With Controlled Folder Access active, only applications explicitly allowed by the user or policy can modify protected folder contents.

**View ransomware protection history**

![Ransomware protection history](screenshots/image37.png)

**Enable Core Isolation (Memory Integrity)**

![Core isolation -- Memory Integrity enabled](screenshots/image20.png)

Memory Integrity (Hypervisor-Protected Code Integrity, HVCI) uses hardware virtualization to isolate core Windows kernel processes in a separate, protected environment. This prevents kernel-level malware and rootkits from injecting code into kernel memory, even if they manage to execute with elevated privileges. It requires compatible hardware (VT-x/AMD-V with SLAT support) and is one of the strongest protections available on modern Windows 10 systems.

---

## 10. Reputation-Based Protection

In Windows Security under `App and browser control > Reputation-based protection settings`, all SmartScreen and potentially unwanted application (PUA) controls were verified as enabled:

- Check apps and files
- SmartScreen for Microsoft Edge
- Potentially unwanted app blocking
- SmartScreen for Microsoft Store apps

![Reputation-based protection -- all toggles on](screenshots/image33.png)

SmartScreen evaluates downloaded files and applications against Microsoft's cloud reputation database. Files with no reputation or a known-malicious reputation are flagged before execution. PUA blocking prevents installation of adware, bundled unwanted software, and aggressive advertising tools that may not qualify as outright malware but degrade security posture.

---

## 11. Firewall Verification

All three Windows Firewall network profiles were verified to be active:

- Domain network
- Private network
- Public network

![Windows Firewall -- all profiles on](screenshots/image10.png)

The Windows Firewall must be active across all profiles because a machine's profile can change (e.g., connecting to a public hotspot switches to the Public profile). If any profile is off, the machine is unprotected in that network context. Domain profile is particularly important in enterprise environments where Group Policy manages firewall rules.

---

## 12. Disable Unused Applications

Unused applications increase the attack surface. Each installed application is a potential vulnerability -- outdated software, unpatched libraries, or weak default configurations can all be exploited. Applications confirmed as unnecessary were removed or disabled.

![Unused applications disabled](screenshots/image13.png)

---

## 13. User Account Control (UAC)

User Account Control was reviewed and configured to the appropriate notification level.

![UAC configured](screenshots/image9.png)

UAC enforces privilege separation on Windows. Even when logged in as an administrator, applications run with standard user privileges by default. Elevation is only granted when explicitly confirmed by the user. This limits the damage a malicious process can do if it executes under the current session -- it cannot silently install software, modify system files, or change security settings without triggering a UAC prompt.

---

## Hardening Summary

The table below summarizes every configuration change applied in this lab alongside its security rationale.

| Area | Setting | Value Applied | Threat Mitigated |
|------|---------|--------------|-----------------|
| Password Policy | Enforce password history | 24 passwords | Credential cycling / reuse |
| Password Policy | Maximum password age | 60 days | Stale/compromised credentials |
| Password Policy | Minimum password age | 1 day | History bypass |
| Password Policy | Minimum password length | 14 characters | Brute-force attacks |
| Password Policy | Complexity requirements | Enabled | Dictionary attacks |
| Password Policy | Reversible encryption | Disabled | Plaintext password exposure |
| Account Lockout | Lockout threshold | 10 attempts | Automated brute-force |
| Account Lockout | Lockout duration | 15 minutes | Sustained credential attacks |
| Audit Policy | All nine categories | Success and Failure | Forensic visibility |
| User Rights | Network access | All removed | Remote share attacks |
| User Rights | Local logon | Guest removed | Unauthenticated local access |
| User Rights | RDP logon | All removed | RDP brute-force / exploitation |
| Security Options | Administrator name | Renamed | Targeted credential attacks |
| Security Options | Guest name | Renamed | Targeted credential attacks |
| Logon Settings | Lock screen user info | Hidden | Physical access OSINT |
| Logon Settings | CTRL+ALT+DEL | Required | Fake logon screen attacks |
| Logon Settings | Last signed-in username | Hidden | Username enumeration |
| Logon Settings | Inactivity lock | 15 minutes | Unattended session access |
| Logon Settings | Legal banner | Configured | Compliance / legal notice |
| Windows Defender | Sample submission | Disabled | Data exfiltration to cloud |
| Windows Defender | Scan exclusions | Removed | Malware persistence bypass |
| Windows Defender | Controlled Folder Access | Enabled | Ransomware file encryption |
| Windows Defender | Memory Integrity (HVCI) | Enabled | Kernel-level code injection |
| Windows Defender | SmartScreen / PUA blocking | All on | Malicious download execution |
| Firewall | All profiles | On | Unauthorized network access |
| UAC | Notification level | Configured | Silent privilege escalation |

---

## Key Takeaways

**Defense in depth:** No single hardening control is sufficient on its own. This lab applied controls across authentication, authorization, logging, malware protection, and network access -- each layer compensates for the weaknesses of the others.

**Default configurations are not secure:** The baseline `net accounts` output at the start of the lab showed that out-of-the-box Windows 10 has minimal password requirements, no lockout policy, and no audit logging. Every system needs explicit hardening before deployment.

**Audit logging is non-negotiable:** Without the audit policy enabled, every other hardening control operates silently. There is no way to know whether an attack was attempted, succeeded, or was blocked without logs. Enabling both success and failure events across all categories provides the forensic foundation for any incident response.

**Obscurity has limited but real value:** Renaming the Administrator and Guest accounts does not prevent a determined attacker indefinitely, but it eliminates trivial automated attacks that target predictable names and adds a step to any manual attack. Layered with stronger controls, it contributes to the overall hardening posture.

---

## Disclaimer

This lab was performed on a virtual machine in a controlled academic environment as part of CNS3003: Security Testing and Detection at the University of Technology, Jamaica. All changes documented here were applied to an isolated test system. These configurations should be tested in a lab environment before being applied to production systems, as some settings (particularly RDP removal and network access restrictions) may affect legitimate remote access workflows.

---

*University of Technology, Jamaica -- Faculty of Computing and Engineering*
*School of Computing and Information Technology*
