import time
import os
import sys
import functools
from trie_generator import trie_generator, load_trie, save_trie, load_trie_pickle, save_trie_pickle


def letter_boxed_solver(trie, all_letters, challenge_words=8):
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

    # need logic for finding words with different set of letters to check for
    # each position ie, if 'a' is chosen as the first letter, 'defghijkl' needs
    # to be chosen from for the next letter
    words = find_letter_boxed(trie, all_letters)
    print(words)
    running_total = 0
    for value in words.values():
        running_total += len(value)
    print("num words: ", running_total)
    print(challenge_words)
    print(int(challenge_words))
    solutions = find_all_word_chains(words, all_letters, int(challenge_words))
    print(f"Found {len(solutions)} solutions")

    return solutions


def find_letter_boxed(trie, letters):
    # given the 7 letters that a part of the spelling bee, find all words
    # that can be created from them, with the necessary letter passed in
    # as the first in the list of letters, if a word is found and does not
    # contain the needed letter, discard the word from the final list
    word_dict = {}
    sides = [letters[i: i + 3] for i in range(0, 12, 3)]

    for i, side in enumerate(sides):
        for letter in side:
            # Even though this is a nested loop it should only be 12 cycles,
            # they'll be long but still only 12
            start_node = trie.head.get(letter)

            if start_node:
                find_letter_boxed_helper(trie, start_node, word_dict, "",
                                         sides, i)

    return word_dict


def find_letter_boxed_helper(trie, curr_node, word_dict, curr_string,
                             letters, curr_side_idx):
    if not curr_node:
        return

    curr_string += curr_node.char
    if curr_node.is_word and len(curr_string) >= 3:
        first_letter = curr_string[0]
        if first_letter in word_dict:
            word_dict[first_letter].append(curr_string)
        else:
            word_dict[first_letter] = [curr_string]

    if not curr_node.children:
        return

    sides = [letters[i] for i in range(4) if i != curr_side_idx]
    for side in sides:
        for letter in side:
            child_node = curr_node.children.get(letter)
            if child_node:
                find_letter_boxed_helper(trie, child_node, word_dict,
                                         curr_string, letters,
                                         letters.index(side))

    return


def find_all_word_chains(word_dict, letters, max_words, max_solutions=100):
    solutions = []

    for words_in_solution in range(1, max_words + 1):
        def find_chains(current_chain, covered_letters, length):
            #debug_print(current_chain)
            if (length > words_in_solution):
                return []
            if len(covered_letters) == len(letters):
                solutions.append(current_chain)
                return []
            if len(solutions) >= max_solutions:
                return []

            last_letter = current_chain[-1][-1]
            for word in word_dict.get(last_letter, []):
                if word_dict not in current_chain:
                    new_covered_letters = covered_letters | set(word)
                    if len(new_covered_letters) > len(covered_letters):
                        find_chains(current_chain + [word], new_covered_letters, length + 1)

        for letter, word_list in word_dict.items():
            for word in word_list:
                find_chains([word], set(word), 1)

        if len(solutions) >= max_solutions:
            break

    #print(f"Found {len(solutions)} solutions")
    return solutions


def debug_print(chain):
    print(f"Chain: {' -> '.join(chain)}")
    print(f"Covered lettters: {set(''.join(chain))}")
    print()


if __name__ == '__main__':
    start_time = time.time()

    # trie_file_name = 'trie.json'
    trie_file_name = 'small_trie.pkl'
    if os.path.exists(trie_file_name):
        print('loading existing Trie')
        # trie = load_trie(trie_file_name).head
        trie = load_trie_pickle(trie_file_name)
        if not len(sys.argv) > 2:
            words = letter_boxed_solver(trie, sys.argv[1])
        else:
            words = letter_boxed_solver(trie, sys.argv[1], sys.argv[2])
            for solution in words:
                debug_print(solution)
        print(words)
    else:
        print("generating new trie from english word list")
        trie = trie_generator('common_words.txt')
        # save_trie(trie, trie_file_name)
        save_trie_pickle(trie, trie_file_name)
        if not len(sys.argv) > 2:
            words = letter_boxed_solver(trie, sys.argv[1])
        else:
            words = letter_boxed_solver(trie, sys.argv[1], sys.argv[2])
        print(words)

    solve_time = time.time() - start_time
    print(solve_time)

    print(trie.count_nodes())
