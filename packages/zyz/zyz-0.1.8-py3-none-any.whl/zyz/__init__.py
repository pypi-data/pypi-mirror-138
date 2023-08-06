import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def help():

    print("****************************************\n")
    print("Help:\n")
    print("* Install zyz package:\n")
    print("pip install -U zyz -i https://pypi.python.org/pypi\n")
    print("* Use with zyz package:\n")
    print("python -c 'import zyz;zyz.help()'\n")
    print("****************************************\n")
