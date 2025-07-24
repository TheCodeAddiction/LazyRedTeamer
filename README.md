# LazyRedTeamer

> **LazyRedTeamer** is a growing toolbox that bundles together the one‑off scripts I kept writing during red‑team engagements, CTFs and certification labs. Each helper script wraps a longer command‑line incantation so that I can stay in the *flow* instead of copy‑pasting cheat‑sheets.

⚠️ **For authorised security testing and learning only!**

---

## ✨ Key Features

| Script | What it automates |
| ------ | ----------------- |
| `nscan` | Runs an Nmap scan with aggressive discovery, default scripts, version detection and auto‑generated HTML report. |
| `nxcrecon` | Opinionated wrapper around NetExec (`nxc`) that sweeps common services (SMB, WinRM, RDP, MSSQL, WMI, NFS, FTP, SSH). |
| `adrecon` | Chains BloodHound collection, Kerberoasting and AS‑REP roasting for quick AD situational awareness. |
| `lazytest` | A tiny diagnostic script that just runs `whoami` so you can verify the toolbox is on your `$PATH`. |

---

## 🚀 Quick Start

```bash
# 1. Grab the code
git clone https://github.com/TheCodeAddiction/LazyRedTeamer.git

# 2. Add the bin/ directory to your PATH
export PATH="$PWD/LazyRedTeamer/bin:$PATH"

# 3. Sanity‑check
lazytest   # should print your current username
```

> **Tip:** Want the PATH change every time you open a terminal?  Append the `export` line above to `~/.bashrc` (or `~/.zshrc`).

---

## 📦 Dependencies

| Script | External tools |
| ------ | -------------- |
| `nscan` | `nmap` ≥ 7.94, `xsltproc`, `firefox` |
| `nxcrecon` | [`nxc`](https://github.com/chvancooten/NXC) |
| `adrecon` | `bloodhound‑python`, `impacket` (for `GetUserSPNs.py` and `GetNPUsers.py`) |

Install them with your favourite package manager.  On Debian‑based systems for example:

```bash
sudo apt install nmap xsltproc firefox-esr
pipx install bloodhound-python impacket nxc
```

---

## 🛠 Scripts in Depth

### nscan — one‑shot Nmap wrapper

**Synopsis**

```bash
nscan [--no-ping | -np] <target | CIDR | ip_list.txt>
```

**Options**

| Option | Explanation |
|--------|-------------|
| `-h`, `--help` | Show help message and exit. |
| `--no-ping`, `-np` | Skip the initial ICMP ping sweep when the target is a CIDR range. |
| `<target>` | Single IP/hostname, CIDR range (e.g. `10.0.0.0/24`) or text file with one host per line. |

**What it does**

1. Optionally ping‑sweeps CIDR ranges and builds a list of responsive hosts.  
2. Runs `nmap -sS -sV -sC -O -p- -Pn` against each host.  
3. Saves XML (`tcp_<target>.xml`) and prettified HTML (`tcp_<target>.html`) reports and auto‑opens the latter in Firefox.

**Examples**

```bash
# Full TCP port scan of a single host
nscan 192.168.1.10

# Scan a /24 network but only after verifying hosts are up
nscan 10.10.10.0/24

# Skip the ping sweep (useful if ICMP is filtered)
nscan --no-ping 10.10.10.0/24

# Feed nmap a custom list of hosts
nscan live_hosts.txt
```

---

### nxcrecon — opinionated NetExec sweep

**Synopsis**

```bash
nxcrecon -u <user> (-p <password> | -H <NTLM>) -t <target|list> [--local-auth] [--no-bruteforce]
```

**Options**

| Option | Explanation |
|--------|-------------|
| `-u`, `--username` *REQ* | Username to authenticate with. |
| `-p`, `--password` | Clear‑text password (mutually exclusive with `-H`). |
| `-H`, `--hash` | NTLM hash (mutually exclusive with `-p`). |
| `-t`, `--target` *REQ* | Single IP/CIDR or file containing targets. |
| `--local-auth` | Attempt local rather than domain authentication. |
| `--no-bruteforce` | Add `--no-bruteforce` to every NetExec call. |
| `-h`, `--help` | Show help message and exit. |

**What it does**

Runs a battery of `nxc` modules (SMB, WinRM, RDP, MSSQL, WMI, NFS, FTP and SSH) against the target set with the chosen credentials, printing each underlying command for transparency.

**Examples**

```bash
# Spray a password across a /24 using domain creds
nxcrecon -u alice -p 'Winter2025!' -t 192.168.56.0/24

# Use an NTLM hash against hosts listed in a file
nxcrecon -u bob -H aad3b435b51404eeaad3b435b51404ee:32ed87bdb5fdc5e9cba88547376818d4 -t targets.txt --no-bruteforce
```

---

### adrecon — Active Directory reconnaissance helper

**Synopsis**

```bash
adrecon -u <user> -d <domain> -dc <dc_ip> -ns <dns_ip> (-p <password> | -H <hash>)
```

**Options**

| Option | Explanation |
|--------|-------------|
| `-u`, `--username` *REQ* | Domain user account. |
| `-d`, `--domain` *REQ* | AD domain (e.g. `corp.local`). |
| `-dc`, `--dc` *REQ* | Domain Controller hostname or IP. |
| `-ns`, `--nameserver` *REQ* | DNS server IP (passed to tools). |
| `-p`, `--password` | Password (mutually exclusive with `-H`). |
| `-H`, `--hash` | NTLM hash (mutually exclusive with `-p`). |
| `-h`, `--help` | Show help message and exit. |

**What it does**

1. Collects BloodHound data (`bloodhound-python -c all`).  
2. Kerberoasts with `GetUserSPNs.py`.  
3. Attempts AS‑REP roasting with `GetNPUsers.py` (only if a clear‑text password is supplied).

**Examples**

```bash
# All‑in‑one recon using a password
adrecon -u alice -p 'Winter2025!' -d corp.local -dc dc.corp.local -ns 10.0.0.2

# Same but with an NTLM hash
adrecon -u svc_account -H 1b6453892473a467d07372d45eb05abc2031647a -d corp.local -dc 10.0.0.1 -ns 10.0.0.2
```

## ⚖️ Responsible / Legal Use

The scripts in this repository can **damage systems or breach policies** when misused. You are *solely* responsible for ensuring you have **written permission** to test the targets you point them at.

The author(s) and contributors accept **no liability** for any direct or indirect damage arising from the use of these tools. When in doubt, **don’t run it**.

---

## 🙏 Credits

- [nmap](https://nmap.org) – network exploration tool and security scanner.  
- [NXC](https://github.com/chvancooten/NXC) – Powerful network eXfiltration & Crack utility.  
- [BloodHound](https://github.com/BloodHoundAD/BloodHound) / [bloodhound‑python](https://github.com/fox-it/BloodHound.py).  
- [Impacket](https://github.com/fortra/impacket).

> *Happy hacking*
