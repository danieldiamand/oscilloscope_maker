import wave, struct, math
from readObj import readObj
from rotateVertex import rotateVertices
from eulerianPath import orderEdges

class Line():
    scale = 1
    def __init__(self, x1,y1,x2,y2, speed):
        self.x1 = x1*self.scale
        self.y1 = y1*self.scale
        self.x2 = x2*self.scale
        self.y2 = y2*self.scale
        self.xChange = (self.x2-self.x1)
        self.yChange = (self.y2-self.y1)
        self.distance = math.hypot(self.xChange, self.yChange)
        self.stepsToDraw = max(int(self.distance/speed),1)
        self.xStep = self.xChange/self.stepsToDraw
        self.yStep = self.yChange/self.stepsToDraw
    def walkPos(self, stepNum):
        return self.x1 + self.xStep*stepNum, self.y1 + self.yStep*stepNum


class ObjAnimator:
    def __init__(self, objFileName, scale, initRotation= None):
        Line.scale = scale
        rawVertices, rawEdges = readObj(objFileName)
        self.verticies = rotateVertices(rawVertices, initRotation if initRotation else [0,0,0])
        self.edges = orderEdges(rawEdges) 
        self.fileArray = []

    def addToFileArray(self, sample):
        binarySample = int(sample * (2 ** 15 - 1))
        self.fileArray.append(struct.pack("<h", binarySample))

  
    def saveAsFile(self, saveFileName):
        with wave.open(saveFileName+".wav", "w") as f:
            f.setnchannels(2)
            f.setsampwidth(2)
            f.setframerate(44100)
            # f.writeframes(sum(self.fileArray))
    
    def animateRotation(self, draws, rotationPerDraw, drawSpeed):
        print("animate")
        vertices = self.verticies
        for _ in range(draws):
            lineArray = []
            for edge in self.edges:
                lineArray.append(Line(vertices[edge[0]][0],vertices[edge[0]][1], vertices[edge[1]][0], vertices[edge[1]][1], drawSpeed))
            for line in lineArray:
                for step in range(line.stepsToDraw):
                    self.addToFileArray(line.walkPos(step)[0])
                    self.addToFileArray(line.walkPos(step)[1])
            vertices = rotateVertices(vertices, rotationPerDraw)

spinCube = ObjAnimator("cube", 0.4)
spinCube.animateRotation(360, [0,1,0], 0.01)
spinCube.saveAsFile("test")