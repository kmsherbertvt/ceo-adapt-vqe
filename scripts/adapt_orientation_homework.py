# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:16:40 2024

@author: kmsherbertvt

Simple homework assignment to intimate oneself with the inputs and outputs of ADAPT.

# Goal
    Write your own Python script to run ADAPT, using one of the example scripts as a template.

# Requirements
    1. Configure ADAPT to use the Coupled Exchange Operator pool, always adding just one parameter per adaptation.

    2. Solve the lithium hydride (LiH) molecule with a bond distance of 3.0Å, to chemical accuracy.

    3. Neatly print out the sequence of operators that ADAPT selects.

    4. Generate a plot of energy error vs ADAPT iterations, similar to Fig. 3 of the original ADAPT paper.

# Bonus
    Run the same ansatz, but with sampling noise. How close is it to chemical accuracy?

(Unfortunately, the current version of the code isn't equipped to do sampling noise with the CEO pool, so the bonus isn't really very achievable.)


# Solution Key
This script is a copy of one of Mafalda's examples, with the requisite changes.
I anticipate the following "gotchas":

    1. Identifying the correct pool as OVP_CEO requires carefully reading the CEO paper. But even once you've done that, you've got to set TETRIS to false!

    2. Changing the molecule is easy. But you'll also need to change the number of iterations and the threshold so that ADAPT runs long enough to get to chemical accuracy. (I selected my threshold so that ADAPT considers itself "converged" for these particular settings, right at chemical accuracy.)

    3. The original example has the code to print out all operators in the ansatz. The only question is, will the students consider this "neat"?

    4. The original example does *not* give a complete tutorial in accessing information from `data`. You'll have to dive into the code, or exploit Python's introspection, to work out how to get access to the energy errors from each iteration. Oh also you have to figure out how to plot things but whatever.

"""

from adaptvqe.molecules import create_lih   # NOTE: Must change this to set the right system.
from adaptvqe.pools import OVP_CEO
from adaptvqe.algorithms.adapt_vqe import LinAlgAdapt, SampledLinAlgAdapt   # NOTE: BONUS Must change this to do sampling run.

r = 3.0                     # NOTE: Must change this to set the right system.
molecule = create_lih(r)    # NOTE: Must change this to set the right system.
pool = OVP_CEO(molecule)    # NOTE: Must use this to get the right pool.

my_adapt = LinAlgAdapt(     # NOTE: BONUS Must change this to do sampling run.
    pool=pool,
    molecule=molecule,
    max_adapt_iter=10,      # NOTE: Must change this to get to chemical accuracy.
    recycle_hessian=True,
    tetris=False,           # NOTE: Must change this to ensure 1 parameter/adaptation.
    verbose=True,
    threshold=0.066,        # NOTE: Must change this to get to chemical accuracy.
    # shots=1024,             # NOTE: BONUS Must add this to do sampling run.
)

my_adapt.run()
data = my_adapt.data



# DISPLAY POOL OPERATORS NEATLY
print(
    "Final operators in the ansatz: ",
    [pool.get_op(index) for index in data.result.ansatz.indices],
)
# NOTE: This isn't really what I call "neatly" - I'm just looking forward to seeing what my students come up with.

# PLOT ENERGY ERROR
import matplotlib
import matplotlib.pyplot as plt

plt.plot(data.evolution.errors)
plt.yscale('log')
plt.show()
# NOTE: This is far from a publishable figure. Once again I just want to see what the students will do. Well, that and challenge them to find `data.evolution`. That's the important part...