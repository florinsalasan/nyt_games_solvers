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
python spelling_bee.py {7 daily letters} {trie.pkl (optional)}
```

Defaults to creating the smaller trie with ~20k words, if something other than 'small_trie.pkl' is
passed in as the trie parameter it will generate the larger trie with ~360k words, not all of 
them are accepted by the NYT games in my experience.

## Letter Boxed Solver
Generated a smaller trie that only contains commonly used words to severly limit the search space,
and instead of generating every possible solution I instead limit it to the first 10 results, each
solution starting with a different word. Otherwise the runtime would be insanely long, first attempt
took around an hour while the limited one on the small trie took under 2 seconds

## How to use the Letter Boxed Solver
Used dolph's dictionary repo to grab the ~20k most common english words and copying them into a
text file in the same directory as the script as 'common_words.txt'. The script then creates and 
serializes the trie if it doesn't exist yet, or reads the serialized trie in. From there simply run
```
python letter_boxed.py {12 puzzle letters} {Max number of words for the solution}
```

The 12 letters should have the 3 letters for each side together, the order of which side is passed in
as arguments doesn't matter. For example:

```
   a  b  c 
d           g
e           h
f           i
   j  k  l 
```
can be inputted in as abcdefghijkl, or jklabcghidef or any other order of the sides. Even the letters
within the sides can be rearranged as long as the 3 letters are grouped together. And then the max number
of words is the challenge numbers, and the solutions generated typically don't reach the limit on the number
of words in the chain.

### Extra notes for Spelling Bee
When I downloaded the words_alpha.txt file I removed all instances of the '^M' character
with a script. Then when reading in the file with file.readlines() python adds in newline 
characters for each word, so I removed those as well before placing inserting every word
into the Trie structure otherwise I found that it would mark the end of a word incorrectly.

### Resources used:

- dwyl's [english-words](https://github.com/dwyl/english-words) repository
- dolph's [dictionary](https://github.com/dolph/dictionary) repository for a more concentrated word list
- ThePrimeagen's course on [data structures and algorithms](https://frontendmasters.com/courses/algorithms/) on FrontendMasters

## WARNING:
The generated Trie is around 500-600 MB in size if you serialize with json, not meant to be used on devices with
small amounts of storage space. Also I removed the to and from dict methods, so those would have to be rewritten

### TODO:
- [x] Look into other methods of serializing the Trie like protobuf or messagepack -> Changed to pickling, now takes ~1.5s for spelling_bee instead of ~9 that json was taking to rebuild the trie
- [ ] Add tests?
- [ ] Reword insert method to insert words that end in non-alphabet characters like newline or '^M'
- [ ] Change the output to be better formatted, possibly return a dict of words based on length and special category for pangrams
- [x] Add other games -> Added letter boxed creates 10 solutions would prefer to tweak it so that multiple solutions cannot begin with the same word
