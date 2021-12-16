def readObj(objFile):
    obj = open(objFile+".obj", "r").read().split("\n")
    vertices = []
    edges = []
    for line in obj:
        if (len(line)>0): #check line isn't empty
            if (line[0] == "v"): #collecting vertices
                tempArray = line.split(" ")
                tempArray.pop(0)
                tempArray = [float(x) for x in tempArray] #converting strings to floats
                vertices.append(tempArray)
            elif (line[0] == "l"): #collecting lines
                tempArray = line.split(" ")
                tempArray.pop(0)
                tempArray = [int(x)-1 for x in tempArray] #converting strings to useful ints
                edges.append(tempArray) 
    largestVert = max(map(max, vertices)) #find largest vertex
    vertices = [[coord/largestVert for coord in vertex] for vertex in vertices] #scale all vertices to be within range -1 to 1, this is not enough when rotating also
    return(vertices,edges)
