# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import torch

print("torch version {}".format(torch.__version__))
print("cuda is available {}".format(torch.cuda.is_available()))
print("torch is install in {}".format(torch.__file__))

import sys

print(sys.version)

x = torch.rand(5, 3)
print(x)
print(torch.cuda.is_available())

