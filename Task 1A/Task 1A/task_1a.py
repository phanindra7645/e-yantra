
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a.py
# Functions:		readImage, solveMaze
# 					[ Comma separated list of functions in this file ]
# Global variables:	CELL_SIZE
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20


def readImage(img_file_path):
    global h2,w2
    #originalImage = cv2.imread('C:/Users/Dell/Desktop/task1#rr/2. Practice/Task 1B/task_1b_images/maze00.jpg')
    originalImage = cv2.imread(img_file_path)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
      
    (thresh, binary_img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
   
    return binary_img

#N=h2-1
#M=w2-1
final=[]

def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):
    ########################
    binary_img=original_binary_img
    [h,wq]=binary_img.shape
    h2=int(h/10)
    w2=int(wq/10)
    main_img=np.zeros((h2+1,w2+1))
    #blacks=0 #whites=1
    h1=int(h/20)
    w1=int(wq/20)
    for i in range(h1):
       for j in range(w1):   
        #strips across row 16x4
            if binary_img[20*i+10,20*j+19]==255:
               main_img[2*i+1][2*j+2]=1
        #strips across column  4x16 
            if binary_img[20*i+19,20*j+10]==255:
                main_img[2*i+2][2*j+1]=1
        # white cells 16x16
            main_img[2*i+1][1+2*j]=1
    maze=main_img[1:h2,1:h2]     
    maze=maze.astype(int) 
    #######################
    global final,M,N
    shortestPath = []
    N=no_cells_height*2-1
    M=no_cells_width*2-1
    sol = [ [ 0 for j in range(M) ] for i in range(N) ] 

    path = solveMazeUtil(maze, initial_point, final_point , sol)

    if len(path) == 0: 
    	print("Solution doesn't exist"); 
    	return False
    final=path[:]
    # return True
    count=0
    for (x,y) in final:
        if x%2 == 0 and y%2 == 0:
            shortestPath.append((int(x/2),int(y/2)))
    count = len(shortestPath)
    print(shortestPath)
    return shortestPath


#############	You can add other helper functions here		#############
def isValid(maze, sol, x, y):
    if not(maze[x][y]==0 or sol[x][y]!=0):
        return True
    return False

def isSafe( x, y ): 
	if x >= 0 and x < M and y >= 0 and y < N : 
		return True
	
	return False

def solveMazeUtil(maze, a, b, sol): 
    a1 = 2*a[0]
    a2 = 2*a[1]
    queue = [(a1,a2)]
    sol[a1][a2]=1
    
    parent = [[(-1,-1) for i in range(M)] for i in range(N)]
	# if (x, y is goal) return True 
    count = 0
    
    	# Check if maze[x][y] is valid 
    while  len(queue) > 0:
        x, y = queue.pop(0)
        count += 1
        
        if x==b[0]*2 and y==b[1]*2:
            break
        
        if isSafe( x+1, y) and isValid(maze,sol,x+1,y):
            sol[x+1][y] = 1
            queue.append((x+1, y))
            parent[x+1][y] = (x,y)
            
        if isSafe( x, y+1) and isValid(maze,sol,x,y+1):    
            sol[x][y+1] = 1
            queue.append((x,y+1))
            parent[x][y+1] = (x,y)
        
        if isSafe( x-1, y) and isValid(maze,sol,x-1,y):
            sol[x-1][y] = 1
            queue.append((x-1,y))
            parent[x-1][y] = (x,y)
            
        if isSafe( x, y-1) and isValid(maze,sol,x,y-1):
            sol[x][y-1] = 1
            queue.append((x,y-1))
            parent[x][y-1] = (x,y)
            
        
        
    
    if(parent[M-1][N-1] == (-1,-1)):
        return []
    else:
        path = []
        x,y = b[0]*2,b[1]*2
        while x != -1 and y != -1 :
            path.append((x,y))
            x,y = parent[x][y]
        path.reverse()
        return path


#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (1, 3)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)
        
		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()    
	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


