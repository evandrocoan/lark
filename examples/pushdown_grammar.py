from pushdown import Lark

parser = Lark(open('examples/pushdown.pushdown'), parser="lalr")

grammar_files = [
    'examples/python2.pushdown',
    'examples/python3.pushdown',
    'examples/pushdown.pushdown',
    'examples/relative-imports/multiples.pushdown',
    'examples/relative-imports/multiple2.pushdown',
    'examples/relative-imports/multiple3.pushdown',
    'source/pushdown/grammars/common.pushdown',
]

def test():
    for grammar_file in grammar_files:
        tree = parser.parse(open(grammar_file).read())
    print("All grammars parsed successfully")

if __name__ == '__main__':
    test()
