from __future__ import print_function
import argparse
import sys
import nltk
from collections import defaultdict

class Transition:
    """Encapsulates metadata related to productions."""
    
    def __init__(self, production, terminalDict):
        self.Production = production
        self.Terminals = list()
        self.Nonterminals = list()
        self.TerminalDict = terminalDict
        rhs = production.rhs()
        for item in rhs:
            if type(item) is nltk.grammar.Nonterminal:
                self.Nonterminals.append(item)
            else:
                assert type(item) == str
                self.Terminals.append(item)


    def IsNice(self) -> bool:
        """Returns True if the transition is nice, otherwise False."""
        if (len(self.Nonterminals) == 2 and len(self.Terminals) == 0) or (len(self.Nonterminals) == 0 and len(self.Terminals) == 1):
            return True
        else:
            return False

    def IsUnitProduction(self) -> bool:
        return len(self.Terminals) == 0 and len(self.Nonterminals) == 1

    def __str__(self) -> str:
        return str(self.Production)

class ConvertToCnf:
    """Converts a grammar to Chomsky Normal Form (CNF)."""

    def __init__(self, grammarFilePath):
        rules = nltk.data.load('file://' + grammarFilePath, 'text')
        self.grammar = nltk.CFG.fromstring(rules)
        eprint('Original Grammar:')
        eprint(self.grammar)
        eprint()
        self.TerminalDict = defaultdict(lambda : None)

    def Convert(self):
        niceList = list()
        naughtyList = list()
        for naughty in self.grammar.productions():
            transition = Transition(naughty, self.TerminalDict)
            self.AddToList(niceList, naughtyList, transition)
        
        #self.DisplayAll(niceList, naughtyList)

        # Hybrid Productions
        naughtyList = self.ConvertHybridProductions(niceList, naughtyList)
        
        #self.DisplayAll(niceList, naughtyList)

        naughtyList = self.ConvertUnitProductions(niceList, naughtyList)
        
        #self.DisplayAll(niceList, naughtyList)

        naughtyList = self.ConvertChainsToNonterminalPairs(niceList, naughtyList)

        self.DisplayAll(niceList, naughtyList)

        #assert len(naughtyList) == 0

        #newProductions = list()
        #for niceTransition in niceList:
        #    newProductions.append(niceTransition.Production)
        #newGrammar = nltk.grammar.CFG(self.grammar._start, newProductions)
        #assert newGrammar.is_chomsky_normal_form
        #eprint()
        #eprint('Final Grammar:')
        #eprint(newGrammar)

        eprint('Conversion Completed.')
        
    def ConvertHybridProductions(self, niceList, naughtyList):
        eprint('Convert Hybrid Productions:')
        newNaughtyList = list()
        for naughty in naughtyList:
            # Check if there are any non-terminals:
            noOfTerminals = len(naughty.Terminals)
            if noOfTerminals > 0:
                #eprint('Replacing ', naughty.Production, ' with:')
                terminalToNonterminalLookup = dict()
                for terminal in naughty.Terminals:
                    # Get a unique symbol for our terminal.
                    symbol = self.GetUniqueNonterminalName(terminal)
                    # Map a new non-terminal to the terminal
                    nonterminalForTerminal = nltk.grammar.Nonterminal(symbol)
                    self.TerminalDict[symbol] = nonterminalForTerminal
                    terminalToNonterminalLookup[terminal] = nonterminalForTerminal
                    newProduction = nltk.grammar.Production(nonterminalForTerminal, (terminal,))
                    newTransition1 = Transition(newProduction, self.TerminalDict)
                    self.AddToList(niceList, newNaughtyList, newTransition1)
                # Replace all the (bad) references to the terminals with (good) references to nonterminals.
                newRhs = tuple()
                for x in naughty.Production._rhs:
                    if type(x) == str:
                        nonterminal = terminalToNonterminalLookup[terminal]
                        newRhs= newRhs + (nonterminal,)
                    else:
                        newRhs= newRhs + (x,)
                # We have made this naughty child nice.
                naughtyToNice = Transition(nltk.grammar.Production(naughty.Production._lhs, newRhs), self.TerminalDict)
                assert len(naughtyToNice.Terminals) < noOfTerminals
                assert len(naughtyToNice.Terminals) == 0
                self.AddToList(niceList, newNaughtyList, naughtyToNice)
            else:
                assert len(naughty.Nonterminals) > 0
                # Keep this child on the naughty list... We'll deal with him soon.
                newNaughtyList.append(naughty)
        # Update the naughty list.
        naughtyList = newNaughtyList
        return naughtyList

    def ConvertUnitProductions(self, niceList, naughtyList):
        eprint('Convert Unit Productions:')
        i = 1   # Force entering the loop once.
        while i > 0:
            i = 0
            newNaughtyList = list()
            for naughty in naughtyList:
                assert len(naughty.Terminals) == 0
                if naughty.IsUnitProduction():
                    i += 1
                    #eprint('Removing: ', naughty.Production)

                    # Note: This step does not remove any transitions. 
                    # It only adds near-duplicates with the aim of remove the unit productions.

                    # Look for matching transitions in both the naughtyList and the niceList.
                    # If a match is found, then map the LHS of the naughty transition 
                    # to a clone of the matching transition's RHS production rule.
                    for transition in list(set().union(niceList, naughtyList)):
                        if (transition.Production._lhs,) == naughty.Production._rhs:
                            newTransition1 = Transition(nltk.grammar.Production(naughty.Production._lhs, transition.Production._rhs, ), self.TerminalDict)
                            self.AddToList(niceList, newNaughtyList, newTransition1)
                    # Swallow the production. i.e. the naughty transition is not added to the newNaughtyList.
                else:
                    # Save non-unit-production transitions for later. We'll deal with them next.
                    newNaughtyList.append(naughty)
            # Update the naughty list.
            naughtyList = newNaughtyList
        return naughtyList

    def ConvertChainsToNonterminalPairs(self, niceList, naughtyList):
        eprint('Convert Chains To Nonterminals Pairs:')
        while len(naughtyList) > 0:
            newNaughtyList = list()
            for naughty in naughtyList:
                #eprint('Replacing ', naughty.Production, ' with:')
                noOfNonterminals = len(naughty.Production._rhs)
                assert noOfNonterminals > 2
                lhs = naughty.Production._lhs
                assert type(lhs) == nltk.grammar.Nonterminal
                finalNonterminal = naughty.Production._rhs[noOfNonterminals - 1]
                assert type(finalNonterminal) == nltk.grammar.Nonterminal
                nonfinalNonterminals = tuple()
                for i in range(noOfNonterminals - 1):
                    nonterminal = naughty.Production._rhs[i]
                    assert type(nonterminal) is nltk.grammar.Nonterminal
                    intermediateName = self.GetUniqueNonterminalName("X")
                    nonfinalNonterminals = nonfinalNonterminals + (nonterminal,)
                intermediateNonterminal = nltk.grammar.Nonterminal(intermediateName)
                self.TerminalDict[intermediateName] = intermediateNonterminal
                newProduction1 = nltk.grammar.Production(lhs, (intermediateNonterminal, finalNonterminal))
                newProduction2 = nltk.grammar.Production(intermediateNonterminal, nonfinalNonterminals)
                assert len(newProduction1) == 2
                niceList.append(Transition(newProduction1, self.TerminalDict))
                #eprint(newProduction1)
                self.AddToList(niceList, newNaughtyList, Transition(newProduction2, self.TerminalDict))
            naughtyList = newNaughtyList;
        return naughtyList
    
    def AddToList(self, niceList, naughtyList, transition):
        """Adds the specified transition to either the niceList or the naughtyList, as appropriate."""
        if transition.IsNice():
            niceList.append(transition)
        else:
            naughtyList.append(transition)

    def PrintTransition(self, transition):
        """Print's a transition"""
        if transition.IsNice():
            print(transition)
        else:
            print('*', transition)
    
    def DisplayAll(self, niceList, naughtyList):
        """Displays all the transitions"""

        # Display the Start transition:
        for transition in list(set().union(niceList, naughtyList)):
            if transition.Production._lhs == self.grammar._start:
                self.PrintTransition(transition)

        # Display all the non-Start transitions:
        for transition in list(set().union(niceList, naughtyList)):
            if transition.Production._lhs != self.grammar._start:
                self.PrintTransition(transition)

    def GetUniqueNonterminalName(self, suggestedName):
        assert type(suggestedName) == str
        key = '_' + suggestedName.upper() + '_'
        i = 0
        # Check for duplicate keys:
        while key in self.TerminalDict:
            i += 1
            key = '_' + suggestedName.upper() + str(i) + '_'
        # Return the unique key:
        return key;
  
def main():
    """Parses the command line parameters and converts the specified grammar to CNF."""

    parser = argparse.ArgumentParser(description='Converts a grammar to Chomsky Normal Form (CNF).')
    parser.add_argument('grammarFile', type=str, help='the name of the file containing a context free grammar.')
    ns = parser.parse_args()

    # Input Validation:
    eprint('Grammar File: ', ns.grammarFile)
    converter = ConvertToCnf(ns.grammarFile)
    converter.Convert()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    main()
