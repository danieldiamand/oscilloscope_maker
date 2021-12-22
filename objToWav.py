import wave, struct, math
from readObj import readObj
from rotateVertex import rotateVertices
from chinesePostman import eulerianPath

objFileName = "cube"
saveFileName = "cubeTest"
frameRate = 44100
initRotation = [0,0,0] #in degrees
rotationArray = [0,0,0] #in degrees
rotations = 360
loops = 1 #how many loops it runs for
scale = 0.4
speedLimit = 0.02

class Line:
    def __init__(self, x1,y1,x2,y2):
        self.x1 = x1*scale
        self.y1 = y1*scale
        self.x2 = x2*scale
        self.y2 = y2*scale
        self.drawFrames = 14 #how many frames it takes to draw line, ie how long it takes to move between point 1 and 2 
        self.xStep = (self.x2-self.x1)/self.drawFrames
        self.yStep = (self.y2-self.y1)/self.drawFrames
 
def addToFile(sample):
    sample = int(sample * (2 ** 15 - 1))
    f.writeframes(struct.pack("<h", sample))


vertices, edges = readObj(objFileName)
vertices = rotateVertices(vertices, initRotation)
maxVertix = max([max(edge) for edge in edges])+1
edges = eulerianPath(edges)

with wave.open(saveFileName+".wav", "w") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(frameRate)
    for i in range(rotations):
        lineArray = []
        for edge in edges:
            lineArray.append(Line(vertices[edge[0]][0],vertices[edge[0]][1], vertices[edge[1]][0], vertices[edge[1]][1]))
        for line in lineArray:
            for i in range(line.drawFrames):
                addToFile(line.x1+(line.xStep*i))
                addToFile(line.y1+(line.yStep*i))
        vertices = rotateVertices(vertices, rotationArray)
