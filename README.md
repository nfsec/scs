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

### License

**Small Computer Scripts** are published under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
