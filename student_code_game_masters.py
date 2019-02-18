from game_master import GameMaster
from read import *
from util import *
import pdb

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        don = [False,False,False,False,False]

        askp1 = parse_input("fact: (empty peg1)")
        askp2 = parse_input("fact: (empty peg2)")
        askp3 = parse_input("fact: (empty peg3)")

        Peg1 = []
        Peg2 = []
        Peg3 = []

        pegs1 = []
        pegs2 = []
        pegs3 = []
        i = 1
        
        while i < 6:
            pegs1.append(parse_input("fact: (on disk" + str(i) + " peg1)"))
            pegs2.append(parse_input("fact: (on disk" + str(i) + " peg2)"))
            pegs3.append(parse_input("fact: (on disk" + str(i) + " peg3)"))
            i = i + 1
        

        if self.kb.kb_ask(askp1) != False:
            Peg1 = ()
        else:
            cf = 0
            cb = 1
            
            for f in pegs1:
                if self.kb.kb_ask(f) != False:
                    don[cf] = True
                cf = cf + 1
            for b in don:
                if b == True:
                    Peg1.append(cb)
                cb = cb + 1
            Peg1 = tuple(Peg1)
            don = [False,False,False,False,False]


        if self.kb.kb_ask(askp2) != False:
            Peg2 = ()
        else:
            cf = 0
            cb = 1
            
            for f in pegs2:
                if self.kb.kb_ask(f) != False:
                    don[cf] = True
                cf = cf + 1
            for b in don:
                if b == True:
                    Peg2.append(cb)
                cb = cb + 1
            Peg2 = tuple(Peg2)
            don = [False,False,False,False,False]

        if self.kb.kb_ask(askp3) != False:
           Peg3 = ()
        else:
            cf = 0
            cb = 1
            
            for f in pegs3:
                if self.kb.kb_ask(f) != False:
                    don[cf] = True
                cf = cf + 1
            for b in don:
                if b == True:
                    Peg3.append(cb)
                cb = cb + 1
            Peg3 = tuple(Peg3)
            don = [False,False,False,False,False]

        theTups = (Peg1 , Peg2 , Peg3)
        return theTups



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        #basically just adding facts and retracting facts
        theDisk = movable_statement.terms[0].term.element
        frompeg = movable_statement.terms[1].term.element
        topeg = movable_statement.terms[2].term.element

        newlocation = parse_input("fact: (on " + theDisk + " " + topeg + ")")
        oldlocation = parse_input("fact: (on " + theDisk + " " + frompeg + ")")
         
        self.kb.kb_assert(newlocation)
        self.kb.kb_retract(oldlocation)

        belowDisk = [False,False,False,False,False]
        askBelow = []
        i = 1
        while i < 6:
            askBelow.append(parse_input("fact: (ont " + theDisk + " disk" + str(i) + ")"))
            i = i + 1

        cf = 0
        cb = 1

        for f in askBelow:
            if self.kb.kb_ask(f) != False:
                belowDisk[cf] = True
                break
            cf = cf + 1

        for b in belowDisk:
            if b == True:
                break
            cb = cb + 1

        #making sure theere is something under disk were moving if we need to make changes or nah
        if cb < 6:
            fromPegBelowDisk = "disk" + str(cb)

            newTopFromPeg = parse_input("fact: (TheTop " + fromPegBelowDisk + " " + frompeg + ")")
            self.kb.kb_assert(newTopFromPeg)

            oldOnt = parse_input("fact: (ont " + theDisk + " " + fromPegBelowDisk + ")")        
            self.kb.kb_retract(oldOnt)
        else:
            #since there was nothing under disk this peg is now empty
            FromPegIsEmpty = parse_input("fact: (empty " + frompeg + ")")
            self.kb.kb_assert(FromPegIsEmpty)

        oldTopFromPeg = parse_input("fact: (TheTop " + theDisk + " " + frompeg + ")")
        self.kb.kb_retract(oldTopFromPeg)

        


        topegEmpty = False
        checkEmpty = parse_input("fact: (empty " + topeg + ")")

        if self.kb.kb_ask(checkEmpty) != False:
            topegEmpty = True

        if topegEmpty == False:
            toPegTop = [False,False,False,False,False]
            askTop = []
            i = 1
            while i < 6:
                askTop.append(parse_input("fact: (TheTop disk" + str(i) + " " + topeg + ")"))
                i = i + 1

            cf = 0
            cb = 1

            for f in askTop:
                if self.kb.kb_ask(f) != False:
                    toPegTop[cf] = True
                    break
                cf = cf + 1

            for b in toPegTop:
                if b == True:
                    break
                cb = cb + 1

            toPegTopDisk = "disk" + str(cb)
            oldTopToPeg = parse_input("fact: (TheTop " + toPegTopDisk + " " + topeg + ")")
            self.kb.kb_retract(oldTopToPeg)

            newOnt = parse_input("fact: (ont " + theDisk + " " + toPegTopDisk + ")")
            self.kb.kb_assert(newOnt)
        else:
            #since it was empty before we have to say it no longer is
            toPegWasEmpty = parse_input("fact: (empty " + topeg + ")")
            self.kb.kb_retract(toPegWasEmpty)

        newTopToPeg = parse_input("fact: (TheTop " + theDisk + " " + topeg + ")")
        self.kb.kb_assert(newTopToPeg)

        
      

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        i = 1
        j = 1
        t1facts = []
        t2facts = []
        t3facts = []
        t4facts = []
        t5facts = []
        t6facts = []
        t7facts = []
        t8facts = []
        emfacts = []

        firstRow = []
        secondRow = []
        thirdRow = []

        for i in range(1,4):
            for j in range(1,4):
                t1facts.append(parse_input("fact: (position tile1 pos" + str(i) + " pos" + str(j) + ")"))
                t2facts.append(parse_input("fact: (position tile2 pos" + str(i) + " pos" + str(j) + ")"))
                t3facts.append(parse_input("fact: (position tile3 pos" + str(i) + " pos" + str(j) + ")"))
                t4facts.append(parse_input("fact: (position tile4 pos" + str(i) + " pos" + str(j) + ")"))
                t5facts.append(parse_input("fact: (position tile5 pos" + str(i) + " pos" + str(j) + ")"))
                t6facts.append(parse_input("fact: (position tile6 pos" + str(i) + " pos" + str(j) + ")"))
                t7facts.append(parse_input("fact: (position tile7 pos" + str(i) + " pos" + str(j) + ")"))
                t8facts.append(parse_input("fact: (position tile8 pos" + str(i) + " pos" + str(j) + ")"))
                emfacts.append(parse_input("fact: (position empty pos" + str(i) + " pos" + str(j) + ")"))
            
        
        #what mean [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)]
        cf = 0
        t1 = []
        for f in t1facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t1 = [1,cf]
            firstRow.append(t1)
        elif(cf == 1 or cf == 4 or cf == 7):
            t1 = [1,cf]
            secondRow.append(t1)
        else:
            t1 = [1,cf]
            thirdRow.append(t1)

        cf = 0
        t2 = []
        for f in t2facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t2 = [2,cf]
            firstRow.append(t2)
        elif(cf == 1 or cf == 4 or cf == 7):
            t2 = [2,cf]
            secondRow.append(t2)
        else:
            t2 = [2, cf]
            thirdRow.append(t2)

        cf = 0
        t3 = []
        for f in t3facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t3 = [3,cf]
            firstRow.append(t3)
        elif(cf == 1 or cf == 4 or cf == 7):
            t3 = [3,cf]
            secondRow.append(t3)
        else:
            t3 = [3, cf]
            thirdRow.append(t3)

        cf = 0
        t4 = []
        for f in t4facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t4 = [4,cf]
            firstRow.append(t4)
        elif(cf == 1 or cf == 4 or cf == 7):
            t4 = [4,cf]
            secondRow.append(t4)
        else:
            t4 = [4,cf]
            thirdRow.append(t4)

        cf = 0
        t5 = []
        for f in t5facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t5 = [5,cf]
            firstRow.append(t5)
        elif(cf == 1 or cf == 4 or cf == 7):
            t5 = [5,cf]
            secondRow.append(t5)
        else:
            t5 = [5, cf]
            thirdRow.append(t5)

        cf = 0
        t6 = []
        for f in t6facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t6 = [6,cf]
            firstRow.append(t6)
        elif(cf == 1 or cf == 4 or cf == 7):
            t6 = [6,cf]
            secondRow.append(t6)
        else:
            t6 = [6, cf]
            thirdRow.append(t6)
        
        cf = 0
        t7 = []
        for f in t7facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t7 = [7,cf]
            firstRow.append(t7)
        elif(cf == 1 or cf == 4 or cf == 7):
            t7 = [7,cf]
            secondRow.append(t7)
        else:
            t7 = [7,cf]
            thirdRow.append(t7)

        cf = 0
        t8 = []
        for f in t8facts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            t8 = [8,cf]
            firstRow.append(t8)
        elif(cf == 1 or cf == 4 or cf == 7):
            t8 = [8,cf]
            secondRow.append(t8)
        else:
            t8 = [8, cf]
            thirdRow.append(t8)

        cf = 0
        em = []
        for f in emfacts:
            if self.kb.kb_ask(f) != False:
                break
            cf = cf + 1
        if(cf == 0 or cf == 3 or cf == 6):
            em = [-1,cf]
            firstRow.append(em)
        elif(cf == 1 or cf == 4 or cf == 7):
            em = [-1,cf]
            secondRow.append(em)
        else:
            em = [-1, cf]
            thirdRow.append(em)

        for i in range(0,2):
            for j in range(1,3):
                if firstRow[i][1] > firstRow[j][1]:
                    firstRow[j], firstRow[i] = firstRow[i], firstRow[j]
        
        for i in range(0,2):
            for j in range(1,3):
                if secondRow[i][1] > secondRow[j][1]:
                    secondRow[j], secondRow[i] = secondRow[i], secondRow[j]

        for i in range(0,2):
            for j in range(1,3):
                if thirdRow[i][1] > thirdRow[j][1]:
                    thirdRow[j], thirdRow[i] = thirdRow[i], thirdRow[j]
        
        onerow = []
        tworow = []
        threerow = []

        for i in range(0,3):
            onerow.append(firstRow[i][0])
            tworow.append(secondRow[i][0])
            threerow.append(thirdRow[i][0])
        
        firstRow = tuple(onerow)
        secondRow = tuple(tworow)
        thirdRow = tuple(threerow)

        theTups = (firstRow, secondRow, thirdRow)
        return theTups


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        theTile = movable_statement.terms[0].term.element
        fromPosX = movable_statement.terms[1].term.element
        fromPosY = movable_statement.terms[2].term.element
        toPosX = movable_statement.terms[3].term.element
        toPosY = movable_statement.terms[4].term.element
        
        NewTileLoc = parse_input("fact: (position " + theTile + " " + toPosX + " " + toPosY + ")")
        NewEmptyLoc = parse_input("fact: (position empty " + fromPosX + " " + fromPosY + ")")

        OldTileLoc = parse_input("fact: (position " + theTile + " " + fromPosX + " " + fromPosY + ")")
        OldEmptyLoc = parse_input("fact: (position empty " + toPosX + " " + toPosY + ")")

        self.kb.kb_assert(NewTileLoc)
        self.kb.kb_assert(NewEmptyLoc)

        self.kb.kb_retract(OldEmptyLoc)
        self.kb.kb_retract(OldTileLoc)
        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
