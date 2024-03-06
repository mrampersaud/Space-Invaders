"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _right: whether the alien wave is currently moving to the right
    #Invariant: _right is a bool
    #
    # Attribute _left: whether the alien wave is currently moving to the left
    #Invariant: _left is a bool
    #
    # Attribute _abolt1: number of step until alien fire
    # Invariant: _abolt1 is an integer between 1 and BOLT_RATE
    #
    # Attribute _steps: number of steps an alien has moved
    # Invariant: _steps is an integer between 0 and BOLT_RATE
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a wave of aliens
        """
        self._ship = Ship()
        self._aliens = self.alienwave()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], linecolor='grey', linewidth=1.5)
        #self._lives =
        self._time = 0
        self._right = True
        self._left = False
        self._abolt1 = random.randint(1, BOLT_RATE)
        self._steps = 0

    def alienwave(self):
        """
        Returns a 2D list as a wave of aliens
        """
        wave = []
        left = ALIEN_H_SEP + ALIEN_WIDTH//2
        ceil = GAME_HEIGHT - ALIEN_CEILING
        bottom = ceil - (ALIEN_HEIGHT + ALIEN_V_SEP)*(ALIEN_ROWS)

        for row in range(ALIEN_ROWS):
            newrow = []
            if (row % 6) == 0 or (row % 6) == 1:
                for pos in range(ALIENS_IN_ROW):
                    alien = Alien(x = left, y = bottom, source = 'alien1.png')
                    newrow.append(alien)
                    left = left + ALIEN_H_SEP + ALIEN_WIDTH

            elif (row % 6) == 2 or (row % 6) == 3:
                for pos in range(ALIENS_IN_ROW):
                    alien = Alien(x = left, y = bottom, source = 'alien2.png')
                    newrow.append(alien)
                    left = left + ALIEN_H_SEP + ALIEN_WIDTH

            elif (row % 6) == 4 or (row % 6) == 5:
                for pos in range(ALIENS_IN_ROW):
                    alien = Alien(x = left, y = bottom, source = 'alien3.png')
                    newrow.append(alien)
                    left = left + ALIEN_H_SEP + ALIEN_WIDTH

            left = ALIEN_H_SEP + (ALIEN_WIDTH//2)
            bottom = bottom + ALIEN_HEIGHT + ALIEN_V_SEP
            wave.append(newrow)
        return wave


    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates a single frame in the game. Moves ship, aliens, and bolt.
        """
        # FOR CONTROLLING SHIP
        if input.is_key_down('left'):
            self._ship.x = max(0+(SHIP_WIDTH//2),  self._ship.x-SHIP_MOVEMENT)
            #print(id(self._ship))
        if input.is_key_down('right'):
            self._ship.x = min(GAME_WIDTH - (SHIP_WIDTH//2), self._ship.x+SHIP_MOVEMENT)
            #print(id(self._ship))

        # FOR CONTROLLING SHIP BOLTS
        if input.is_key_down('spacebar'):
            accum = 0
            for player in self._bolts:
                if player.isPlayerBolt():
                    accum += 1
            if accum == 0:
                bolt = Bolt(x=self._ship.x, y=self._ship.y, velocity=BOLT_SPEED)
                self._bolts.append(bolt)
        for x in self._bolts:
            if x.y > GAME_HEIGHT:
                self._bolts.remove(x)
            else:
                x.y += x.getBoltSpeed()

        # FOR CONTROLLING ALIENS
        right = GAME_WIDTH - (ALIEN_H_SEP + ALIEN_WIDTH//2)
        left = ALIEN_WIDTH//2 + ALIEN_H_SEP
        if self._time > ALIEN_SPEED:
            self._time = 0
            self._steps+=1

            if self._right: #if moving right, keep moving right
                for alien in self._aliens:
                    for pos in range(len(alien)):
                        alien[pos].x += ALIEN_H_WALK
            if self._left: #if moving left, ...
                for alien in self._aliens:
                    for pos in range(len(alien)):
                        alien[pos].x -= ALIEN_H_WALK

            rightalien = self.findright()
            leftalien = self.findleft()

            if rightalien.x > right:
                for pos in range(len(alien)):
                    for alien in self._aliens:
                        alien[pos].y -= ALIEN_V_WALK
                        self._right = False
                        self._left = True

            if leftalien.x < left:
                for pos in range(len(alien)):
                    for alien in self._aliens:
                        alien[pos].y -= ALIEN_V_WALK
                        self._right = True
                        self._left = False
        else:
            self._time += dt
            self._steps += dt

        # FOR CONTROLLING ALIEN BOLTS
        for row in self._aliens:
            accum = 0
            for alien in self._bolts:
                if alien.isAlienBolt():
                    accum += 1
            if accum == 0:
                alienshoot = self.findbottom(random.randint(0, len(row)-1))
                if alienshoot is not None:
                    if self._steps == self._abolt1:
                        self._abolt1 = random.randint(1, BOLT_RATE)
                        self._steps = 0
                        alienbolt = Bolt(alienshoot.x, alienshoot.y, velocity=-BOLT_SPEED)
                        self._bolts.append(alienbolt)
                        for abolt in self._bolts:
                            if abolt.y < GAME_HEIGHT:
                                self._bolts.remove(abolt)
                            else:
                                abolt.y -= abolt.getBoltSpeed
                        # else:
                        #     self._steps += dt

    def findright(self):
        """
        Returns rightmost alien object
        """
        xval = 0
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if xval == 0 or alien.x > xval.x:
                        xval = alien
        return xval

    def findleft(self):
        """
        Returns the leftmost alien objects
        """
        xval = 0
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if xval == 0 or alien.x < xval.x:
                        xval = alien
        return xval

    def findbottom(self, col):
        """
        Returns the alien in the bottom-most position of a certain column of the wave

        Parameter col: a valid column number in the 2D list
        Precondition: col is an int >= 0
        """
        for row in range(len(self._aliens)):
            if self._aliens[row][col] is not None:
                return self._aliens[row][col]



    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        for row in self._aliens:
            for alien in row:
                alien.draw(view)

        self._ship.draw(view)
        self._dline.draw(view)

        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
