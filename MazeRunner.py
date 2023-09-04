import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

maze = np.zeros((31,31),int) # Make a 31x31 grid of zeros - this leaves space for a gap in between each line (for walls) as well as a border
for i in range(31):
    for j in range(31):
        if i==0 or i==30 or j==0 or j==30: maze[i][j] = 1 # Set border of maze = 1

lines = open("maze.txt","r").read().split("\n") # Split text file into line-by-line array

for i in range(1,len(lines)): # Skip the first line - first line will be csv header

    lines[i] = lines[i].split(",") # Split line by comma

    x = 2 * int(lines[i][0]) + 1 # Map x to maze
    y = 2 * (14 - int(lines[i][1])) + 1 # Map y to maze

    maze[x][y+1] = int(lines[i][2]) # Put roof above
    maze[x+1][y] = int(lines[i][3]) # Put wall right
    maze[x][y-1] = int(lines[i][4]) # Put floor below
    maze[x-1][y] = int(lines[i][5]) # Put wall left
    if maze[x][y+1] and maze[x+1][y]: maze[x+1][y+1] = 1 # Top right corner
    if maze[x+1][y] and maze[x][y-1]: maze[x+1][y-1] = 1 # Bottom right corner
    if maze[x][y-1] and maze[x-1][y]: maze[x-1][y-1] = 1 # Bottom left corner
    if maze[x-1][y] and maze[x][y+1]: maze[x-1][y+1] = 1 # Top left corner

# Breadth-First Search Algorithm
currentX, currentY = 15, 15 # Start pathing from middle of maze
currentPath = [] # To keep track of path from any given point as we will be jumping around a lot
expanded, fringe = [], [[currentX,currentY,currentPath]] # Create arrays for previous moves, path and fringe
maze[15][15] = 2 # As we have already added it to the fringe
flag = 0 # We will use a simple flag to determine if we found a solution or not

while len(fringe) > 0: # Keep looping until there is nothing new to expand

    expanded.append(fringe[0]) # Expand next (least deep) fringe coordinate

    currentX = fringe[0][0] # Update X
    currentY = fringe[0][1] # Update Y
    currentPath = fringe[0][2] # Update current path

    if currentX == 29 and currentY == 1: # If goal is reached:
        print("Solution Found!") # Task 2
        flag = 1 # Trigger the flag
        break # Break out of loop to stop inefficiency

    if not maze[currentX][currentY + 1]: # Check if above is moveable
        fringe.append([currentX,currentY + 1,currentPath + [1]]) # Add to fringe if it is
        maze[currentX][currentY + 1] = 2 # Label it as "spotted"

    if not maze[currentX + 1][currentY]: # Check if right is moveable
        fringe.append([currentX + 1,currentY,currentPath + [2]]) # Add to fringe if it is
        maze[currentX + 1][currentY] = 2 # Label it as "spotted"

    if not maze[currentX][currentY - 1]: # Check if below is moveable
        fringe.append([currentX,currentY - 1,currentPath + [3]]) # Add to fringe if it is
        maze[currentX][currentY - 1] = 2 # Label it as "spotted"

    if not maze[currentX - 1][currentY]: # Check if left is moveable
        fringe.append([currentX - 1,currentY,currentPath + [4]]) # Add to fringe if it is
        maze[currentX - 1][currentY] = 2 # Label it as "spotted"
    
    fringe.pop(0) # Remove newly expanded node from fringe

