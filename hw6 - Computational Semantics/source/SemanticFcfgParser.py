import argparse
import nltk
import sys

        
def main():
    # Parse the command line arguments.
    # If none are provided, use the SVM classifier.
    parser = argparse.ArgumentParser(description='Performs the parsing and compositional semantic analysis for Hw6.')
    parser.add_argument('input_grammar_filename', type=str, help='The name of the file holding the grammar with FOL semantic attachments that you created to implement the rule-to-rule style compositional semantic analysis.')
    parser.add_argument('input_sentences_filename', type=str, help='The name of the file holding the sentences to parse and perform semantic analysis on.')
    args = parser.parse_args()
    eprint(args)
    
    # 1.a. Load the grammar:
    with open(args.input_grammar_filename, "r") as f:
        grammar_as_text = f.read()
    grammar = nltk.grammar.FeatureGrammar.fromstring(grammar_as_text)

    # 1.b. Create a parser:
    parser = nltk.parse.FeatureChartParser(grammar, trace=0)

    # 2. Load the test sentences:
    # Iterate over each of the sentences in the sentences file,
    # writing the number of parses for each sentence:
    with open(args.input_sentences_filename, "r") as f:
        correct_count = 0
        line_count = 0
        sentences = f.readlines()
        for sentence in sentences:
            sentence = sentence.strip()
            line_count += 1
            eprint()
            print(sentence)
            if len(sentence) == 0:
                continue
            

            if sentence[0] == '*':
                is_supposed_to_be_invalid = True
                sentence = sentence[1:]
            else:    
                is_supposed_to_be_invalid = False

            # Try parse the sentence
            try:
                any_parse = parser.parse_one(nltk.word_tokenize(sentence))
            except Exception as e: 
                eprint(e)
                any_parse = None

            is_correct = False
            # If possible, print the parse:
            if any_parse is None:
                output_text = ''
                if is_supposed_to_be_invalid:
                    is_correct = True
            else:
                #output_text = any_parse.pformat(margin=float("inf"))
                #expression = nltk.sem.Expression.fromstring(output_text)
                output_text = str(any_parse.label()['SEM'].simplify())
                is_correct = '\\' not in output_text

            print(output_text)

            if is_correct:
                correct_count += 1
                eprint("Correct!")
            else:
                eprint("Wrong!")
    eprint('Found {}/{} acceptible sentences.'.format(correct_count, line_count))


def eprint(*args, **kwargs):
    """Print to STDERR (as opposed to STDOUT)"""
    print(*args, file=sys.stderr, **kwargs)
    pass


if __name__ == "__main__":
    main()
