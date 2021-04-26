import itertools
import random


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
        #if the length of the amount of open cells is the same as the count of bombs
        if(len(self.cells) == self.count):
            #the open cells are all bombs, returns the set of all bombs
            return(self.cells)
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #if the bomb count is zero
        if(self.count == 0):
            #all spaces are safe, which returns all spots that are safe
            return (self.cells)
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #if the cell is in the list of available cells, else do nothing
        if cell in self.cells:
            # identify the cell as a bomb, remove it from the list of existing bomb locations
            # no error message using discard method
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #if cell in self.cells, else do nothing
        if cell in self.cells:
            #remove the cell since known
            self.cells.discard(cell)

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
        # 1 and 2). mark the cell as a move that has been made and marks as safe
        self.mark_safe(cell)
        self.moves_made.add(cell)

        # 3). new set defined by the new safe cell
        new_sentence = set()
        # loop over cells within one row and column of safe spot
        # if loop cell equals the safe cell, continue
        # all other cells will need to be determined as either safe or a mine
        # once all cells have been determined, return all neighboring cells as a new sentence in knowledge
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                
                # check for other safe cells, loop over them
                if((i, j) in self.safes):
                    continue

                #check for mines
                if((i, j) in self.mines):
                    count -= 1
                    continue
                # otherwise add them to sentence (ex. adding to the new set)
                if(0 <= i < self.height and 0 <= j < self.width):
                    new_sentence.add((i, j))
        # side-note: after this loop we have created a new sentence which is ready to be added to the knowledge base
        self.knowledge.append(Sentence(new_sentence, count))

        # 4). loop through knowledge base, starting from beginning again
        # check existing surrounding points of bombs and safe in knowledge base, drawing new conclusions
        # Loop over all cells within one row and column
        # if conclusions can be drawn from the new bomb cell or safe cell, update the cells knowledge base accordingly
        # remove any known bombs or safes from knowledge base

        #mark new safes and new mines
        # continuously update surrounding areas of spots
        #while():
        future_mines = set()
        future_safes = set()
        #loop through KB
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                print(mine)
                future_mines.add(mine)
            for safe in sentence.known_safes():
                print(safe)
                future_safes.add(safe)
            print(sentence)

        for mine in future_mines:
            self.mark_mine(mine)
        for safe in future_safes:
            self.mark_safe(safe)

        #remove empty sentences

        inferences = []
        removals = []
        #add new sentences from new knowledge base
        for sentence1 in self.knowledge:
            # mark for removal if it is empty
            if sentence1.cells == set():
                removals.append(sentence1)
                continue
            # pick another
            for sentence2 in self.knowledge:
                # mark for removal if empty
                if sentence2.cells == set():
                    removals.append(sentence2)
                    continue
                # make sure they're different sentences
                if sentence1 != sentence2:
                    # if s2 is a subset of s1
                    if sentence2.cells.issubset(sentence1.cells):
                        diff_cells = sentence1.cells.difference(sentence2.cells)
                        diff_count = sentence1.count - sentence2.count
                        # an inference can be drawn
                        new_inference = Sentence(diff_cells, diff_count)
                        if new_inference not in self.knowledge:
                            inferences.append(new_inference)

        # remove sentences without any cells
        self.knowledge = [x for x in self.knowledge if x not in removals]
        

        #continue same block of code as above but continuously until all sentences/inferences have been resolved
        while inferences:
            for sentence in inferences:
                self.knowledge.append(sentence)

            # updates new mines
            future_mines = set()
            future_safes = set()
            #loop through KB
            for sentence in self.knowledge:
                for mine in sentence.known_mines():
                    print(mine)
                    future_mines.add(mine)
                for safe in sentence.known_safes():
                    print(safe)
                    future_safes.add(safe)
                print(sentence)

            for mine in future_mines:
                self.mark_mine(mine)
            for safe in future_safes:
                self.mark_safe(safe)

            inferences = []
            removals = []
            #add new sentences from new knowledge base
            for sentence1 in self.knowledge:
                # mark for removal if it is empty
                if sentence1.cells == set():
                    removals.append(sentence1)
                    continue
                # pick another
                for sentence2 in self.knowledge:
                    # mark for removal if empty
                    if sentence2.cells == set():
                        removals.append(sentence2)
                        continue
                    # make sure they're different sentences
                    if sentence1 != sentence2:
                        # if s2 is a subset of s1
                        if sentence2.cells.issubset(sentence1.cells):
                            diff_cells = sentence1.cells.difference(sentence2.cells)
                            diff_count = sentence1.count - sentence2.count
                            # an inference can be drawn
                            new_inference = Sentence(diff_cells, diff_count)
                            if new_inference not in self.knowledge:
                                inferences.append(new_inference)

            # remove sentences without any cells
            self.knowledge = [x for x in self.knowledge if x not in removals]

            
            
        #(compare multiple sentences to each other) - checking for subsets of sets, if new sentence is not in KB, append to KB
        # 5.) if we find anything new when searching the knowledge base
        # add new sentences to the knowledge base

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # returns a safe cell to choose on the board, known in safes, not already move made
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #completely random move
        all_moves = set(itertools.product(range(self.height), range(self.width)))
        moves_left = list(all_moves - self.mines - self.moves_made)
        if not moves_left:
            return None
        return random.choice(moves_left)
