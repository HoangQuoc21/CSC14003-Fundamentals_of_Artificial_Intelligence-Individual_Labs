from io import FileIO


class pl_resolution:

    # Define Logical Expressions that can apppear in statement
    EXPRESSIONS = ['OR']

    # Constructor
    def __init__(self, kb: list, alpha: str):

        # Attribute
        self.__kb = [] # __kb is the list that contains many lists of strings (clauses) 
        self.__alpha = []   # _alpha is the list of literal in alpha statement and already inverse
        self.__result = [] # _result is the 3D list that contains lists of list result clauses (2D array)
        self.__isEntails = False
        self.__details = [] # Use to track which clause resolve which clause


        # Load raw kb (as readline) from file to the list
        for str_clause in kb: 
            # Get list of literals
            clause_as_list_of_literal = self.process(str_clause) 

            # Sort the literals in each clause
            self.__kb.append(self.sort_clause(clause_as_list_of_literal))


        # Load alpha state to the kb and reverse it
        alpha_statement_as_list_of_literal = self.sort_clause(self.process(alpha)) 

        for literal in alpha_statement_as_list_of_literal:
            self.__alpha.append(self.get_inverse_literal(literal))



        # In this Lab, alpha statement has format 'A OR -B...'
        # That means that after being inverse, alpha statement has format:
        # '-A AND B...'
        # Because each literal in alpha is connected together by expresion AND,
        # each literal in alpha will be treated has a clause in kb.
        # So we need to add each literal in aplha to kb [] one by one.


        # Add inverse alpha to kb
        for literal in self.__alpha:
            if [literal] not in kb:
                self.__kb.append([literal])
       

    '''''''''''''''''''''''''''
        HELPER FUNCTION

    '''''''''''''''''''''''''''


    # Use to CONVERT the clause (as str) read from file TO list of literals
    # Input: 'A OR B'
    # Output: ['A', 'B']
    @staticmethod
    def process(clause : str) -> list:
        result = []
        
        # Get literals in the clause
        literals = clause.split(' ')
        
        for literal in literals:
            if len(literal) > 0 and literal not in pl_resolution.EXPRESSIONS:
                result.append(literal)
        
        return result


    # Use to INVERSE a literal
    # Input 1: 'A' 
    # Output 1: '-A'
    # Input 2: '-B'
    # Output 2: 'B'
    @staticmethod
    def get_inverse_literal(literal : str) -> str:
        result = ''

        if '-' in literal:
            result = literal.replace('-', '')
        else:
            result = '-' + literal
    
        return result
    

    # Use to SORT and CLEAR duplicate literal in clause
    # Input: ['A', '-C', 'A', 'B']
    # Output: ['A', 'B', 'C']
    @staticmethod
    def sort_clause(clause : list) -> list:
        # Delete the duplication
        unique = set(clause)

        # Sort the list
        return sorted(unique, key=lambda x: x.lstrip('-'))
    

    # Use to convert clause as list of literal to string that can write to file
    # Input: ['A', 'B', 'C']
    # Output: 'A OR B OR C'
    @staticmethod
    def get_cnf_format_of(clause : list) -> str:

        result = ''

        if len(clause) == 0:
            result = '{}'
        
        elif len(clause) == 1:
            result = clause[0]

        else:
            for literal in clause[:-1]:
                result += literal
                result += ' OR '
            result += clause[-1]
        
        return result


    # Use to CHECK if two literals is inversed of each other
    # Input 1: 'A' and '-A'
    # Output 1: True
    # Input 2:  'A and 'B'
    # Output 2: False
    @staticmethod
    def is_inverse(literal_a : str, literal_b : str) -> bool:

        # Get the inversion of 1 clause
        inverse_literal = pl_resolution.get_inverse_literal(literal_a)

        # Check it with the other clause
        result = False

        if inverse_literal == literal_b:
            result = True

        return result
    
    
    # Use to check if a Clause is always true
    # Ex: A OR -A is true, A OR B OR -A is true.
    @staticmethod
    def is_always_valid(clause : list) -> bool:
        for i in range(len(clause) - 1):
            for j in range(i + 1, len(clause)):
                if (pl_resolution.is_inverse(clause[i], clause[j])):
                    return True
        return False

    # Use to RESOLVE two clause
    @staticmethod
    def resolve_two_clause(clause_a : list, clause_b : list) -> list:
        # result is an list of resolve clause (str list)
        result = []

        for i in range(len(clause_a)):
            for j in range(len(clause_b)):
                if pl_resolution.is_inverse(clause_a[i], clause_b[j]):
                    resolvent = clause_a[:i] + clause_a[i + 1:] + clause_b[:j] + clause_b[j + 1:]
                    result.append(pl_resolution.sort_clause(resolvent))

        return result
    

    # Main Algorithm
    def pl_resolution(self) -> bool:
        while True:
            
            # list of resolved clauses (str list) after each iterate through _kb
            resolve_clauses = [] 

            for i in range(len(self.__kb) - 1):
                for j in range(i + 1, len(self.__kb)):
                    resolvents = self.resolve_two_clause(self.__kb[i], self.__kb[j])

                    # Clause 1: A RESOLVE with Clause 2: -A -> resolvents.append([])
                    if [] in resolvents:
                        self.__isEntails = True
                    
                    # Add new resolvent to the list
                    for resolvent in resolvents:
                        if self.is_always_valid(resolvent):
                            continue
                        if resolvent not in resolve_clauses and resolvent not in self.__kb:
                            resolve_clauses.append(resolvent)
                            self.__details.append((self.__kb[i],self.__kb[j]))


            # Add list to the result     
            self.__result.append(resolve_clauses)

            if len(resolve_clauses) == 0:
                self.__isEntails = False
                return False

            for clause in resolve_clauses:
                if clause not in self.__kb: 
                    self.__kb.append(clause)

            if self.__isEntails:
                return True


    def print_output(self, details : bool = False, f : FileIO = None) -> None:
        
        for i in range(len(self.__result)):
            print(len(self.__result[i]), file = f)
            for j in range(len(self.__result[i])):
                if not details:
                    print(self.get_cnf_format_of(self.__result[i][j]), file = f)
        
        print('YES', file = f) if self.__isEntails else print('NO', file = f)
        
        
        # Use this to output detail of each step
        # print('\n\n-----------------', file = f)
        # print('DETAILS', file = f)
        # print('-----------------', file = f)
        # for i in range(len(self.__details)):
        #     print( '(' +self.get_cnf_format_of(self.__details[i][0]) + ') hop giai voi (' + self.get_cnf_format_of(self.__details[i][1]) +')', file = f)
        