# Sorry for AI sloop readme, I will re-write this later.
# LazyRedTeamer

> **LazyRedTeamer** is a growing toolbox that bundles together one‑off scripts I kept writing during red‑team engagements, CTFs and certification labs. Each helper wraps a longer command-line workflow so I can stay in the *flow* instead of juggling cheat-sheets.

⚠️ **For authorised security testing and learning only!**

---

## ✨ Key Features

| Script | What it automates |
| ------ | ----------------- |
| `nscan` | Nmap wrapper with optional ping sweep, full TCP scan, XML + HTML output. |
| `nxcrecon` | Opinionated NetExec (`nxc`) sweep across common enterprise protocols. |
| `adrecon` | BloodHound collection + Kerberoast + AS-REP roast helper workflow. |
| `webfuzz.py` | Multi-pass Gobuster wrapper for directories/files/words with extensions. |
| `icsphish.py` | Sends HTML + ICS calendar invite emails from custom templates. |
| `icsphish_offsec.py` | Older/offsec variant of the ICS invitation sender flow. |
| `pysrv` | Quick Python HTTP file server on a chosen port. |
| `psrv` | Alias-style helper to start a Python HTTP server quickly. |
| `lazytest` | Tiny sanity check (`whoami`) to verify your PATH/toolbox setup. |

---

## 🚀 Quick Start

    # 1) Clone
    git clone https://github.com/TheCodeAddiction/LazyRedTeamer.git

    # 2) Add bin/ to PATH (from repo root)
    export PATH="$PWD/LazyRedTeamer/bin:$PATH"

    # 3) Test that scripts are reachable
    lazytest

> **Tip:** Add the `export PATH=...` line to `~/.bashrc` or `~/.zshrc` to keep it permanent.

---

## 📦 Dependencies

| Script | External tools required |
| ------ | ----------------------- |
| `nscan` | `nmap`, `xsltproc`, `firefox` |
| `nxcrecon` | `nxc` (NetExec) |
| `adrecon` | `bloodhound-python`, `impacket` (`GetUserSPNs.py`, `GetNPUsers.py`) |
| `webfuzz.py` | `gobuster` |
| `icsphish.py` / `icsphish_offsec.py` | Reachable SMTP server + Python stdlib |
| `pysrv` / `psrv` / `lazytest` | Python |

Install them with your favourite package manager.  On Debian‑based systems for example:

```bash
sudo apt install nmap xsltproc firefox-esr gobuster
pipx install nxc bloodhound-python impacket
```

---

## 🛠 Scripts in Depth

### `lazytest` — verify setup fast

**Synopsis**

    lazytest

**What it does**

Runs `whoami` and prints the current user. Useful to confirm your `bin/` path is wired correctly.

---

### `pysrv` / `psrv` — instant local HTTP file server

**Synopsis**

    pysrv <port>
    psrv <port>

**Examples**

    pysrv 8000
    psrv 9000

**What it does**

Starts:

    python -m http.server <port>

---

### `nscan` — one-shot Nmap wrapper with ping sweep support

**Synopsis**

    nscan [--no-ping | -np] <target | CIDR | ip_list.txt>

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

### `nxcrecon` — NetExec protocol sweep helper

**Synopsis**

    nxcrecon -u <user> (-p <password> | -H <NTLM>) -t <target|list> [--local-auth] [--no-bruteforce]

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

### `adrecon` — AD recon chain helper

**Synopsis**

    adrecon -u <user> -d <domain> -dc <dc_ip_or_name> -ns <dns_ip> (-p <password> | -H <hash>)

| Option | Explanation |
|--------|-------------|
| `-u`, `--username` *REQ* | Domain user account. |
| `-d`, `--domain` *REQ* | AD domain (e.g. `corp.local`). |
| `-dc`, `--dc` *REQ* | Domain Controller hostname or IP. |
| `-ns`, `--nameserver` *REQ* | DNS server IP (passed to tools). |
| `-p`, `--password` | Password (mutually exclusive with `-H`). |
| `-H`, `--hash` | NTLM hash (mutually exclusive with `-p`). |
---

### `webfuzz.py` — simple Gobuster multi-pass wrapper

**Synopsis**

    python3 bin/webfuzz.py -u <url>

**What it does**

Runs three Gobuster passes against:
- `raft-large-directories-lowercase.txt`
- `raft-large-files-lowercase.txt` (+ extensions)
- `raft-large-words-lowercase.txt` (+ extensions)

Current behavior includes:
- redirect following (`-r`)
- filtered status handling via blacklist
- extension sweep (including `php`, `aspx`, `jsp`, etc.)

**Example**

    python3 bin/webfuzz.py -u http://192.168.56.101

---

### `icsphish.py` — template-driven HTML + ICS invite sender

**Synopsis**

    python3 bin/icsphish.py \
      --smtp-server <smtp_host> \
      --from <sender_email> \
      --to <recipient_email> \
      --event-url <url_or_text> \
      --ics-template <path_to_ics_template> \
      --html-template <path_to_html_template>

**What it does**

Builds an email with:
- HTML message body
- calendar invite (`.ics`) payload

---

### `icsphish_offsec.py` — legacy/offsec ICS sender variant

**Synopsis**

    python3 bin/icsphish_offsec.py <smtp_server> <sender_email> <recipient_email> <event_url>

**What it does**

Older variant of the calendar invite sender flow using local template files.

---

## ⚖️ Responsible / Legal Use

These scripts can be disruptive if misused. You are solely responsible for ensuring you have explicit authorization before testing any systems.

---

## 🙏 Credits

- [nmap](https://nmap.org)
- [NetExec (NXC)](https://github.com/Pennyw0rth/NetExec)
- [BloodHound](https://github.com/BloodHoundAD/BloodHound)
- [bloodhound-python](https://github.com/fox-it/BloodHound.py)
- [Impacket](https://github.com/fortra/impacket)
- [Gobuster](https://github.com/OJ/gobuster)

> *Happy hacking*

```bash
# All‑in‑one recon using a password
adrecon -u alice -p 'Winter2025!' -d corp.local -dc dc.corp.local -ns 10.0.0.2

# Same but with an NTLM hash
adrecon -u svc_account -H 1b6453892473a467d07372d45eb05abc2031647a -d corp.local -dc 10.0.0.1 -ns 10.0.0.2
```

## ⚖️ Responsible / Legal Use

These scripts can be disruptive if misused. You are solely responsible for ensuring you have explicit authorization before testing any systems.

---

## 🙏 Credits

- [nmap](https://nmap.org) – network exploration tool and security scanner.  
- [NXC](https://github.com/Pennyw0rth/NetExec) – Powerful network eXfiltration & Crack utility.  
- [BloodHound](https://github.com/BloodHoundAD/BloodHound) / [bloodhound‑python](https://github.com/fox-it/BloodHound.py).  
- [Impacket](https://github.com/fortra/impacket)
- [Gobuster](https://github.com/OJ/gobuster)

> *Happy hacking*
