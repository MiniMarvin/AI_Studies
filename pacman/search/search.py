# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


## TODO: implement iterative DFS
def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  # visited = []
  # st = (problem.getStartState(), "")
  # lst = recursive_dfs(st, problem, visited)
  # lst = [a for a in reversed(lst)]
  
  # print lst
  lst = iterative_dfs(problem)
  
  return  lst


def iterative_dfs(problem):
  visited = set()
  final_path = util.Stack()
  stack = util.Stack()
  st = (problem.getStartState(), None, None)

  stack.push(st)

  while not stack.isEmpty():
    # retrieve the node in the top of the stack
    node, father, action = stack.pop()
    
    # mark as visited and add to the path end
    visited.add(node)
    final_path.push((node, father, action))

    # Check if won
    if problem.isGoalState(node):
      print "Won at: ", node
      break

    # add to the stack the next nodes to visit
    nxt = problem.getSuccessors(node)
    non_visiteds = []


    # if found some element to iter over
    for a in nxt:
      element, element_action, trash = a
      if element not in visited:
        non_visiteds += [element]
        stack.push((element, node, element_action))
    

    # did not found any element, it means dead end them we need to retrieve to find the next step
    if len(nxt) == 0 or len(non_visiteds) == 0:
      final_path.pop()
      while len(final_path.list) > 0:
        top_node, top_father, top_action = stack.list[len(stack.list) - 1]
        move_node, move_father, move_action = final_path.list[len(final_path.list) - 1]
        
        # keep removing from the list untill top_father be the move_node
        if move_node == top_father:
          break
        print "Removing: ", final_path.list[len(final_path.list) - 1]
        final_path.pop()

      continue

  move_seq = [a[2] for a in final_path.list if a[2] != None]
  print "Iterative DFS result: ", move_seq
  return move_seq

def recursive_dfs(st, problem, visited):
  """
  st[0] - the state
  st[1] - the position to follow
  """
  # print st
  
  if problem.isGoalState(st[0]):

    # return [converter[st[1]]]
    return [st[1]]

  nxt = problem.getSuccessors(st[0])

  if len(nxt) == 0: # no valid moves from here
    return []

  visited += [st[0]]

  for a in nxt:
    if a[0] not in visited:
      # print a
      res = recursive_dfs(a, problem, visited)
      if len(res) == 0:
        continue
      else:
        # return res + [st[1]]
        if st[1] != '':
          return res + [st[1]]

        return res

  return []

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  # util.raiseNotDefined()
  lst = iterative_bfs(problem)
  return lst


## TODO: modify the code for the sequence move lists become coherent need a lot of lists
def iterative_bfs(problem):
  """
  element[0] - the node position
  element[1] - the node father
  element[2] - the move made to reach this position from his father
  """
  visited = set()
  final_path = []
  queue = util.Queue()
  st = (problem.getStartState(), None, None)
  final_seq = []

  queue.push(st)
  final_path += [[st]]

  while not queue.isEmpty():
    node, father, action = queue.pop()
    
    print queue.list

    # if we already visited that node ignore it
    if node in visited:
      # print "already visited: ", node
      continue
    
    # if not just add to the visited nodes list
    visited.add(node)

    # generate new lists with the actual element at it end
    # print "my lists: "
    for a in final_path:
      try:
        if father == a[len(a) - 1][0]:
          lst = list(a) + [(node, father, action)]
          final_path += [lst]
          # print lst
      except Exception as e:
        continue

    # check if we found our goal
    if problem.isGoalState(node):
      # print "\n\n\nFOUND AN ANSWER AT: ", node, "\n\n\n"
      for lst in final_path:
        if (node, father, action) in lst:
          final_seq = [a[2] for a in lst if a[2] != None]
          # print final_seq
          break
      break

    nxt = problem.getSuccessors(node)
    for element, element_move, trash in nxt:
      if element not in visited:
        queue.push((element, node, element_move))

    # use the visited heuristics to avoid the hyper expansion of the tree

  # print final_seq
  return final_seq
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  # util.raiseNotDefined()
  st = (0, problem.getStartState())
  frontier = util.PriorityQueue()

  frontier.push(st[1], st[0])

  cost_list = dict({
    st[1]: {
      'cost': 0,
      'action': ''
      }
    })

  goal_node = (-1,-1)
  seq = []
  total_cost = 0

  while not frontier.isEmpty():
    node = frontier.pop()
    # print "Node: ", node

    if problem.isGoalState(node):
      # print "Answer found at: ", node
      goal_node = node
      total_cost = cost_list[node]['cost']
      seq += [cost_list[node]['action']]
      break

    nxt = problem.getSuccessors(node)

    for element in nxt:
      el_node, el_move, trash = element
      # print "Cost List: ", cost_list

      # insert elements in the priority queue 
      new_cost = problem.costFn(el_node) + cost_list[node]['cost']
      try:
        old_cost = cost_list[el_node]['cost']
      except Exception as e:
        old_cost = float("inf")
      
      if new_cost < old_cost:
        frontier.push(el_node, new_cost)
        cost_list[el_node] = {'cost': new_cost, 'action': el_move}
    pass

  # to retrieve the sequence is necessary to go looking for the nodes one by one untill the begin
  while goal_node != problem.getStartState():
    nxt = problem.getSuccessors(goal_node)
    for element in nxt:
      el_node, el_move, trash = element
      goal_cost = problem.costFn(goal_node)
      if total_cost - goal_cost == cost_list[el_node]['cost']:
        goal_node = el_node
        total_cost -= goal_cost
        seq += [cost_list[el_node]['action']]
        break

  seq = [a for a in reversed(seq) if a != '']
  print seq

  return seq


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
