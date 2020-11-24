# Change Log

### 0.1.5 2020-11-23

MyPy type annotation support was added. Type annotations always existed in the code, but I only recently discovered MyPy doesn't pick them up for packages unless `py.typed` is added to the distribution. Ugh.

FrontDoor now also supports decorating functions which don't accept a list of strings. This is done by checking the arity of the function before calling it using the inspect module, and should work with Python 2 and Python 3.

### 0.1.2 2018-04-08

First significant release to PyPi. Before this project was expected to be vendored.
