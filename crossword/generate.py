import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

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
        for v in self.domains:
            for word in set(self.domains[v]):
                if len(word) != v.length: #if word length isn't as required by variable, remove it
                    self.domains[v].remove(word)
                

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y] #get overlap
        if overlap is None: #if no overlap, great!
            return False
            
        change = False #used to see if domain of x has been changed
        for wordx in set(self.domains[x]):
            common = False #checks for existence of any word pair have same letter in the overlap
            for wordy in set(self.domains[y]):
                    if wordx[overlap[0]] == wordy[overlap[1]]:
                        common = True #if common is true, break out
                        break
            if not common: #if no commoness exists, remove the wordx from domain of x
                self.domains[x].remove(wordx)
                change = True
                
        return change
                        
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = [] #create a list of arcs
            for word1 in self.domains: #copy everything
                for word2 in self.crossword.neighbors(word1):
                    arcs.append((word1, word2))
        
        while arcs: #so long as there are arcs
            word1, word2 = arcs.pop() #pop a variable pair
            if self.revise(word1, word2): #if a revision is made
                if not self.domains[word1]: #if domain of word1 has nothing
                    return False
                for word in (self.crossword.neighbors(word1) - self.domains[word2]):
                    arcs.append((word, word1)) #append the words that aren't in domain of word2
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(self.crossword.variables - set(assignment)) == 0 #return true if there is no difference
    
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = set() #set of possible words
        for word in assignment:
            if assignment[word] in words: #if duplicate entries exist, return False
                return False
            else:
                words.add(assignment[word]) #add the word
                
            if word.length != len(assignment[word]): #if incorrect length, return False
                return False
            
            for neighbour in self.crossword.neighbors(word):
                if neighbour in assignment:
                    overlap = self.crossword.overlaps[word, neighbour]
                    if assignment[word][overlap[0]] != assignment[neighbour][overlap[1]]: #if wrong letter in overlap, return False
                        return False
        return True
            

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        new_domain = {}
        for word in self.domains[var]:
            new_domain[word] = 0
            for neighbour in self.crossword.neighbors(var) - set(assignment):
                if word in self.domains[neighbour]:#if word is common
                    new_domain[word] += 1 #add to common word count of the word
        return sorted(new_domain, key = new_domain.get) #sort based on value (common word counts) and return the keys

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_value = None
        for word in (self.crossword.variables - set(assignment)):
            #if min_value is none or if number of variables in domain is lower than that of min_value or if it is equal and number of neighbors (degree) of word is more than that of min value
            if min_value is None or len(self.domains[word]) < len(self.domains[min_value]) or (len(self.domains[word]) == len(self.domains[min_value]) and len(self.crossword.neighbors(word)) > len(self.crossword.neighbors(min_value))):
                min_value = word
                
        return min_value
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):#return if complete
            return assignment
            
        word = self.select_unassigned_variable(assignment) #select minimum valued word
        for Word in self.domains[word]:
            assignment[word] = Word #map Words in min valued word domain to min valued word
            if self.consistent(assignment): #if after this, crossword is consistent
                Assignment = self.backtrack(assignment) #continue and select next unassigned variable and repeat
                if Assignment is not None:
                    return Assignment#return at the end of all recursive calls
            assignment.pop(word)#if inconsistent, remove this word and continue
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
