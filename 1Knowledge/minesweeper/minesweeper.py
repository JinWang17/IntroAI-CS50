import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        #print(i, j, self.board[i][j])
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if self.count == len(self.cells) else set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if 0 == self.count else set()

    
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # The mark_mine function should first check to see if cell is one of the cells included in the sentence.
        if cell in self.cells:
            # If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, 
            # but still represents a logically correct sentence given that cell is known to be a mine.
            self.cells.remove(cell)
            self.count -= 1
        # If cell is not in the sentence, then no action is necessary.
               

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #The mark_safe function should first check to see if cell is one of the cells included in the sentence.
        if cell in self.cells:
            # If cell is in the sentence, the function should update the sentence so that cell is no longer in 
            # the sentence, but still represents a logically correct sentence given that cell is known to be safe.
            self.cells.remove(cell)
            #If cell is not in the sentence, then no action is necessary.


            
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        # Reason for using list, not set for knowledge:
        # elements in set is not mutable, although set itself is mutable. 
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)        
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        
        
    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # 2) mark the cell as safe, and update any sentences that contain the cell as well
        self.safes.add(cell)
        for k in self.knowledge:
            k.mark_safe(cell)
            
        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        # Be sure to only include cells whose state is still undetermined in the sentence.
        tempNeighbor = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Add to set if status not known as mine or safe
                if 0 <= i < self.height and 0 <= j < self.width:
                    if ((i, j) in self.mines):
                        count -= 1
                    elif ((i, j) in self.safes):
                        continue
                    else:
                        tempNeighbor.add((i, j))
        newKnowledge = Sentence(tempNeighbor, count)
        # update knowledge if there is anything new to be learned from this cell 
        if len(newKnowledge.cells) > 0 and (not newKnowledge in self.knowledge):
            self.knowledge.append(newKnowledge)
        
        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        # print(self.knowledge)
        flag = True
        # as long as the knowledge base is being updated, perform another loop to update until stable version is reached
        while(flag):
            # deep copy is necessary because sentence in self.knowledge may be changed on the sentence level
            tempKnowledge = copy.deepcopy(self.knowledge)
            flag = False
            #set_trace()
            # mark as safe or as mines if it can be concluded based on the AI's knowledge base
            for i, k in enumerate(tempKnowledge):
                for m in k.known_mines():
                    #print(f"mines:{m}")
                    self.mark_mine(m)
                    flag = True
                for s in k.known_safes():
                    #print(f"safes:{s}")
                    self.mark_safe(s)
                    flag = True 
                    
            #set_trace()
            # add new sentences to the AI's knowledge base if they can be inferred from existing knowledge
            tempKnowledge = copy.deepcopy(self.knowledge)
            for k1, k2 in itertools.combinations(tempKnowledge, 2):
                if k1.cells and k2.cells:
                    if k1.cells < k2.cells:
                        temp = Sentence(k2.cells - k1.cells, k2.count - k1.count)
                        if len(temp.cells) > 0 and (not temp in self.knowledge):
                            self.knowledge.append(temp)
                            flag = True
                    elif k1.cells > k2.cells:
                        temp = Sentence(k1.cells - k2.cells, k1.count - k2.count)
                        if len(temp.cells) > 0 and (not temp in self.knowledge):
                            self.knowledge.append(temp)
                            flag = True

            #set_trace()       
            # delete empty sentences
            for k in self.knowledge:
                if k.cells == set():
                    self.knowledge.remove(k)
            #set_trace()        
                
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # The move returned must be known to be safe, and not a move already made.
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) > 0:
            return safe_moves.pop() 
        else:
            return None # If no safe move can be guaranteed, the function should return None.
        

        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # The move must not be a move that has already been made/ is known to be a mine.
        all_moves = {(x, y) for x in range(self.width) for y in range(self.height)}
        #print(all_moves)
        possible_moves = all_moves - self.moves_made - self.mines
        
        if len(possible_moves) > 0:
            return random.sample(possible_moves, k = 1)[0] 
        else:
            return None # If no such moves are possible, the function should return None
   
