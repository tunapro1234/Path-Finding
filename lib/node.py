from res.glob import *
import pygame

class Node:
    def __init__(self, startPos, size, state=0):
        self.l_score = float("Infinity")
        self.h_score = None
        self.state = state

        self.rect = pygame.Rect(startPos, size)

    def calc_h_score(self, nodePos, endNodePos):
        (xt, yt), (xe, ye) = nodePos, endNodePos
        self.h_score = ((abs(xt)-abs(xe)) ** 2 + (abs(yt)-abs(ye)) ** 2) ** 0.5
    
    @property
    def score(self):
        return self.l_score + self.h_score

    @property
    def state(self):
        # BOŞ
        if self.color == colors.black:
            return states.empty
        
        # BAŞLANGIÇ
        elif self.color == colors.turq:
            return states.start
        
        # DUVAR
        elif self.color == colors.white:
            return states.wall
        
        # BİTİŞ
        elif self.color == colors.red:
            return states.end
        
        # KULLANILMIŞ
        elif self.color == colors.blue:
            return states.old
        
        # GELECEK
        elif self.color == colors.green:
            return states.new
        
        # SONUÇ
        elif self.color == colors.orange:
            return states.final

    @state.setter
    def state(self, value):
        # BOŞ
        if value == states.empty:
            self.color = colors.black
            return states.empty
        
        # BAŞLANGIÇ
        elif value == states.start:
            self.color = colors.turq
            return states.start
        
        # DUVAR
        elif value == states.wall:
            self.color = colors.white
            return states.wall
        
        # BİTİŞ
        elif value == states.end:
            self.color = colors.red
            return states.end
        
        # KULLANILMIŞ
        elif value == states.old:
            self.color = colors.blue
            return states.old
        
        # GELECEK
        elif value == states.new:
            self.color = colors.green
            return states.new
        
        # SONUÇ
        elif value == states.final:
            self.color = colors.orange
            return states.final

    def __repr__(self):
        return f"({self.state}, {self.color})"