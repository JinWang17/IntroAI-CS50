import sys
import copy
import itertools

from crossword import *

class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with starting point, direction, and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == Variable.DOWN else 0),
                 self.j + (k if self.direction == Variable.ACROSS else 0))
            )

    def __hash__(self):
        # The hash() method returns the hash value of an object if it has one.
        # Hash values are just integers that are used to compare dictionary keys
        # during a dictionary lookup quickly.
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.direction == other.direction) and
            (self.length == other.length)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        # The repr() function returns a printable representation of the given object.
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():

    def __init__(self, structure_file, words_file):

        # Determine structure of crossword
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            self.structure = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    if j >= len(contents[i]):
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                self.structure.append(row)

        # Save vocabulary list
        with open(words_file) as f:
            self.words = set(f.read().upper().splitlines())

        # Determine variable set
        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):

                # Vertical words
                starts_word = (
                    self.structure[i][j]
                    and (i == 0 or not self.structure[i - 1][j])
                )
                # A vertical variable starts at (i, j) is equivalent to the following:
                # 1) (i, j) is a blank entry
                # 2) (i, j) is already at the top of the row OR (i-1, j) is not blank
                
                if starts_word:
                    length = 1
                    for k in range(i + 1, self.height):
                        if self.structure[k][j]:
                            length += 1
                        else:
                            break
                    if length > 1: # if length > 1, then we are sure it is down, not across
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.DOWN,
                            length=length
                        ))

                # Horizontal words
                starts_word = (
                    self.structure[i][j]
                    and (j == 0 or not self.structure[i][j - 1])
                )
                if starts_word:
                    length = 1
                    for k in range(j + 1, self.width):
                        if self.structure[i][k]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.ACROSS,
                            length=length
                        ))

        # Compute overlaps for each word
        # For any pair of variables v1, v2, their overlap is either:
        #    None, if the two variables do not overlap; or
        #    (i, j), where v1's ith character overlaps v2's jth character
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )

    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var]
        )


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
            # initial domain for each var in variables is the full list of words
        }

    #？？？？？ need to understand after have a legit assignment!!
    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)     
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # To remove a value x from the domain of a variable v, since 
        # self.domains is a dictionary mapping variables to sets of values, 
        # you can call self.domains[v].remove(x).
        temp_domain = copy.deepcopy(self.domains)
        
        for var in self.crossword.variables:
            for word in temp_domain[var]:
                if len(word) != var.length:
                    self.domains[var].remove(word)
                # set_trace()
        
        # No return value is necessary for this function. (Because remove
        # is operating on the self.domains directly.)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        # x and y: both be Variable objects representing variables in the puzzle.
        # x arc consistent with y when every value in the domain of x 
        # has a possible value in the domain of y that does not cause a conflict. 
        
        flag = False
        if(self.crossword.overlaps[(x, y)]):
            #set_trace()
            (ii, jj) = self.crossword.overlaps[(x, y)] 
            # i'th place in x needs to be the same as j'th place in y
            temp = copy.deepcopy(self.domains[x])
            for word1 in temp:
                # remove values from `self.domains[x]` for which there is no
                # possible corresponding value for `y` in `self.domains[y]`.
                # The domain of y should be left unmodified.
                if(all(word2[jj] != word1[ii] for word2 in self.domains[y])):
                    flag = True
                    self.domains[x].remove(word1)          
        
        # Return True if a revision was made to the domain of `x`; return
        # False if no revision was made.
        return(flag)
             

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # The ac3 function should, using the AC3 algorithm, enforce arc consistency on the problem. 
        # Arc consistency is achieved when all the values in each variable’s domain 
        # satisfy that variable’s binary constraints.

        # If arcs is None, start with an initial queue of all of the arcs in the problem. 
        # Otherwise, start with an initial queue of only the arcs in the list arcs 
        # (where each arc is a tuple (x, y) of a variable x and a different variable y).
        if not arcs:
            arcs = list(itertools.permutations(self.crossword.variables, 2))
        #set_trace()
        
        while arcs:
            # stop when all arcs have been enforced the arc consistency criteria 
            x, y = arcs.pop(0)
            #set_trace()
            # revise each arc in the queue one at a time
            revised = self.revise(x, y)
            if revised:
                # Any time you make a change to a domain, need to add additional 
                # arcs to your queue to ensure that other arcs stay consistent.
                if len(self.domains[x]) == 0:
                    # return False if one or more domains end up empty.
                    return False
                for z in self.crossword.variables:
                    if z == y or z == x:
                        continue
                    elif self.crossword.overlaps[(z, x)]:
                        arcs.append((z, x))

        # Return True if arc consistency is enforced and no domains are empty
        return True
        
        # You do not need to worry about enforcing word uniqueness in this function 
        # (you’ll implement that check in the consistent function.)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # An assignment is a dictionary where the keys are Variable objects and 
        # the values are strings representing the words those variables will take on.
        
        # complete if a value is assigned to each key (regardless of what that value is).
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for (x, y) in self.crossword.overlaps:
            # Only consider if there is non-empty overlap
            if self.crossword.overlaps[(x, y)]:    
                # Only consider arcs where both are assigned
                if x not in assignment or y not in assignment:
                    continue
                (ii, jj) = self.crossword.overlaps[(x, y)]
                # If both have same value, then not consistent
                if assignment[x][ii] != assignment[y][jj]:
                    return False

        # If nothing inconsistent, then assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
    
        rule_out = dict()
        
        for value in self.domains[var]:
            n = 0
            # least-constraining values heuristic: the number of values ruled out for neighboring unassigned variables. 
            for neighbor in self.crossword.variables:
                # will not count the neighbors that already has an assignment
                if neighbor not in assignment:
                    # will not count if not neighbors
                    if self.crossword.overlaps([var, neighbor]):                  
                        (ii, jj) = self.crossword.overlaps([var, neighbor])
                        for neighbor_value in self.domains[neighbor]:
                            if value[ii] != neighbor_value[jj]:
                                n += 1
            rule_out[value] = n
        
        # you should order your results in ascending order of n.
        result = sorted(rule_out, key=lambda item: rule_out[item])

        # return a list of all of the values in the domain of var, ordered according to the 
        # least-constraining values heuristic
        return list(result)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        heuristic = dict()
        
        for i in self.crossword.variables:
            if i not in assignment:
                # minimum remaining value heuristic: the fewest number of remaining values in its domain
                remains = len(self.domains[i])
                # the degree heuristic: the largest degree (has the most neighbors)
                degrees = len(self.crossword.neighbors(i))         
                heuristic[i] = (remains, -degrees)
                
        if heuristic:
            heuristic = sorted(heuristic, key=lambda item: heuristic[item])
            return heuristic[0]
        else:
            return None
     
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if len(assignment) == len(self.crossword.variables):
            return assignment
        # Try a new variable
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None: 
                    return result
        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

