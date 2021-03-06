# Pushdown - a modern parsing library for Python

Parse any context-free grammar,
FAST and EASY!

This project is a fork from https://github.com/lark-parser/lark,
and the new name transition still in progress.
Then,
until this process is complete,
you should see the name `Lark` several places.

I forked it and released it with a new name because I did a few changes which breaks
compatibility with old versions of lark and I use these changes in other projects.
Then,
these changes would not be welcome on the upstream (lark-parser) breaking everybody else
builds and I need to distribute these new breaking changes for my other projects.

Despite these small changes,
I still keep this repository up to date with the latest changes from the upstream (lark-parser),
using [https://backstroke.us](https://backstroke.us) to continually fetch new updates,
and merge them back as soon as possible.

And when a got a bunch of free time,
I also still sending back to the upstream (lark-parser) new changes or fixes which could be introduced back on the lark main repository.

Parse any context-free grammar, FAST and EASY!

**Beginners**: Lark is not just another parser. It can parse any grammar you throw at it, no matter how complicated or ambiguous, and do so efficiently. It also constructs a parse-tree for you, without additional code on your part.

**Experts**: Lark implements both Earley(SPPF) and LALR(1), and several different lexers, so you can trade-off power and speed, according to your requirements. It also provides a variety of sophisticated features and utilities.

Pushdown can:
 - Parse all context-free grammars, and handle any ambiguity
 - Build a parse-tree automagically, no construction code required
 - Outperform all other Python libraries when using LALR(1) (Yes, including PLY)
 - Run on every Python interpreter (it's pure-python)
 - Generate a stand-alone parser (for LALR(1) grammars)

And many more features. Read ahead and find out.

Most importantly,
Pushdown will save you time and prevent you from getting parsing headaches.


### Quick links

- [Tutorial](/docs/json_tutorial.md) for writing a JSON parser.


### Install pushdown

    $ pip install pushdown

Pushdown has no dependencies.


### Syntax Highlighting (new)

Pushdown now provides syntax highlighting for its grammar files (\*.pushdown):

- [Sublime Text & TextMate](https://github.com/evandroforks/pushdown_syntax)


### Hello World

Here is a little program to parse "Hello, World!" (Or any other similar phrase):

```python
from pushdown import Lark

l = Lark('''start: WORD "," WORD "!"

            %import common.WORD   // imports from terminal library
            %ignore " "           // Disregard spaces in text
         ''')

print( l.parse("Hello, World!") )
```

And the output is:

```python
Tree(start, [Token(WORD, 'Hello'), Token(WORD, 'World')])
```

Notice punctuation doesn't appear in the resulting tree. It's automatically filtered away by Pushdown.


### Fruit flies like bananas

Pushdown is great at handling ambiguity. Let's parse the phrase "fruit flies like bananas":

![fruitflies.png](examples/fruitflies.png)

See more [examples in the examples directory](examples)



## List of main features

 - Builds a parse-tree (AST) automagically, based on the structure of the grammar
 - **Earley** parser
    - Can parse all context-free grammars
    - Full support for ambiguous grammars
 - **LALR(1)** parser
    - Fast and light, competitive with PLY
    - Can generate a stand-alone parser
 - **CYK** parser, for highly ambiguous grammars (NEW! Courtesy of [ehudt](https://github.com/ehudt))
 - **EBNF** grammar
 - **Unicode** fully supported
 - **Python 2 & 3** compatible
 - Automatic line & column tracking
 - Standard library of terminals (strings, numbers, names, etc.)
 - Import grammars from Nearley.js
 - And much more!

### Comparison to other libraries

#### Performance comparison

Pushdown is the fastest and lightest (lower is better)

![Run-time Comparison](docs/comparison_runtime.png)

![Memory Usage Comparison](docs/comparison_memory.png)


Check out the [JSON tutorial](/docs/json_tutorial.md#conclusion) for more details on how the comparison was made.

*Note: I really wanted to add PLY to the benchmark, but I couldn't find a working JSON parser anywhere written in PLY. If anyone can point me to one that actually works, I would be happy to add it!*

*Note 2: The parsimonious code has been optimized for this specific test, unlike the other benchmarks (Lark included). Its "real-world" performance may not be as good.*

#### Feature comparison

| Library | Algorithm | Grammar | Builds tree? | Supports ambiguity? | Can handle every CFG? | Line/Column tracking | Generates Stand-alone
|:--------|:----------|:----|:--------|:------------|:------------|:----------|:----------
| **Pushdown** | Earley/LALR(1) | EBNF | Yes! | Yes! | Yes! | Yes! | Yes! (LALR only) |
| [PLY](http://www.dabeaz.com/ply/) | LALR(1) | BNF | No | No | No | No | No |
| [PyParsing](http://pyparsing.wikispaces.com/) | PEG | Combinators | No | No | No\* | No | No |
| [Parsley](https://pypi.python.org/pypi/Parsley) | PEG | EBNF | No | No | No\* | No | No |
| [Parsimonious](https://github.com/erikrose/parsimonious) | PEG | EBNF | Yes | No | No\* | No | No |
| [ANTLR](https://github.com/antlr/antlr4) | LL(*) | EBNF | Yes | No | Yes? | Yes | No |


(\* *PEGs cannot handle non-deterministic grammars. Also, according to Wikipedia, it remains unanswered whether PEGs can really parse all deterministic CFGs*)


### How to use Nearley grammars in Pushdown

Pushdown comes with a tool to convert grammars from [Nearley](https://github.com/Hardmath123/nearley), a popular Earley library for Javascript. It uses [Js2Py](https://github.com/PiotrDabkowski/Js2Py) to convert and run the Javascript postprocessing code segments.

Here's an example:
```bash
git clone https://github.com/Hardmath123/nearley
python -m pushdown.tools.nearley nearley/examples/calculator/arithmetic.ne main nearley > ncalc.py
```

You can use the output as a regular python module:

```python
>>> import ncalc
>>> ncalc.parse('sin(pi/4) ^ e')
0.38981434460254655
```


## License

Pushdown uses the [MIT license](LICENSE).

(The standalone tool is under GPL2)

## Contribute

Pushdown is currently accepting pull-requests. See [How to develop Lark](/docs/how_to_develop.md)


## Donate

For the original project called `lark-parser`, see: https://github.com/lark-parser/lark#donate


## Contact

For the original project called `lark-parser`, see: https://github.com/lark-parser/lark#contact

For this fork project called `pushdown`,
just open a new issue on:
https://github.com/evandrocoan/pushdown/issues


## Unit Tests

To run all Unit Tests (from python 2.7 up to the latest version of python),
install Python 2.7 and tox.
Then,
run the command `tox` on the root of this project (where the main setup.py file is on).

If you would like to only run the Unit Tests for Python version 2.7,
you can run the command `tox -e py27`


## Sublime Text Dependency

To use this as a Package Control Dependency https://packagecontrol.io/docs/dependencies create
this `dependencies.json` file on the root of your Package:
```json
{
    "*": {
        "*": [
            "debugtools",
            "pushdownparser"
        ]
    }
}
```

