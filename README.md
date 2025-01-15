### Small Computer Scripts
* **pkgkeeper** - *(Python 2.7)* adds or removes packages from hold state with [apt-mark](http://manpages.ubuntu.com/manpages/trusty/en/man8/apt-mark.8.html) tool in Ubuntu using python sets.

##### EXAMPLE:
```
	root@darkstar:~# apt-mark showhold
	python
	nginx
	root@darkstar:~# ./pkgkeeper.py apache2 nginx
	What to add: set(['apache2'])
	What to remove: set(['python'])
	What to add: set([])
	What to remove: set(['python'])
	root@darkstar:~# apt-mark showhold
	apache2
	nginx
```

* **httpsrvreaper** - *(Python 3.2)* simple HTTP scanner to collect information about "Server" header.

##### EXAMPLE:
```
	root@darkstar:~# ./httpsrvreaper.py 1 5 &
	root@darkstar:~# ls
	1.0.0.0.log  2.0.0.0.log  3.0.0.0.log  4.0.0.0.log  5.0.0.0.log
	root@darkstar:~# cat 4.0.0.0.log
	{"IP": "4.2.103.43", "Time": "0.306944", "Server": "Apache/2.2.25 (Win32) mod_ssl/2.2.25 OpenSSL/0.9.8y mod_jk/1.2.40"}
```

* **fabric** - *(Python 2.7)* Fabric input file for multinodes managment.

##### EXAMPLE:
```
	root@darkstar:~# fab --skip-bad-hosts command:'uptime'
	[node1.com] Executing task 'command'
	Hostname: node1.com
	[node1.com] sudo: uptime
	[node1.com] out: sudo password:
	[node1.com] out: 20:22  up 47 mins, 2 users, load averages: 0,82 1,04 1,10
	[node1.com] out:

	||| Done.
```

* **bleachbitch** - *(Python 3.5.1)* Searches for cache, history, logs and temporary files on Linux.

##### EXAMPLE:
```
    root@darkstar:~# python bleachbitch.py
    ### Checking:  Links 2 - Web browser
    ~/.links2/links.his - Not Found.
    ~/.links/links.his - FOUND !!!
```

* **unhider** - *(Python 3.10.12)* Show hidden PIDs by libprocesshider.so on Linux system .

##### EXAMPLE:
```
	root@darkstar:~# ./unhider.py
	## Hidden PID revealer v0.2 by NFsec.pl
	
	Scanning system please wait...
	
	PIDs from /proc: [1, 1313, 1983, 1984, 3118, 3119, 3120, 3121, 3124, 3125]
	
	PIDs enumerated: [1, 3125, 3146, 3671, 3739, 3759, 3837, 3838, 3860, 3861]
	
	Hidden PIDs: [3860]
```

* **sslsrvreaper** - *(Python 3.11.2)* Get domain TLS information from domains.txt.

##### EXAMPLE:
```
    root@darkstar:~# cat domains.txt
    0-1.cloud
    0-1.ir
    root@darkstar:~# ./sslsrvreaper.py
    root@darkstar:~# cat domains.log
    {
      "subject_hostName": "0-1.cloud",
      "subject_hostIP": "185.18.213.82",
      "subject_commonName": "*.0-1.cloud",
      "issuer_countryName": "PL",
      "issuer_organizationName": "Unizeto Technologies S.A.",
      "issuer_organizationalUnitName": "Certum Certification Authority",
      "issuer_commonName": "Certum Domain Validation CA SHA2",
      "version": 3,
      "serialNumber": "7064FDD670C62CDD5289E98EBF5AACA2",
      "notBefore": "Aug 26 13:20:32 2024 GMT",
      "notAfter": "Sep 25 13:20:31 2025 GMT",
      "subjectAltName": [
        "*.0-1.cloud",
        "0-1.cloud"
      ],
      "OCSP": "http://dvcasha2.ocsp-certum.com",
      "caIssuers": "http://repository.certum.pl/dvcasha2.cer",
      "crlDistributionPoints": "http://crl.certum.pl/dvcasha2.crl"
    }
```
* **phisherfisher** - *(Python 3.11.2)* Check if phishing domian if known to CERT.pl.

##### EXAMPLE:
```
agresor@darkstar:~$ ./phisherfisher allegr00lokalnie.47906408.xyz
INFO: Based on score, no similar phishing domain(s) found.
INFO: Based on subdomain charm, no similar phishing domain(s) found
INFO: Domain charm found 70 similar phishing domain(s). Example:
      all-egr0lokalnie.52312226.xyz with score 96.55.
```

### License

**Small Computer Scripts** are published under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
