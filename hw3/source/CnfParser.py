import argparse
import nltk
import os
import sys
import time

class Cell(object):

    Production = None
    R = -1

    def __init__(self, production, offset):
        self.Production = production
        self.R = offset

    def __str__(self):
        return '{} ({})'.format(str(self.Production), self.R)


class CustomSet(set):

    def __str__(self):
        text = '{'
        isFirst = True
        for x in self:
            if isFirst:
                isFirst = False
            else:
                text += ', '
            text += str(x)
        return text + '}'

class CnfParser(object):
    """A parser that applies the grammar to find out all available interpretations of a sentence."""

    grammar = None

    def __init__(self, grammar):
        self.grammar = grammar


    def __is_in_here(self, nonterminal, mySet) -> bool:
        if mySet is None:
            return False
        for item in mySet:
            assert type(item) == Cell
            if nonterminal == item.Production.lhs():
                return True
        return False

    def parse(self, tokens):
        length = len(tokens)

        table = self.__initialize_table_cache(length, tokens)


        for c_i in range(2, length + 1):
            for r_i in range(c_i - 2, -1, -1):
                # Break the range into two: a left and a right.
                for offset in range(r_i + 1, c_i):

                    for p in self.grammar.productions():
                        rhs = p.rhs()
                        if len(rhs) == 2 \
                            and self.__is_in_here(rhs[0], table[r_i][offset]) \
                            and self.__is_in_here(rhs[1], table[offset][c_i]):
                            table[r_i][c_i].add(Cell(p, offset))
                
        #self.print_table(table)

        # Backtrace:
        results = self.recursive_backtrace(self.grammar.start(), table, r_i=0, c_i=len(table[0]) - 1)
        return results

    def recursive_backtrace(self, lhs, table, r_i, c_i) -> []:
        results = []
        myCustomSet = table[r_i][c_i]
        cell = None
        for cell in myCustomSet:
            if cell.Production.lhs() == lhs:
                production_rhs = cell.Production.rhs()
                count = len(production_rhs)
                if count == 1:
                    results.append("({} {})".format(lhs, production_rhs[0]))
                elif count == 2:
                    assert r_i < cell.R
                    assert cell.R < c_i
                    results_left = self.recursive_backtrace(production_rhs[0], table, r_i, cell.R)
                    results_right = self.recursive_backtrace(production_rhs[1], table, cell.R, c_i)
                    for l in results_left:
                        for r in results_right:
                            results.append('({} ({} {}))'.format(lhs, l, r))
                else:
                    assert False
        return results
    
    def __initialize_table_cache(self, length, tokens) -> []:
        i = 0
        table = []
        for r_i in range(length):
            table.append([])
            for c_i in range(length + 1):
                if c_i == r_i:
                    # c_i chosen arbitrary out of c_i and r_i (which are equal).
                    table[r_i].append(tokens[c_i])
                elif c_i == i + 1:
                    this_set = CustomSet()
                    for p in self.grammar.productions(rhs=tokens[i]):
                        this_set.add(Cell(p, r_i))
                    table[r_i].append(this_set)
                elif c_i > i:
                    table[r_i].append(CustomSet())
                else:
                    table[r_i].append(None)
            i += 1
        #self.print_table(table)
        return table


    def print_table(self, table):
        #eprint()
        str_table = []
        for r_i in range(len(table)):
            str_table.append([])
            for c_i in range(len(table[0])):
                if table[r_i][c_i] is None:
                    str_table[r_i].append('')
                elif len(str(table[r_i][c_i])) > 0:
                    str_table[r_i].append(str(table[r_i][c_i]))
                else:
                    str_table[r_i].append('')

        longest_cols = [
            (max([len(str(r_i[i])) for r_i in table]) + 3)
            for i in range(len(table[0]))
        ]
        row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
        for r_i in str_table:
            eprint(row_format.format(*r_i))
 

    def parse_all_sentences(self, lines):
        totalNoOfParses = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            no_of_parses = 0
            tokens = nltk.word_tokenize(line)
            print(line)
            for interpretation in self.parse(tokens):
                interpretation_as_tree = nltk.Tree.fromstring(interpretation)
                print(interpretation_as_tree)
                no_of_parses += 1
            print('Number of parses: ', no_of_parses)
            print()
            totalNoOfParses = totalNoOfParses + no_of_parses
                    
        eprint('Average parses per sentence:', totalNoOfParses / len(lines))

def main():
    """Calls parse with the parameters passed on the command line."""

    # Input Validation:    
    parser = argparse.ArgumentParser(description='Parses the specified sentences using the specified grammar.')
    parser.add_argument('grammar_file_path', type=str, help='the name of the file containing the grammar.')
    parser.add_argument('sentence_file_path', type=str, help='the name of the file containing the sentences.')
    ns = parser.parse_args()

    # Load the grammar using NLTK:
    rules = nltk.data.load('file://' + ns.grammar_file_path, 'text')
    grammar = nltk.CFG.fromstring(rules)

    # Load the parser using NLTK:
    parser = CnfParser(grammar)

     # Iterate over each of the sentences in the sentences file,
    # writing the number of parses for each sentence:
    with open(ns.sentence_file_path, "r") as sentence_file:
        lines = sentence_file.readlines()
        parser.parse_all_sentences(lines)
    
    eprint('Done.')

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
