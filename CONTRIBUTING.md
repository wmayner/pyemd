Installation issues
===================

Before opening an issue related to installation, please try to install PyEMD in
a fresh, empty Python 3 virtual environment and check that the problem
persists:

```shell
pip install virtualenvwrapper
mkvirtualenv -p `which python3` pyemd
# Now we're an empty Python 3 virtual environment
pip install pyemd
```

PyEMD is not officially supported for (but may nonetheless work with) the following:

- Python 2
- Anaconda distributions
- Windows operating systems

However, if you need to use it in these cases, pull requests are welcome!
