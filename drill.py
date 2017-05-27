#!/usr/bin/env python
# coding: utf-8
import pygame, sys, random 
import datetime
from pygame.locals import *

BASICFONTSIZE = 70
TEXTCOLOR = (100, 0, 20)
SHADOWCOLOR = (90, 90, 99)


pygame.init()

DISPLAYSURF = pygame.display.set_mode((800, 700))
pygame.display.set_caption('calc practice')
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
JAPANESEFONT = pygame.font.Font('DroidSansJapanese.ttf', BASICFONTSIZE)

good = pygame.mixer.Sound("./media/beep1.ogg")
bad = pygame.mixer.Sound("./media/badswap.wav")

# making problems
range_a = (1, 20)
range_b = (1, 20)
high_scores = []
prev_score  = None
prev_miss = 0
prev_time = None
n_of_problems = 30
surface = pygame.Surface(DISPLAYSURF.get_size())
ans = 0

def drawText(text, x, y, c, font = BASICFONT): # {{{
    textSurf = font.render(text, True, c)
    textRect = textSurf.get_rect()
    textRect.left = x 
    textRect.top  = y
    surface.blit(textSurf, textRect)
# }}}

def shadowedText(s, x, y):# {{{
    drawText(s, x, y, SHADOWCOLOR)
    drawText(s, x-3, y-3, TEXTCOLOR)
# }}}

def eventLoop(draw, handler): # {{{
    cont = True
    while cont:
        draw()
        for event in pygame.event.get():
            if not handler(event):
                cont = False
        DISPLAYSURF.blit(surface, surface.get_rect())
        pygame.display.update()
# }}}

###############################################################################
def initialize_state():# {{{
    global probs, answers, tick_or_cross, inputs, current_prob, probs_str, start_time
    start_time = datetime.datetime.now()
    probs = [(random.randint(*range_a), random.randint(*range_b)) for _ in range(n_of_problems)]
    answers = [a+b for a,b in probs]
    tick_or_cross = [None] * n_of_problems
    inputs = [None] * n_of_problems
    current_prob = 0
    probs_str = ["%d + %d =" % (a, b) for a,b in probs]
# }}}


def drawTitleScreen(): # {{{
    surface.fill((10, 200, 20))
    drawText(u"計算どりーる", 150, 100, SHADOWCOLOR, JAPANESEFONT)
    drawText("HIT ANY KEY", 200, 300, SHADOWCOLOR)
    if prev_score:
        drawText(u"前のスコア：", 20, 450, (100, 230, 130), JAPANESEFONT)
        drawText("%d (miss %d)" % (prev_score, prev_miss), 400, 460, (100, 230, 130))
        drawText("[%4d.%2d]" % (prev_time.seconds, prev_time.microseconds/10000), 400, 550, (100, 230, 130))
# }}}

def drawScreen(): # {{{
    surface.fill((10, 200, 20));
    for (i, s) in enumerate(probs_str):
        prob_no = i - current_prob + 3
        if 0 <= prob_no <= 6:
            shadowedText(s, 100, prob_no*100)
            if inputs[i]:
                drawText(str(inputs[i]), BASICFONTSIZE/2*len(probs_str[i])+80,
                        100*prob_no, (10, 100, 20))
                if tick_or_cross[i] == True:
                    drawText("OK", BASICFONTSIZE/2*len(probs_str[i])+180, 100*prob_no, (100,255,100))
                elif tick_or_cross[i] == False:
                    drawText("NG", BASICFONTSIZE/2*len(probs_str[i])+180, 100*prob_no, (255,0,0))

    curtime = datetime.datetime.now() - start_time
    drawText("%4d.%02d"% (curtime.seconds, curtime.microseconds/10000),
           500, 0, (111, 111, 0))
#}}}

def mainGameHandler(event): # {{{
    global ans, current_prob, high_scores, prev_time, prev_score, prev_miss
    if event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
            ans /= 10
        if event.key >= K_0 and event.key <= K_9:
            ans = ans * 10 + (event.key - K_0)
        if event.key == K_RETURN:
            if ans == answers[current_prob]:
                tick_or_cross[current_prob] = True
                good.play()
            else:
                tick_or_cross[current_prob] = False
                bad.play()
            ans = 0
            current_prob += 1
            if current_prob >= n_of_problems:
                prev_score = sum([1 for i in tick_or_cross if i])
                prev_miss  = sum([1 for i in tick_or_cross if not i])
                high_scores.append(prev_score)
                high_scores.sort()
                high_scores = high_scores[:3]
                prev_time = datetime.datetime.now() - start_time
                return False
        inputs[current_prob] = ans

    if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
        return False

    return True
# }}}

def titleHandler(event): # {{{
    if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    if event.type == KEYDOWN:
        return False
    return True
# }}}


while True:
    initialize_state()
    eventLoop(
        drawTitleScreen, 
        titleHandler)
    eventLoop(
        drawScreen,
        mainGameHandler)

#  vi: foldmethod=marker