if flag: # He only leaves the maze if he finds an exit

    xBestMoves, yBestMoves = [15], [15] # We must make a list of coordinates that detail the best possible path (for part 4)
    previousMove = 0 # Variable to hold what the previous move was
    directionLines = [] # This will hold the directions we use for the txt file
    f = open("directions.txt", "w") # Open the file to write directions
    for move in currentPath: # The final path (best solution)   
        if move == 1: # Move up
            xBestMoves.append(xBestMoves[-1])
            yBestMoves.append(yBestMoves[-1] + 1)
            if previousMove == 1: directionLines.append("STRAIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 4: directionLines.append("RIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 2: directionLines.append("LEFT\n") # Change of direction based on what the previous move was
        if move == 2: # Move right
            xBestMoves.append(xBestMoves[-1] + 1)
            yBestMoves.append(yBestMoves[-1])
            if previousMove == 2: directionLines.append("STRAIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 1: directionLines.append("RIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 3: directionLines.append("LEFT\n") # Change of direction based on what the previous move was
        if move == 3: # Move down
            xBestMoves.append(xBestMoves[-1])
            yBestMoves.append(yBestMoves[-1] - 1)
            if previousMove == 3: directionLines.append("STRAIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 2: directionLines.append("RIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 4: directionLines.append("LEFT\n") # Change of direction based on what the previous move was
        if move == 4: # Move left
            xBestMoves.append(xBestMoves[-1] - 1)
            yBestMoves.append(yBestMoves[-1])
            if previousMove == 4: directionLines.append("STRAIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 3: directionLines.append("RIGHT\n") # Change of direction based on what the previous move was
            if previousMove == 1: directionLines.append("LEFT\n") # Change of direction based on what the previous move was
        previousMove = move

    xBestMoves.append(30) # Add in the last little bit where Thomas leaves the side of the maze (x)
    yBestMoves.append(1) # Add in the last little bit where Thomas leaves the side of the maze (y)
    f.writelines(directionLines) 
else:
    print("No Solution Found :(")


xExploration, yExploration = [15], [15] # We must make a list of coordinates where Thomas travelled (for part 3)
allPaths = [row[2] for row in expanded] # Get all the expanded paths

for path in allPaths:

    stitch = [] # Clear out stitch
    for move in path:
        stitch.append((move+2)%4) # Add on the "reverse" move
        if stitch[-1] == 0: stitch[-1] = 4  # If the "reverse" move is 0 then make it 4 as 0 is not a move
    stitch.reverse() # Flip it so that its the reverse of the normal moveset (this will send it back to the origin)
    path += stitch # Stitch it on! Esssentially this whole process is to take the path from the origin to the current node and then "stitch on" the reverse path to send it back to the origin

    for move in path: # Then go through and actually apply the moves
        if move == 1: # Move up
            xExploration.append(xExploration[-1])
            yExploration.append(yExploration[-1] + 1)
        if move == 2: # Move right
            xExploration.append(xExploration[-1] + 1)
            yExploration.append(yExploration[-1])
        if move == 3: # Move down
            xExploration.append(xExploration[-1])
            yExploration.append(yExploration[-1] - 1)
        if move == 4: # Move left
            xExploration.append(xExploration[-1] - 1)
            yExploration.append(yExploration[-1])

if flag:
    del xExploration[len(xExploration)-len(stitch):len(xExploration)] # If an exit is reached, stop Thomas from returning to origin by removing the last few stitched on movements (x)
    del yExploration[len(yExploration)-len(stitch):len(yExploration)] # If an exit is reached, stop Thomas from returning to origin by removing the last few stitched on movements (y)
    xExploration.append(30) # Add in the last little bit where Thomas leaves the side of the maze (x)
    yExploration.append(1) # Add in the last little bit where Thomas leaves the side of the maze (y) 


# Create plot points for walls
xWalls, yWalls = [], []
for i in range(31):
    for j in range(31):
        if maze[i][j] == 1:
            xWalls.append(i) 
            yWalls.append(j)


# Code for creating the animated plot for Thomas's exploration
fig, ax = plt.subplots()
ax.set_xlim(-1,31)
ax.set_ylim(-1,31)
line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animateBestPath(i):
    x = xBestMoves[:i+1]
    y = yBestMoves[:i+1] 
    line.set_data(x, y)
    return line,

def animateExploration(i):
    line.set_linestyle(":")
    x = xExploration[:i+1]
    y = yExploration[:i+1] 
    line.set_data(x, y)
    print("Generating Exploration GIF: " + str(round((i/len(xExploration))*100)) + "%")
    return line,

# Create the plot for the best path
if flag:
    plt.scatter(xWalls,yWalls,c="#000000",marker="s")
    bestPathPlot = FuncAnimation(fig, animateBestPath, init_func=init,frames=len(xBestMoves), interval=1000, blit=True)
    plt.title("Best Maze Path")
    ax.set_aspect('equal', adjustable='box')
    ax.set_axis_off()
    plt.tight_layout()
    bestPathPlot.save('BestPath.gif',writer=PillowWriter(fps=60),dpi=100)
    plt.close()


# Create the plot for the exploration
# Since its breadth first search, Thomas goes back through the origin (glade) each time to get from point to point,
# because he always prioritises checking the closest unexplored point to the glade. (as this will let him find the most optimal path to the exit.)
# The exploration plot moves relatively fast but you can see him backtrack to the origin every time. The more he walks over a certain spot, the thicker the line will get. He only "explores" each square once.
# You could sort of think about this as him going out every day, mapping the closest unexplored tile, then coming home, and repeating. (That's how it works in the movies)
# The resulting GIF is several minutes long so it takes a while to render
explorationPlot = FuncAnimation(fig, animateExploration, init_func=init,frames=len(xExploration), interval=1, blit=True)
plt.title("Maze Runner Exploration")
ax.set_aspect('equal', adjustable='box')
ax.set_axis_off()
plt.tight_layout()
explorationPlot.save('Exploration.gif',writer=PillowWriter(fps=60),dpi=100)
plt.close()