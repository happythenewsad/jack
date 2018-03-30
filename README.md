What is Jack?
=============

Jack is a Blackjack game engine written in python3. It is intended to be
easily configurable for different house rules and strategies of play. It can simulate thousands of Blackjack games per second on a single thread.


Instructions:
=============

Supported environment(s): MacOS 10.x

Required software: python 3.x, jupyter notebook (optional)

To run tests: 

    $ python3 test_runner.py

The best way to get a feel for the code/API is to open experiments.ipynb
with jupyter notebook, run the existing experiments, and create your own.



Gameplay Assumptions 
====================

stand on soft 17
8 deck shoe
4 other players. Active player is rightmost.
When shoe is finished during active hand, new shoe is drawn from and then play ends.
Penetration: 75%
Double down allowed after pair splitting
second splits allowed (easier to implement)
  should work as is, just implement playerHand correctly 




TODO
====

- allow variable betting (currently assumes every bet is 1 unit)
- implement different strategies
- Have logging configurable from notebook




Misc
====

Blackjack rules at casinos:

https://wizardofvegas.com/guides/blackjack-survey//
DOA: double on anything
DAS: double after split

most 6-8 deck games in vegas are DOA and DAS

House edge === expected loss

