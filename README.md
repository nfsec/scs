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

### License

**Small Computer Scripts** are published under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
