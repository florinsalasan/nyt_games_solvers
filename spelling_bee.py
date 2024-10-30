import time
import os
import sys
from trie_generator import trie_generator, load_trie, save_trie, load_trie_pickle, save_trie_pickle


def spelling_bee_solver(trie, letters):
    words = find_spelling_bee(trie, letters)
    filtered_words = [word for word in words
                      if all(letter in word for letter in letters)]
    return filtered_words


def find_spelling_bee(trie, letters):
    # given the 7 letters that a part of the spelling bee, find all words
    # that can be created from them, with the necessary letter passed in
    # as the first in the list of letters, if a word is found and does not
    # contain the needed letter, discard the word from the final list
    must_include_letter = letters[0]
    words = []
    for i in range(len(letters)):
        start_node = trie.head.get(letters[i])

        if start_node is None:
            continue

        # Otherwise, call the find_helper to find all words starting with
        # each of the letters we passed in
        endings = find_spelling_bee_helper(trie, start_node, [], "", letters)

        for ending in endings:
            # if it's the first letter being checked automatically accept the
            # word as it contains the mandatory letter, otherwise check for it
            if i == 0 or must_include_letter in ending:
                words.append(ending)

    return words


def find_spelling_bee_helper(trie, curr_node, endings, curr_string, letters):
    # the curr_node will be a node in the head of the Trie that matches
    # one of the 7 letters that are passed in to find(). From there DFS
    # until we hit a leaf, then pop until it's possible to walk a different
    # path, only walk paths that are the letters passed in
    if curr_node is None or not curr_node:
        # Honestly don't remember why I included this in my trie
        # implmenetation in TypeScript, the comments say that this
        # indicates that the branch has been fully traversed, I'm using
        # find_letter_node_in_children which can return None so this is
        # helpful after all
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
        child_node = curr_node.children.get(letters[i])
        recursed_endings = find_spelling_bee_helper(
                trie,
                child_node,
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
        words = spelling_bee_solver(trie, sys.argv[1])
        print(words)
    else:
        print("generating new trie from english word list")
        trie = trie_generator('words_alpha.txt')
        # save_trie(trie, trie_file_name)
        save_trie_pickle(trie, trie_file_name)
        words = spelling_bee_solver(trie, sys.argv[1])
        print(words)

    solve_time = time.time() - start_time
    print(solve_time)

    print(trie.count_nodes())
