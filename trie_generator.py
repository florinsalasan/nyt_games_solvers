import json
import pickle
import sys


class TrieNode:
    node_id_counter = 0

    def __init__(self, is_word: bool, char: str):
        self.is_word = is_word
        self.char = char
        self.children = {}
        self.node_id = TrieNode.node_id_counter
        TrieNode.node_id_counter += 1

    def __str__(self, indent=0):
        output = '   ' * indent + f"char: {self.char}, is_word: {self.is_word}\n"
        for child in self.children:
            output += child.__str__(indent + 1)
        return output


class Trie:
    # Won't implement delete or it's helper for now, shouldn't be needed
    def __init__(self):
        self.head: list[TrieNode] = {}

    def __str__(self):
        output = ""
        for node in self.head:
            output += node.__str__()
        return output

    def insert(self, word):
        if word[0] not in self.head:
            self.head[word[0]] = TrieNode(is_word=False, char=word[0])

        self.insert_helper(word[1:], self.head[word[0]])

    def insert_helper(self, remaining_data, curr_node):
        if not remaining_data:
            curr_node.is_word = True
            return

        if remaining_data[0] not in curr_node.children:
            curr_node.children[remaining_data[0]] = TrieNode(is_word=False, char=remaining_data[0])

        self.insert_helper(remaining_data[1:], curr_node.children[remaining_data[0]])

    def find_letter_node_in_children(self, char, node):
        return node.children.get(char)

    def count_nodes(self):
        stack = list(self.head.values())
        count = 0

        while stack:
            node = stack.pop()
            count += 1
            stack.extend(node.children.values())

        return count


def trie_generator(file_name) -> Trie:
    test_trie = Trie()

    file = open(file_name, "r")
    lines = file.readlines()
    for i in range(len(lines)):
        curr_word = lines[i]
        if curr_word[-1] == '\n':
            curr_word = curr_word[:-1]
        test_trie.insert(curr_word)

    return test_trie


def load_trie(trie_file_name):
    with open(trie_file_name, 'r') as file:
        data = json.load(file)
        new_trie = Trie()
        new_trie.head = Trie.from_dict(data)
        return new_trie


def save_trie(trie, filename):
    with open(filename, 'w') as f:
        json.dump(trie.to_dict(), f, indent=4)


def load_trie_pickle(trie_file_name):
    with open(trie_file_name, 'rb') as f:
        loaded_trie = pickle.load(f)
        return loaded_trie


def save_trie_pickle(trie, filename):
    with open(filename, 'wb') as f:
        pickle.dump(trie, f)
