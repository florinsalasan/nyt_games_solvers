def spelling_bee_solver():
    return False
    # Took the find function out of trie_generator since it's specific
    # to 7 letter spelling bee requirements

    def find(self, letters):
        # given the 7 letters that a part of the spelling bee, find all words
        # that can be created from them, with the necessary letter passed in
        # as the first in the list of letters, if a word is found and does not
        # contain the needed letter, discard the word from the final list
        must_include_letter = letters[0]
        words = []
        for i in range(len(letters)):
            start_node = None
            for j in range(len(self.head)):
                if letters[i] == self.head[j].char:
                    start_node = self.head[j]

            # Should mean that a starting node doesn't exist. This should never
            # happen for solving the spelling bee. since I'm building a Trie
            # that contains 360k+ english words
            if start_node is None:
                continue

            # Otherwise, call the find_helper to find all words starting with
            # each of the letters we passed in
            endings = self.find_helper(start_node, [], "")

            for ending in endings:
                if i == 0 or ending.contains(must_include_letter):
                    words.append(ending)

        return words

    def find_helper(self, curr_node, endings, curr_string, letters):
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
        if curr_node.is_word and not endings.contains(curr_string):
            # if we've reached the end of a word add it to the endings
            endings.append(curr_string)

        if len(curr_node.children) == 0:
            # No children to delve deeper into, we're at a leaf
            return endings

        new_endings = []
        for i in range(len(letters)):
            recursed_endings = self.find_helper(
                    self.find_letter_node_in_children(letters[i], curr_node),
                    endings,
                    curr_string
            )

            recursed_endings = [ending for ending in recursed_endings if
                                ending not in new_endings]

            new_endings = list(set(new_endings + recursed_endings))

        endings = list(set(new_endings + endings))
        return endings


if __name__ == '__main__':
    spelling_bee_solver()
