from clusters import printclust
import sys
try:
    from StringIO import StringIO  # for Python 2
except ImportError:
    from io import StringIO  # for Python 3


def terminaldenokuma(function):
    def wrapper(*args,**kwargs):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        function(*args, **kwargs)
        sys.stdout = old_stdout
        contents = mystdout.getvalue()
        mystdout.close()
        return contents
    return wrapper


@terminaldenokuma
def print_terminalden(*args, **kwargs):
    print(*args, **kwargs)


@terminaldenokuma
def printcluster_terminalden(clust, labels, n=0):
    printclust(clust, labels, n)


