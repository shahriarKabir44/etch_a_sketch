from re import S
from tkinter.messagebox import NO
import cv2


class Point:
    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.isWithinSegment = True
        self.next: Point = None
        self.prev: Point = None
        self.color: tuple = color

    def connect(self, pt):
        self.next = pt
        pt.prev = self


class LinkedList:
    def __init__(self, head: Point) -> None:
        self.head: Point = head
        self.tail: Point = head

    def canTakePoint(self, point1, point2, minimumDistance):
        x1, y1 = point1
        x2, y2 = point2
        return (x1-x2)**2 + (y1-y2)**2 >= minimumDistance**2

    def append(self, pt: Point):
        if self.head == None:
            self.head = pt
            self.tail = pt
            return
        self.tail.connect(pt)
        self.tail = pt

    def pop(self, pt: Point):
        l = pt.prev
        r = pt.next
        if l == None and r == None:
            self.head = None
            self.tail = None
            return
        if l == None:
            self.head = r
            self.head.prev = None
            return
        if r == None:
            self.tail = l
            self.tail.next = None
            return
        l.next = r
        r.prev = l

    def findAndRemove(self, leftIndex, threshold=15):
        top = self.head
        while top != None:
            if not self.canTakePoint([top.x, top.y], leftIndex, threshold):
                if top.prev != None:
                    top.prev.isWithinSegment = False
                    temp = top.next
                    self.pop(top)
                    top = temp
            else:
                top = top.next

    def drawLineSegments(self, point1: Point, point2: Point, imageObject):
        cv2.line(imageObject, (point1.x, point1.y),
                 (point2.x, point2.y), point1.color, 15)

    def draw(self, imageObject):
        top = self.head
        while top != None:
            if top.prev:
                if top.prev.isWithinSegment:
                    self.drawLineSegments(top, top.prev, imageObject)
            top = top.next
