import sys


class TrieNode:
    node_id_counter = 0

    def __init__(self, is_word: bool, char: str,
                 children: list['TrieNode']):
        self.is_word = is_word
        self.char = char
        self.children = children
        self.node_id = TrieNode.node_id_counter
        TrieNode.node_id_counter += 1

    def __str__(self, indent=0):
        output = '   ' * indent + f"char: {self.char}, is_word: {self.is_word}\n"
        for child in self.children:
            output += child.__str__(indent + 1)
        return output

    def to_dict(self):
        return {
            'char': self.char,
            'is_word': self.is_word,
            'node_id': self.node_id,
            'children': [child.to_dict() for child in self.children]
        }

    @classmethod
    def from_dict(cls, data):
        # Take in data about a node and turns it into a TrieNode from a dictionary

        node = TrieNode(
                is_word=data['is_word'],
                char=data['char'],
                children=[cls.from_dict(child) for child in data['children']]
        )
        node.node_id = data['node_id']

        return node


class Trie:
    # Won't implement delete or it's helper for now, shouldn't be needed
    def __init__(self):
        self.head: list[TrieNode] = []

    def __str__(self):
        output = ""
        for node in self.head:
            output += node.__str__()
        return output

    def insert(self, word):
        # We insert the first char with this method, and then call
        # insert_helper to insert the rest of the string
        for i in range(len(self.head)):
            if self.head[i].char == word[0]:
                self.insert_helper(word[1:], self.head[i])
                return

        # If we get here, we have to insert a new TrieNode into the head
        new_node = TrieNode(is_word=False,
                            char=word[0],
                            children=[])
        if len(word) == 1:
            new_node.is_word = True
            self.head.append(new_node)
            return

        # Call the insert helper on the rest of the word continuing
        # from the new_node
        self.insert_helper(word[1:], new_node)
        # This doesn't dupe since we return early in the len == 1 case
        self.head.append(new_node)

    def insert_helper(self, remaining_data, curr_node):
        # recursively insert with some extra parameters compared to insert
        # base case is remaining_data = ""
        if (remaining_data == ""):
            # TODO: determine if this line is needed
            return

        # Loop over the curr_node's children to find the node that represents
        # the first letter of the data we're inserting
        for i in range(len(curr_node.children)):
            if (curr_node.children[i].char == remaining_data[0]):
                return self.insert_helper(
                    remaining_data[1:],
                    curr_node.children[i]
                )

        # If we reach this point it means that we looped over the curr_node's
        # children with parts of the string still needed to insert. So we
        # have to create new node to insert, and mark it as a word if it's the
        # last letter
        new_node = TrieNode(
                is_word=False,
                char=remaining_data[0],
                children=[]
        )
        if (len(remaining_data) == 1):
            new_node.is_word = True

        curr_node.children.append(new_node)
        self.insert_helper(remaining_data[1:], new_node)

    def find_spelling_bee(self, letters):
        # given the 7 letters that a part of the spelling bee, find all words
        # that can be created from them, with the necessary letter passed in
        # as the first in the list of letters, if a word is found and does not
        # contain the needed letter, discard the word from the final list
        must_include_letter = letters[0]
        words = []
        for i in range(len(letters)):
            start_node = None
            for node in self.head:
                if letters[i] == node.char:
                    start_node = node

            # Should mean that a starting node doesn't exist. This should never
            # happen for solving the spelling bee. since I'm building a Trie
            # that contains 360k+ english words
            if start_node is None:
                continue

            # Otherwise, call the find_helper to find all words starting with
            # each of the letters we passed in
            endings = self.find_spelling_bee_helper(start_node, [], "", letters)

            for ending in endings:
                if i == 0 or must_include_letter in ending:
                    words.append(ending)

        return words

    def find_spelling_bee_helper(self, curr_node, endings, curr_string, letters):
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
            recursed_endings = self.find_spelling_bee_helper(
                    self.find_letter_node_in_children(letters[i], curr_node),
                    endings,
                    curr_string,
                    letters
            )

            recursed_endings = [ending for ending in recursed_endings if
                                ending not in new_endings]

            new_endings = list(set(new_endings + recursed_endings))

        endings = list(set(new_endings + endings))
        return endings

    def find_letter_node_in_children(self, char, node):
        # if either char or the current node is not defined, return early
        if char is None or node is None:
            return None

        # Loop over the children of the current node to look a match
        for i in range(len(node.children)):
            if node.children[i].char == char:
                return node.children[i]

        # If we got here there is no match, so return None
        return None

    def count_nodes(self):
        stack = self.head
        count = 0

        while stack:
            node = stack.pop()
            count += 1
            stack.extend(node.children)

        return count

    def to_dict(self):
        nodes = []
        for child_trie in self.head:
            nodes.append(child_trie.to_dict())

        return nodes

    @classmethod
    def from_dict(cls, data):
        trie = cls()
        trie.head = [TrieNode.from_dict(data[i]) for i in range(len(data))]

        return trie


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
