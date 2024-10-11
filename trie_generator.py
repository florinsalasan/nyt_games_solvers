class TrieNode:
    def __init__(self, is_word: bool, char: str,
                 children: list['TrieNode'], parent: ('TrieNode' or None)):
        self.is_word = is_word
        self.char = char
        self.children = children
        self.parent = parent


class Trie:
    # Won't implement delete or it's helper for now, shouldn't be needed
    def __init__(self):
        self.head: list[TrieNode] = []

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
                            children=[],
                            parent=None)
        if len(word) == 1:
            new_node.is_word = True
            return

        # Call the insert helper on the rest of the word continuing
        # from the new_node
        self.insert_helper(word[1:], new_node)
        self.head.append(new_node)

    def insert_helper(self, remaining_data, curr_node):
        # recursively insert with some extra parameters compared to insert
        # base case is remaining_data = "" so we return as we're done mark
        # parent node as the end of a word?
        if (remaining_data == ""):
            # TODO: determine if this line is needed
            # curr_node.parent.is_word = True
            return

        # Loop over the curr_node's children to find the node that represents
        # the first letter of the data we're inserting
        for i in range(len(curr_node.children)):
            if (curr_node.children[i] == remaining_data[0]):
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
                children=[],
                parent=curr_node
        )
        if (len(remaining_data) == 1):
            new_node.is_word = True

        curr_node.children.append(new_node)
        self.insert_helper(remaining_data[1:], new_node)

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


def trie_generator() -> Trie:
    # TODO: read text file with all english words, build out a trie tree in
    # here. Will make helpers for the Trie structure, and for serializing it.
    file = open("words_alpha.txt", "r")
    print(file.readline())
    print(file.readline())
    print(file.readline())
    print(file.readline())
    return


if __name__ == '__main__':
    trie_generator()
