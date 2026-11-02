StateMint
=========

StateMint finds the state-space model of a lumped-parameter dynamic system
from its elemental and constraint equations, following Rowell and Wormley,
*System Dynamics: An Introduction* (1997), chapter 5. See the `tutorial
<https://github.com/CameronDevine/StateMint/blob/master/tutorial.md>`_ for how
to prepare the equations and the `paper <https://doi.org/10.21105/jose.00044>`_
for background.

Install it with ``pip install StateMint``.

.. code-block:: python

   import StateMint

   sys = StateMint.Solve(
       ['Fs'],                                  # inputs
       ["vm' = Fm/m", "FK' = K*vK"],            # state-variable elemental equations
       ['FB = B*vB'],                           # other elemental equations
       ['Fm = Fs - FK - FB', 'vK = vm', 'vB = vm'],  # constraints
       ['vm', 'FK + FB'])                       # outputs
   sys.A, sys.B, sys.C, sys.D

.. toctree::
   :maxdepth: 2

API
---

.. automodule:: StateMint.StateMint
   :members: Solve, StateMintError, output, split_entries, names

.. automodule:: StateMint.to_numpy
   :members:

.. automodule:: StateMint.web
   :members: solve_fields, format_model, solve_json, FIELDS
