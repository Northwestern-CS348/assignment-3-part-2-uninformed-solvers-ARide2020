
from solver import *

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
        checkState = self.currentState.state
        visted = self.visited[self.currentState]

        if checkState == victory:
            return True ##or do nothing

        if(self.visited[self.currentState] == False):
            self.visited[self.currentState] = True

            dep = self.currentState.depth
            childrenLen = len(self.gm.getMovables())
            childs = self.gm.getMovables()

            if childrenLen != 0:
                for i in range(0,childrenLen):
                    nextState = childs[i]
                    theGame.makeMove(nextState)
                    self.currentState.children.append(GameState(theGame.getGameState(), dep + 1, nextState))
                    theGame.reverseMove(nextState)
                    self.currentState.children[i].parent = self.currentState


                nextStatid = self.currentState.nextChildToVisit
                self.currentState.nextChildToVisit += 1

                nextState = self.currentState.children[nextStatid].requiredMovable
                theGame.makeMove(nextState)
                self.currentState = self.currentState.children[nextStatid]

                self.solveOneStep()

            else:
                theGame.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

                for c in self.currentState.children:
                    if self.visited[c] != True:
                        self.currentState = c
                        self.solveOneStep()
        else:
                theGame.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

                for c in self.currentState.children:
                    if self.visited[c] != True:
                        self.currentState = c
                        self.solveOneStep()


            

        
class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

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
        return True
