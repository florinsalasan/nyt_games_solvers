import time
import os
import sys
from trie_generator import trie_generator, load_trie, save_trie, load_trie_pickle, save_trie_pickle


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

    # split the letters into 4 groups, 3 letters per group
    letters = [all_letters[i:i+3] for i in range(0, 12, 3)]

    # need logic for finding words with different set of letters to check for
    # each position ie, if 'a' is chosen as the first letter, 'defghijkl' needs
    # to be chosen from for the next letter, going to use helpers for this

    words = find_letter_boxed(trie, letters)

    if challenge_words != 0:
        filter_solutions = [word for word in words
                            if len(word) >= 3]
        return filter_solutions

    # Given all of the words that can be made in the box, we just
    # need to connect them now from tail of one to start of another
    # until all letters are covered, could use another helper here

    solutions = words_to_solutions(words)

    return solutions


def words_to_solutions(words):
    print(words)
    return


def find_letter_boxed(trie, letters):
    words = []
    for i in range(len(letters)):
        for j in range(len(letters[i])):
            start_node = None
            for node in trie.head:
                if letters[i][j] == node.char:
                    start_node = node

            # Should mean that a starting node doesn't exist. This should never
            # happen for solving the spelling bee. since I'm building a Trie
            # that contains 360k+ english words
            if start_node is None:
                continue

            # Otherwise, call the find_helper to find all words starting with
            # each of the letters we passed in
            endings = find_letter_boxed_helper(trie, start_node, [], "", letters)

            for ending in endings:
                words.append(ending)

    return words


def find_letter_boxed_helper(trie, curr_node, endings, curr_string, letters):
    if not curr_node or curr_node is None:
        return endings
    curr_string += curr_node.char

    if curr_node.is_word and curr_string not in endings:
        # if we've reached the end of a word add it to the endings
        endings.append(curr_string)

    if len(curr_node.children) == 0:
        # No children to delve deeper into, we're at a leaf
        return endings

    new_endings = []
    for i in range(len(letters)):
        if curr_node.char not in letters[i]:
            for j in range(len(letters[i])):
                recursed_endings = find_letter_boxed_helper(
                        trie,
                        trie.find_letter_node_in_children(letters[i][j], curr_node),
                        endings,
                        curr_string,
                        letters
                )

                recursed_endings = [ending for ending in recursed_endings if
                                    ending not in new_endings]

                new_endings = list(set(new_endings + recursed_endings))

    endings = list(set(new_endings + endings))
    return endings


if __name__ == '__main__':
    start_time = time.time()

    # trie_file_name = 'trie.json'
    trie_file_name = 'trie.pkl'
    if os.path.exists(trie_file_name):
        print('loading existing Trie')
        # trie = load_trie(trie_file_name).head
        trie = load_trie_pickle(trie_file_name)
        words = letter_boxed_solver(trie, sys.argv[1])
        print(words)
    else:
        print("generating new trie from english word list")
        trie = trie_generator('words_alpha.txt')
        # save_trie(trie, trie_file_name)
        save_trie_pickle(trie, trie_file_name)
        words = letter_boxed_solver(trie, sys.argv[1])
        print(words)

    solve_time = time.time() - start_time
    print(solve_time)

    print(trie.count_nodes())
