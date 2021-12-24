import wave, struct, math, numpy as np
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
        print(self.xChange)
        self.yChange = (self.y2-self.y1)
        self.distance = math.hypot(self.xChange, self.yChange)
        self.stepsToDraw = max(int(self.distance*500/speed),1)
        self.xStep = self.xChange/self.stepsToDraw
        self.yStep = self.yChange/self.stepsToDraw
    def _walkPos(self, stepNum):
        return self.x1 + self.xStep*stepNum, self.y1 + self.yStep*stepNum


class ObjAnimator:
    def __init__(self, objFileName, scale, initRotation= None):
        """
        test
        """
        Line.scale = scale
        rawVertices, rawEdges = readObj(objFileName)
        self.vertices = rotateVertices(rawVertices, initRotation if initRotation else [0,0,0])
        self.edges = orderEdges(rawEdges) 
        self.fileArray = []

    def _addToFileArray(self, sample):
        binarySample = int(sample * (2 ** 15 - 1))
        self.fileArray.append(struct.pack("<h", binarySample))

  
    def saveAsFile(self, saveFileName):
        """Saves object as .wav file"""
        with wave.open(saveFileName+".wav", "w") as f:
            f.setnchannels(2)
            f.setsampwidth(2)
            f.setframerate(44100)
            f.writeframes(np.array(self.fileArray).tobytes())

    def _draw(self, vertices, drawSpeed):
        lineArray = []
        for edge in self.edges:
            lineArray.append(Line(vertices[edge[0]][0],vertices[edge[0]][1], vertices[edge[1]][0], vertices[edge[1]][1], drawSpeed))
        for line in lineArray:
            for step in range(line.stepsToDraw):
                self._addToFileArray(line._walkPos(step)[0])
                self._addToFileArray(line._walkPos(step)[1])
    
    def animateStill(self, draws, drawSpeed):
        """
        Draws object still
        
        :param int draws: How many times to draw object
        :param int drawSpeed: How fast drawing point moves, in screen width/1000 per frame, use 9ish for steady image
        """
        for _ in range(draws):
            self._draw(self.vertices, drawSpeed)

    def animateRotation(self, draws, drawSpeed, drawRotation):
        """
        Draws object rotating
        
        :param int draws: How many times to draw object
        :param int drawSpeed: How fast drawing point moves, use 9ish for steady image. In unit (screen width/1000 per frame) 
        :param array or tuple drawRotation: Rotates vertices by (x,y,z) per draw, in degrees
        """
        vertices = self.vertices
        for _ in range(draws):
            self._draw(vertices, drawSpeed)
            vertices = rotateVertices(vertices, drawRotation)
    
    def animateSpeedChange(self, draws, startSpeed, endSpeed, steepness):
        """
        Draws object with changing drawSpeed
        
        :param int draws: How many times to draw object
        :param int startSpeed: How fast drawing point moves at start of draws. In unit (screen width/1000 per frame) 
        :param int endSpeed: How fast drawing point moves at end of draws. In unit (screen width/1000 per frame) 
        :param int steepness: (-steepness/x) determines rate of accelation of drawSpeed.
        """
        quadratic = [endSpeed-startSpeed,(draws-1)*(endSpeed-startSpeed),(draws-1)*-steepness]
        a=min(np.roots(quadratic))
        b=startSpeed-(-steepness/a)
        for x in range(draws):
            drawSpeed = (-steepness/(x+a))+b
            self._draw(self.vertices, drawSpeed)


if __name__ == "__main__":
    spinCube = ObjAnimator("square", 1)
    spinCube.animateRotation(360, 9, (0,1,0))
    spinCube.saveAsFile("testCube")
