'''StateMint: state-space models from elemental and constraint equations.'''

from .StateMint import Solve, StateMintError, output, split_entries

__version__ = '3.0.0.dev0'

__all__ = ['Solve', 'StateMintError', 'output', 'split_entries', '__version__']
