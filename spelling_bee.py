import json
import time
import os
import sys
from trie_generator import Trie, trie_generator


def load_trie(trie_file_name):
    with open(trie_file_name, 'r') as file:
        data = json.load(file)
        new_trie = Trie()
        new_trie.head = Trie.from_dict(data)
        return new_trie


def save_trie(trie, filename):
    with open(filename, 'w') as f:
        json.dump(trie.to_dict(), f, indent=4)


def spelling_bee_solver(trie, letters):
    words = trie.find_spelling_bee(letters)
    filtered_words = [word for word in words if all(letter in word for letter in letters)]
    return filtered_words


if __name__ == '__main__':
    start_time = time.time()

    trie_file_name = 'trie.json'
    if os.path.exists(trie_file_name):
        print('loading existing Trie')
        trie = load_trie(trie_file_name).head
        words = spelling_bee_solver(trie, sys.argv[1])
        print(words)
    else:
        print("generating new trie from english word list")
        trie = trie_generator('words_alpha.txt')
        save_trie(trie, trie_file_name)
        words = spelling_bee_solver(trie, sys.argv[1])
        print(words)

    solve_time = time.time() - start_time
    print(solve_time)

    print(trie.count_nodes())
