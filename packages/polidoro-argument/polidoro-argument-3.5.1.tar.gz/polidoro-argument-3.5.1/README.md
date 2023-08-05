# Polidoro Argument 
[![Tests](https://github.com/heitorpolidoro/polidoro-argument/actions/workflows/test.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-argument/actions/workflows/test.yml)
[![Upload Python Package](https://github.com/heitorpolidoro/polidoro-argument/actions/workflows/python-publish.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-argument/actions/workflows/python-publish.yml)
[![Lint with comments](https://github.com/heitorpolidoro/polidoro-argument/actions/workflows/python-lint.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-argument/actions/workflows/python-lint.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/polidoro-argument)
[![Coverage Status](https://coveralls.io/repos/github/heitorpolidoro/polidoro-argument/badge.svg?branch=master)](https://coveralls.io/github/heitorpolidoro/polidoro-argument?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=heitorpolidoro_polidoro-argument&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=heitorpolidoro_polidoro-argument)

[![Latest](https://img.shields.io/github/release/heitorpolidoro/polidoro-argument.svg?label=latest)](https://github.com/heitorpolidoro/polidoro-argument/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/polidoro-argument)

![PyPI - Downloads](https://img.shields.io/pypi/dm/polidoro-argument?label=PyPi%20Downloads)

![GitHub](https://img.shields.io/github/license/heitorpolidoro/polidoro-argument)

Package to simplify creating command line arguments for scripts in Python.

#### How to use:

- Decorate the method you want to create an argument from with `@Argument`.
- Decorate the method you want to call from command line with `@Command`.
- Create a `PolidoroArgumentParser` 
- Call `parser.parse_args()`

All keywords arguments to `@Argument` and `@Command` are the same as in [argparse.ArgumentParser.add_argument](https://docs.python.org/3.7/library/argparse.html#the-add-argument-method) except for 'action' and 'nargs'.
'action' is a custom Action created to run the decorated method and 'nargs' is the number of parameters in the decorated method.

###### Examples:
foo.py
```python

from polidoro_argument import Argument, PolidoroArgumentParser

@Argument
def bar():
    print('hi')

PolidoroArgumentParser().parse_args()
# OR
parser = PolidoroArgumentParser()
parser.parse_args()
```
Result:
```bash
$ python foo.py --bar
hi 
```

You can pass argument to the method

```python
from polidoro_argument import Argument

@Argument
def bar(baz=None):
    print(baz)
```
```bash
$ python foo.py --bar Hello
Hello
```
To create commands

```python
from polidoro_argument import Command


@Command
def command():
    print('this is a command')
```
```bash
$ python foo.py command
this is a command
```
With arguments

```python
from polidoro_argument import Command


@Command
def command_with_arg(arg, arg1=None):
    print('this the command arg: %s, arg1: %s' % (arg, arg1))
```
```bash
$ python foo.py command_with_arg Hello
this the command arg: Hello, arg1: None
$ python foo.py command_with_arg Hello --arg1 World
this the command arg: Hello, arg1: World
```
Using a Class
```python
from polidoro_argument import Argument, Command

class ClassCommand:
    @staticmethod
    @Argument
    def argument_in_class():
        print('argument_in_class called')

    @staticmethod
    @Command
    def command_in_class(arg='Oi'):
        print('command_in_class called. arg=%s' % arg)
```
```bash
$ python foo.py classcommand --argument_in_class
argument_in_class called
$ python foo.py classcommand command_in_class
command_in_class called. arg=Oi
$ python foo.py classcommand command_in_class --arg=Ola
command_in_class called. arg=Ola
```
Undefined number of arguments

```python
from polidoro_argument import Argument


@Argument
def argument(*args, **kwargs):
    print(args, kwargs)


@Argument
def command(*args, **kwargs):
    print(args, kwargs)
```
```bash
$ python foo.py --argument arg1 arg2 kwarg1=1 kwarg2 2 # without '--' in kwargs
('arg1', 'arg2') {'kwarg1': 1, 'kwarg2: 2'}
$ python foo.py command arg1 arg2 --kwarg1=1 --kwarg2 2 # with '--' in kwargs
('arg1', 'arg2') {'kwarg1': 1, 'kwarg2: 2'} 
 
```
Default Command

It's possible to define a _default command_ to be called when no argument is passed to a command or there is some unrecognized arguments

```python
from polidoro_argument import Command


class Bar(object):
    help = 'cli help'
    description = 'description'

    @staticmethod
    @Command
    def default_command(*remainder):
        if remainder:
            print('with remainders:', *remainder)
        else:
            print('without remainders')
```
```bash
$ python foo.py bar
without remainders
$ python foo.py bar r1 r2 r3
with remainders: r1 r2 r3
```
