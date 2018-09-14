"""This module implements a LALR(1) Parser
"""
# Author: Erez Shinan (2017)
# Email : erezshin@gmail.com
import sys

from ..exceptions import LarkError, UnexpectedToken, UnexpectedCharacters
from ..lexer import Token

from .. errors import parser_errors
from .lalr_analysis import LALR_Analyzer, Shift

class Parser:
    def __init__(self, parser_conf):
        assert all(r.options is None or r.options.priority is None
                   for r in parser_conf.rules), "LALR doesn't yet support prioritization"
        analysis = LALR_Analyzer(parser_conf)
        analysis.compute_lookahead()
        callbacks = {rule: getattr(parser_conf.callback, rule.alias or rule.origin, None)
                          for rule in parser_conf.rules}

        self._parse_table = analysis.parse_table
        self.parser_conf = parser_conf
        self.parser = _Parser(analysis.parse_table, callbacks)
        self.parse = self.parser.parse

###{standalone

class _Parser:
    def __init__(self, parse_table, callbacks):
        self.states = parse_table.states
        self.start_state = parse_table.start_state
        self.end_state = parse_table.end_state
        self.callbacks = callbacks
        # TODO Verify whether `parser_errors` can be a member class atribute.
        # It depends on whether this is an member class object or static.
        # self.parser_errors = []

    def parse(self, seq, set_state=None):
        # stack of error contexts allowing this function to be reentrant
        # parser_errors = self.parser_errors
        parser_errors.append([])

        token = None
        stream = iter(seq)
        states = self.states

        state_stack = [self.start_state]
        value_stack = []

        if set_state: set_state(self.start_state)

        def get_action(key):
            state = state_stack[-1]
            try:
                return states[state][key]
            except KeyError:
                expected = [s for s in states[state].keys() if s.isupper()]

                # TODO filter out rules from expected
                parser_errors[-1].append(UnexpectedToken(token, expected, state=state))
                # print(f'parser_errors {parser_errors}', file=sys.stderr)

                # Just take the first expected key
                for s in states[state].keys():
                    if s.isupper():
                        # print(f"For {state} and {key}, returning key {s} - {states[state][s]}", file=sys.stderr)
                        return states[state][s]

        def reduce(rule):
            size = len(rule.expansion)
            if size:
                s = value_stack[-size:]
                del state_stack[-size:]
                del value_stack[-size:]
            else:
                s = []

            value = self.callbacks[rule](s)

            _action, new_state = get_action(rule.origin.name)
            assert _action is Shift
            state_stack.append(new_state)
            value_stack.append(value)

        def raise_parsing_errors():
            # print(f'parser_errors: {parser_errors}', file=sys.stderr)
            if parser_errors[-1]:
                error_messages = []
                for index, exception in enumerate(parser_errors[-1]):
                    # Comment out this if to show the duplicated error messages removed
                    if not index or index > 0 and exception != parser_errors[-1][index-1]:
                        if type(exception) is UnexpectedCharacters:
                            error_messages.append('\nLexer error: %s' % exception)
                        elif type(exception) is UnexpectedToken:
                            error_messages.append('\nParser error: %s' % exception)

                raise SyntaxError(''.join( error_messages ))

        try:
            # Main LALR-parser loop
            # print('', file=sys.stderr); index = -1
            for token in stream:
                # index += 1; x = token; print(repr(f"[@{index},{x.pos_in_stream}:{x.pos_in_stream+len(x.value)-1}='{x.value}'<{x.type}>,{x.line}:{x.column}]"), file=sys.stderr)
                while True:
                    # print(f'token {type(token)} {token}', file=sys.stderr)
                    action, arg = get_action(token.type)
                    if arg == self.end_state:
                        break
                    if action is Shift:
                        state_stack.append(arg)
                        value_stack.append(token)
                        if set_state: set_state(arg)
                        break # next token
                    else:
                        reduce(arg)

            raise_parsing_errors()
            token = Token.new_borrow_pos('<EOF>', token, token) if token else Token('<EOF>', '', 0, 1, 1)

            while True:
                _action, arg = get_action('$END')
                if _action is Shift:
                    if arg != self.end_state:
                        raise_parsing_errors()
                        assert arg == self.end_state
                    val ,= value_stack
                    return val
                else:
                    reduce(arg)

            raise_parsing_errors()

        finally:
            # unstack the current erro context on finish
            parser_errors.pop()

###}
