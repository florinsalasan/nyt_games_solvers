# NYT Games Solver(s)

I'm tired of not finding the pangram in the Spelling Bee game so I wanted
to write a script to find all possible pangrams for me. Still thinking about
whether or not I want to work on other games afterwards.

## Spelling Bee Solver

General idea I think will be to spend some time taking a list of all english words
and throwing them into a Trie tree. Then serializing it so that it doesn't have to 
be redone everytime, and then the input to the solver will be the 7 letters from 
the daily puzzle. Then it's a matter traversing through the tree checking for each letter 
over and over again, collecting words along the way. 

## How to use the Spelling Bee Solver
Using dwyl's repository I downloaded a copy of his words_alpha.txt file and placed it in
the same directory as the python scripts. From there simply run 

```
python spelling_bee.py {7 daily letters}
```

When inputting the 7 letters, make the mandatory letter the first. For example if
the 7 letters in alphabetical order are 'abcdefg' and the necessary letter is 'd',
the parameter should be passed in as 'd{remaining 6 letters in any order}'. The script
will return a list of pangrams that can be made from the 7 letters, some may not 
be accepted by the NYT game as this is a list that contains some extremely obscure words.
Feel free to replace the list with other ones.

### Extra notes for Spelling Bee
When I downloaded the words_alpha.txt file I removed all instances of the '^M' character
with a script. Then when reading in the file with file.readlines() python adds in newline 
characters for each word, so I removed those as well before placing inserting every word
into the Trie structure otherwise I found that it would mark the end of a word incorrectly.


### Resources used:

- dwyl's [english-words](https://github.com/dwyl/english-words) repository
- ThePrimeagen's course on [data structures and algorithms](https://frontendmasters.com/courses/algorithms/) on FrontendMasters

## WARNING:
The generated Trie is around 500-600 MB in size, not meant to be used on devices with
small amounts of storage space. 

### TODO:
- [x] Look into other methods of serializing the Trie like protobuf or messagepack -> Changed to pickling, now takes ~1.5s for spelling_bee instead of ~9 that json was taking to rebuild the trie
- [ ] Add tests?
- [ ] Reword insert method to insert words that end in non-alphabet characters like newline or '^M'
- [ ] Change the output to be better formatted, possibly return a dict of words based on length and special category for pangrams
- [ ] Add other games
