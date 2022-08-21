# How to add python libraries

**All the following commands are expected to be executed in the `test/` directory.**

Confirm that pipenv is installed in your python environment:
e.g.
```sh
$ python3 -m pip list
Package          Version
---------------- ---------
certifi          2021.10.8
distlib          0.3.4
filelock         3.6.0
pip              22.0.4
pipenv           2022.5.2 # here I can confirm pipenv is installed
platformdirs     2.5.2
setuptools       56.0.0
six              1.16.0
virtualenv       20.14.1
virtualenv-clone 0.5.7
```

Add a library in Pipfile by hand:
e.g.
```sh
$ cat ./Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
numpy = "*"
flake8 = "*"
qiskit = "==0.37.*" # here I added a new library by hand

[requires]
python_version = "3.8"
```

Execute the following command:
```sh
$ pipenv lock -r > requirements.txt
```
e.g.
```sh
$ pipenv lock -r > requirements.txt
...(omit)
NOTE: the requirements command parses Pipfile.lock directly without performing any
locking operations. Updating packages should be done by running pipenv lock.
Pipfile.lock (f54424) out of date, updating to (2bfa05)...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Updated Pipfile.lock (2bfa05)!
```

That's it!
