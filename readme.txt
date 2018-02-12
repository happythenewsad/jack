Instructions:
=============

Use jupyter notebook to open experiments.ipynb and run experiments.

To run tests: $python3 test_runner.py


Gameplay Assumptions 
===========

stand on soft 17
8 deck shoe
4 other players. Active player is rightmost.
When shoe is finished during active hand, new shoe is drawn from and then play ends.
Penetration: 75%
Double down allowed after pair splitting
second splits allowed (easier to implement)
  should work as is, just implement playerHand correctly 

House edge === expected loss


TODO
======

- allow variable betting (currently assumes every bet is 1 unit)
- implement different strategies
- Have logging configurable from notebook




Misc
=====

Blacjack rules at casinos:

https://wizardofvegas.com/guides/blackjack-survey//
DOA: double on anything
DAS: double after split

most 6-8 deck games in vegas are DOA and DAS



