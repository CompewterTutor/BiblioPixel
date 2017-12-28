import os
from .. project import data_maker, defaults, project
from .. util import json

"""Common command line arguments for run and demo."""


def _get_version():
    from os.path import abspath, dirname, join
    filename = join(dirname(dirname(dirname(abspath(
        __file__)))), 'bibliopixel', 'VERSION')
    return open(filename).read().strip()


VERSION = _get_version()
COMPONENTS = 'driver', 'layout', 'animation'
PRESET_LIBRARY_DEFAULT = '~/.bibliopixel'
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'critical')
ENABLE_PRESETS = False
NUMBER_TYPES = ('python',) + data_maker.NUMPY_TYPES


def add_common_flags(parser):
    parser.add_argument(
        '--loglevel', choices=LOG_LEVELS, default='info', help=LOGLEVEL_HELP)
    parser.add_argument(
        '--verbose', '-v', action='store_true', help=VERBOSE_HELP)
    parser.add_argument(
        '--version', action='store_true', help=VERSION_HELP)
    parser.add_argument(
        '-x', '--isolate', action='store_true', help=ISOLATE_HELP)


def add_project_flags(parser):
    parser.add_argument(
        '-a', '--animation', default=None,
        help='Default animation type if no animation is specified')

    parser.add_argument(
        '-b', '--brightness', default=None,
        help='Override project brightness value')

    parser.add_argument(
        '-d', '--defaults', default=None, nargs='*',
        action='append', help='Use this default setting')

    parser.add_argument(
        '--dimensions', '--dim', default=None,
        help='x, (x, y) or (x, y, z) dimensions for project')

    parser.add_argument(
        '--dump', action='store_true',
        help='Dump the full project after loading but before running')

    parser.add_argument(
        '--dry_run', action='store_true',
        help='Load projects but do not run them')

    parser.add_argument(
        '-f', '--fail_on_exception', action='store_true',
        help='If true, bp fail if any subanimation fails to construct')

    parser.add_argument(
        '-l', '--layout', default=None,
        help='Default layout class if no layout is specified')

    parser.add_argument(
        '--numbers', '-n', default='python', choices=NUMBER_TYPES,
        help=NUMBERS_HELP)

    parser.add_argument('-p', '--path', default=None, help=PATH_HELP)

    parser.add_argument(
        '--pause', default=0, help='Time to pause between running animations')

    parser.add_argument(
        '-r', '--run_for', default=None, help=RUN_FOR_HELP)

    parser.add_argument(
        '-s', action='store_true', help='Run SimPixel at the default URL')

    parser.add_argument(
        '--simpixel', help='Run SimPixel at a specific URL')

    parser.add_argument(
        '--slideshow', default=0, help='Run `bp` sequence in slideshow mode, '
        'where each animation is shown for this many seconds')

    parser.add_argument(
        '-t', '--ledtype', default=None,
        help='Default LED type if no LED type is specified')


def _make_project_flags(args):
    def get_value(name):
        value = getattr(args, name, None)
        if not value:
            return {}

        if '{' in value:
            return json.loads(value)

        return {'typename': value}

    project_flags = {name: get_value(name) for name in COMPONENTS}
    if args.ledtype:
        project_flags['driver']['ledtype'] = args.ledtype

    if args.brightness:
        project_flags['layout']['brightness'] = int(args.brightness)

    if args.defaults:
        # Arguments come in like: [['foo'], ['bar'], ['baz'], ...]
        # I have no idea why.
        defs = [(a[0] if isinstance(a, list) else a) for a in args.defaults]
        defaults.set_project_defaults(defs)

    if args.numbers != 'python':
        project_flags['numbers'] = args.numbers

    if args.run_for is not None:
        project_flags.setdefault('run', {})['seconds'] = float(args.run_for)

    if args.slideshow:
        project_flags.setdefault('animation', {})['slideshow'] = float(
            args.slideshow)

    if args.dimensions is not None:
        dimensions = args.dimensions.split(',')
        try:
            project_flags['dimensions'] = [int(i) for i in dimensions]
        except:
            raise ValueError('--dimensions must be one to three numbers '
                             'separated by commas.')

    return project_flags


def make_animation(args, desc, **kwds):
    project_flags = _make_project_flags(args)
    return project.project(project_flags, desc, **kwds)


# Help messages.

PATH_HELP = """\
A list of directories, separated by colons, 'which are added to the end of
`sys.path`.

You can also use loady-style paths which start with `//git/` to
dynamically load a library from a public git repository.

See https://github.com/ManiacalLabs/BiblioPixel/wiki/BiblioPixel-Paths
for more information.
"""

LOGLEVEL_HELP = """\
Set what level of events to log. Higher log levels print less."""

ISOLATE_HELP = """\
Run BiblioPixel in isolated mode, where it cannot see your local files.
This means that it will not see any local Python classes in your directories
and it won't see your local aliases.

Running your project in isolated mode help makes sure that your project will
work on other machines without modification.
"""

NUMBERS_HELP = """
The type of numbers that are used in color list calculations.

  `python` means to use the classic Python lists of (r, g, b) tuples.

  Anything else is a numpy type, which means that bp uses numpy arrays, which
  use much faster arithmetic.

  numpy types include:
    """ + ' '.join(data_maker.NUMPY_TYPES)

PRESET_HELP = """Filenames for preset library"""

RUN_FOR_HELP = """How long to run the animation (overrides runner.seconds)."""

VERBOSE_HELP = """\
If this is set, then errors are reported with a full stack trace, and
loglevel is by default set to debug..
"""

VERSION_HELP = """\
Print the current version number of BiblioPixel (%s).
""" % VERSION


# TODO: this should go somewhere else
"""
Set defaults for projects using JSON.

A Project is a JSON file or equivalently a Python dictionary that describes
a BibliopPixel installation.  The top-level keys in a Project are called the
sections and a Project might have the following sections:

    {sections}

Often some sections of your project correspond to hardware and thus rarely
change, so the `bp default` command allows you to set defaults so you
don't have to mention these from your project at all.
"""
