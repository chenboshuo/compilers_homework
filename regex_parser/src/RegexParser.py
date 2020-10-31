from Automata import Automata


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

    # def build_NFA(self):
    #     """build a NFA from pattern create :class:`Automata.Automata`

    #     :return: the NFA of the current pattern

    #     :rtype: Automata.Automata
    #     """
    #     language = set()
    #     self.buffer = []
    #     self.automata = []
    #     previous = r'\epsilon'
    #     for char in self.pattern:
    #         if char in self.alphabet:
    #             pass
    #             # TODO
    #     return None

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
        if self.peek() == '(': # TODO match ()
            pass 
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


if __name__ == "__main__":
    # test the cases of the only letter
    test1 = RegexParser("a")
    print(test1.parse_base_part())
    """output
        states: {1, 2}
        start state:    1
        final state:    {2}
        transitions:
                1->2 on 'a'
    """

    # test the escape symbol
    test2 = RegexParser("\*")
    print(test2.parse_base_part())
    """output
        states: {1, 2}
        start state:    1
        final state:    {2}
        transitions:
                1->2 on '*'
    """

    # test parse factor part
    test3 = RegexParser('a*')
    print(test3.parse_factor_part())
    """output
        states: {1, 2}
        start state:    1
        final state:    {2}
        transitions:
                1->2 on '\epsilon'
                1->2 on 'a'

                2->1 on '\epsilon'    
    """
    
