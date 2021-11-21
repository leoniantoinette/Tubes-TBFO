import grammar_converter

class Node:
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

class Parser:
    def __init__(self, grammar, sentence):
        self.parse_table = None
        self.prods = {}
        self.grammar = grammar_converter.convert_grammar(grammar_converter.read_grammar(grammar))

    def __call__(self, sentence):
        self.input = sentence.split()
        self.parse()

    def parse(self):
        length = len(self.input)
        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(self.input):
            for rule in self.grammar:
                if f"'{word}'" == rule[1]:
                    self.parse_table[0][i].append(Node(rule[0], word))

        # testing
        # print(self.parse_table)

        for words_to_consider in range(2, length + 1):
            for starting_cell in range(0, length - words_to_consider + 1):
                for left_size in range(1, words_to_consider):
                    right_size = words_to_consider - left_size

                    left_cell = self.parse_table[left_size - 1][starting_cell]
                    right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.parse_table[words_to_consider - 1][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )
        # testing
        # print(self.parse_table)

    def print_tree(self):
        start_symbol = self.grammar[0][0]
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            print("Accepted!")
            #     print("\nPossible parse(s):")
            # trees = [generate_tree(node) for node in final_nodes]
            # if output:
            #     for tree in trees:
            #         print(tree)
            # else:
            #     return trees
        else:
            print("Syntax error!")