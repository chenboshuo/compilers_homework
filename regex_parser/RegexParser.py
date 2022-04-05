from regex_parser.Automata import Automata


class RegexParser:
    """
    store and parse a apttern

    .. code-block:: text

        <regex> ::= <term> '|' <regex>
                  |  <term>

        <term> ::= { <factor> }

        <factor> ::= <base> { '*' }

        <base> ::= <char>
                |  '\\' <char>
                |  '(' <regex> ')'


    :param pattern: the pattern to match the string
    :type pattern: str

    :ivar self.pattern: the pattern
    :ivar self.NFA: the NFA machine
    """
    # alphabet = set([chr(i) for i in range(65, 91)])\
    #     .union([chr(i) for i in range(97, 123)])\
    #     .union([chr(i) for i in range(48, 58)])


    def __init__(self, pattern: str):
        """store and parse a apttern

        :param pattern: the pattern to match the string
        :type pattern: str
        """
        self.pattern = pattern
        # self.NFA = self.build_NFA()


    def peek(self) -> str:
        """returns the next item of input without consuming it;

        :return: the next character
        :rtype: str
        """
        return self.pattern[0]

    def eat(self, item:str) -> None:
        """eat(item) consumes the next item of input, failing if not equal to item.


        :param item: the next item
        :type item: str
        :raises RuntimeError: get the wrong letter.
        """
        if(self.peek() == item):
            self.pattern = self.pattern[1:]
        else:
            raise RuntimeError(f"expect: {item}; got {self.peek()}")

    def next(self) -> str:
        """returns the next item of input and consumes it;

        :return: the next character
        :rtype: str
        """
        c = self.peek()
        self.eat(c)
        return c

    def parse_base_part(self) -> Automata:
        """check the cases encountered

        .. code-block:: text

            <base> ::= <char>
                    |  '\\' <char>
                    |  '(' <regex> ')'

        :return: Automata of this part
        :rtype: Automata
        """
        if self.peek() == '(':
            self.eat('(')
            r = self.parse_regex()
            self.eat(')')
            return r

        elif self.peek() == '\\':
            self.eat('\\')
            esc = self.next()
            return Automata.basic_construct(esc)
        else:
            return Automata.basic_construct(self.next())

    def parse_factor_part(self) -> Automata:
        base = self.parse_base_part()

        while(self.pattern and self.peek() == '*'):
            self.eat('*')
            base = Automata.star_operation(base)

        return base

    def parse_term_part(self) -> Automata:
        """check that it has not reached the boundary of a term or the end of the input:

        .. code-block:: text

            <term> ::= { <factor> }

        :return: the NFA of this part
        :rtype: Automata
        """
        factor = Automata.empty_construct()
        while(self.pattern and self.peek() != ')' and self.peek() != '|'):
            next_factor = self.parse_factor_part()
            factor = Automata.concatenation(factor, next_factor)

        return factor

    def parse_regex(self) -> Automata:
        """For regex() method, we know that we must parse at least one term,
        and whether we parse another

        .. code-block::text

            <regex> ::= <term> '|' <regex>
                      |  <term>

        :return: the NFA
        :rtype: Automata
        """
        term = self.parse_term_part()
        if(self.pattern and self.peek() == '|'):
            self.eat('|')
            regex = self.parse_regex()
            return Automata.union(term, regex)
        else:
            return term
