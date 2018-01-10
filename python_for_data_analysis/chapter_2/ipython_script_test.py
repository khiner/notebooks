import sys

def f(x, y, z):
    return (x + y) / z

a = 5
b = 6
c = 7.5

result = f(a, b, c)

if len(sys.argv) > 1:
    print('argument passed in is: ', sys.argv[1])


if 'variable_for_script' in locals():
    print('I have access to the IPython variable `variable_for_script`, and its value is ', variable_for_script)
