
from solver import *
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function. (look at getmovables check iterate getmovables from left to right)
        (can't keep track of were we came from easily have to go back up tree to find where were before and then do next)
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #constructing tree, make a root node which is a gamestate object
        #we are given a game state
        #default state is your original kb facts
        #look at solver.py # hash states can hash tuples
        
        theGame = self.gm #just the game master not game state
        victory = self.victoryCondition
        checkState = theGame.getGameState()
        #visted = self.visited[self.currentState]

        if(checkState == victory):
            return True ##or do nothing

        dep = self.currentState.depth
        childrenLen = len(self.gm.getMovables())
        childs = self.gm.getMovables()

        if(childrenLen != 0):#if theres no kids were at the bottom

            for i in range(0,childrenLen):#just putting all the kids with their parent
                nextMove = childs[i]
                theGame.makeMove(nextMove)

                childState = GameState(theGame.getGameState(), dep + 1, nextMove)
                #self.currentState.children.append(GameState(theGame.getGameState(), dep + 1, nextState))
                if(not self.visited.get(childState, False)):
                    if(not childState in self.currentState.children):
                        self.currentState.children.append(childState)
                        childState.parent = self.currentState

                theGame.reverseMove(nextMove)
                #self.currentState.children[i].parent = self.currentState
            
            MovesLeft = False
            
            for kiddos in self.currentState.children:#going down the  branch and becoming a human child or a kiddo and making 
                nextMove = kiddos.requiredMovable #sure we got visited as an old man by those very childrens
                theGame.makeMove(nextMove)
                
                self.visited[kiddos] = True
                self.currentState = kiddos

                MovesLeft = True
                break
            
            if(MovesLeft == False):#if theres no moves/kids left we got to the parent
                self.currentState = self.currentState.parent
                self.solveOneStep()
                
        else:#if no kids we go to the parent
            self.currentState = self.currentState.parent
            self.solveOneStep()
        
            
        if(theGame.getGameState() == victory):#check if we got it else no
            return True
        else:
            return False
        

            # nextStatid = self.currentState.nextChildToVisit
            # self.currentState.nextChildToVisit += 1

            # nextState = self.currentState.children[nextStatid].requiredMovable
            # theGame.makeMove(nextState)
            # self.currentState = self.currentState.children[nextStatid]

            # self.solveOneStep()
               

        
class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.TheQueue = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        theGame = self.gm #just the game master not game state
        victory = self.victoryCondition
        #checkState = theGame.getGameState()
        #visted = self.visited[self.currentState]

        # if(checkState == victory):
        #     return True ##or do nothing
        
        if self.TheQueue.empty():#if the queue is empty we have to put something in it else we are gonna pop what was in it

            childrenLen = len(self.gm.getMovables())
            childs = self.gm.getMovables()
            dep = self.currentState.depth

            for i in range(0,childrenLen):#just putting all the kids with their parent
                nextMove = childs[i]
                theGame.makeMove(nextMove)

                childState = GameState(theGame.getGameState(), dep + 1, nextMove)
                #self.currentState.children.append(GameState(theGame.getGameState(), dep + 1, nextState))
                if(not self.visited.get(childState, False)):
                    if(not childState in self.currentState.children):
                        self.currentState.children.append(childState)
                        childState.parent = self.currentState
                        self.visited[childState] = True
                        self.TheQueue.put_nowait(childState)

                theGame.reverseMove(nextMove)

        nextState = self.TheQueue.get()

        while 1: #this just gets us to the root node and then stops
            if not self.currentState.parent:
                break

            prevStat = self.currentState.requiredMovable
            theGame.reverseMove(prevStat)
            self.currentState = self.currentState.parent
        #now we gotta find where we were in the tree
        while nextState.depth != self.currentState.depth: #just us going down under as the assuies say
            theMove = nextState

            while(self.currentState.depth + 1) != theMove.depth:#getting right underneath the current state
                theMove = theMove.parent
            
            for kiddos in self.currentState.children:#then if its the right kid we gonna hop into that
                if kiddos.requiredMovable == theMove.requiredMovable:
                    theGame.makeMove(kiddos.requiredMovable)
                    self.currentState = kiddos
                    break

        if(theGame.getGameState() == victory):
            return True

        childrenLen = len(self.gm.getMovables())
        childs = self.gm.getMovables()
        dep = self.currentState.depth
         
        for i in range(0,childrenLen):#just putting all the kids with their parent
                nextMove = childs[i]
                theGame.makeMove(nextMove)

                childState = GameState(theGame.getGameState(), dep + 1, nextMove)
                #self.currentState.children.append(GameState(theGame.getGameState(), dep + 1, nextState))
                if(not self.visited.get(childState, False)):
                    if(not childState in self.currentState.children):
                        self.currentState.children.append(childState)
                        childState.parent = self.currentState
                        self.visited[childState] = True
                        self.TheQueue.put_nowait(childState)

                theGame.reverseMove(nextMove)







        

        
