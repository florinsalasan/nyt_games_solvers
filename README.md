# NYT Games Solver(s)

I'm tired of not finding the panagram in the Spelling Bee game so I wanted
to write a script to find all possible panagrams for me. Still thinking about
whether or not I want to work on other games afterwards.

## Spelling Bee Solver

General idea I think will be to spend some time taking a list of all english words
and throwing them into a Trie tree. Then serializing it so that it doesn't have to 
be redone everytime, and then the input to the solver will be the 7 letters from 
the daily puzzle. Then it's a matter traversing through the tree checking for each letter 
over and over again, collecting words along the way. Time to build it
