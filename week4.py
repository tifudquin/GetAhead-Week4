import math

def addSameColumns(combinedRows, row, endCol):
	''' 
	Computes and adds the values in the current row that is in overlap with
	the maximum common row length (or the maximum common width of the subrectangle)

	Args:
		combinedRows: The current sum of the largest area of the subrectangle
		row: The current row of the list that is being processed in the outer loop
		endCol: The length of the maximum common width; serves as an indicator of 
			as to which column's values should only be added to combinedRows
	
	Returns:
		Returns the sum of both the largest area of the current subrectangle and 
		the values in the current row that overlaps with the maximum 
	'''

	for i in range(endCol):
		combinedRows += row[i]
	return combinedRows

def subtractExcessColumns(combinedRows, startCol, endCol, li, rowIndex):
	''' 
	Subtracts the excess column values of the previous sum of max are to get
	the sum of the current max area

	Args:
		combinedRows: The current sum of the largest area of the rectangle
		startCol: The length of the current max common width of the subrectangle;
			serves as an indicator as to where the excess column values will start
		endCol: The length of the previous maximum common width; 
			serves as indicator as to where the excess column values will end
		li: The list of lists of positive integers
		rowIndex: The index of the current row being processed in the outer loop
	
	Returns:
		Returns the updated sum of the largest area of the subrectangle
		(with the excess columns and values  from the previous largest area of
		subrectangle subtracted)
	'''

	for i in range(startCol, endCol):
		for j in range(1, rowIndex + 1):
			combinedRows -= li[rowIndex - j][i]
	return combinedRows

def getMaxArea(li, counter):
	''' 
	Computes and gets the maximum sum of each row and compares it with 
	the sum of largest area of the subrectangle

	Args:
		li: The list of lists of positive integers
		counter: The number of times the loop has already ran; used to get the 
			correct position/indices
	
	Returns:
		The sum of the largest area of the subrectangle and its indices
	'''

	maxSumRow = 0

	maxCombinedRows = []
	maxCombinedPositions = []

	maxRowLength = math.inf

	for rowIndex, row in enumerate(li):

		# Sum of row
		sumRow = sum(num for num in row)

		if sumRow > maxSumRow:
			maxSumRow = sumRow
			sumRowPosition = [(rowIndex + counter, 0), (rowIndex + counter + 1, len(row))]

		'''
		The start of the computation of Max Sum of Common Maximum Width
		'''

		currRowLength = len(row)

		# If current row is the first row of the list
		if maxRowLength == math.inf:
			combinedRows = sumRow
			combinedPositions = sumRowPosition
		else:
			# Get the previous max sum of common minimum width
			combinedRows = maxCombinedRows[len(maxCombinedRows) - 1]
			
			# If the maximum common rectangle width is less than currRowLength
			if maxRowLength < currRowLength:

				# Add only the values in the current row 
				# that overlaps with the maximum common width
				combinedRows = addSameColumns(combinedRows, row, maxRowLength)
				combinedPositions = [(0 + counter, 0), (rowIndex + counter + 1, maxRowLength)]

			# If the maximum common width is greater than 
			# or equal to the currRowLength
			else:
				# Add all the values in the current row
				combinedRows += sumRow

				if maxRowLength > currRowLength:
					# Subtract the excess values/columns of the 
					# previous max area to the current max area
					combinedRows = subtractExcessColumns(combinedRows, currRowLength, maxRowLength, li, rowIndex)

				combinedPositions = [(0 + counter, 0), (rowIndex + counter + 1, currRowLength)]

		maxRowLength = min(maxRowLength, currRowLength)

		maxCombinedRows.append(combinedRows)
		maxCombinedPositions.append(combinedPositions)

	combinedRows = max(maxCombinedRows)
	maxIndex = maxCombinedRows.index(combinedRows)
	combinedPositions = maxCombinedPositions[maxIndex]

	# Compare max sum of each row (maxSumRow) to the
	# max sum of the sum of largest area of the subrectangle (combinedRows)
	if combinedRows < maxSumRow:
		combinedRows = maxSumRow
		combinedPositions = sumRowPosition
		
	return [combinedRows, combinedPositions]


def getLargestAreaSum(li):
	# A function that finds the rectangle containing the largest sum 
	# Such that the rectangle does not contain any empy/missing cells
	# Input is a list of lists of positive integers
	# This returns the pair of array indices that represent the rectangle

	''' 
	Finds the subrectangle containing the largest sum such that the
	rectangle does not contain any empty/missing cells

	Args:
		li: The list of lists of positive integers
	
	Returns:
		The sum of the largest area of the whole list of lists and its indices
	'''

	maxRectangle = []

	# Counter for pop()
	# Used to get the correct position/indices
	counter = 0 

	while len(li) > 0:
		subRectangle = getMaxArea(li, counter)

		if counter == 0:
			maxRectangle = subRectangle

		if maxRectangle[0] < subRectangle[0]:
			maxRectangle = subRectangle

		li.pop(0)
		counter += 1

	position = str(maxRectangle[1][0]) + " -- " + str(maxRectangle[1][1])

	return position
