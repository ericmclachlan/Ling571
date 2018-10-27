import argparse
import nltk
import sys

        
def main():
    # Parse the command line arguments.
    # If none are provided, use the SVM classifier.
    parser = argparse.ArgumentParser(description='Generates parses, where possible, for the ')
    parser.add_argument('input_grammar_filename', type=str, help='The name of the file holding the feature-based grammar that you created to implement the necessary grammatical constraints.')
    parser.add_argument('input_sentence_filename', type=str, help='The name of the file holding the sentences to test for grammaticality and parse.')
    args = parser.parse_args()
    eprint(args)
    
    # 1.a. Load the grammar:
    with open(args.input_grammar_filename, "r") as f:
        grammar_as_text = f.read()
    grammar = nltk.grammar.FeatureGrammar.fromstring(grammar_as_text)

    # 1.b. Create a parser:
    parser = nltk.FeatureEarleyChartParser(grammar)

    # 2. Load the test sentences:
    # Iterate over each of the sentences in the sentences file,
    # writing the number of parses for each sentence:
    with open(args.input_sentence_filename, "r") as f:
        correct_count = 0
        line_count = 0
        sentences = f.readlines()
        for sentence in sentences:
            sentence = sentence.strip()
            line_count += 1
            eprint()
            eprint('Line {}: {}'.format(line_count, sentence))
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
                output_text = any_parse.pformat(margin=float("inf"))
                is_correct = True

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


if __name__ == "__main__":
    main()
