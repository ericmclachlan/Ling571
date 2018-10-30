import argparse
import math
import nltk
import re
import sys


class ParseSummary:
    """This object wraps the result of a parse or even a partial parse."""

    def __init__(self, text : str, log_probability : float):
        self.log_probability = log_probability
        self.text = text



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

class PcnfParser(object):
    """A parser that applies the grammar to find out all available interpretations of a sentence."""

    grammar = None
    log_probability_of_production = {}
    min_log_probability = None

    def __init__(self, pcfg_filename):
        
        start = None
        # Read the file:
        with open(pcfg_filename, "r") as f:
            lines = f.readlines()
        # Parse the file's contents:
        productions = []
        for line in lines:
            matches = re.match("(\S+)\s*->\s*(\S+)(\s+\S+)?\s+\[([0-9.]+)\]?", line)
            groups = matches.groups()
            group_count = len(groups)
            assert group_count == 4
            lhs = nltk.Nonterminal(groups[0].strip())
            if groups[2] is None:
                production = nltk.Production(lhs, [ groups[1].strip('\'') ])
            else:
                production = nltk.Production(lhs, [ nltk.Nonterminal(groups[1].strip()), nltk.Nonterminal(groups[2].strip()) ])
            log_probability = math.log(float(groups[3].strip()))
            
            # Read the Production rule:
            if (start is None):
                start = lhs

            productions.append(production)
            self.log_probability_of_production[production] = log_probability
            if self.min_log_probability is None or math.fabs(log_probability) > math.fabs(self.min_log_probability):
                self.min_log_probability = log_probability
        self.grammar = nltk.grammar.CFG(start, productions, False)
        # Make it much less probable than the actual minimum_log_probability but still non-zero.
        self.min_log_probability = self.min_log_probability / 2


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
        for cell in myCustomSet:
            if cell.Production.lhs() == lhs:
                production_rhs = cell.Production.rhs()
                count = len(production_rhs)
                if count == 1:
                    results.append(ParseSummary("({} {})".format(lhs, production_rhs[0]), self.log_probability_of_production[cell.Production]))
                elif count == 2:
                    assert r_i < cell.R
                    assert cell.R < c_i
                    results_left = self.recursive_backtrace(production_rhs[0], table, r_i, cell.R)
                    results_right = self.recursive_backtrace(production_rhs[1], table, cell.R, c_i)
                    for l in results_left:
                        for r in results_right:
                                results.append(ParseSummary('({} {} {})'.format(lhs, l.text, r.text), self.log_probability_of_production[cell.Production] + l.log_probability + r.log_probability))
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
  
        
def main():
    # Parse the command line arguments.
    # Parse the command line arguments.
    # If none are provided, use the SVM classifier.
    parser = argparse.ArgumentParser(description='Code implementing PCKY')
    parser.add_argument('input_PCFG_file', type=str, help='The name of the file holding the induced PCFG grammar to be read.')
    parser.add_argument('test_sentence_filename', type=str, help='The name of the file holding the test sentences to be parsed.')
    args = parser.parse_args()
    eprint(args)
    
    # Load the parser using NLTK:
    parser = PcnfParser(args.input_PCFG_file)

    # Iterate over each of the sentences in the sentences file,
    # writing the number of parses for each sentence:
    with open(args.test_sentence_filename, "r") as f:
        lines = f.readlines()
        totalNoOfParses = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            no_of_parses = 0
            tokens = nltk.word_tokenize(line)
            #print(line)
            interpretations = parser.parse(tokens)
            max_prob = None
            best_interpretation = ''
            for interpretation in interpretations:
                if max_prob is None or math.fabs(interpretation.log_probability) < math.fabs(max_prob):
                    max_prob = interpretation.log_probability
                    best_interpretation = interpretation.text
            print(best_interpretation)
            no_of_parses += 1
            totalNoOfParses = totalNoOfParses + no_of_parses

    #eprint('Done.')

def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
