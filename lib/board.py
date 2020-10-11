from lib.node import Node
from res.glob import * 
import pygame

class Board:
    def __init__(self, screen, size, pixel_num, draw_grid, map=0, animations=1):
        self.pNum = pixel_num
        self.screen = screen
        self._drawGrid = draw_grid

        self.height = size[1]
        self.width = size[0]
        
        self.pHeight = self.height // self.pNum
        self.pWidth = self.width // self.pNum
        
        self.startNodePos = None
        self.endNodePos = None

        self.animations = animations
        self.__initNodes(map)

    def setNodeState(self, pos, state):
        if state == states.start:
            self.startNodePos = pos
        elif state == states.end:
            self.endNodePos = pos

        if pos == self.startNodePos and state != states.start:
            self.startNodePos = None
        elif pos == self.endNodePos and state != states.end:
            self.endNodePos = None

        self.nodes[pos[0]][pos[1]].state = state
    
    def setNodeHScore(self, pos, value):
        self.nodes[pos[0]][pos[1]].hScore = value
    
    def setNodeLScore(self, pos, value):
        self.nodes[pos[0]][pos[1]].lScore = value
    
    def setNodePrev(self, pos, prevPos):
        self.nodes[pos[0]][pos[1]].prev = prevPos
    
    def getNodeState(self, pos: tuple):
        if (0 <= pos[0] < self.pNum) and (0 <= pos[1] < self.pNum):
            return self.nodes[pos[0]][pos[1]].state
                    
    def getNodeScore(self, pos:tuple):
        return self.nodes[pos[0]][pos[1]].getScore(pos, self.endNodePos)

    def __initNodes(self, map):
        self.nodes = []
        
        for x in range(self.pNum):
            self.nodes.append([])
            for y in range(self.pNum):
                startPos = (x * self.pWidth, y * self.pHeight)
                nodeState = 0
                
                if map == 1:
                    nodeState = states.empty if y % 2 == 0 else states.wall
                
                elif map == 2:
                    pLast = self.pNum-1
                    if (x+1) % 3 == 0 and y != pLast:
                        nodeState = states.empty
                    elif (y % 2 == 0 or y == pLast) and (x, y) not in [(0,0), (1,0), (pLast, pLast-1), (pLast-1, pLast-1)]:
                        nodeState = states.wall

                elif map == 3:
                    if (x+1) % 3 == 0:
                        nodeState = states.empty
                    elif y % 2 == 0:
                        if 0 in [x % 6, (x - 1) % 6]:
                            nodeState = states.wall
                    else:
                        if 0 in [(x + 3) % 6, (x + 2) % 6]:
                            nodeState = states.wall
                    
                self.nodes[-1].append(Node(startPos, (self.pWidth, self.pHeight), state=nodeState))

    def __drawGrid(self):
        for x in range(self.pNum+1):
            pygame.draw.line(self.screen, colors.white, (x * self.pWidth, 0), (x * self.pWidth, self.height))
        
        for y in range(self.pNum+1):
            pygame.draw.line(self.screen, colors.white, (0, y * self.pHeight), (self.width, y * self.pHeight))
    
    def getClickedPos(self, mousePos):
        x, y = (mousePos[0] // self.pWidth, mousePos[1] // self.pHeight)
        
        if x > (self.pNum - 1) or y > (self.pNum - 1):
            return self.pNum, self.pNum
        
        return x, y

    def update(self):
        # print(f"S: {self.startNodePos}, E: {self.endNodePos}")
        
        for x in range(self.pNum):
            for y in range(self.pNum):
                self.drawPixel((x, y))
        
        if self._drawGrid:
            self.__drawGrid()

    def drawPixel(self, pos):
        currentNode = self.nodes[pos[0]][pos[1]]
        pygame.draw.rect(self.screen, currentNode.color, currentNode.rect)

    def clearAlgorithm(self):
        for x in range(self.pNum):
            for y in range(self.pNum):
                if self.getNodeState((x, y)) in [states.new, states.final, states.old]:
                    self.setNodeState((x, y), states.empty)
                self.setNodeLScore((x, y), None)
                self.setNodeHScore((x, y), None)
        
    def sortNodes(self, neighbourPositions):
        return neighbourPositions.sort(key=self.getNodeScore)
    
    def drawFinal(self):
        p = self.nodes[self.endNodePos[0]][self.endNodePos[1]].prev
        while p != self.startNodePos:
            self.setNodeState(p, states.final)
            p = self.nodes[p[0]][p[1]].prev
    
    def calcNeighbours(self, x, y):
        oldLScore = self.nodes[x][y].lScore
        # print(oldLScore)
        
        # eski bloğu eskittik (eğer başlangıç değilse)
        self.setNodeState((x, y), states.old) if self.getNodeState((x, y)) != states.start else None
        
        # yeni akraba pozisyonları
        neighbourPositions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        found = False
        
        # Boş blok filtresi
        newNeighbourPositions = []
        for pos in neighbourPositions:
            if self.getNodeState(pos) == states.empty:
                newNeighbourPositions.append(pos)
                self.setNodeLScore(pos, oldLScore+1)
                self.setNodePrev(pos, (x, y))
                
                # olabilen akrabalar yeni renklerine boyandı
                self.setNodeState(pos, states.new)
            
            elif self.getNodeState(pos) == states.end:
                self.setNodePrev(pos, (x, y))
                found = pos
        
        if found:
            return found, True
        
        return newNeighbourPositions, False
        
    def startAlgorithm(self, updateFunc):
        self.clearAlgorithm()
        
        # Başlangıç bloğunu geçmişi temizlendi
        self.nodes[self.startNodePos[0]][self.startNodePos[1]].lScore = 0
        
        # node pointer vectorü
        currentNodePositions = []
        
        # start nodeunu ekledim
        currentNodePositions.append(self.startNodePos)
        found = False
        
        while True:
            if not found:
                self.sortNodes(currentNodePositions)
                newNodes, found = self.calcNeighbours(*currentNodePositions[0])
                
                if found:
                    self.drawFinal()                    
                
                currentNodePositions += newNodes
                del currentNodePositions[0]
        
            if (not self.animations and found) or self.animations:
                if (rv := updateFunc()) != 1:
                    break
            
            elif not len(currentNodePositions):
                rv = 2
                break
        
        
        if rv == 2:
            self.clearAlgorithm()
        
        return rv