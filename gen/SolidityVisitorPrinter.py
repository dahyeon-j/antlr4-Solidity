import sys
from antlr4 import *
import SolidityParser
import SolidityLexer
import SolidityVisitor

def main(file_name):
    input = FileStream(file_name)

    lexer = SolidityLexer.SolidityLexer(input)

    stream = CommonTokenStream(lexer)

    parser = SolidityParser.SolidityParser(stream)

    tree = parser.sourceUnit()
    printer = SolidityVisitor.SolidityVisitor()

    printer.visitSourceUnit(tree)

if __name__ == '__main__':
    main("test.sol")