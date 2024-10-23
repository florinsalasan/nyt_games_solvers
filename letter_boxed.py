import time
import os
import sys
from trie_generator import trie_generator, load_trie, save_trie


def letter_boxed_solver(trie, all_letters, challenge_words=0):
    # Assumes that the input will split the order the letters so that
    # 3 letters in a row all make up each side of the box:
    # ie an input of abcdefghijkl will represent:
    #    a  b  c
    #  d         j
    #  e         k
    #  f         l
    #    g  h  i
    # and then I can create a script to solve the puzzle from there, can also
    # add an input that will only provide solutions that are equal to or less
    # than the number of words the challenge is (letter boxed has a line asking
    # users to try solving within x number of words)

    # as solutions are found add them to the list
    solutions = []

    # split the letters into 4 groups, 3 letters per group
    letters = [all_letters[i:i+3] for i in range(0, 12, 3)]

    # need logic for finding words with different set of letters to check for
    # each position ie, if 'a' is chosen as the first letter, 'defghijkl' needs
    # to be chosen from for the next letter, going to use helpers for this
    

    if challenge_words != 0:
        filter_solutions = [solution for solution in solutions
                            if len(solution) <= challenge_words]
        return filter_solutions

    return solutions


if __name__ == '__main__':
    start_time = time.time()

    trie_file_name = 'trie.json'
    if os.path.exists(trie_file_name):
        print('loading existing Trie')
        trie = load_trie(trie_file_name).head
        words = letter_boxed_solver(trie, sys.argv[1])
        print(words)
    else:
        print("generating new trie from english word list")
        trie = trie_generator('words_alpha.txt')
        save_trie(trie, trie_file_name)
        words = letter_boxed_solver(trie, sys.argv[1])
        print(words)

    solve_time = time.time() - start_time
    print(solve_time)

    print(trie.count_nodes())
