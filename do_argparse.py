
"""
https://docs.python.org/3/library/argparse.html?highlight=argparse#metavar

16.4.2. ArgumentParser objects
class argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=argparse.HelpFormatter, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True)
Create a new ArgumentParser object. All parameters should be passed as keyword arguments. Each parameter has its own more detailed description below, but in short they are:

prog - The name of the program (default: sys.argv[0])
usage - The string describing the program usage (default: generated from arguments added to parser)
description - Text to display before the argument help (default: none)
epilog - Text to display after the argument help (default: none)
parents - A list of ArgumentParser objects whose arguments should also be included
formatter_class - A class for customizing the help output
prefix_chars - The set of characters that prefix optional arguments (default: ‘-‘)
fromfile_prefix_chars - The set of characters that prefix files from which additional arguments should be read (default: None)
argument_default - The global default value for arguments (default: None)
conflict_handler - The strategy for resolving conflicting optionals (usually unnecessary)
add_help - Add a -h/–help option to the parser (default: True)
allow_abbrev - Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)

16.4.3. The add_argument() method
ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
Define how a single command-line argument should be parsed. Each parameter has its own more detailed description below, but in short they are:

name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
action - The basic type of action to be taken when this argument is encountered at the command line.
nargs - The number of command-line arguments that should be consumed.
const - A constant value required by some action and nargs selections.
default - The value produced if the argument is absent from the command line.
type - The type to which the command-line argument should be converted.
choices - A container of the allowable values for the argument.
required - Whether or not the command-line option may be omitted (optionals only).
help - A brief description of what the argument does.
metavar - A name for the argument in usage messages.  
dest - The name of the attribute to be added to the object returned by parse_args().  
"""


import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

#metavar 帮助信息中的别名
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', metavar='YYY')
>>> parser.add_argument('bar', metavar='XXX')
>>> parser.parse_args('X --foo Y'.split())
Namespace(bar='X', foo='Y')
>>> parser.print_help()
usage:  [-h] [--foo YYY] XXX

positional arguments:
 XXX

optional arguments:
 -h, --help  show this help message and exit
 --foo YYY
 
#dest  接收参数的别名
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', dest='bar')
>>> parser.parse_args('--foo XXX'.split())
Namespace(bar='XXX')

#const default  不调用命令时用default的值,调用后用const的值
parser = argparse.ArgumentParser(description="Web crawler")
parser.add_argument(
    '-v', '--verbose', action='count', dest='level1',
    default=2, help='Verbose logging (repeat for more verbose)')
parser.add_argument(
    '-q', '--quiet', action='store_const', const=0, dest='level2',
    default=2, help='Only log errors')
parser.add_argument('--foo', action='store_true',default=False) #--foo未调用时值为False 调用时值为True
>>> parser.parse_args('-q'.split())
Namespace(level1=2, level2=0)    
>>> parser.parse_args('-v -q'.split())
Namespace(level1=3, level2=0)
>>> parser.parse_args('-vv'.split())
Namespace(level1=4, level2=2)
    