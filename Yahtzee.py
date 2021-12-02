import pygame
from pygame.locals import *
import sys
import os
import time
import math
import random
import webbrowser
from itertools import chain
from itertools import groupby

### Get absolute path to resource, works for dev and for PyInstaller. For image of Yahtzee cup.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

yahtzee_cup_image = resource_path("YahtzeeCup.png")

###################################################

### Initialize Game
pygame.init()
pygame.key.set_repeat(500, 25)
clock = pygame.time.Clock() ; FPS = 60
dis = pygame.display.set_mode((1200,750))
pygame.display.set_caption('Yahtzee!')

###################################################

### Fonts
click_font_1 = pygame.font.SysFont("cambria", 18, bold = True)
click_font_2 = pygame.font.SysFont("cambria", 18, bold = True) ; click_font_2.underline = True
click_font_3 = pygame.font.SysFont("arialblack", 26, bold = True) ; click_font_3.underline = True
click_font_4 = pygame.font.SysFont("arialblack", 32, bold = True) ; click_font_4.underline = True
click_font_5 = pygame.font.SysFont("cambria", 23, bold = True)
click_font_6 = pygame.font.SysFont("cambria", 23, bold = True) ; click_font_6.underline = True
title_font = pygame.font.SysFont("ravie", 55)
another_font = pygame.font.SysFont("segoeuisymbol", 40)
another_font_2 = pygame.font.SysFont("segoeuisymbol", 24)
another_underline_font = pygame.font.SysFont("segoeuisymbol", 22) ; another_underline_font.underline = True
shake_font = pygame.font.SysFont("segoeuisymbol", 18, bold = True)
welcome_font_1 = pygame.font.SysFont("cambria", 28)
welcome_font_2 = pygame.font.SysFont("cambria", 24)
welcome_font_3 = pygame.font.SysFont("cambria", 24) ; welcome_font_3.underline = True
player_font = pygame.font.SysFont("cambria", 15)
player_font_2 = pygame.font.SysFont("cambria", 17)
player_font_3 = pygame.font.SysFont("cambria", 18)  ; player_font_3.underline = True 
credit_font = pygame.font.SysFont("tahoma", 10, italic = True)
rule_font_1 = pygame.font.SysFont("tahoma", 16, bold = True)
sc_font = pygame.font.SysFont("segoeuisymbol", 15)
sc_dice_font = pygame.font.SysFont("segoeuisymbol", 18)
sc_dice_font_2 = pygame.font.SysFont("segoeuisymbol", 18, bold = True)
sc_how_font = pygame.font.SysFont("segoeuisymbol", 12)
sc_name_font = pygame.font.SysFont("cambria", 14)
big_dice_font = pygame.font.SysFont("segoeuisymbol", 120)
small_dice_font = pygame.font.SysFont("segoeuisymbol", 80)

###################################################

### Colors
wh = (255, 255, 255) ; blk = (0, 0, 0); red = (255, 0, 0); gr = (70, 70, 70)
p1_color = (70, 150, 255) ; p2_color = (150, 255, 70) ; p3_color = (255, 70, 150) ; p4_color = (255, 150, 70)
p1_color_alt = (50, 110, 195) ; p2_color_alt = (110, 195, 50) ; p3_color_alt = (195, 50, 110) ; p4_color_alt = (195, 110, 50)
p_colors = [p1_color, p2_color, p3_color, p4_color]
p_colors_alt = [p1_color_alt, p2_color_alt, p3_color_alt, p4_color_alt]

###################################################

# Unending game loop (repeats after three games are played and players continue). Resets EVERYTHING.
while wh == (255,255,255):
    ### Player Banks
    p1_score = 0; p2_score = 0; p3_score = 0; p4_score = 0
    yb1 = 0 ; yb2 = 0 ; yb3 = 0; bb = 0

    ###################################################

    ### Dice Combos
    ACES = 0; TWOS = 0; THREES = 0; FOURS = 0; FIVES = 0; SIXES = 0
    KIND3 = 0; KIND4 = 0; FHOUSE = 0; SMALLS = 0; LARGES = 0; YAHTZ = 0; CHANCE = 0
    YAHTZ_B1 = 0; YAHTZ_B2 = 0; YAHTZ_B3 = 0;
    TITLES1 = ["Aces","Twos","Threes","Fours","Fives","Sixes","3 of a Kind","4 of a Kind","Full House","Sm. Straight","Lg. Straight","Chance","Yahtzee"]
    TITLES2 = ["ace","two","three","four","five","six","3k","4k","FH","SS","LS","chance","Y"]
    S_DICT = {} ; S_DICT_RECT = {}

    ###################################################

    ### Score Tracker by Player by Game
    MD1 = {} ; MD2 = {}; MD3 = {}; MD4 = {}
    MD1['p1_g1_ace'] = "" ; MD1['p1_g1_two'] = "" ; MD1['p1_g1_three'] = "" ; MD1['p1_g1_four'] = "" ; MD1['p1_g1_five'] = "" ; MD1['p1_g1_six'] = ""
    MD1['p1_g1_3k'] = "" ; MD1['p1_g1_4k'] = "" ; MD1['p1_g1_FH'] = "" ; MD1['p1_g1_SS'] = "" ; MD1['p1_g1_LS'] = ""; MD1['p1_g1_chance'] = ""
    MD1['p1_g1_Y'] = ""; MD1['p1_g1_YB1'] = ""; MD1['p1_g1_YB2'] = ""; MD1['p1_g1_YB3'] = ""
    MD1['p1_g1_TotalUpper1'] = ""; MD1['p1_g1_TotalUpper2'] = ""; MD1['p1_g1_Bonus'] = ""; MD1['p1_g1_TotalLower'] = ""; MD1['p1_g1_GRAND'] = 0
    MD1['p1_g2_ace'] = "" ; MD1['p1_g2_two'] = "" ; MD1['p1_g2_three'] = "" ; MD1['p1_g2_four'] = "" ; MD1['p1_g2_five'] = "" ; MD1['p1_g2_six'] = ""
    MD1['p1_g2_3k'] = "" ; MD1['p1_g2_4k'] = "" ; MD1['p1_g2_FH'] = "" ; MD1['p1_g2_SS'] = "" ; MD1['p1_g2_LS'] = ""; MD1['p1_g2_chance'] = ""
    MD1['p1_g2_Y'] = ""; MD1['p1_g2_YB1'] = ""; MD1['p1_g2_YB2'] = ""; MD1['p1_g2_YB3'] = ""
    MD1['p1_g2_TotalUpper1'] = ""; MD1['p1_g2_TotalUpper2'] = ""; MD1['p1_g2_Bonus'] = ""; MD1['p1_g2_TotalLower'] = ""; MD1['p1_g2_GRAND'] = 0
    MD1['p1_g3_ace'] = "" ; MD1['p1_g3_two'] = "" ; MD1['p1_g3_three'] = "" ; MD1['p1_g3_four'] = "" ; MD1['p1_g3_five'] = "" ; MD1['p1_g3_six'] = ""
    MD1['p1_g3_3k'] = "" ; MD1['p1_g3_4k'] = "" ; MD1['p1_g3_FH'] = "" ; MD1['p1_g3_SS'] = "" ; MD1['p1_g3_LS'] = ""; MD1['p1_g3_chance'] = ""
    MD1['p1_g3_Y'] = ""; MD1['p1_g3_YB1'] = ""; MD1['p1_g3_YB2'] = ""; MD1['p1_g3_YB3'] = ""
    MD1['p1_g3_TotalUpper1'] = ""; MD1['p1_g3_TotalUpper2'] = ""; MD1['p1_g3_Bonus'] = ""; MD1['p1_g3_TotalLower'] = ""; MD1['p1_g3_GRAND'] = 0
    MD2['p2_g1_ace'] = "" ; MD2['p2_g1_two'] = "" ; MD2['p2_g1_three'] = "" ; MD2['p2_g1_four'] = "" ; MD2['p2_g1_five'] = "" ; MD2['p2_g1_six'] = ""
    MD2['p2_g1_3k'] = "" ; MD2['p2_g1_4k'] = "" ; MD2['p2_g1_FH'] = "" ; MD2['p2_g1_SS'] = "" ; MD2['p2_g1_LS'] = ""; MD2['p2_g1_chance'] = ""
    MD2['p2_g1_Y'] = ""; MD2['p2_g1_YB1'] = ""; MD2['p2_g1_YB2'] = ""; MD2['p2_g1_YB3'] = ""
    MD2['p2_g1_TotalUpper1'] = ""; MD2['p2_g1_TotalUpper2'] = ""; MD2['p2_g1_Bonus'] = ""; MD2['p2_g1_TotalLower'] = ""; MD2['p2_g1_GRAND'] = 0
    MD2['p2_g2_ace'] = "" ; MD2['p2_g2_two'] = "" ; MD2['p2_g2_three'] = "" ; MD2['p2_g2_four'] = "" ; MD2['p2_g2_five'] = "" ; MD2['p2_g2_six'] = ""
    MD2['p2_g2_3k'] = "" ; MD2['p2_g2_4k'] = "" ; MD2['p2_g2_FH'] = "" ; MD2['p2_g2_SS'] = "" ; MD2['p2_g2_LS'] = ""; MD2['p2_g2_chance'] = ""
    MD2['p2_g2_Y'] = ""; MD2['p2_g2_YB1'] = ""; MD2['p2_g2_YB2'] = ""; MD2['p2_g2_YB3'] = ""
    MD2['p2_g2_TotalUpper1'] = ""; MD2['p2_g2_TotalUpper2'] = ""; MD2['p2_g2_Bonus'] = ""; MD2['p2_g2_TotalLower'] = ""; MD2['p2_g2_GRAND'] = 0
    MD2['p2_g3_ace'] = "" ; MD2['p2_g3_two'] = "" ; MD2['p2_g3_three'] = "" ; MD2['p2_g3_four'] = "" ; MD2['p2_g3_five'] = "" ; MD2['p2_g3_six'] = ""
    MD2['p2_g3_3k'] = "" ; MD2['p2_g3_4k'] = "" ; MD2['p2_g3_FH'] = "" ; MD2['p2_g3_SS'] = "" ; MD2['p2_g3_LS'] = ""; MD2['p2_g3_chance'] = ""
    MD2['p2_g3_Y'] = ""; MD2['p2_g3_YB1'] = ""; MD2['p2_g3_YB2'] = ""; MD2['p2_g3_YB3'] = ""
    MD2['p2_g3_TotalUpper1'] = ""; MD2['p2_g3_TotalUpper2'] = ""; MD2['p2_g3_Bonus'] = ""; MD2['p2_g3_TotalLower'] = ""; MD2['p2_g3_GRAND'] = 0
    MD3['p3_g1_ace'] = "" ; MD3['p3_g1_two'] = "" ; MD3['p3_g1_three'] = "" ; MD3['p3_g1_four'] = "" ; MD3['p3_g1_five'] = "" ; MD3['p3_g1_six'] = ""
    MD3['p3_g1_3k'] = "" ; MD3['p3_g1_4k'] = "" ; MD3['p3_g1_FH'] = "" ; MD3['p3_g1_SS'] = "" ; MD3['p3_g1_LS'] = ""; MD3['p3_g1_chance'] = ""
    MD3['p3_g1_Y'] = ""; MD3['p3_g1_YB1'] = ""; MD3['p3_g1_YB2'] = ""; MD3['p3_g1_YB3'] = ""
    MD3['p3_g1_TotalUpper1'] = ""; MD3['p3_g1_TotalUpper2'] = ""; MD3['p3_g1_Bonus'] = ""; MD3['p3_g1_TotalLower'] = ""; MD3['p3_g1_GRAND'] = 0
    MD3['p3_g2_ace'] = "" ; MD3['p3_g2_two'] = "" ; MD3['p3_g2_three'] = "" ; MD3['p3_g2_four'] = "" ; MD3['p3_g2_five'] = "" ; MD3['p3_g2_six'] = ""
    MD3['p3_g2_3k'] = "" ; MD3['p3_g2_4k'] = "" ; MD3['p3_g2_FH'] = "" ; MD3['p3_g2_SS'] = "" ; MD3['p3_g2_LS'] = ""; MD3['p3_g2_chance'] = ""
    MD3['p3_g2_Y'] = ""; MD3['p3_g2_YB1'] = ""; MD3['p3_g2_YB2'] = ""; MD3['p3_g2_YB3'] = ""
    MD3['p3_g2_TotalUpper1'] = ""; MD3['p3_g2_TotalUpper2'] = ""; MD3['p3_g2_Bonus'] = ""; MD3['p3_g2_TotalLower'] = ""; MD3['p3_g2_GRAND'] = 0
    MD3['p3_g3_ace'] = "" ; MD3['p3_g3_two'] = "" ; MD3['p3_g3_three'] = "" ; MD3['p3_g3_four'] = "" ; MD3['p3_g3_five'] = "" ; MD3['p3_g3_six'] = ""
    MD3['p3_g3_3k'] = "" ; MD3['p3_g3_4k'] = "" ; MD3['p3_g3_FH'] = "" ; MD3['p3_g3_SS'] = "" ; MD3['p3_g3_LS'] = ""; MD3['p3_g3_chance'] = ""
    MD3['p3_g3_Y'] = ""; MD3['p3_g3_YB1'] = ""; MD3['p3_g3_YB2'] = ""; MD3['p3_g3_YB3'] = ""
    MD3['p3_g3_TotalUpper1'] = ""; MD3['p3_g3_TotalUpper2'] = ""; MD3['p3_g3_Bonus'] = ""; MD3['p3_g3_TotalLower'] = ""; MD3['p3_g3_GRAND'] = 0
    MD4['p4_g1_ace'] = "" ; MD4['p4_g1_two'] = "" ; MD4['p4_g1_three'] = "" ; MD4['p4_g1_four'] = "" ; MD4['p4_g1_five'] = "" ; MD4['p4_g1_six'] = ""
    MD4['p4_g1_3k'] = "" ; MD4['p4_g1_4k'] = "" ; MD4['p4_g1_FH'] = "" ; MD4['p4_g1_SS'] = "" ; MD4['p4_g1_LS'] = ""; MD4['p4_g1_chance'] = ""
    MD4['p4_g1_Y'] = ""; MD4['p4_g1_YB1'] = ""; MD4['p4_g1_YB2'] = ""; MD4['p4_g1_YB3'] = ""
    MD4['p4_g1_TotalUpper1'] = ""; MD4['p4_g1_TotalUpper2'] = ""; MD4['p4_g1_Bonus'] = ""; MD4['p4_g1_TotalLower'] = ""; MD4['p4_g1_GRAND'] = 0
    MD4['p4_g2_ace'] = "" ; MD4['p4_g2_two'] = "" ; MD4['p4_g2_three'] = "" ; MD4['p4_g2_four'] = "" ; MD4['p4_g2_five'] = "" ; MD4['p4_g2_six'] = ""
    MD4['p4_g2_3k'] = "" ; MD4['p4_g2_4k'] = "" ; MD4['p4_g2_FH'] = "" ; MD4['p4_g2_SS'] = "" ; MD4['p4_g2_LS'] = ""; MD4['p4_g2_chance'] = ""
    MD4['p4_g2_Y'] = ""; MD4['p4_g2_YB1'] = ""; MD4['p4_g2_YB2'] = ""; MD4['p4_g2_YB3'] = ""
    MD4['p4_g2_TotalUpper1'] = ""; MD4['p4_g2_TotalUpper2'] = ""; MD4['p4_g2_Bonus'] = ""; MD4['p4_g2_TotalLower'] = ""; MD4['p4_g2_GRAND'] = 0
    MD4['p4_g3_ace'] = "" ; MD4['p4_g3_two'] = "" ; MD4['p4_g3_three'] = "" ; MD4['p4_g3_four'] = "" ; MD4['p4_g3_five'] = "" ; MD4['p4_g3_six'] = ""
    MD4['p4_g3_3k'] = "" ; MD4['p4_g3_4k'] = "" ; MD4['p4_g3_FH'] = "" ; MD4['p4_g3_SS'] = "" ; MD4['p4_g3_LS'] = ""; MD4['p4_g3_chance'] = ""
    MD4['p4_g3_Y'] = ""; MD4['p4_g3_YB1'] = ""; MD4['p4_g3_YB2'] = ""; MD4['p4_g3_YB3'] = ""
    MD4['p4_g3_TotalUpper1'] = ""; MD4['p4_g3_TotalUpper2'] = ""; MD4['p4_g3_Bonus'] = ""; MD4['p4_g3_TotalLower'] = ""; MD4['p4_g3_GRAND'] = 0

    # Rectangles to blot out all scores in the scorecard
    MD_FILLS = [(310,145,70,20),(310,170,70,20),(310,195,70,20),(310,220,70,20),(310,245,70,20),(310,270,70,20),(310,295,70,20),
                (310,320,70,20),(310,345,70,20),(310,420,70,20),(310,445,70,20),(310,470,70,20),(310,495,70,20),(310,520,70,20),
                (310,545,70,20),(310,570,70,20),(308,595,20,32),(333,595,23,32),(360,595,20,32),(310,635,70,20),(310,675,70,25),
                (402,145,70,20),(402,170,70,20),(402,195,70,20),(402,220,70,20),(402,245,70,20),(402,270,70,20),(402,295,70,20),
                (402,320,70,20),(402,345,70,20),(402,420,70,20),(402,445,70,20),(402,470,70,20),(402,495,70,20),(402,520,70,20),
                (402,545,70,20),(402,570,70,20),(400,595,20,32),(425,595,23,32),(452,595,20,32),(402,635,70,20),(402,675,70,25),
                (494,145,70,20),(494,170,70,20),(494,195,70,20),(494,220,70,20),(494,245,70,20),(494,270,70,20),(494,295,70,20),
                (494,320,70,20),(494,345,70,20),(494,420,70,20),(494,445,70,20),(494,470,70,20),(494,495,70,20),(494,520,70,20),
                (494,545,70,20),(494,570,70,20),(492,595,20,32),(517,595,23,32),(544,595,20,32),(494,635,70,20),(494,675,70,25)]

    # Coordinates to draw scores in the scorecard
    MD_WRITES = [(345,153),(345,179),(345,204),(345,229),(345,254),(345,278),(345,429),(345,454),(345,479),(345,504),(345,529),
                 (345,579),(345,554),(318,610),(344,610),(371,610),(345,303),(345,354),(345,328),(345,643),(345,687),
                 (437,153),(437,179),(437,204),(437,229),(437,254),(437,278),(437,429),(437,454),(437,479),(437,504),(437,529),
                 (437,579),(437,554),(410,610),(436,610),(463,610),(437,303),(437,354),(437,328),(437,643),(437,687),
                 (529,153),(529,179),(529,204),(529,229),(529,254),(529,278),(529,429),(529,454),(529,479),(529,504),(529,529),
                 (529,579),(529,554),(502,610),(528,610),(555,610),(529,303),(529,354),(529,328),(529,643),(529,687)]

    ###################################################

    ### Titles & Names & Credits
    dis.blit(pygame.font.SysFont("ravie", 13).render("Great Shakes, it's...", True, wh), [19, 8])
    dis.blit(title_font.render("Yahtzee!", True, wh), [18, 30])
    dis.blit(sc_name_font.render("Name ___________________________________", True, wh), [370, 64])
    dis.blit(credit_font.render("Completed by Eric Anderson on 12/02/2021 using Pygame, a Python library.", True, wh), [10, 724])
    num_players = 0 ; num_cpu = 0
    player_names = [] ; PLAYER_ORDER = {}
    player1 = "" ; player2 = "" ; player3 = "" ; player4 = ""

    ###################################################

    ### Score Card (first drawing)
    # Asterisks and bars (neatlines)
    for s in range(1,42):
        value = sc_font.render(" ||", True, wh)
        if s < 20 or s > 21:
            if s < 41:
                dis.blit(value, [15, 82.5 + s*15]) ; dis.blit(value, [162.5, 82.5 + s*15])
                dis.blit(value, [292.5, 82.5 + s*15]) ; dis.blit(value, [384, 82.5 + s*15])
                dis.blit(value, [475.5, 82.5 + s*15]) ; dis.blit(value, [567, 82.5 + s*15])
        value = sc_font.render("*", True, wh)
        dis.blit(value, [10, 77.5 + s*15]) ; dis.blit(value, [10, 85 + s*15])
        dis.blit(value, [582, 77.5 + s*15]) ; dis.blit(value, [582, 85 + s*15])
        if s == 34 or s == 35:
            value = sc_font.render("|", True, wh)
            dis.blit(value, [329, 82.5 + s*15]) ; dis.blit(value, [356, 82.5 + s*15])
            dis.blit(value, [421, 82.5 + s*15]) ; dis.blit(value, [448, 82.5 + s*15])
            dis.blit(value, [513, 82.5 + s*15]) ;dis.blit(value, [540, 82.5 + s*15])
            
    # 'How to Play'
    dice = ["\u2680 = 1", "\u2681 = 2", "\u2682 = 3", "\u2683 = 4", "\u2684 = 5", "\u2685 = 6"]
    dice2 = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]
    how_to_1 = ["Add Only Aces", "Add Only Twos", "Add Only Threes", "Add Only Fours", "Add Only Fives", "Add Only Sixes", " ", "Total Score \u2265 63"]
    how_to_2 = ["Add Dice Total", "Add Dice Total", "2 + 3 of a kind", "Sequence of 4", "Sequence of 5", "5 of a kind", "Add Dice Total"]
    dis.blit(sc_how_font.render("\u2713 FOR EACH BONUS", True, wh), [180, 604])
    for d in range (0, 6):
        dis.blit(sc_dice_font.render(dice[d], True, wh), [104, 142 + d*25])
    for h in range (0, 8):
        dis.blit(sc_how_font.render(how_to_1[h], True, wh), [194, 147.5 + h*25])
    for h in range (0, 7):
        dis.blit(sc_how_font.render(how_to_2[h], True, wh), [196, 422.5 + h*25])

    scorecard = "************************************************************************************************"
    dis.blit(sc_font.render(scorecard, True, wh), [11, 84])
    scorecard = "    _____________________      __________________     ____________     ____________     ____________"
    dis.blit(sc_font.render(scorecard, True, wh), [15, 85]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 90])
    scorecard = "       UPPER SECTION          HOW TO PLAY       GAME #1:       GAME #2:       GAME #3:"
    dis.blit(sc_font.render(scorecard, True, wh), [15, 112.5])
    scorecard = "    ----------------------    -------------------    ------------     ------------     ------------"
    dis.blit(sc_font.render(scorecard, True, wh), [15, 125]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 130])
    dis.blit(sc_font.render("      Aces", True, wh), [15, 144])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 155])
    dis.blit(sc_font.render("      Twos", True, wh), [15, 169])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 180])
    dis.blit(sc_font.render("      Threes", True, wh), [15, 194])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 205])
    dis.blit(sc_font.render("      Fours", True, wh), [15, 219])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 230])
    dis.blit(sc_font.render("      Fives", True, wh), [15, 244])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 255])
    dis.blit(sc_font.render("      Sixes", True, wh), [15, 269])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 280])
    dis.blit(sc_font.render("        TOTAL SCORE:                 \u279c \u279c \u279c", True, wh), [15, 294.5])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 305])
    dis.blit(sc_font.render("             BONUS:", True, wh), [15, 319.5])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 330])
    dis.blit(sc_font.render("              TOTAL:                       \u279c \u279c \u279c", True, wh), [15, 344.5])
    scorecard = "    _____________________      __________________     ____________     ____________     ____________"
    dis.blit(sc_font.render(scorecard, True, wh), [15, 350]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 355])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 360]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 365])
    dis.blit(sc_font.render("      LOWER SECTION", True, wh), [15, 387.5])
    scorecard = "    ----------------------    -------------------    ------------     ------------     ------------"
    dis.blit(sc_font.render(scorecard, True, wh), [15, 400]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 405])
    dis.blit(sc_font.render("      3 of a kind", True, wh), [15, 419])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 430])
    dis.blit(sc_font.render("      4 of a kind", True, wh), [15, 444])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 455])
    dis.blit(sc_font.render("      Full House", True, wh), [15, 469])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 480])
    dis.blit(sc_font.render("      Small Straight", True, wh), [15, 494])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 505])
    dis.blit(sc_font.render("      Large Straight", True, wh), [15, 519])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 530])
    dis.blit(sc_font.render("      YAHTZEE", True, wh), [15, 544])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 555])
    dis.blit(sc_font.render("      Chance", True, wh), [15, 569])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 580])
    dis.blit(sc_font.render("             YAHTZEE", True, wh), [13, 594])
    dis.blit(sc_font.render("               BONUS", True, wh), [11, 608])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 619])
    dis.blit(sc_font.render("         TOTAL SCORE:                \u279c \u279c \u279c", True, wh), [14, 633])
    scorecard = "    _____________________      __________________     ____________     ____________     ____________"
    dis.blit(sc_font.render(scorecard, True, wh), [15, 639.5]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 644.5])
    dis.blit(sc_font.render(scorecard, True, wh), [15, 649.5]) ; dis.blit(sc_font.render(scorecard, True, wh), [15, 654.5])
    dis.blit(sc_font.render("         GRAND TOTAL:               \u279c \u279c \u279c", True, wh), [11, 679])
    scorecard = " ********************************************************************************************** "
    dis.blit(sc_font.render(scorecard, True, wh), [13, 700])

    ###################################################

    ### Welcome Screen initiation
    dis.blit(welcome_font_1.render("Welcome! How many players?", True, wh), [690, 500])
    one_p_u = click_font_1.render("One Player", True, wh)
    two_p_u = click_font_1.render("Two Players", True, wh)
    three_p_u = click_font_1.render("Three Players", True, wh)
    four_p_u = click_font_1.render("Four Players", True, wh)
    cpu_zero_u = welcome_font_2.render(" 0 ", True, wh)
    cpu_one_u = welcome_font_2.render(" 1 ", True, wh)
    cpu_two_u = welcome_font_2.render(" 2 ", True, wh)
    cpu_three_u = welcome_font_2.render(" 3 ", True, wh)

    # Get all collision rectangles
    one_p = one_p_u.get_rect() ; two_p = two_p_u.get_rect() ; three_p = three_p_u.get_rect() ; four_p = four_p_u.get_rect()
    cpu_zero = cpu_zero_u.get_rect() ; cpu_one = cpu_one_u.get_rect() ; cpu_two = cpu_two_u.get_rect() ; cpu_three = cpu_three_u.get_rect()
    one_p.x, one_p.y = 625,575
    two_p.x, two_p.y = 750,575
    three_p.x, three_p.y = 890,575
    four_p.x, four_p.y = 1050,575
    cpu_zero.x, cpu_zero.y = 875,630
    cpu_one.x, cpu_one.y = 950,630
    cpu_two.x, cpu_two.y = 1025,630
    cpu_three.x, cpu_three.y = 1100,630
    dis.blit(one_p_u, [625, 575]) ; dis.blit(two_p_u, [750, 575]) ; dis.blit(three_p_u, [890, 575]) ; dis.blit(four_p_u, [1050, 575])

    # Selecting number of players and CPUs
    games_list = ['g1', 'g2', 'g3']
    game = 1
    loop = True ; active = False; clicked = 5
    input_text = ""
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False ; pygame.quit() ; sys.exit()
                
            if one_p.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                clicked = 1
                dis.fill(blk, rect=(592, 625, 1000, 1000))
                dis.blit(click_font_1.render("How many CPU players?", True, wh), [625, 635])
                dis.blit(cpu_zero_u, [875, 630]) ; dis.blit(cpu_one_u, [950, 630]) ; dis.blit(cpu_two_u, [1025, 630]) ; dis.blit(cpu_three_u, [1100, 630])
            elif two_p.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                clicked = 2
                dis.fill(blk, rect=(592, 625, 1000, 1000))
                dis.blit(click_font_1.render("How many CPU players?", True, wh), [625, 635])
                dis.blit(cpu_zero_u, [875, 630]) ; dis.blit(cpu_one_u, [950, 630]) ; dis.blit(cpu_two_u, [1025, 630])
            elif three_p.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                clicked = 3
                dis.fill(blk, rect=(592, 625, 1000, 1000))
                dis.blit(click_font_1.render("How many CPU players?", True, wh), [625, 635])
                dis.blit(cpu_zero_u, [875, 630]) ; dis.blit(cpu_one_u, [950, 630])

            if cpu_zero.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                if clicked == 1:
                    num_players = 1 ; num_cpu = 0 ; player_outofturns = [False]
                    player_scores = [0]
                elif clicked == 2:
                    num_players = 2 ; num_cpu = 0 ; player_outofturns = [False, False]
                    player_scores = [0, 0]
                elif clicked == 3:
                    num_players = 3 ; num_cpu = 0 ; player_outofturns = [False, False, False]
                    player_scores = [0, 0, 0]
            elif cpu_one.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                if clicked == 1:
                    num_players = 2 ; num_cpu = 1 ; player_outofturns = [False, False]
                    player_scores = [0, 0]
                elif clicked == 2:
                    num_players = 3 ; num_cpu = 1 ; player_outofturns = [False, False, False]
                    player_scores = [0, 0, 0]
                elif clicked == 3:
                    num_players = 4 ; num_cpu = 1 ; player_outofturns = [False, False, False, False]
                    player_scores = [0, 0, 0, 0]
            elif cpu_two.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                if clicked == 1:
                    num_players = 3 ; num_cpu = 2 ; player_outofturns = [False, False, False]
                    player_scores = [0, 0, 0]
                elif clicked == 2:
                    num_players = 4 ; num_cpu = 2 ; player_outofturns = [False, False, False, False]
                    player_scores = [0, 0, 0, 0]
            elif cpu_three.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
                if clicked == 1:
                    num_players = 4 ; num_cpu = 3 ; player_outofturns = [False, False, False, False]
                    player_scores = [0, 0, 0, 0]
                    
            # Typing names of non-CPU players
            if (four_p.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP) or num_players != 0:
                clicked = 4
                if num_players == 0:
                    num_players = 4 ; num_cpu = 0  ; player_outofturns = [False, False, False, False]
                    player_scores = [0, 0, 0, 0]
                dis.fill(blk, rect=(592, 40, 1000, 1000))
                name_rect = pygame.draw.rect(dis, (70, 70, 70), pygame.Rect(780, 550, 205, 35))
                dis.blit(sc_font.render("Type name here...", True, wh), [790, 555])
                i = 0
                while num_players - num_cpu > i:
                    dis.blit(welcome_font_1.render("Name of  Player " + str(i+1) + "?", True, wh), [765, 500])
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit() ; sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            active = True if name_rect.collidepoint(event.pos) else False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                input_text = input_text[:-1]
                            elif (event.key not in [pygame.K_RETURN, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_LEFTPAREN, pygame.K_RIGHTPAREN, pygame.K_TAB,
                                                   pygame.K_PERIOD, pygame.K_ASTERISK, pygame.K_BACKQUOTE, pygame.K_SLASH, pygame.K_BACKSLASH, pygame.K_KP_DIVIDE,
                                                   pygame.K_KP_MULTIPLY, pygame.K_KP_PERIOD, pygame.K_CARET,
                                                   pygame.K_COMMA, pygame.K_QUOTE, pygame.K_QUOTEDBL]) and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                                if len(input_text) < 13:
                                    input_text += event.unicode
                            if event.key == pygame.K_RETURN and len(input_text) > 0:
                                if i == 0:
                                    player1 = input_text
                                    center_text = player_font.render("Player 1: " + str(player1), True, p1_color)
                                    dis.blit(center_text,center_text.get_rect(center=(500, 12)))
                                    player_names = [player1]
                                elif i == 1:
                                    player2 = input_text
                                    if player2 == player1:
                                        player2 = str(input_text) + " 2"
                                    center_text = player_font.render("Player 2: " + str(player2), True, p2_color)
                                    dis.blit(center_text,center_text.get_rect(center=(700, 12)))
                                    player_names = [player1, player2]
                                elif i == 2:
                                    player3 = input_text
                                    if player3 == player2 or player3 == player1:
                                        player3 = str(input_text) + " 3"
                                    center_text = player_font.render("Player 3: " + str(player3), True, p3_color)
                                    dis.blit(center_text,center_text.get_rect(center=(900, 12)))
                                    player_names = [player1, player2, player3]
                                elif i == 3:
                                    player4 = input_text
                                    if player4 == player3 or player4 == player2 or player4 == player1:
                                        player4 = str(input_text) + " 4"
                                    center_text = player_font.render("Player 4: " + str(player4), True, p4_color)
                                    dis.blit(center_text,center_text.get_rect(center=(1100, 12)))
                                    player_names = [player1, player2, player3, player4]
                                i += 1
                                dis.fill(blk, rect=(740, 500, 300, 35))
                                input_text = ""
                                dis.blit(sc_font.render(input_text, True, wh), [790, 555])
                                    
                        if not active:
                            input_text = ""
                            if name_rect.collidepoint(pygame.mouse.get_pos()):
                                pygame.draw.rect(dis, (140, 140, 140), name_rect, 3)
                            else:
                                pygame.draw.rect(dis, (70, 70, 70), name_rect)
                            dis.blit(sc_font.render("Type name here...", True, wh), [790, 555])
                        else:
                            pygame.draw.rect(dis, (105, 105, 115), name_rect)
                            pygame.draw.rect(dis, (140, 140, 140), name_rect, 3)
                            dis.blit(sc_font.render(input_text, True, wh), [790, 555]) if len(input_text) > 0 else None
                        pygame.display.flip()
                        
                # Creating CPUs
                if num_cpu == 1:
                    if num_players == 2:
                        player2 = "COMPUTER #1"
                        center_text = player_font.render("Player 2: " + str(player2), True, p2_color)
                        dis.blit(center_text,center_text.get_rect(center=(700, 12)))
                    elif num_players == 3:
                        player3 = "COMPUTER #1"
                        center_text = player_font.render("Player 3: " + str(player3), True, p3_color)
                        dis.blit(center_text,center_text.get_rect(center=(900, 12)))
                    elif num_players == 4:
                        player4 = "COMPUTER #1"
                        center_text = player_font.render("Player 4: " + str(player4), True, p4_color)
                        dis.blit(center_text,center_text.get_rect(center=(1100, 12)))
                elif num_cpu == 2:
                    if num_players == 3:
                        player2 = "COMPUTER #1" ; player3 = "COMPUTER #2"
                        center_text = player_font.render("Player 2: " + str(player2), True, p2_color)
                        dis.blit(center_text,center_text.get_rect(center=(700, 12)))
                        center_text = player_font.render("Player 3: " + str(player3), True, p3_color)
                        dis.blit(center_text,center_text.get_rect(center=(900, 12)))
                    elif num_players == 4:
                        player3 = "COMPUTER #1" ; player4 = "COMPUTER #2"
                        center_text = player_font.render("Player 2: " + str(player3), True, p3_color)
                        dis.blit(center_text,center_text.get_rect(center=(900, 12)))
                        center_text = player_font.render("Player 3: " + str(player4), True, p4_color)
                        dis.blit(center_text,center_text.get_rect(center=(1100, 12)))
                elif num_cpu == 3:
                    player2 = "COMPUTER #1" ; player3 = "COMPUTER #2" ; player4 = "COMPUTER #3"
                    center_text = player_font.render("Player 2: " + str(player2), True, p2_color)
                    dis.blit(center_text,center_text.get_rect(center=(700, 12)))
                    center_text = player_font.render("Player 3: " + str(player3), True, p3_color)
                    dis.blit(center_text,center_text.get_rect(center=(900, 12)))
                    center_text = player_font.render("Player 4: " + str(player4), True, p4_color)
                    dis.blit(center_text,center_text.get_rect(center=(1100, 12)))
                
                loop = False
                dis.fill(blk, rect=(592, 40, 1000, 1000))
                player_names = [player1, player2, player3, player4]
                pygame.display.update()
                                
        # Selecting number of players and CPUs (collision logic)
        if one_p.collidepoint(pygame.mouse.get_pos()) and loop:
            one_p_u = click_font_1.render("One Player", True, blk) ; one_p_c = click_font_2.render("One Player", True, red)
            dis.blit(one_p_u, [625, 575]) ; dis.blit(one_p_c, [625, 575])
        elif two_p.collidepoint(pygame.mouse.get_pos()) and loop:
            two_p_u = click_font_1.render("Two Players", True, blk) ; two_p_c = click_font_2.render("Two Players", True, red)
            dis.blit(two_p_u, [750, 575]) ; dis.blit(two_p_c, [750, 575])
        elif three_p.collidepoint(pygame.mouse.get_pos()) and loop:
            three_p_u = click_font_1.render("Three Players", True, blk) ; three_p_c = click_font_2.render("Three Players", True, red)
            dis.blit(three_p_u, [890, 575]) ; dis.blit(three_p_c, [890, 575])
        elif four_p.collidepoint(pygame.mouse.get_pos()) and loop:
            four_p_u = click_font_1.render("Four Players", True, blk) ; four_p_c = click_font_2.render("Four Players", True, red)
            dis.blit(four_p_u, [1050, 575]) ; dis.blit(four_p_c, [1050, 575])
        elif loop:
            if clicked != 1:
                one_p_c = click_font_2.render("One Player", True, blk) ; one_p_u = click_font_1.render("One Player", True, wh)
                dis.blit(one_p_c, [625, 575]) ; dis.blit(one_p_u, [625, 575])
            if clicked != 2:
                two_p_c = click_font_2.render("Two Players", True, blk) ; two_p_u = click_font_1.render("Two Players", True, wh)
                dis.blit(two_p_c, [750, 575]) ; dis.blit(two_p_u, [750, 575])
            if clicked != 3:
                three_p_c = click_font_2.render("Three Players", True, blk) ; three_p_u = click_font_1.render("Three Players", True, wh)
                dis.blit(three_p_c, [890, 575]) ; dis.blit(three_p_u, [890, 575])
            four_p_c = click_font_2.render("Four Players", True, blk) ; four_p_u = click_font_1.render("Four Players", True, wh)
            dis.blit(four_p_c, [1050, 575]) ; dis.blit(four_p_u, [1050, 575])

        if cpu_zero.collidepoint(pygame.mouse.get_pos()) and clicked < 4:
            cpu_zero_u = welcome_font_2.render(" 0 ", True, blk) ; cpu_zero_c = welcome_font_3.render(" 0 ", True, red)
            dis.blit(cpu_zero_u, [875, 630]) ; dis.blit(cpu_zero_c, [875, 630])
        elif cpu_one.collidepoint(pygame.mouse.get_pos()) and clicked < 4:
            cpu_one_u = welcome_font_2.render(" 1 ", True, blk) ; cpu_one_c = welcome_font_3.render(" 1 ", True, red)
            dis.blit(cpu_one_u, [950, 630]) ; dis.blit(cpu_one_c, [950, 630])
        elif cpu_two.collidepoint(pygame.mouse.get_pos()) and clicked < 3:
            cpu_two_u = welcome_font_2.render(" 2 ", True, blk) ; cpu_two_c = welcome_font_3.render(" 2 ", True, red)
            dis.blit(cpu_two_u, [1025, 630]) ; dis.blit(cpu_two_c, [1025, 630])
        elif cpu_three.collidepoint(pygame.mouse.get_pos()) and clicked < 2:
            cpu_three_u = welcome_font_2.render(" 3 ", True, blk) ; cpu_three_c = welcome_font_3.render(" 3 ", True, red)
            dis.blit(cpu_three_u, [1100, 630]) ; dis.blit(cpu_three_c, [1100, 630])
        elif clicked < 4:
            cpu_zero_c = welcome_font_3.render(" 0 ", True, blk) ; cpu_zero_u = welcome_font_2.render(" 0 ", True, wh)
            cpu_one_c = welcome_font_3.render(" 1 ", True, blk) ; cpu_one_u = welcome_font_2.render(" 1 ", True, wh)
            dis.blit(cpu_one_c, [950, 630]) ; dis.blit(cpu_one_u, [950, 630])
            dis.blit(cpu_zero_c, [875, 630]) ; dis.blit(cpu_zero_u, [875, 630])
            if clicked < 3:
                cpu_two_c = welcome_font_3.render(" 2 ", True, blk) ; cpu_two_u = welcome_font_2.render(" 2 ", True, wh)
                dis.blit(cpu_two_c, [1025, 630]) ; dis.blit(cpu_two_u, [1025, 630])
            if clicked < 2:
                cpu_three_c = welcome_font_3.render(" 3 ", True, blk) ; cpu_three_u = welcome_font_2.render(" 3 ", True, wh)
                dis.blit(cpu_three_c, [1100, 630]) ; dis.blit(cpu_three_u, [1100, 630])

        if clicked == 1:
            dis.fill(blk, rect=(600, 570, 600, 8)) ; dis.fill(blk, rect=(600, 598, 600, 8))
            dis.fill(blk, rect=(737, 570, 8, 30)) ; dis.fill(blk, rect=(858, 570, 8, 30))
            dis.fill(blk, rect=(877, 570, 8, 30)) ; dis.fill(blk, rect=(1012, 570, 8, 30))
            pygame.draw.rect(dis, red, (618, 573, 110, 30), 3)
        elif clicked == 2:
            dis.fill(blk, rect=(600, 570, 600, 8)) ; dis.fill(blk, rect=(600, 598, 600, 8))
            dis.fill(blk, rect=(613, 570, 8, 30)) ; dis.fill(blk, rect=(725, 570, 8, 30))
            dis.fill(blk, rect=(877, 570, 8, 30)) ; dis.fill(blk, rect=(1012, 570, 8, 30))
            pygame.draw.rect(dis, red, (742, 573, 120, 30), 3)
        elif clicked == 3:
            dis.fill(blk, rect=(600, 570, 600, 8)) ; dis.fill(blk, rect=(600, 598, 600, 8))
            dis.fill(blk, rect=(613, 570, 8, 30)) ; dis.fill(blk, rect=(725, 570, 8, 30))
            dis.fill(blk, rect=(737, 570, 8, 30)) ; dis.fill(blk, rect=(858, 570, 8, 30))
            pygame.draw.rect(dis, red, (882, 573, 134, 30), 3)

        pygame.display.flip()

    ###################################################
    COMPCLICK = USEREVENT+1 # Computers don't wait for user input
    SHAKECLICK = USEREVENT+2 # Shake #2 and #3 don't wait for user input
    SCREENCLICK = USEREVENT+3 # Wake up the screen
    
    ### Deciding turn order by dice roll
    loop_3game = True ; pass3 = False
    while loop_3game:
        loop = True ; apass = True; cq = True
        i = 0 ; first = 1; last = 1
        repeats = [] ; repeats_temp = [] ; f = {}
        count = ""
        if num_players > 1:
            while loop:
                if i < 4:
                    pygame.event.post(pygame.event.Event(COMPCLICK)) if "COMPUTER #" in player_names[i] else None      
                if pass3 == True:
                    pygame.event.post(pygame.event.Event(SCREENCLICK))
                    pass3 = False
                        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False ; pygame.quit() ; sys.exit()
 
                    # ROLL button
                    if num_players > i and num_players != 1:
                        if apass:
                            center_text = welcome_font_1.render(str(player_names[i]) + ":", True, p_colors[i])
                            dis.blit(center_text,center_text.get_rect(center=(892, 475)))
                            dis.blit(welcome_font_1.render("Roll the dice to determine turn order!", True, wh), [650, 500])
                            t_roll_u = click_font_3.render("ROLL", True, wh)
                            t_roll = t_roll_u.get_rect()
                            t_roll.x, t_roll.y = 850,590
                            dis.blit(t_roll_u, [850, 590])
                            dis.blit(big_dice_font.render(dice2[first], True, wh), [728, 255])
                            dis.blit(big_dice_font.render(dice2[last], True, wh), [952, 255])
                            apass = False
                            
                        if t_roll.collidepoint(pygame.mouse.get_pos()):
                            dis.fill(blk, rect=(793, 590, 600, 45))
                            t_roll_c = click_font_4.render("ROLL" + str(count), True, red)
                            dis.blit(t_roll_c, [835 - len(count)*6.5, 587.5])
                            if cq:
                                if len(count) < 6:
                                    count = str(count) + "!"
                                else:
                                    dis.blit(sc_name_font.render("Seriously? Just click it.", True, wh), [828, 641])  
                            cq = False
                        else:
                            dis.fill(blk, rect=(793, 590, 600, 45))
                            t_roll_u = click_font_3.render("ROLL", True, wh)
                            dis.blit(t_roll_u, [850, 590])
                            cq = True
                            
                        # Dice rolling animation
                        if event.type == pygame.MOUSEBUTTONUP and t_roll.collidepoint(pygame.mouse.get_pos()) or event.type == COMPCLICK:
                            count = ""
                            anim_count = random.randint(16,25)
                            dis.fill(blk, rect=(592, 40, 580, 370)) ; dis.fill(blk, rect=(630, 600, 580, 35)) ; dis.fill(blk, rect=(800, 630, 580, 35))
                            while anim_count > 0:
                                dis.fill(blk, rect=(592, 40, 580, 370))
                                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(75,135)).render(dice2[random.randint(0,5)], True, wh),
                                         [random.randint(640,830), random.randint(190,270)])
                                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(75,135)).render(dice2[random.randint(0,5)], True, wh),
                                         [random.randint(850,1050), random.randint(190,270)])
                                pygame.display.flip()
                                anim_count -= 1
                                time.sleep(.055)
                            if anim_count == 0:
                                first = random.randint(0,5) ; last = random.randint(0,5)
                                dis.fill(blk, rect=(592, 40, 580, 370)) ; dis.fill(blk, rect=(630, 400, 580, 235))
                                dis.blit(big_dice_font.render(dice2[first], True, wh), [728, 255])
                                dis.blit(big_dice_font.render(dice2[last], True, wh), [952, 255])
                                center_text = welcome_font_1.render(str(player_names[i]) + ":", True, p_colors[i])
                                dis.blit(center_text,center_text.get_rect(center=(892, 450)))
                                dis.blit(welcome_font_1.render("You rolled " + str(first+last+2) + ".", True, wh), [810, 475])
                                pygame.display.flip()
                                time.sleep(2.25)
                                dis.fill(blk, rect=(630, 400, 680, 235))
                                if num_players > i+1 and len(f) == 0:
                                    dis.blit(welcome_font_1.render(str(player_names[i+1]) + ":", True, p_colors[i+1]),
                                             [886 - (len(player_names[i+1]))*6.75, 465])
                                    dis.blit(welcome_font_1.render("Roll the dice to determine turn order!", True, wh), [650, 500])
                                    dis.blit(t_roll_u, [850, 590])
                                if i == 0:
                                    dis.fill(blk, rect=(600, 650, 210, 20))
                                    dis.blit(player_font_2.render("P1: " + str(player_names[i] + ": " + str(first+last+2)), True, p1_color), [600, 650])
                                elif i == 1:
                                    dis.fill(blk, rect=(600, 672, 210, 20))
                                    dis.blit(player_font_2.render("P2: " + str(player_names[i] + ": " + str(first+last+2)), True, p2_color), [600, 672])
                                elif i == 2:
                                    dis.fill(blk, rect=(600, 694, 210, 20))
                                    dis.blit(player_font_2.render("P3: " + str(player_names[i] + ": " + str(first+last+2)), True, p3_color), [600, 694])
                                elif i == 3:
                                    dis.fill(blk, rect=(600, 716, 210, 20))
                                    dis.blit(player_font_2.render("P4: " + str(player_names[i] + ": " + str(first+last+2)), True, p4_color), [600, 716])
                                PLAYER_ORDER[player_names[i]]= first+last+2

                            # Determining ties based on roll results
                            if len(repeats) == 0 and len(f) != 0:
                                i = num_players
                            elif len(f) != 0:
                                repeats.pop(0)
                                i = num_players if len(repeats) == 0 else repeats[0] - 1
                            else:
                                i += 1
                                    
                            if num_players == i:
                                f = {}
                                repeats = []
                                it = list(set(PLAYER_ORDER.values()))
                                for k, v in PLAYER_ORDER.items():
                                    if v not in f:
                                        f[v] = [k]
                                    else:
                                        f[v].append(k)
                                for j in range(0,len(it)):
                                    if len(f[it[j]]) > 1:
                                        for k in range(0,len(f[it[j]])):
                                           repeats.append(1+player_names.index(f[it[j]][k]))
                                        i = repeats[0] - 1
                                        repeats_temp = repeats.copy()

                            # Tie or no tie? Display
                            if len(f) != 0 and len(repeats) > 0:
                                center_text = welcome_font_1.render(str(player_names[repeats[0]-1]) + ":", True, p_colors[repeats[0]-1])
                                dis.blit(center_text,center_text.get_rect(center=(892, 475)))
                                tie_text = pygame.font.SysFont("cambria", 21).render("Tiebreaker! (Players " + str(str(repeats_temp).replace("[","").replace("]","")) + ")", True, wh)
                                dis.blit(tie_text,tie_text.get_rect(center=(892, 430)))
                                dis.blit(welcome_font_1.render("Roll the dice to break the tie!", True, wh), [705, 500])
                                dis.blit(t_roll_u, [850, 590])
                            elif len(f) != 0 and len(repeats) == 0:
                                dis.fill(blk, rect=(600, 650, 300, 200))
                                dis.fill(blk, rect=(400, 1, 800, 40))
                                dis.blit(welcome_font_1.render("Done! Here is the playing order:", True, wh), [695, 455])
                                v_align = 1
                                while len(f) > 0:
                                    popped = str(f.pop(max(f))).replace("[","").replace("]","").replace("'","")
                                    center_text = welcome_font_1.render(str(v_align) + ".) " + popped, True, p_colors[player_names.index(popped)])
                                    dis.blit(center_text,center_text.get_rect(center=(900, 475 + (v_align*45))))
                                    center_text = player_font.render("Player " + str(player_names.index(popped) + 1) + ": " + str(popped), True, p_colors[player_names.index(popped)])
                                    dis.blit(center_text,center_text.get_rect(center=(300 + 200*v_align, 12)))
                                    center_text = player_font.render(str(player_scores[player_names.index(popped)]) + " Points", True, p_colors_alt[player_names.index(popped)])
                                    dis.blit(center_text,center_text.get_rect(center=(300 + 200*v_align, 30)))
                                    v_align += 1
                                contin_u = click_font_1.render("Continue ->", True, wh)
                                contin = contin_u.get_rect()
                                contin.x, contin.y = 1050,695
                                dis.blit(contin_u, [1050, 695])
                    # Wait for user to view and move on from turn order results
                    else:
                        contin_u = click_font_1.render("Continue ->", True, wh)
                        contin = contin_u.get_rect()
                        contin.x, contin.y = 1050,695
                        dis.blit(contin_u, [1050, 695])
                        if contin.collidepoint(pygame.mouse.get_pos()):
                            dis.fill(blk, rect=(1050, 695, 200, 200))
                            contin_c = click_font_2.render("Continue ->", True, red)
                            dis.blit(contin_c, [1050, 695])
                        else:
                            dis.fill(blk, rect=(1050, 695, 200, 200))
                            contin_u = click_font_1.render("Continue ->", True, wh)
                            dis.blit(contin_u, [1050, 695]) 
                        if event.type == pygame.MOUSEBUTTONUP and contin.collidepoint(pygame.mouse.get_pos()):
                            dis.fill(blk, rect=(595, 40, 1000, 1000))
                            loop = False

                pygame.display.update()
            pygame.display.flip()

    ###################################################
        ### 5-second Loading Screen
        dis.blit(title_font.render("Yahtzee!", True, wh), [730, 100])
        dis.blit(welcome_font_1.render("will begin in...", True, wh), [800, 200])
        dis.blit(pygame.font.SysFont("arialblack", 65).render("5", True, wh), [870, 275])
        image = pygame.transform.scale(pygame.image.load(yahtzee_cup_image), (200, 200))

        c1 = 0 ; c2 = 1
        retain = []
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False ; pygame.quit() ; sys.exit()
            
            c1 += 1 ; time.sleep(0.025)
            if c1 % 65 <= 23 and c2 < 6:
                dis.fill(blk, rect=(650, 365, 1000, 1000))
                dis.blit(pygame.transform.rotate(image, 5*(c1 % 65)), [848, 365])
            elif c1 % 65 > 23 and c1 % 65 <= 30 and c1 % 2 == 1 and c2 < 6:
                dis.fill(blk, rect=(665, 455, 230, 230))
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(58,63)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(825,850), random.randint(480,505)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(58,63)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(810,835), random.randint(460,485)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(58,63)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(795,820), random.randint(490,515)])
            elif c1 % 65 > 30 and c1 % 65 <= 37 and c1 % 2 == 1 and c2 < 6:
                dis.fill(blk, rect=(665, 455, 230, 230))
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(55,60)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(800,825), random.randint(505,530)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(55,60)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(785,815), random.randint(485,510)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(55,60)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(770,795), random.randint(515,540)])
            elif c1 % 65 > 37 and c1 % 65 <= 44 and c1 % 2 == 1 and c2 < 6:
                dis.fill(blk, rect=(665, 455, 230, 230))
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(52,57)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(775,800), random.randint(530,555)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(52,57)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(775,800), random.randint(560,585)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(52,57)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(760,785), random.randint(510,535)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(52,57)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(745,760), random.randint(540,565)])
            elif c1 % 65 > 44 and c1 % 65 <= 51 and c1 % 2 == 1 and c2 < 6:
                dis.fill(blk, rect=(665, 455, 230, 230))
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(49,54)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(750,775), random.randint(565,580)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(49,54)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(750,775), random.randint(595,610)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(49,54)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(735,750), random.randint(535,560)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(49,54)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(710,735), random.randint(565,590)])
            elif c1 % 65 > 51 and c1 % 65 <= 53 and c1 % 2 == 1 and c2 < 6:
                dis.fill(blk, rect=(665, 455, 230, 230))
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(46,51)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(755,765), random.randint(575,585)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(46,51)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(735,750), random.randint(635,645)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(46,51)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(715,725), random.randint(555,565)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(46,51)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(670,680), random.randint(615,625)])
                dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(46,51)).render(dice2[random.randint(0,5)], True, wh),
                        [random.randint(695,705), random.randint(595,605)])
                
            if c1 % 40 == 0 and c2 < 6:
                dis.fill(blk, rect=(592, 290, 600, 100))
                dis.blit(pygame.font.SysFont("arialblack", 65).render(str(5-c2), True, wh), [870, 275])
                c2 += 1
            if c2 == 6:
                c2 += 1
                dis.fill(blk, rect=(592, 100, 1000, 1000))
                dis.blit(pygame.font.SysFont("arialblack", 50).render("Good Luck!", True, wh), [746, 275])
            if c1 == 320:
                dis.fill(blk, rect=(592, 50, 1000, 1000))
                loop = False 
            pygame.display.flip()

        ###################################################

        ### Fill in info about player who is currently rolling
        PLAYER_ORDER = {k: v for k, v in sorted(PLAYER_ORDER.items(), key=lambda item: item[1], reverse = True)}
        pc = 0
        current_player = player_names[0] if num_players == 1 else list(PLAYER_ORDER.keys())[pc]
        current_player_alt = str("p" + str(player_names.index(current_player)+1))
        current_player_color = p_colors[player_names.index(current_player)]
        current_player_color_alt = p_colors_alt[player_names.index(current_player)] 
        curr_MD = {}
        if current_player_alt == "p1":
            curr_MD = MD1
        elif current_player_alt == "p2":
            curr_MD = MD2
        elif current_player_alt == "p3":
            curr_MD = MD3
        elif current_player_alt == "p4":
            curr_MD = MD4

        ###################################################

        ### Rulebook Transition period of 3000 milliseconds
        rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
        r = rules_u.get_rect()
        r.x, r.y = 505,718
        dis.blit(rules_u, [505, 718])
        pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
        dis.blit(player_font.render("<-----  If you need to review the rules, click here.", True, wh), [595, 719])
        pygame.display.update()
        loop = True ; a = 0
        while loop and a < 2201:
            if a < 2200:
                dis.blit(player_font.render("<-----  If you need to review the rules, click here.", True, wh), [595, 719])
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False ; pygame.quit() ; sys.exit()

                # Rulebook click option
                if r.collidepoint(pygame.mouse.get_pos()):
                    dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (255, 150, 150), (499, 717, 87, 25), 2)
                    rules_c = rule_font_1.render("Rulebook", True, (255, 150, 150))
                    dis.blit(rules_c, [505, 718])
                else:
                    dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
                    rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
                    dis.blit(rules_u, [505, 718]) 
                if event.type == pygame.MOUSEBUTTONUP and r.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open(r"https://www.hasbro.com/common/instruct/Yahtzee.pdf")
            a += 1

        ###################################################

        ### MAIN GAME!
        # Display kept dice set
        dis.blit(small_dice_font.render("__", True, current_player_color), [655, 50])
        dis.blit(small_dice_font.render("__", True, current_player_color), [755, 50])
        dis.blit(small_dice_font.render("__", True, current_player_color), [855, 50])
        dis.blit(small_dice_font.render("__", True, current_player_color), [955, 50])
        dis.blit(small_dice_font.render("__", True, current_player_color), [1055, 50])
        dis.blit(sc_dice_font.render(" |                                                                                                |", True, current_player_color), [638, 150])
        dis.blit(sc_dice_font.render("   -  -  -  -  -  -  Your Saved Dice (click to remove)  -  -  -  -  -  -   ", True, current_player_color), [640, 160])
        pygame.display.update()

        # Current dice values info
        this_roll = {}; keep_set = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        keep_set_col = {1: (255,255,255,255), 2: (255,255,255,255), 3: (255,255,255,255), 4: (255,255,255,255), 5: (255,255,255,255)}
        k1 = False ; k2 = False; k3 = False; k4 = False; k5 = False
        uk1 = False ; uk2 = False; uk3 = False; uk4 = False; uk5 = False

        loop = True ; new_turn = True ; nah = True; count = ""
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False ; pygame.quit() ; sys.exit()
                    
                # Rulebook click option
                if r.collidepoint(pygame.mouse.get_pos()):
                    dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (255, 150, 150), (499, 717, 87, 25), 2)
                    rules_c = rule_font_1.render("Rulebook", True, (255, 150, 150))
                    dis.blit(rules_c, [505, 718])
                else:
                    dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
                    rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
                    dis.blit(rules_u, [505, 718]) 
                if event.type == pygame.MOUSEBUTTONUP and r.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open(r"https://www.hasbro.com/common/instruct/Yahtzee.pdf")

            # Re-colorize scorecard and other features
            if new_turn:
                new_turn = False
                greet_opt = [", it's your turn!", ", you're up!", ", take it away!", ", let's see a Yahtzee!", ", shake the dice!"] # Random greeting
                center_text = welcome_font_1.render(str(current_player) + greet_opt[random.randint(0,4)], True, current_player_color)
                dis.blit(center_text,center_text.get_rect(center=(900, 635)))
                dis.blit(click_font_1.render(current_player, True, current_player_color), [417, 56])
                scorecard = "************************************************************************************************"
                dis.fill(blk, rect=(10, 88, 580, 9)) ; dis.fill(blk, rect=(10, 706, 580, 9))
                dis.fill(blk, rect=(8, 88, 9, 629)) ; dis.fill(blk, rect=(580, 88, 9, 629))
                dis.blit(sc_font.render(scorecard, True, current_player_color), [11, 84])
                dis.blit(sc_font.render(scorecard, True, current_player_color), [13, 700])
                scorecard = "    _____________________      __________________     ____________     ____________     ____________"
                for i in range(0,len(MD_WRITES)):
                    center_text = sc_dice_font_2.render(str(list(curr_MD.values())[i]), True, current_player_color)
                    dis.blit(center_text,center_text.get_rect(center=MD_WRITES[i]))
                ty = [85,90,350,355,360,365,639.5,644.5,649.5,654.5]
                for i in ty:
                    dis.blit(sc_font.render(scorecard, True, current_player_color), [15, i])
                dis.fill(blk, rect=(15, 97.5, 15, 608)) ; dis.fill(blk, rect=(162.5, 97.5, 15, 608))
                dis.fill(blk, rect=(292.5, 97.5, 15, 608)) ; dis.fill(blk, rect=(384, 97.5, 15, 608))
                dis.fill(blk, rect=(475.5, 97.5, 15, 608)) ; dis.fill(blk, rect=(567, 97.5, 15, 608))
                for s in range(1,42):
                    value = sc_font.render(" ||", True, current_player_color)
                    if s < 20 or s > 21:
                        if s < 41:
                            dis.blit(value, [15, 82.5 + s*15]) ; dis.blit(value, [162.5, 82.5 + s*15])
                            dis.blit(value, [292.5, 82.5 + s*15]) ; dis.blit(value, [384, 82.5 + s*15])
                            dis.blit(value, [475.5, 82.5 + s*15]) ; dis.blit(value, [567, 82.5 + s*15])
                    value = sc_font.render("*", True, current_player_color)
                    dis.blit(value, [10, 77.5 + s*15]) ; dis.blit(value, [10, 85 + s*15])
                    dis.blit(value, [582, 77.5 + s*15]) ; dis.blit(value, [582, 85 + s*15])
                pygame.display.update()

                # Other display items
                image = pygame.transform.scale(pygame.image.load(yahtzee_cup_image), (265, 265))
                dis.blit(image, [938, 180])
                dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, wh), [690, 180])
                dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, wh), [790, 180])
                dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, wh), [640, 280])
                dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, wh), [740, 280])
                dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, wh), [840, 280])
                dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, wh), [840, 280])
                dis.blit(small_dice_font.render("-", True, current_player_color), [1065, 614])
                dis.blit(shake_font.render("Shake #1", True, current_player_color), [1100, 665])
                dis.blit(shake_font.render("Shake #2", True, gr), [1100, 690])
                dis.blit(shake_font.render("Shake #3", True, gr), [1100, 715])
                t_shake_u = click_font_3.render("SHAKE", True, wh)
                t_shake = t_shake_u.get_rect()
                t_shake.x, t_shake.y = 846,485
                dis.blit(t_shake_u, [846, 485])

                # Shake animation (if not out of turns)
                if player_outofturns[player_names.index(current_player)] == False:
                    loop2 = True ; loop3 = True; loop4 = True; cq = True; simulate = True
                    shake_count = 1 ; anim_count = 0
                    while loop2:
                        if "COMPUTER #" in current_player:
                            pygame.event.post(pygame.event.Event(COMPCLICK))
                        elif shake_count > 1:
                            pygame.event.post(pygame.event.Event(SHAKECLICK))
                            
                        for event2 in pygame.event.get():
                            if event2.type == pygame.QUIT:
                                loop2 = False ; pygame.quit() ; sys.exit()
                                
                            # Rulebook click option
                            if r.collidepoint(pygame.mouse.get_pos()):
                                dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (255, 150, 150), (499, 717, 87, 25), 2)
                                rules_c = rule_font_1.render("Rulebook", True, (255, 150, 150))
                                dis.blit(rules_c, [505, 718])
                            else:
                                dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
                                rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
                                dis.blit(rules_u, [505, 718]) 
                            if event2.type == pygame.MOUSEBUTTONUP and r.collidepoint(pygame.mouse.get_pos()):
                                webbrowser.open(r"https://www.hasbro.com/common/instruct/Yahtzee.pdf")
                                
                            # Don't hover over SHAKE too much!
                            if t_shake.collidepoint(pygame.mouse.get_pos()) and anim_count == 0 and shake_count == 1 and "COMPUTER #" not in current_player:
                                dis.fill(blk, rect=(789, 485, 600, 45))
                                t_shake_c = click_font_4.render("SHAKE" + str(count), True, current_player_color)
                                dis.blit(t_shake_c, [831 - len(count)*6.5, 482.5])
                                if cq:
                                    if len(count) < 6:
                                        count = str(count) + "!"
                                    else:
                                        dis.blit(sc_name_font.render("Seriously? Just SHAKE it.", True, wh), [827, 536])  
                                cq = False
                            elif anim_count == 0 and shake_count == 1 and "COMPUTER #" not in current_player:
                                dis.fill(blk, rect=(789, 485, 600, 45))
                                t_shake_u = click_font_3.render("SHAKE", True, wh)
                                dis.blit(t_shake_u, [846, 485])
                                cq = True

                            # Commence the shaking!
                            if (event2.type == pygame.MOUSEBUTTONUP and t_shake.collidepoint(pygame.mouse.get_pos()) and anim_count == 0) or (anim_count == 0 and event2.type == COMPCLICK) or event2.type == SHAKECLICK:
                                if event2.type == COMPCLICK and shake_count == 1:
                                    dis.fill(blk, rect=(789, 485, 600, 45))
                                    pygame.display.update()
                                    time.sleep(1.25)
                                nah = False ; count = ""
                                dis.fill(blk, rect=(775, 465, 250, 100))
                                while anim_count <= 150:
                                    if anim_count < 16:
                                        dis.fill(blk, rect=(938, 188, 300, 285))
                                        dis.blit(pygame.transform.rotate(image, 6*anim_count), [938, 180])
                                    elif anim_count < 32:
                                        dis.fill(blk, rect=(620, 188, 345, 260))
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[1]), [680+(12*(anim_count-16)), 180+(4*(anim_count-16))])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[2]), [780+(5*(anim_count-16)), 180+(4*(anim_count-16))])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[3]), [630+(15*(anim_count-16)), 280-(3*(anim_count-16))])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[4]), [730+(9*(anim_count-16)), 280-(3*(anim_count-16))])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[5]), [830+(2.25*(anim_count-16)), 280-(2.75*(anim_count-16))])
                                    elif anim_count < 40:
                                        dis.fill(blk, rect=(620, 188, 665, 260))
                                        dis.blit(pygame.transform.rotate(image, 90), [938+(16*(anim_count-32)), 180])
                                    elif anim_count < 48:
                                        dis.fill(blk, rect=(620, 188, 665, 260))
                                        dis.blit(pygame.transform.rotate(image, 90), [1050-(16*(anim_count-40)), 180])
                                    elif anim_count < 97 and anim_count % 2 == 0:
                                        dis.fill(blk, rect=(598, 188, 665, 260))
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[1]), [590+(1*(anim_count-48)), 230])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[2]), [665+(1.5*(anim_count-48)), 230])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[3]), [740+(2*(anim_count-48)), 230])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[4]), [815+(2.5*(anim_count-48)), 230])
                                        dis.blit(big_dice_font.render(dice2[random.randint(0,5)], True, keep_set_col[5]), [890+(3*(anim_count-48)), 230])
                                    elif anim_count < 150 and anim_count % 2 == 0:
                                        ends = [random.randint(102,150), random.randint(102,150), random.randint(102,150), random.randint(102,150), random.randint(102,150)]
                                        if anim_count < ends[0]:
                                            dis.fill(blk, rect=(648, 200, 80, 250))
                                            this_roll[1] = random.randint(0,5) + 1
                                            dis.blit(big_dice_font.render(dice2[this_roll[1]-1], True, keep_set_col[1]), [648, 230])
                                            dis.blit(another_font.render(str(this_roll[1]), True, keep_set_col[1]), [682, 215])
                                        if anim_count < ends[1]:
                                            dis.fill(blk, rect=(747, 200, 80, 250))
                                            this_roll[2] = random.randint(0,5) + 1
                                            dis.blit(big_dice_font.render(dice2[this_roll[2]-1], True, keep_set_col[2]), [747, 230])
                                            dis.blit(another_font.render(str(this_roll[2]), True, keep_set_col[2]), [781, 215])                                 
                                        if anim_count < ends[2]:
                                            dis.fill(blk, rect=(846, 200, 80, 250))
                                            this_roll[3] = random.randint(0,5) + 1
                                            dis.blit(big_dice_font.render(dice2[this_roll[3]-1], True, keep_set_col[3]), [846, 230])
                                            dis.blit(another_font.render(str(this_roll[3]), True, keep_set_col[3]), [880, 215])
                                        if anim_count < ends[3]:
                                            dis.fill(blk, rect=(945, 200, 80, 250))
                                            this_roll[4] = random.randint(0,5) + 1
                                            dis.blit(big_dice_font.render(dice2[this_roll[4]-1], True, keep_set_col[4]), [945, 230])
                                            dis.blit(another_font.render(str(this_roll[4]), True, keep_set_col[4]), [979, 215])
                                        if anim_count < ends[4]:
                                            dis.fill(blk, rect=(1044, 200, 80, 250))
                                            this_roll[5] = random.randint(0,5) + 1
                                            dis.blit(big_dice_font.render(dice2[this_roll[5]-1], True, keep_set_col[5]), [1044, 230])
                                            dis.blit(another_font.render(str(this_roll[5]), True, keep_set_col[5]), [1078, 215])
                                            
                                        # Retain the values of the kept dice
                                        this_roll[1] = keep_set[1] if keep_set[1] != 0 else this_roll[1]
                                        this_roll[2] = keep_set[2] if keep_set[2] != 0 else this_roll[2]
                                        this_roll[3] = keep_set[3] if keep_set[3] != 0 else this_roll[3]
                                        this_roll[4] = keep_set[4] if keep_set[4] != 0 else this_roll[4]
                                        this_roll[5] = keep_set[5] if keep_set[5] != 0 else this_roll[5]
                                        
                                    pygame.display.flip()
                                    anim_count += 1
                                    time.sleep(.024)
                                   
                                # Text based on shake number
                                if shake_count == 1 or shake_count == 2:
                                    dis.fill(blk, rect=(600, 600, 600, 56))
                                    center_text = welcome_font_1.render("Click a score, or set dice aside and re-shake.", True, current_player_color)
                                    dis.blit(center_text,center_text.get_rect(center=(900, 635)))
                                elif shake_count == 3:
                                    dis.fill(blk, rect=(600, 600, 600, 56))
                                    center_text = welcome_font_1.render("Click on a score to end your turn.", True, current_player_color)
                                    dis.blit(center_text,center_text.get_rect(center=(900, 635)))
                                    
                                # Set up "Keep" buttons and subsequent mouse hover shading
                                keep1_u = click_font_1.render("Keep", True, keep_set_col[1]) ; keep2_u = click_font_1.render("Keep", True, keep_set_col[2])
                                keep3_u = click_font_1.render("Keep", True, keep_set_col[3]) ; keep4_u = click_font_1.render("Keep", True, keep_set_col[4])
                                keep5_u = click_font_1.render("Keep", True, keep_set_col[5])
                                keep1 = keep1_u.get_rect() ; keep2 = keep2_u.get_rect() ; keep3 = keep3_u.get_rect() ; keep4 = keep4_u.get_rect() ; keep5 = keep5_u.get_rect()
                                keep1.x, keep1.y = 672,365
                                keep2.x, keep2.y = 771,365
                                keep3.x, keep3.y = 870,365
                                keep4.x, keep4.y = 969,365
                                keep5.x, keep5.y = 1068,365
                                if "COMPUTER #" not in current_player: 
                                    dis.blit(keep1_u, [672, 365]) ; dis.blit(keep2_u, [771, 365]) ; dis.blit(keep3_u, [870, 365]) ; dis.blit(keep4_u, [969, 365]) ; dis.blit(keep5_u, [1068, 365])

                                # Display scoring options
                                dis.blit(another_underline_font.render("Scoring Options:", True, wh), [816, 474])
                                scorecard = "__________________________________________________________"
                                dis.blit(another_underline_font.render(scorecard, True, wh), [633, 450])
                                dis.blit(another_underline_font.render(scorecard, True, wh), [633, 580])
                                scorecard = pygame.transform.rotate(another_underline_font.render("______________", True, wh), 90)
                                scorecard_rect = scorecard.get_rect()
                                scorecard_rect = dis.get_rect() ; scorecard_rect = dis.get_rect()
                                scorecard_rect.x, scorecard_rect.y = 607,478
                                dis.blit(scorecard, scorecard_rect)
                                scorecard_rect.x, scorecard_rect.y = 1130,478
                                dis.blit(scorecard, scorecard_rect)
                                pygame.display.update()

                                # Dice scoring possibilities LOGIC
                                S_DISP_LIST = [] ; S_SCORE_LIST = [] ; S_THING_LIST = []
                                S_DICT_RECT.clear()
                                comp_multiplier = 1.4 if "COMPUTER #" in current_player else 1
                                ACES = sum(1 for i in list(this_roll.values()) if i == 1) ; TWOS = sum(1 for i in list(this_roll.values()) if i == 2)
                                THREES = sum(1 for i in list(this_roll.values()) if i == 3) ; FOURS = sum(1 for i in list(this_roll.values()) if i == 4)
                                FIVES = sum(1 for i in list(this_roll.values()) if i == 5) ; SIXES = sum(1 for i in list(this_roll.values()) if i == 6)
                                NUMS_LIST = [ACES, TWOS, THREES, FOURS, FIVES, SIXES]
                                CHANCE = sum(list(this_roll.values()))
                                if ACES == 5 or TWOS == 5 or THREES == 5 or FOURS == 5 or FIVES == 5 or SIXES == 5:
                                    if YAHTZ == 50 and YAHTZ_B1 == 100 and list(curr_MD.values())[14+((game-1)*21)] != '':
                                        if list(curr_MD.values())[15+((game-1)*21)] == '':
                                            YAHTZ_B3 = 100
                                            S_DISP_LIST.append("Yahtzee Bonus: 100 Pts.") ; S_SCORE_LIST.append(100) ; S_THING_LIST.append("YB3")
                                    elif YAHTZ == 50 and list(curr_MD.values())[13+((game-1)*21)] != '':
                                        if list(curr_MD.values())[14+((game-1)*21)] == '':
                                            YAHTZ_B2 = 100
                                            S_DISP_LIST.append("Yahtzee Bonus: 100 Pts.") ; S_SCORE_LIST.append(100) ; S_THING_LIST.append("YB2")
                                    elif YAHTZ == 50 and list(curr_MD.values())[12+((game-1)*21)] != '' and list(curr_MD.values())[12+((game-1)*21)] != 0:
                                        if list(curr_MD.values())[13+((game-1)*21)] == '':
                                            YAHTZ_B1 = 100
                                            S_DISP_LIST.append("Yahtzee Bonus: 100 Pts.") ; S_SCORE_LIST.append(100) ; S_THING_LIST.append("YB1")
                                    else:
                                        if list(curr_MD.values())[12+((game-1)*21)] == '' and list(curr_MD.values())[12+((game-1)*21)] != 0:
                                            YAHTZ = 50
                                            S_DISP_LIST.append("YAHTZEE: 50 Pts.") ; S_SCORE_LIST.append(50) ; S_THING_LIST.append("Y")
                                if (ACES >= 1 and TWOS >= 1 and THREES >= 1 and FOURS >= 1 and FIVES >= 1) or (TWOS >= 1 and THREES >= 1 and FOURS >= 1 and FIVES >= 1 and SIXES >= 1):
                                    if list(curr_MD.values())[10+((game-1)*21)] == '':
                                        LARGES = 40
                                        S_DISP_LIST.append("Lg. Straight: 40 Pts.") ; S_SCORE_LIST.append(40) ; S_THING_LIST.append("LS")
                                if (ACES >= 1 and TWOS >= 1 and THREES >= 1 and FOURS >= 1) or (TWOS >= 1 and THREES >= 1 and FOURS >= 1 and FIVES >= 1) or (THREES >= 1 and FOURS >= 1 and FIVES >= 1 and SIXES >= 1):
                                    if list(curr_MD.values())[9+((game-1)*21)] == '':
                                        SMALLS = 30
                                        S_DISP_LIST.append("Sm. Straight: 30 Pts.") ; S_SCORE_LIST.append(30) ; S_THING_LIST.append("SS")
                                if 2 in NUMS_LIST and 3 in NUMS_LIST:
                                    if list(curr_MD.values())[8+((game-1)*21)] == '':
                                        FHOUSE = 25
                                        S_DISP_LIST.append("Full House: 25 Pts.") ; S_SCORE_LIST.append(25*comp_multiplier) ; S_THING_LIST.append("FH")
                                if ACES == 4 or TWOS == 4 or THREES == 4 or FOURS == 4 or FIVES == 4 or SIXES == 4:
                                    if list(curr_MD.values())[7+((game-1)*21)] == '':
                                        KIND4 = sum(list(this_roll.values()))
                                        S_DISP_LIST.append("4 Of A Kind: " + str(KIND4) + " Pts.") ; S_SCORE_LIST.append(KIND4) ; S_THING_LIST.append("4k")
                                if ACES >= 3 or TWOS >= 3 or THREES >= 3 or FOURS >= 3 or FIVES >= 3 or SIXES >= 3:
                                    if list(curr_MD.values())[6+((game-1)*21)] == '':
                                        KIND3 = sum(list(this_roll.values()))
                                        S_DISP_LIST.append("3 Of A Kind: " + str(KIND3) + " Pts.") ; S_SCORE_LIST.append(KIND3) ; S_THING_LIST.append("3k")
                                        
                                if list(curr_MD.values())[11+((game-1)*21)] == '':
                                    S_DISP_LIST.append("Chance: " + str(CHANCE) + " Pts.") ; S_SCORE_LIST.append(CHANCE) ; S_THING_LIST.append("chance")
                                if ACES > 1:
                                    if list(curr_MD.values())[0+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Aces: " + str(ACES) + " Pts.") ; S_SCORE_LIST.append(ACES) ; S_THING_LIST.append("ace")
                                elif ACES == 1:
                                    if list(curr_MD.values())[0+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Aces: " + str(ACES) + " Point") ; S_SCORE_LIST.append(((ACES)*comp_multiplier)*comp_multiplier) ; S_THING_LIST.append("ace")
                                if TWOS > 0:
                                    if list(curr_MD.values())[1+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Twos: " + str(TWOS*2) + " Pts.") ; S_SCORE_LIST.append(((TWOS*2)*comp_multiplier)*comp_multiplier) ; S_THING_LIST.append("two")
                                if THREES > 0:
                                    if list(curr_MD.values())[2+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Threes: " + str(THREES*3) + " Pts.") ; S_SCORE_LIST.append(((THREES*3)*comp_multiplier)*comp_multiplier) ; S_THING_LIST.append("three")
                                if FOURS > 0:
                                    if list(curr_MD.values())[3+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Fours: " + str(FOURS*4) + " Pts.") ; S_SCORE_LIST.append((FOURS*4)*comp_multiplier) ; S_THING_LIST.append("four")
                                if FIVES > 0:
                                    if list(curr_MD.values())[4+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Fives: " + str(FIVES*5) + " Pts.") ; S_SCORE_LIST.append((FIVES*5)*comp_multiplier) ; S_THING_LIST.append("five")
                                if SIXES > 0:
                                    if list(curr_MD.values())[5+((game-1)*21)] == '':
                                        S_DISP_LIST.append("Sixes: " + str(SIXES*6) + " Pts.") ; S_SCORE_LIST.append((SIXES*6)*comp_multiplier) ; S_THING_LIST.append("six")
                                
                                # If no options!
                                if S_THING_LIST == []:
                                    iterate = [i for i, x in enumerate(list(curr_MD.values())[0+((game-1)*21):13+((game-1)*21)]) if x == '']
                                    for it in iterate:
                                        S_DISP_LIST.append(str(TITLES1[it]) + ": 0 Pts.")
                                        S_THING_LIST.append(str(TITLES2[it]))
                                        S_SCORE_LIST.append(0)
                                        
                                # Display options in proper order at proper coordinates
                                for d in range(0,len(S_DISP_LIST)):
                                    temp_render = click_font_1.render(S_DISP_LIST[d], True, wh)
                                    S_DICT['sdl_' + str(d+1)] = temp_render
                                    S_DICT_RECT['sdl_' + str(d+1)] = S_DICT['sdl_' + str(d+1)].get_rect()
                                    S_DICT_RECT['sdl_' + str(d+1)].x, S_DICT_RECT['sdl_' + str(d+1)].y = 643+((math.floor(d/3))*196), 513+((d % 3)*32)
                                    dis.blit(temp_render, [645+((math.floor(d/3))*(205-(math.floor(d/6)*15))), 513+((d % 3)*32)])
                               
                                # Decide to keep/remove dice
                                if shake_count < 3:
                                    t_shake2_u = click_font_3.render("SHAKE", True, wh)
                                    t_shake2 = t_shake2_u.get_rect()
                                    t_shake2.x, t_shake2.y = 836,412
                                    dis.blit(t_shake2_u, [836, 412]) if "COMPUTER #" not in current_player else None
                                    
                                pygame.display.update()

                                ######## COMPUTER SIMULATION TO DETERMINE BEST COURSE OF ACTION ######## 
                                best_option = 0
                                phase = 0
                                if "COMPUTER #" in current_player and shake_count < 3 and simulate:
                                    roll_options = [[[]],[this_roll[1]],[this_roll[2]],[this_roll[3]],[this_roll[4]],[this_roll[5]],
                                                    [this_roll[1],this_roll[2]],[this_roll[1],this_roll[3]],[this_roll[1],this_roll[4]],
                                                    [this_roll[1],this_roll[5]],[this_roll[2],this_roll[3]],[this_roll[2],this_roll[4]],
                                                    [this_roll[2],this_roll[5]],[this_roll[3],this_roll[4]],[this_roll[3],this_roll[5]],
                                                    [this_roll[4],this_roll[5]],[this_roll[1],this_roll[2],this_roll[3]],
                                                    [this_roll[1],this_roll[2],this_roll[4]],[this_roll[1],this_roll[2],this_roll[5]],
                                                    [this_roll[1],this_roll[3],this_roll[4]],[this_roll[1],this_roll[3],this_roll[5]],
                                                    [this_roll[1],this_roll[4],this_roll[5]],[this_roll[2],this_roll[3],this_roll[4]],
                                                    [this_roll[2],this_roll[3],this_roll[5]],[this_roll[2],this_roll[4],this_roll[5]],
                                                    [this_roll[3],this_roll[4],this_roll[5]],[this_roll[1],this_roll[2],this_roll[3],this_roll[4]],
                                                    [this_roll[1],this_roll[2],this_roll[3],this_roll[5]],[this_roll[1],this_roll[2],this_roll[4],this_roll[5]],
                                                    [this_roll[1],this_roll[3],this_roll[4],this_roll[5]],[this_roll[2],this_roll[3],this_roll[4],this_roll[5]],
                                                    [this_roll[1],this_roll[2],this_roll[3],this_roll[4],this_roll[5]]]
                                    avg_max = 0
                                    avg_max_list = []
                                    test_phase_list = []
                                    for a in roll_options:
                                        avg_max = 0
                                        for b in range(1, 1501):
                                            test_phase_list.clear()
                                            test_phase_list.append(a)
                                            test_phase_list = sum(test_phase_list,[])
                                            if test_phase_list == [[]]:
                                                test_phase_list.clear()
                                            while len(test_phase_list) < 5:
                                                test_phase_list.append(random.randint(1,6))
                                            # Dice scoring possibilities LOGIC
                                            S_SCORE_LIST_SIM = []
                                            ACES_SIM = sum(1 for i in test_phase_list if i == 1) ; TWOS_SIM = sum(1 for i in test_phase_list if i == 2)
                                            THREES_SIM = sum(1 for i in test_phase_list if i == 3) ; FOURS_SIM = sum(1 for i in test_phase_list if i == 4)
                                            FIVES_SIM = sum(1 for i in test_phase_list if i == 5) ; SIXES_SIM = sum(1 for i in test_phase_list if i == 6)
                                            NUMS_LIST_SIM = [ACES, TWOS, THREES, FOURS, FIVES, SIXES]
                                            CHANCE_SIM = sum(test_phase_list)
                                            YAHTZ_SIM = YAHTZ; YAHTZ_B1_SIM = YAHTZ_B1; YAHTZ_B2_SIM = YAHTZ_B1; YAHTZ_B3_SIM = YAHTZ_B1
                                            LARGES_SIM = LARGES; SMALLS_SIM = SMALLS; FHOUSE_SIM = FHOUSE; KIND4_SIM = KIND4; KIND3_SIM = KIND3

                                            if ACES_SIM == 5 or TWOS_SIM == 5 or THREES_SIM == 5 or FOURS_SIM == 5 or FIVES_SIM == 5 or SIXES_SIM == 5:
                                                if YAHTZ_SIM == 50 and YAHTZ_B1_SIM == 100 and list(curr_MD.values())[14+((game-1)*21)] != '':
                                                    if list(curr_MD.values())[15+((game-1)*21)] == '':
                                                        YAHTZ_B3_SIM = 100
                                                        S_SCORE_LIST_SIM.append(100)
                                                elif YAHTZ_SIM == 50 and list(curr_MD.values())[13+((game-1)*21)] != '':
                                                    if list(curr_MD.values())[14+((game-1)*21)] == '':
                                                        YAHTZ_B2_SIM = 100
                                                        S_SCORE_LIST_SIM.append(100)
                                                elif YAHTZ_SIM == 50 and list(curr_MD.values())[12+((game-1)*21)] != '' and list(curr_MD.values())[12+((game-1)*21)] != 0:
                                                    if list(curr_MD.values())[13+((game-1)*21)] == '':
                                                        YAHTZ_B1_SIM = 100
                                                        S_SCORE_LIST_SIM.append(100)
                                                else:
                                                    if list(curr_MD.values())[12+((game-1)*21)] == '' and list(curr_MD.values())[12+((game-1)*21)] != 0:
                                                        YAHTZ_SIM = 75
                                                        S_SCORE_LIST_SIM.append(75)
                                            if (ACES_SIM >= 1 and TWOS_SIM >= 1 and THREES_SIM >= 1 and FOURS_SIM >= 1 and FIVES_SIM >= 1) or (TWOS_SIM >= 1 and THREES_SIM >= 1 and FOURS_SIM >= 1 and FIVES_SIM >= 1 and SIXES_SIM >= 1):
                                                if list(curr_MD.values())[10+((game-1)*21)] == '':
                                                    LARGES_SIM = 40
                                                    S_SCORE_LIST_SIM.append(45)
                                            if (ACES_SIM >= 1 and TWOS_SIM >= 1 and THREES_SIM >= 1 and FOURS_SIM >= 1) or (TWOS_SIM >= 1 and THREES_SIM >= 1 and FOURS_SIM >= 1 and FIVES_SIM >= 1) or (THREES_SIM >= 1 and FOURS_SIM >= 1 and FIVES_SIM >= 1 and SIXES_SIM >= 1):
                                                if list(curr_MD.values())[9+((game-1)*21)] == '':
                                                    SMALLS_SIM = 30
                                                    S_SCORE_LIST_SIM.append(30)
                                            if 2 in NUMS_LIST_SIM and 3 in NUMS_LIST_SIM:
                                                if list(curr_MD.values())[8+((game-1)*21)] == '':
                                                    FHOUSE_SIM = 25
                                                    S_SCORE_LIST_SIM.append(25+10) # +10 to give more favor to FULL HOUSE
                                            if ACES_SIM == 4 or TWOS_SIM == 4 or THREES_SIM == 4 or FOURS_SIM == 4 or FIVES_SIM == 4 or SIXES_SIM == 4:
                                                if list(curr_MD.values())[7+((game-1)*21)] == '':
                                                    KIND4_SIM = sum(test_phase_list)
                                                    S_SCORE_LIST_SIM.append(KIND4_SIM)
                                            if ACES_SIM >= 3 or TWOS_SIM >= 3 or THREES_SIM >= 3 or FOURS_SIM >= 3 or FIVES_SIM >= 3 or SIXES_SIM >= 3:
                                                if list(curr_MD.values())[6+((game-1)*21)] == '':
                                                    KIND3_SIM = sum(test_phase_list)
                                                    S_SCORE_LIST_SIM.append(KIND3_SIM)
                                                    
                                            if list(curr_MD.values())[11+((game-1)*21)] == '':
                                                S_SCORE_LIST_SIM.append(CHANCE_SIM)
                                            if ACES_SIM > 0:
                                                if list(curr_MD.values())[0+((game-1)*21)] == '':
                                                    S_SCORE_LIST_SIM.append(((ACES_SIM)*1.4)*1.4)  # 1.4 multiplier to factor in potential bonus
                                            if TWOS_SIM > 0:
                                                if list(curr_MD.values())[1+((game-1)*21)] == '':
                                                    S_SCORE_LIST_SIM.append(((TWOS_SIM*2)*1.4)*1.4)  # 1.4 multiplier to factor in potential bonus
                                            if THREES_SIM > 0:
                                                if list(curr_MD.values())[2+((game-1)*21)] == '':
                                                    S_SCORE_LIST_SIM.append(((THREES_SIM*3)*1.4)*1.4)  # 1.4 multiplier to factor in potential bonus
                                            if FOURS_SIM > 0:
                                                if list(curr_MD.values())[3+((game-1)*21)] == '':
                                                    S_SCORE_LIST_SIM.append((FOURS_SIM*4)*1.4)  # 1.4 multiplier to factor in potential bonus
                                            if FIVES_SIM > 0:
                                                if list(curr_MD.values())[4+((game-1)*21)] == '':
                                                    S_SCORE_LIST_SIM.append((FIVES_SIM*5)*1.4)  # 1.4 multiplier to factor in potential bonus
                                            if SIXES_SIM > 0:
                                                if list(curr_MD.values())[5+((game-1)*21)] == '':
                                                    S_SCORE_LIST_SIM.append((SIXES_SIM*6)*1.4) # 1.4 multiplier to factor in potential bonus
                                            if len(S_SCORE_LIST_SIM) == 0:
                                                S_SCORE_LIST_SIM.append(0)
                                                
                                            avg_max += sum(S_SCORE_LIST_SIM) / len(S_SCORE_LIST_SIM)

                                        avg_max_list.append(avg_max/1500)
                                        phase += 1
                                    best_option = avg_max_list.index(max(avg_max_list))
                                    simulate = False

                                loop3 = True
                                while loop3:
                                    for event3 in pygame.event.get():
                                        if event3.type == pygame.QUIT:
                                            loop3 = False ; pygame.quit() ; sys.exit()
                                            
                                        # Rulebook click option
                                        if r.collidepoint(pygame.mouse.get_pos()):
                                            dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (255, 150, 150), (499, 717, 87, 25), 2)
                                            rules_c = rule_font_1.render("Rulebook", True, (255, 150, 150))
                                            dis.blit(rules_c, [505, 718])
                                        else:
                                            dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
                                            rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
                                            dis.blit(rules_u, [505, 718]) 
                                        if event3.type == pygame.MOUSEBUTTONUP and r.collidepoint(pygame.mouse.get_pos()):
                                            webbrowser.open(r"https://www.hasbro.com/common/instruct/Yahtzee.pdf")

                                        if t_shake2.collidepoint(pygame.mouse.get_pos()) and shake_count < 3 and 0 in keep_set.values() and "COMPUTER #" not in current_player:
                                            dis.fill(blk, rect=(774, 412, 600, 45))
                                            t_shake2_c = click_font_4.render("SHAKE" + str(count), True, current_player_color)
                                            dis.blit(t_shake2_c, [823, 408])
                                        elif shake_count < 3 and 0 in keep_set.values() and "COMPUTER #" not in current_player:
                                            dis.fill(blk, rect=(774, 412, 600, 45))
                                            t_shake2_u = click_font_3.render("SHAKE", True, wh)
                                            dis.blit(t_shake2_u, [836, 412])

                                        # Keep, hover
                                        if keep1.collidepoint(pygame.mouse.get_pos()) and k1 == False and keep_set[1] == 0 and "COMPUTER #" not in current_player:
                                            keep1_u = click_font_1.render("Keep", True, blk) ; keep1_c = click_font_2.render("Keep", True, current_player_color)
                                            dis.blit(keep1_u, [672, 365]) ; dis.blit(keep1_c, [672, 365])
                                            dis.blit(big_dice_font.render(dice2[this_roll[1]-1], True, current_player_color), [648, 230])
                                        elif keep2.collidepoint(pygame.mouse.get_pos()) and k2 == False and keep_set[2] == 0 and "COMPUTER #" not in current_player:
                                            keep2_u = click_font_1.render("Keep", True, blk) ; keep2_c = click_font_2.render("Keep", True, current_player_color)
                                            dis.blit(keep2_u, [771, 365]) ; dis.blit(keep2_c, [771, 365])
                                            dis.blit(big_dice_font.render(dice2[this_roll[2]-1], True, current_player_color), [747, 230])
                                        elif keep3.collidepoint(pygame.mouse.get_pos()) and k3 == False and keep_set[3] == 0 and "COMPUTER #" not in current_player:
                                            keep3_u = click_font_1.render("Keep", True, blk) ; keep3_c = click_font_2.render("Keep", True, current_player_color)
                                            dis.blit(keep3_u, [870, 365]) ; dis.blit(keep3_c, [870, 365])
                                            dis.blit(big_dice_font.render(dice2[this_roll[3]-1], True, current_player_color), [846, 230])
                                        elif keep4.collidepoint(pygame.mouse.get_pos()) and k4 == False and keep_set[4] == 0 and "COMPUTER #" not in current_player:
                                            keep4_u = click_font_1.render("Keep", True, blk) ; keep4_c = click_font_2.render("Keep", True, current_player_color)
                                            dis.blit(keep4_u, [969, 365]) ; dis.blit(keep4_c, [969, 365])
                                            dis.blit(big_dice_font.render(dice2[this_roll[4]-1], True, current_player_color), [945, 230])
                                        elif keep5.collidepoint(pygame.mouse.get_pos()) and k5 == False and keep_set[5] == 0 and "COMPUTER #" not in current_player:
                                            keep5_u = click_font_1.render("Keep", True, blk) ; keep5_c = click_font_2.render("Keep", True, current_player_color)
                                            dis.blit(keep5_u, [1068, 365]) ; dis.blit(keep5_c, [1068, 365])
                                            dis.blit(big_dice_font.render(dice2[this_roll[5]-1], True, current_player_color), [1044, 230])
                                        elif "COMPUTER #" not in current_player:
                                            if k1 == False and keep_set[1] == 0:
                                                keep1_c = click_font_2.render("Keep", True, blk) ; keep1_u = click_font_1.render("Keep", True, wh)
                                                dis.blit(keep1_c, [672, 365]) ; dis.blit(keep1_u, [672, 365])
                                                dis.blit(big_dice_font.render(dice2[this_roll[1]-1], True, wh), [648, 230])
                                                dis.blit(another_font.render(str(this_roll[1]), True, wh), [682, 215])
                                            if k2 == False and keep_set[2] == 0:
                                                keep2_c = click_font_2.render("Keep", True, blk) ; keep2_u = click_font_1.render("Keep", True, wh)
                                                dis.blit(keep2_c, [771, 365]) ; dis.blit(keep2_u, [771, 365])
                                                dis.blit(big_dice_font.render(dice2[this_roll[2]-1], True, wh), [747, 230])
                                                dis.blit(another_font.render(str(this_roll[2]), True, wh), [781, 215])
                                            if k3 == False and keep_set[3] == 0:
                                                keep3_c = click_font_2.render("Keep", True, blk) ; keep3_u = click_font_1.render("Keep", True, wh)
                                                dis.blit(keep3_c, [870, 365]) ; dis.blit(keep3_u, [870, 365])
                                                dis.blit(big_dice_font.render(dice2[this_roll[3]-1], True, wh), [846, 230])
                                                dis.blit(another_font.render(str(this_roll[3]), True, wh), [880, 215])
                                            if k4 == False and keep_set[4] == 0:
                                                keep4_c = click_font_2.render("Keep", True, blk) ; keep4_u = click_font_1.render("Keep", True, wh)
                                                dis.blit(keep4_c, [969, 365]) ; dis.blit(keep4_u, [969, 365])
                                                dis.blit(big_dice_font.render(dice2[this_roll[4]-1], True, wh), [945, 230])
                                                dis.blit(another_font.render(str(this_roll[4]), True, wh), [979, 215])
                                            if k5 == False and keep_set[5] == 0:
                                                keep5_c = click_font_2.render("Keep", True, blk) ; keep5_u = click_font_1.render("Keep", True, wh)
                                                dis.blit(keep5_c, [1068, 365]) ; dis.blit(keep5_u, [1068, 365])
                                                dis.blit(big_dice_font.render(dice2[this_roll[5]-1], True, wh), [1044, 230])
                                                dis.blit(another_font.render(str(this_roll[5]), True, wh), [1078, 215])

                                        correct = -1
                                        for rect in list(S_DICT_RECT.values()):
                                            correct += 1
                                            position = [645+((math.floor(correct/3))*(205-(math.floor(correct/6)*15))), 513+((correct%3)*32)]
                                            if rect.collidepoint(pygame.mouse.get_pos()):
                                                dis.blit(click_font_1.render(S_DISP_LIST[correct], True, blk), position)
                                                dis.blit(click_font_2.render(S_DISP_LIST[correct], True, current_player_color), position)
                                            else:
                                                dis.blit(click_font_2.render(S_DISP_LIST[correct], True, blk), position)
                                                dis.blit(click_font_1.render(S_DISP_LIST[correct], True, wh), position)

                                        # Keep, clicking
                                        if (event3.type == pygame.MOUSEBUTTONUP and keep1.collidepoint(pygame.mouse.get_pos())) or (k1 == False and shake_count < 3 and "COMPUTER #" in current_player and best_option in [1,6,7,8,9,16,17,18,19,20,21,26,27,28,29,31]):
                                            unkeep1_u = small_dice_font.render(dice2[this_roll[1]-1], True, current_player_color_alt)
                                            unkeep1 = unkeep1_u.get_rect()
                                            unkeep1.x, unkeep1.y = 657,56
                                            dis.blit(unkeep1_u, [657, 56])
                                            dis.fill(blk, rect=(655, 220, 80, 180))
                                            dis.blit(another_font_2.render(str(this_roll[1]), True, current_player_color_alt), [682, 56])
                                            k1 = True ; uk1 = True
                                            keep_set[1] = this_roll[1] ; keep_set_col[1] = (0,0,0,0)
                                            dis.fill(blk, rect=(774, 412, 600, 45)) if 0 not in keep_set.values() else None
                                            if "COMPUTER #" in current_player:
                                                time.sleep(0.5) ; pygame.display.update()
                                        if (event3.type == pygame.MOUSEBUTTONUP and keep2.collidepoint(pygame.mouse.get_pos())) or (k2 == False and shake_count < 3 and "COMPUTER #" in current_player and best_option in [2,6,10,11,12,16,17,18,22,23,24,26,27,28,30,31]):
                                            unkeep2_u = small_dice_font.render(dice2[this_roll[2]-1], True, current_player_color_alt)
                                            unkeep2 = unkeep2_u.get_rect()
                                            unkeep2.x, unkeep2.y = 757,56
                                            dis.blit(unkeep2_u, [757, 56])
                                            dis.fill(blk, rect=(755, 220, 80, 180))
                                            dis.blit(another_font_2.render(str(this_roll[2]), True, current_player_color_alt), [781, 56])
                                            k2 = True ; uk2 = True
                                            keep_set[2] = this_roll[2] ; keep_set_col[2] = (0,0,0,0)
                                            dis.fill(blk, rect=(774, 412, 600, 45)) if 0 not in keep_set.values() else None
                                            if "COMPUTER #" in current_player:
                                                time.sleep(0.5) ; pygame.display.update()
                                        if (event3.type == pygame.MOUSEBUTTONUP and keep3.collidepoint(pygame.mouse.get_pos())) or (k3 == False and shake_count < 3 and "COMPUTER #" in current_player and best_option in [3,7,10,13,14,16,19,20,22,23,25,26,27,29,30,31]):
                                            unkeep3_u = small_dice_font.render(dice2[this_roll[3]-1], True, current_player_color_alt)
                                            unkeep3 = unkeep3_u.get_rect()
                                            unkeep3.x, unkeep3.y = 857,56
                                            dis.blit(unkeep3_u, [857, 56])
                                            dis.fill(blk, rect=(855, 220, 80, 180))
                                            dis.blit(another_font_2.render(str(this_roll[3]), True, current_player_color_alt), [880, 56])
                                            k3 = True ; uk3 = True
                                            keep_set[3] = this_roll[3] ; keep_set_col[3] = (0,0,0,0)
                                            dis.fill(blk, rect=(774, 412, 600, 45)) if 0 not in keep_set.values() else None
                                            if "COMPUTER #" in current_player:
                                                time.sleep(0.5) ; pygame.display.update()
                                        if (event3.type == pygame.MOUSEBUTTONUP and keep4.collidepoint(pygame.mouse.get_pos())) or (k4 == False and shake_count < 3 and "COMPUTER #" in current_player and best_option in [4,8,11,13,15,17,19,21,22,24,25,26,28,29,30,31]):
                                            unkeep4_u = small_dice_font.render(dice2[this_roll[4]-1], True, current_player_color_alt)
                                            unkeep4 = unkeep4_u.get_rect()
                                            unkeep4.x, unkeep4.y = 957,56
                                            dis.blit(unkeep4_u, [957, 56])
                                            dis.fill(blk, rect=(955, 220, 80, 180))
                                            dis.blit(another_font_2.render(str(this_roll[4]), True, current_player_color_alt), [979, 56])
                                            k4 = True ; uk4 = True
                                            keep_set[4] = this_roll[4] ; keep_set_col[4] = (0,0,0,0)
                                            dis.fill(blk, rect=(774, 412, 600, 45)) if 0 not in keep_set.values() else None
                                            if "COMPUTER #" in current_player:
                                                time.sleep(0.5) ; pygame.display.update()
                                        if (event3.type == pygame.MOUSEBUTTONUP and keep5.collidepoint(pygame.mouse.get_pos())) or (k5 == False and shake_count < 3 and "COMPUTER #" in current_player and best_option in [5,9,12,14,15,18,20,21,23,24,25,27,28,29,30,31]):
                                            unkeep5_u = small_dice_font.render(dice2[this_roll[5]-1], True, current_player_color_alt)
                                            unkeep5 = unkeep5_u.get_rect()
                                            unkeep5.x, unkeep5.y = 1057,56
                                            dis.blit(unkeep5_u, [1057, 56])
                                            dis.fill(blk, rect=(1055, 220, 80, 180))
                                            dis.blit(another_font_2.render(str(this_roll[5]), True, current_player_color_alt), [1078, 56])
                                            k5 = True ; uk5 = True
                                            keep_set[5] = this_roll[5] ; keep_set_col[5] = (0,0,0,0)
                                            dis.fill(blk, rect=(774, 412, 600, 45)) if 0 not in keep_set.values() else None
                                            if "COMPUTER #" in current_player:
                                                time.sleep(0.5) ; pygame.display.update()

                                        # Unkeep, hover (else clicking)
                                        if uk1:
                                            if unkeep1.collidepoint(pygame.mouse.get_pos()):
                                                unkeep1_u = small_dice_font.render(dice2[this_roll[1]-1], True, blk)
                                                unkeep1_c = small_dice_font.render(dice2[this_roll[1]-1], True, wh)
                                                dis.blit(unkeep1_u, [657, 56]) ; dis.blit(unkeep1_c, [657, 56])
                                                dis.blit(another_font_2.render(str(this_roll[1]), True, wh), [682, 56])
                                            else:
                                                unkeep1_c = small_dice_font.render(dice2[this_roll[1]-1], True, blk)
                                                unkeep1_u = small_dice_font.render(dice2[this_roll[1]-1], True, current_player_color_alt)
                                                dis.blit(unkeep1_c, [657, 56]) ; dis.blit(unkeep1_u, [657, 56])
                                                dis.blit(another_font_2.render(str(this_roll[1]), True, current_player_color_alt), [682, 56])
                                            if (event3.type == pygame.MOUSEBUTTONUP and unkeep1.collidepoint(pygame.mouse.get_pos())) or (k1 and shake_count < 3 and "COMPUTER #" in current_player and best_option not in [1,6,7,8,9,16,17,18,19,20,21,26,27,28,29,31]):
                                                uk1 = False ; k1 = False
                                                dis.fill(blk, rect=(658, 65, 80, 75))
                                                keep_set[1] = 0; keep_set_col[1] = (255,255,255,255)
                                                if "COMPUTER #" in current_player:
                                                    dis.blit(big_dice_font.render(dice2[this_roll[1]-1], True, wh), [648, 230])
                                                    dis.blit(another_font.render(str(this_roll[1]), True, wh), [682, 215])
                                                    time.sleep(0.5) ; pygame.display.update()
                                                pygame.event.post(pygame.event.Event(SHAKECLICK))
                                        if uk2:
                                            if unkeep2.collidepoint(pygame.mouse.get_pos()):
                                                unkeep2_u = small_dice_font.render(dice2[this_roll[2]-1], True, blk)
                                                unkeep2_c = small_dice_font.render(dice2[this_roll[2]-1], True, wh)
                                                dis.blit(unkeep2_u, [757, 56]) ; dis.blit(unkeep2_c, [757, 56])
                                                dis.blit(another_font_2.render(str(this_roll[2]), True, wh), [781, 56])
                                            else:
                                                unkeep2_c = small_dice_font.render(dice2[this_roll[2]-1], True, blk)
                                                unkeep2_u = small_dice_font.render(dice2[this_roll[2]-1], True, current_player_color_alt)
                                                dis.blit(unkeep2_c, [757, 56]) ; dis.blit(unkeep2_u, [757, 56])
                                                dis.blit(another_font_2.render(str(this_roll[2]), True, current_player_color_alt), [781, 56])
                                            if (event3.type == pygame.MOUSEBUTTONUP and unkeep2.collidepoint(pygame.mouse.get_pos())) or (k2 and shake_count < 3 and "COMPUTER #" in current_player and best_option not in [2,6,10,11,12,16,17,18,22,23,24,26,27,28,30,31]):
                                                uk2 = False ; k2 = False
                                                dis.fill(blk, rect=(758, 65, 80, 75))
                                                keep_set[2] = 0; keep_set_col[2] = (255,255,255,255)
                                                if "COMPUTER #" in current_player:
                                                    dis.blit(big_dice_font.render(dice2[this_roll[2]-1], True, wh), [747, 230])
                                                    dis.blit(another_font.render(str(this_roll[2]), True, wh), [781, 215])
                                                    time.sleep(0.5) ; pygame.display.update()
                                                pygame.event.post(pygame.event.Event(SHAKECLICK))
                                        if uk3:
                                            if unkeep3.collidepoint(pygame.mouse.get_pos()):
                                                unkeep3_u = small_dice_font.render(dice2[this_roll[3]-1], True, blk)
                                                unkeep3_c = small_dice_font.render(dice2[this_roll[3]-1], True, wh)
                                                dis.blit(unkeep3_u, [857, 56]) ; dis.blit(unkeep3_c, [857, 56])
                                                dis.blit(another_font_2.render(str(this_roll[3]), True, wh), [880, 56])
                                            else:
                                                unkeep3_c = small_dice_font.render(dice2[this_roll[3]-1], True, blk)
                                                unkeep3_u = small_dice_font.render(dice2[this_roll[3]-1], True, current_player_color_alt)
                                                dis.blit(unkeep3_c, [857, 56]) ; dis.blit(unkeep3_u, [857, 56])
                                                dis.blit(another_font_2.render(str(this_roll[3]), True, current_player_color_alt), [880, 56])
                                            if (event3.type == pygame.MOUSEBUTTONUP and unkeep3.collidepoint(pygame.mouse.get_pos())) or (k3 and shake_count < 3 and "COMPUTER #" in current_player and best_option not in [3,7,10,13,14,16,19,20,22,23,25,26,27,29,30,31]):
                                                uk3 = False ; k3 = False
                                                dis.fill(blk, rect=(858, 65, 80, 75))
                                                keep_set[3] = 0; keep_set_col[3] = (255,255,255,255)
                                                if "COMPUTER #" in current_player:
                                                    dis.blit(big_dice_font.render(dice2[this_roll[3]-1], True, wh), [846, 230])
                                                    dis.blit(another_font.render(str(this_roll[3]), True, wh), [880, 215])
                                                    time.sleep(0.5) ; pygame.display.update()
                                                pygame.event.post(pygame.event.Event(SHAKECLICK))
                                        if uk4:
                                            if unkeep4.collidepoint(pygame.mouse.get_pos()):
                                                unkeep4_u = small_dice_font.render(dice2[this_roll[4]-1], True, blk)
                                                unkeep4_c = small_dice_font.render(dice2[this_roll[4]-1], True, wh)
                                                dis.blit(unkeep4_u, [957, 56]) ; dis.blit(unkeep4_c, [957, 56])
                                                dis.blit(another_font_2.render(str(this_roll[4]), True, wh), [979, 56])
                                            else:
                                                unkeep4_c = small_dice_font.render(dice2[this_roll[4]-1], True, blk)
                                                unkeep4_u = small_dice_font.render(dice2[this_roll[4]-1], True, current_player_color_alt)
                                                dis.blit(unkeep4_c, [957, 56]) ; dis.blit(unkeep4_u, [957, 56])
                                                dis.blit(another_font_2.render(str(this_roll[4]), True, current_player_color_alt), [979, 56])
                                            if (event3.type == pygame.MOUSEBUTTONUP and unkeep4.collidepoint(pygame.mouse.get_pos())) or (k4 and shake_count < 3 and "COMPUTER #" in current_player and best_option not in [4,8,11,13,15,17,19,21,22,24,25,26,28,29,30,31]):
                                                uk4 = False ; k4 = False
                                                dis.fill(blk, rect=(958, 65, 80, 75))
                                                keep_set[4] = 0; keep_set_col[4] = (255,255,255,255)
                                                if "COMPUTER #" in current_player:
                                                    dis.blit(big_dice_font.render(dice2[this_roll[4]-1], True, wh), [945, 230])
                                                    dis.blit(another_font.render(str(this_roll[4]), True, wh), [979, 215])
                                                    time.sleep(0.5) ; pygame.display.update()
                                                pygame.event.post(pygame.event.Event(SHAKECLICK))
                                        if uk5:
                                            if unkeep5.collidepoint(pygame.mouse.get_pos()):
                                                unkeep5_u = small_dice_font.render(dice2[this_roll[5]-1], True, blk)
                                                unkeep5_c = small_dice_font.render(dice2[this_roll[5]-1], True, wh)
                                                dis.blit(unkeep5_u, [1057, 56]) ; dis.blit(unkeep5_c, [1057, 56])
                                                dis.blit(another_font_2.render(str(this_roll[5]), True, wh), [1078, 56])
                                            else:
                                                unkeep5_c = small_dice_font.render(dice2[this_roll[5]-1], True, blk)
                                                unkeep5_u = small_dice_font.render(dice2[this_roll[5]-1], True, current_player_color_alt)
                                                dis.blit(unkeep5_c, [1057, 56]) ; dis.blit(unkeep5_u, [1057, 56])
                                                dis.blit(another_font_2.render(str(this_roll[5]), True, current_player_color_alt), [1078, 56])
                                            if (event3.type == pygame.MOUSEBUTTONUP and unkeep5.collidepoint(pygame.mouse.get_pos())) or (k5 and shake_count < 3 and "COMPUTER #" in current_player and best_option not in [5,9,12,14,15,18,20,21,23,24,25,27,28,29,30,31]):
                                                uk5 = False ; k5 = False
                                                dis.fill(blk, rect=(1058, 65, 80, 75))
                                                keep_set[5] = 0; keep_set_col[5] = (255,255,255,255)
                                                if "COMPUTER #" in current_player:
                                                    dis.blit(big_dice_font.render(dice2[this_roll[5]-1], True, wh), [1044, 230])
                                                    dis.blit(another_font.render(str(this_roll[5]), True, wh), [1078, 215])
                                                    time.sleep(0.5) ; pygame.display.update()
                                                pygame.event.post(pygame.event.Event(SHAKECLICK))
                                            
                                        # Shake again
                                        if (event3.type == pygame.MOUSEBUTTONUP and t_shake2.collidepoint(pygame.mouse.get_pos()) and 0 in keep_set.values() and shake_count < 3) or (0 in keep_set.values() and shake_count < 3 and "COMPUTER #" in current_player and best_option != 31):
                                            if "COMPUTER #" in current_player:
                                                simulate = True
                                                dis.fill(blk, rect=(774, 412, 600, 45))
                                                pygame.event.clear()
                                                pygame.display.update() ; time.sleep(1.75)
                                            loop3 = False ; anim_count = 0 ; shake_count += 1
                                            dis.fill(blk, rect=(600, 200, 600, 475))
                                            dis.fill(blk, rect=(1050, 650, 150, 175))
                                            dis.blit(small_dice_font.render("-", True, current_player_color), [1065, 614+((shake_count-1)*25.5)])
                                            if shake_count == 2:
                                                dis.blit(shake_font.render("Shake #1", True, gr), [1100, 665])
                                                dis.blit(shake_font.render("Shake #2", True, current_player_color), [1100, 690])
                                                dis.blit(shake_font.render("Shake #3", True, gr), [1100, 715])
                                            if shake_count == 3:
                                                dis.blit(shake_font.render("Shake #1", True, gr), [1100, 665])
                                                dis.blit(shake_font.render("Shake #2", True, gr), [1100, 690])
                                                dis.blit(shake_font.render("Shake #3", True, current_player_color), [1100, 715])
                                            if "COMPUTER #" in current_player:
                                                pygame.event.clear()
                                                break;
                                            
                                        # New calculations and displaying (if choosing to score) for the appropriate player
                                        correct = -1 ; bone = True
                                        for rect in list(S_DICT_RECT.values()):
                                            correct += 1
                                            position = [645+((math.floor(correct/3))*(205-(math.floor(correct/6)*15))), 513+((correct%3)*32)]
                                            if (event3.type == pygame.MOUSEBUTTONUP and rect.collidepoint(pygame.mouse.get_pos())) or ("COMPUTER #" in current_player and shake_count == 3) or ("COMPUTER #" in current_player and best_option == 31):
                                                if "COMPUTER #" in current_player:
                                                    # Choose highest scoring option (usually)
                                                    if max(S_SCORE_LIST) < 9:
                                                        correct = S_SCORE_LIST.index(min(S_SCORE_LIST))
                                                    else:
                                                        correct = S_SCORE_LIST.index(max(S_SCORE_LIST))
                                                    dis.fill(blk, rect=(774, 412, 600, 45))
                                                    pygame.display.update() ; time.sleep(1.75)
                                                    pygame.event.clear()
                                                for i in range(0,len(MD_FILLS)):
                                                    dis.fill(blk, rect = MD_FILLS[i])
                                                if isinstance(S_SCORE_LIST[correct], float) and S_THING_LIST[correct] in ['one', 'two', 'three']:
                                                    S_SCORE_LIST[correct] = round((S_SCORE_LIST[correct]/1.4)/1.4)
                                                elif isinstance(S_SCORE_LIST[correct], float):
                                                    S_SCORE_LIST[correct] = round(S_SCORE_LIST[correct]/1.4)
                                                yb1 = 0 ; yb2 = 0 ; yb3 = 0 ; bb = 0
                                                if S_SCORE_LIST[correct] == 100:
                                                    curr_MD[current_player_alt+"_"+games_list[game-1]+"_"+S_THING_LIST[correct]] = "\u2713"
                                                else:
                                                    curr_MD[current_player_alt+"_"+games_list[game-1]+"_"+S_THING_LIST[correct]] = S_SCORE_LIST[correct]
                                                yb1 = 100 if curr_MD[current_player_alt+"_"+games_list[game-1]+"_YB1"] != "" else yb1                                           
                                                yb2 = 100 if curr_MD[current_player_alt+"_"+games_list[game-1]+"_YB2"] != "" else yb2
                                                yb3 = 100 if curr_MD[current_player_alt+"_"+games_list[game-1]+"_YB3"] != "" else yb3
                                                curr_MD[current_player_alt+"_"+games_list[game-1]+"_TotalLower"] = yb1 + yb2 + yb3 + sum(filter(lambda i: isinstance(i, int), list(curr_MD.values())[((game-1)*21+6):((game-1)*21+13)]))
                                                curr_MD[current_player_alt+"_"+games_list[game-1]+"_GRAND"] = yb1 + yb2 + yb3 + sum(filter(lambda i: isinstance(i, int), list(curr_MD.values())[((game-1)*21+0):((game-1)*21+13)]))
                                                curr_MD[current_player_alt+"_"+games_list[game-1]+"_TotalUpper1"] = sum(filter(lambda i: isinstance(i, int), list(curr_MD.values())[((game-1)*21+0):((game-1)*21+6)]))
                                                curr_MD[current_player_alt+"_"+games_list[game-1]+"_TotalUpper2"] = sum(filter(lambda i: isinstance(i, int), list(curr_MD.values())[((game-1)*21+0):((game-1)*21+6)]))                                            
                                                if curr_MD[current_player_alt+"_"+games_list[game-1]+"_TotalUpper1"] >= 63 and '' not in list(curr_MD.values())[((game-1)*21+0):((game-1)*21+6)] and bone:
                                                    bone = False
                                                    curr_MD[current_player_alt+"_"+games_list[game-1]+"_Bonus"] = 35
                                                    curr_MD[current_player_alt+"_"+games_list[game-1]+"_TotalUpper2"] += 35
                                                    curr_MD[current_player_alt+"_"+games_list[game-1]+"_GRAND"] += 35
                                                elif curr_MD[current_player_alt+"_"+games_list[game-1]+"_TotalUpper1"] < 63 and '' not in list(curr_MD.values())[((game-1)*21+0):((game-1)*21+6)] and bone:
                                                    bone = False
                                                    curr_MD[current_player_alt+"_"+games_list[game-1]+"_Bonus"] = 0
                                                player_scores[player_names.index(current_player)] = curr_MD[current_player_alt+"_"+games_list[game-1]+"_GRAND"]
                                                for i in range(0,len(MD_WRITES)):
                                                    center_text = sc_dice_font_2.render(str(list(curr_MD.values())[i]), True, current_player_color)
                                                    dis.blit(center_text,center_text.get_rect(center=MD_WRITES[i]))
                                                dis.fill(blk, rect=(600, 360, 600, 305))
                                                if S_SCORE_LIST[correct] == 1:
                                                    center_text = welcome_font_1.render(str(current_player) + ", you scored " + str(S_SCORE_LIST[correct]) + " point!", True, current_player_color)
                                                else:
                                                    center_text = welcome_font_1.render(str(current_player) + ", you scored " + str(S_SCORE_LIST[correct]) + " points!", True, current_player_color)
                                                dis.blit(center_text,center_text.get_rect(center=(900, 525)))
                                                center_text = player_font_2.render("(" + S_DISP_LIST[correct].split(":")[0] + ")", True, current_player_color)
                                                dis.blit(center_text,center_text.get_rect(center=(900, 555)))
                                                dis.fill(blk, rect=(295, 26, 1000, 14))
                                                v_align = 1

                                                # Re-assign curr_MD to global dictionary
                                                if current_player_alt == "p1":
                                                    MD1 = curr_MD
                                                elif current_player_alt == "p2":
                                                    MD2 = curr_MD
                                                elif current_player_alt == "p3":
                                                    MD3 = curr_MD
                                                elif current_player_alt == "p4":
                                                    MD4 = curr_MD
                                                
                                                # Reset players scores at top (if more than one player/CPU)
                                                for po in list(PLAYER_ORDER.keys()):
                                                    if player_scores[player_names.index(po)] == 1:
                                                        center_text = player_font.render(str(player_scores[player_names.index(po)]) + " Point", True, p_colors_alt[player_names.index(po)])
                                                    else:
                                                        center_text = player_font.render(str(player_scores[player_names.index(po)]) + " Points", True, p_colors_alt[player_names.index(po)])
                                                    dis.blit(center_text,center_text.get_rect(center=(300 + 200*v_align, 30)))
                                                    v_align += 1
                                                pygame.display.update()
                                                time.sleep(1.25)

                                                # Wait for user to view and move on from scoring results page
                                                contin_u = click_font_5.render("Continue ->", True, wh)
                                                contin = contin_u.get_rect()
                                                contin.x, contin.y = 840,602
                                                dis.blit(contin_u, [840, 602])
                                                pygame.display.update()
                                                loop4 = True
                                                while loop4:
                                                    for event4 in pygame.event.get():
                                                        if event4.type == pygame.QUIT:
                                                            loop4 = False ; pygame.quit() ; sys.exit()
                                                            
                                                        # Rulebook click option (still...)
                                                        if r.collidepoint(pygame.mouse.get_pos()):
                                                            dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (255, 150, 150), (499, 717, 87, 25), 2)
                                                            rules_c = rule_font_1.render("Rulebook", True, (255, 150, 150))
                                                            dis.blit(rules_c, [505, 718])
                                                        else:
                                                            dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
                                                            rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
                                                            dis.blit(rules_u, [505, 718]) 
                                                        if event4.type == pygame.MOUSEBUTTONUP and r.collidepoint(pygame.mouse.get_pos()):
                                                            webbrowser.open(r"https://www.hasbro.com/common/instruct/Yahtzee.pdf")
                                                            
                                                        if contin.collidepoint(pygame.mouse.get_pos()):
                                                            dis.fill(blk, rect=(840, 602, 130, 40))
                                                            contin_c = click_font_6.render("Continue ->", True, red)
                                                            dis.blit(contin_c, [840, 602])
                                                        else:
                                                            dis.fill(blk, rect=(840, 602, 130, 40))
                                                            contin_u = click_font_5.render("Continue ->", True, wh)
                                                            dis.blit(contin_u, [840, 602])
                                                            
                                                        if event4.type == pygame.MOUSEBUTTONUP and contin.collidepoint(pygame.mouse.get_pos()):
                                                            simulate = True
                                                            loop4 = False
                                                        pygame.display.update()
                                                
                                                # Check if no more possible turns and restrict that player from continuing
                                                if '' not in list(curr_MD.values())[((game-1)*21+0):((game-1)*21+13)]:
                                                    player_outofturns[player_names.index(current_player)] = True

                                                # Prepare board and logic for next player
                                                loop2 = False; loop3 = False ; new_turn = True
                                                anim_count = 0 ; shake_count = 1
                                                pc += 1
                                                current_player = player_names[0] if num_players == 1 else list(PLAYER_ORDER.keys())[pc % num_players]
                                                current_player_alt = str("p" + str(player_names.index(current_player)+1))
                                                current_player_color = p_colors[player_names.index(current_player)]
                                                current_player_color_alt = p_colors_alt[player_names.index(current_player)]
                                                this_roll = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}; keep_set = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                                                keep_set_col = {1: (255,255,255,255), 2: (255,255,255,255), 3: (255,255,255,255), 4: (255,255,255,255), 5: (255,255,255,255)}
                                                k1 = False ; k2 = False; k3 = False; k4 = False; k5 = False
                                                uk1 = False ; uk2 = False; uk3 = False; uk4 = False; uk5 = False

                                                # Replace scoreboard with new player's board
                                                for i in range(0,len(MD_FILLS)):
                                                    dis.fill(blk, rect = MD_FILLS[i])
                                                for i in range(0,len(MD_WRITES)):
                                                    if current_player_alt == "p1":
                                                        curr_MD = MD1
                                                        center_text = sc_dice_font_2.render(str(list(MD1.values())[i]), True, current_player_color)
                                                    elif current_player_alt == "p2":
                                                        curr_MD = MD2
                                                        center_text = sc_dice_font_2.render(str(list(MD2.values())[i]), True, current_player_color)
                                                    elif current_player_alt == "p3":
                                                        curr_MD = MD3
                                                        center_text = sc_dice_font_2.render(str(list(MD3.values())[i]), True, current_player_color)
                                                    elif current_player_alt == "p4":
                                                        curr_MD = MD4
                                                        center_text = sc_dice_font_2.render(str(list(MD4.values())[i]), True, current_player_color)
                                                    dis.blit(center_text,center_text.get_rect(center=MD_WRITES[i]))
                                                    
                                                dis.fill(blk, rect=(628, 65, 600, 605)) ; dis.fill(blk, rect=(415, 56, 150, 22)) ; dis.fill(blk, rect=(1050, 650, 45, 150))
                                                dis.blit(click_font_1.render(current_player, True, current_player_color), [417, 56])
                                                dis.blit(small_dice_font.render("__", True, current_player_color), [655, 50])
                                                dis.blit(small_dice_font.render("__", True, current_player_color), [755, 50])
                                                dis.blit(small_dice_font.render("__", True, current_player_color), [855, 50])
                                                dis.blit(small_dice_font.render("__", True, current_player_color), [955, 50])
                                                dis.blit(small_dice_font.render("__", True, current_player_color), [1055, 50])
                                                dis.blit(sc_dice_font.render(" |                                                                                                |", True, current_player_color), [638, 150])
                                                dis.blit(sc_dice_font.render("   -  -  -  -  -  -  Your Saved Dice (click to remove)  -  -  -  -  -  -   ", True, current_player_color), [640, 160])

                                                pygame.display.update()
                                                
                                                if best_option == 31:
                                                   pygame.event.clear() 
                                                   break;
                                            
                                        if loop3 == False and loop4 == False:
                                            pygame.event.clear()
                                            break;
                                                
                                    if "COMPUTER #" in current_player:
                                        pygame.event.post(pygame.event.Event(SHAKECLICK))
    
                                    pygame.display.update()
                        
                            if loop3 == False and loop4 == False:
                                pygame.event.clear()
                                break;
                        
                        pygame.display.update()
                else:
                    dis.fill(blk, rect=(592, 100, 650, 552))
                    center_text = welcome_font_1.render("No more turns for you, " + str(current_player) + "!", True, wh)
                    dis.blit(center_text,center_text.get_rect(center=[900, 450]))
                    l = True ; a = 0
                    while l and a < 2201:
                        for event5 in pygame.event.get():
                            if event5.type == pygame.QUIT:
                                l = False ; pygame.quit() ; sys.exit()

                            # Rulebook click option
                            if r.collidepoint(pygame.mouse.get_pos()):
                                dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (255, 150, 150), (499, 717, 87, 25), 2)
                                rules_c = rule_font_1.render("Rulebook", True, (255, 150, 150))
                                dis.blit(rules_c, [505, 718])
                            else:
                                dis.fill(blk, rect=(505, 718, 80, 50)) ; pygame.draw.rect(dis, (150, 150, 255), (499, 717, 87, 25), 2)
                                rules_u = rule_font_1.render("Rulebook", True, (150, 150, 255))
                                dis.blit(rules_u, [505, 718]) 
                            if event5.type == pygame.MOUSEBUTTONUP and r.collidepoint(pygame.mouse.get_pos()):
                                webbrowser.open(r"https://www.hasbro.com/common/instruct/Yahtzee.pdf")
                        a += 1
                        pygame.display.update()
                                
                    # Re-reset board
                    anim_count = 0 ; shake_count = 1 ; new_turn = True
                    pc += 1
                    current_player = player_names[0] if num_players == 1 else list(PLAYER_ORDER.keys())[pc % num_players]
                    current_player_alt = str("p" + str(player_names.index(current_player)+1))
                    current_player_color = p_colors[player_names.index(current_player)]
                    current_player_color_alt = p_colors_alt[player_names.index(current_player)]
                    for i in range(0,len(MD_FILLS)):
                        dis.fill(blk, rect = MD_FILLS[i])
                    for i in range(0,len(MD_WRITES)):
                        if current_player_alt == "p1":
                            curr_MD = MD1
                            center_text = sc_dice_font_2.render(str(list(MD1.values())[i]), True, current_player_color)
                        elif current_player_alt == "p2":
                            curr_MD = MD2
                            center_text = sc_dice_font_2.render(str(list(MD2.values())[i]), True, current_player_color)
                        elif current_player_alt == "p3":
                            curr_MD = MD3
                            center_text = sc_dice_font_2.render(str(list(MD3.values())[i]), True, current_player_color)
                        elif current_player_alt == "p4":
                            curr_MD = MD4
                            center_text = sc_dice_font_2.render(str(list(MD4.values())[i]), True, current_player_color)
                        dis.blit(center_text,center_text.get_rect(center=MD_WRITES[i]))
                       
                    dis.fill(blk, rect=(628, 65, 600, 605)) ; dis.fill(blk, rect=(415, 56, 150, 22)) ; dis.fill(blk, rect=(1050, 650, 45, 150))
                    dis.blit(click_font_1.render(current_player, True, current_player_color), [417, 56])
                    dis.blit(small_dice_font.render("__", True, current_player_color), [655, 50])
                    dis.blit(small_dice_font.render("__", True, current_player_color), [755, 50])
                    dis.blit(small_dice_font.render("__", True, current_player_color), [855, 50])
                    dis.blit(small_dice_font.render("__", True, current_player_color), [955, 50])
                    dis.blit(small_dice_font.render("__", True, current_player_color), [1055, 50])
                    dis.blit(sc_dice_font.render(" |                                                                                                |", True, current_player_color), [638, 150])
                    dis.blit(sc_dice_font.render("   -  -  -  -  -  -  Your Saved Dice (click to remove)  -  -  -  -  -  -   ", True, current_player_color), [640, 160])

                    dis.blit(click_font_1.render(current_player, True, current_player_color), [417, 56])
                    scorecard = "************************************************************************************************"
                    dis.fill(blk, rect=(10, 88, 580, 9)) ; dis.fill(blk, rect=(10, 706, 580, 9))
                    dis.fill(blk, rect=(8, 88, 9, 629)) ; dis.fill(blk, rect=(580, 88, 9, 629))
                    dis.blit(sc_font.render(scorecard, True, current_player_color), [11, 84])
                    dis.blit(sc_font.render(scorecard, True, current_player_color), [13, 700])
                    scorecard = "    _____________________      __________________     ____________     ____________     ____________"
                    ty = [85,90,350,355,360,365,639.5,644.5,649.5,654.5]
                    for i in ty:
                        dis.blit(sc_font.render(scorecard, True, current_player_color), [15, i])
                    dis.fill(blk, rect=(15, 97.5, 15, 608)) ; dis.fill(blk, rect=(162.5, 97.5, 15, 608))
                    dis.fill(blk, rect=(292.5, 97.5, 15, 608)) ; dis.fill(blk, rect=(384, 97.5, 15, 608))
                    dis.fill(blk, rect=(475.5, 97.5, 15, 608)) ; dis.fill(blk, rect=(567, 97.5, 15, 608))
                    for s in range(1,42):
                        value = sc_font.render(" ||", True, current_player_color)
                        if s < 20 or s > 21:
                            if s < 41:
                                dis.blit(value, [15, 82.5 + s*15]) ; dis.blit(value, [162.5, 82.5 + s*15])
                                dis.blit(value, [292.5, 82.5 + s*15]) ; dis.blit(value, [384, 82.5 + s*15])
                                dis.blit(value, [475.5, 82.5 + s*15]) ; dis.blit(value, [567, 82.5 + s*15])
                        value = sc_font.render("*", True, current_player_color)
                        dis.blit(value, [10, 77.5 + s*15]) ; dis.blit(value, [10, 85 + s*15])
                        dis.blit(value, [582, 77.5 + s*15]) ; dis.blit(value, [582, 85 + s*15])

                    dis.fill(blk, rect=(1060, 612, 150, 150))
                    dis.blit(small_dice_font.render("-", True, current_player_color), [1065, 614])
                    dis.blit(shake_font.render("Shake #1", True, current_player_color), [1100, 665])
                    dis.blit(shake_font.render("Shake #2", True, gr), [1100, 690])
                    dis.blit(shake_font.render("Shake #3", True, gr), [1100, 715])
                        
                    pygame.display.update()
            pygame.display.update()
                
            # End the game! All players exhaust their turns   
            if False not in player_outofturns:
                dis.fill(blk, rect=(592, 100, 650, 552)) ; dis.fill(blk, rect=(415, 56, 150, 22))
                dis.fill(blk, rect=(1060, 612, 150, 150)) ; dis.fill(blk, rect=(490, 712, 500, 50))
                center_text = pygame.font.SysFont("cambria", 36).render("Game #" + str(game) + " Over!", True, wh)
                dis.blit(center_text,center_text.get_rect(center=[900, 160]))
                pygame.display.update()

                # If anyone is tied, have a roll off
                if len(player_scores) != len(set(player_scores)) and 0 not in player_scores:
                    time.sleep(2)
                    center_text = pygame.font.SysFont("cambria", 36).render("We have a tie!", True, wh)
                    dis.blit(center_text,center_text.get_rect(center=[900, 215]))
                    pygame.display.update() ; time.sleep(2)

                    # Which players are tied?
                    ties = [] ; tie_names1 = [] ; tie_names2 = [] ; aand = ""
                    for w in range(0,600):
                        t = [i for i, x in enumerate(player_scores) if x == w]
                        if len(t) > 1:
                            ties.append(t)
                    if len(ties) > 0:
                        for w in range(0,len(ties[0])):
                            tie_names1.append(player_names[ties[0][w]])
                        if len(ties) > 1:
                            aand = " and "
                            for w in range(0,len(ties[1])):
                                tie_names2.append(player_names[ties[1][w]])
                    for w in range(0,len(ties)):
                        loop7 = True ; apass = True ; out = True
                        i = 0 ; first = 1; last = 1
                        repeats2 = [] ; repeats_temp2 = [] ; f2 = {}
                        PLAYER_ORDER = {}
                        count = ""
                        if w == 0 and len(ties) >= 1:
                            tie_text = pygame.font.SysFont("cambria", 21).render("Tiebreaker #1! (" + ', '.join(tie_names1) + ")", True, wh)
                        elif w == 1 and len(ties) >= 1:
                            tie_text = pygame.font.SysFont("cambria", 21).render("Tiebreaker #2! (" + ', '.join(tie_names2) + ")", True, wh)
                        else:
                            tie_text = pygame.font.SysFont("cambria", 21).render("Tiebreaker! (" + ', '.join(tie_names1) + ")", True, wh)
                        dis.blit(tie_text,tie_text.get_rect(center=(892, 400)))
                        center_text = welcome_font_1.render(str(player_names[ties[w][i]]) + ":", True, p_colors[ties[w][i]])
                        dis.blit(center_text,center_text.get_rect(center=(892, 475)))
                        dis.blit(welcome_font_1.render("Highest roll wins the tiebreaker!", True, wh), [685, 500])
                        t_roll_u = click_font_3.render("ROLL", True, wh)
                        t_roll = t_roll_u.get_rect()
                        t_roll.x, t_roll.y = 850,590
                        dis.blit(t_roll_u, [850, 590])
                        dis.blit(big_dice_font.render(dice2[first], True, wh), [738, 225])
                        dis.blit(big_dice_font.render(dice2[last], True, wh), [972, 225])
                        pygame.display.update()
                        while loop7:
                            if len(ties[w]) > i:
                                pygame.event.post(pygame.event.Event(COMPCLICK)) if "COMPUTER #" in player_names[ties[w][i]] else None
     
                            for event7 in pygame.event.get():
                                if event7.type == pygame.QUIT:
                                    loop7 = False ; pygame.quit() ; sys.exit()

                                if out:
                                    if t_roll.collidepoint(pygame.mouse.get_pos()):
                                        dis.fill(blk, rect=(793, 590, 600, 45))
                                        t_roll_c = click_font_4.render("ROLL" + str(count), True, red)
                                        dis.blit(t_roll_c, [835 - len(count)*6.5, 587.5])
                                        if cq:
                                            if len(count) < 6:
                                                count = str(count) + "!"
                                            else:
                                                dis.blit(sc_name_font.render("Seriously? Just click it.", True, wh), [828, 641])  
                                        cq = False
                                    else:
                                        dis.fill(blk, rect=(793, 590, 600, 45))
                                        t_roll_u = click_font_3.render("ROLL", True, wh)
                                        dis.blit(t_roll_u, [850, 590])
                                        cq = True
                                
                                # Dice rolling animation
                                    if event7.type == pygame.MOUSEBUTTONUP and t_roll.collidepoint(pygame.mouse.get_pos()) or event7.type == COMPCLICK:
                                        if event7.type == COMPCLICK:
                                            dis.fill(blk, rect=(793, 590, 600, 45)) ; time.sleep(1)
                                        count = ""
                                        anim_count = random.randint(16,25)
                                        dis.fill(blk, rect=(592, 40, 580, 350)) ; dis.fill(blk, rect=(630, 600, 580, 35)) ; dis.fill(blk, rect=(800, 630, 580, 35))
                                        while anim_count > 0:
                                            dis.fill(blk, rect=(592, 40, 580, 350))
                                            dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(75,135)).render(dice2[random.randint(0,5)], True, wh),
                                                     [random.randint(640,830), random.randint(160,240)])
                                            dis.blit(pygame.font.SysFont("segoeuisymbol", random.randint(75,135)).render(dice2[random.randint(0,5)], True, wh),
                                                     [random.randint(850,1050), random.randint(160,240)])
                                            pygame.display.flip()
                                            anim_count -= 1
                                            time.sleep(.055)
                                        if anim_count == 0:
                                            first = random.randint(0,5) ; last = random.randint(0,5)
                                            dis.fill(blk, rect=(592, 40, 580, 350)) ; dis.fill(blk, rect=(630, 460, 580, 180))
                                            dis.blit(big_dice_font.render(dice2[first], True, wh), [728, 225])
                                            dis.blit(big_dice_font.render(dice2[last], True, wh), [952, 225])
                                            center_text = welcome_font_1.render(str(player_names[ties[w][i]]) + ":", True, p_colors[ties[w][i]])
                                            dis.blit(center_text,center_text.get_rect(center=(892, 450)))
                                            dis.blit(welcome_font_1.render("You rolled " + str(first+last+2) + ".", True, wh), [810, 475])
                                            pygame.display.flip()
                                            time.sleep(2.25)
                                            dis.fill(blk, rect=(630, 415, 680, 220))
                                            if len(ties[w]) > i+1 and len(f) == 0:
                                                center_text = welcome_font_1.render(str(player_names[ties[w][i+1]]) + ":", True, p_colors[ties[w][i+1]])
                                                dis.blit(center_text,center_text.get_rect(center=(892, 475)))
                                                dis.blit(welcome_font_1.render("Highest roll wins the tiebreaker!", True, wh), [690, 500])
                                                dis.blit(t_roll_u, [850, 590])
                                            if i == 0:
                                                dis.fill(blk, rect=(600, 650, 210, 20))
                                                dis.blit(player_font_2.render(str(player_names[ties[w][i]] + ": " + str(first+last+2)), True, p_colors[ties[w][i]]), [600, 650])
                                            elif i == 1:
                                                dis.fill(blk, rect=(600, 672, 210, 20))
                                                dis.blit(player_font_2.render(str(player_names[ties[w][i]] + ": " + str(first+last+2)), True, p_colors[ties[w][i]]), [600, 672])
                                            elif i == 2:
                                                dis.fill(blk, rect=(600, 694, 210, 20))
                                                dis.blit(player_font_2.render(str(player_names[ties[w][i]] + ": " + str(first+last+2)), True, p_colors[ties[w][i]]), [600, 694])
                                            elif i == 3:
                                                dis.fill(blk, rect=(600, 716, 210, 20))
                                                dis.blit(player_font_2.render(str(player_names[ties[w][i]] + ": " + str(first+last+2)), True, p_colors[ties[w][i]]), [600, 716])
                                            PLAYER_ORDER[player_names[ties[w][i]]]= first+last+2
                                            
                                        # Determining ties based on roll results
                                        if len(repeats2) == 0 and len(f2) != 0:
                                            i = len(ties[w])
                                        elif len(f2) != 0:
                                            repeats2.pop(0)
                                            i = len(ties[w]) if len(repeats2) == 0 else repeats2[0] - 1
                                        else:
                                            i += 1
                                                
                                        if len(ties[w]) == i:
                                            f2 = {}
                                            repeats2 = []
                                            it = list(set(PLAYER_ORDER.values()))
                                            for k, v in PLAYER_ORDER.items():
                                                if v not in f2:
                                                    f2[v] = [k]
                                                else:
                                                    f2[v].append(k)
                                            for j in range(0,len(it)):
                                                if len(f2[it[j]]) > 1:
                                                    for k in range(0,len(f2[it[j]])):
                                                       repeats2.append(1+player_names.index(f2[it[j]][k]))
                                                    i = repeats2[0] - 1
                                                    repeats_temp2 = repeats2.copy()

                                        # Display and update scores accordingly
                                        if len(f2) != 0 and len(repeats2) > 0:
                                            dis.fill(blk, rect=(592, 390, 600, 195))
                                            i = 0 ; first = 1; last = 1
                                            repeats2 = [] ; repeats_temp2 = [] ; f2 = {}
                                            PLAYER_ORDER = {}
                                            count = ""
                                            center_text = welcome_font_1.render(str(player_names[ties[w][i]]) + ":", True, p_colors[ties[w][i]])
                                            dis.blit(center_text,center_text.get_rect(center=(890, 475)))
                                            if w == 0 and len(ties) >= 1:
                                                tie_text = pygame.font.SysFont("cambria", 21).render("Still a tie! (" + ', '.join(tie_names1) + ")", True, wh)
                                            elif w == 1 and len(ties) >= 1:
                                                tie_text = pygame.font.SysFont("cambria", 21).render("Still a tie! (" + ', '.join(tie_names2) + ")", True, wh)
                                            else:
                                                tie_text = pygame.font.SysFont("cambria", 21).render("Still a tie! (" + ', '.join(tie_names1) + ")", True, wh)
                                            dis.blit(tie_text,tie_text.get_rect(center=(890, 400)))
                                            dis.blit(welcome_font_1.render("Highest roll wins the tiebreaker!", True, wh), [690, 500])
                                            dis.blit(t_roll_u, [850, 590])
                                        elif len(f2) != 0 and len(repeats2) == 0:
                                            dis.fill(blk, rect=(592, 360, 600, 400))
                                            dis.fill(blk, rect=(400, 1, 800, 40))
                                            if len(ties) > 1:
                                                dis.blit(welcome_font_1.render("Done! Tiebreaker #" + str(w+1) + " results:", True, wh), [720, 455])
                                            else:
                                                dis.blit(welcome_font_1.render("Done! Tiebreaker results:", True, wh), [736, 455])
                                            v_align = 1 ; out = False
                                            while len(f2) > 0:
                                                popped = str(f2.pop(max(f2))).replace("[","").replace("]","").replace("'","")
                                                center_text = welcome_font_1.render(popped + ": " + str(player_scores[player_names.index(popped)]) +
                                                                                        " + " + str((len(ties[w]) - v_align)*.1) + " = " +
                                                                                        str(player_scores[player_names.index(popped)]+((len(ties[w])-v_align)*.1)) + " pts.",
                                                                                        True, p_colors[player_names.index(popped)])
                                                dis.blit(center_text,center_text.get_rect(center=(900, 475 + (v_align*45))))
                                                player_scores[player_names.index(popped)] += (len(ties[w]) - v_align)*.1
                                                v_align += 1
                                            contin_u = click_font_1.render("Continue ->", True, wh)
                                            contin = contin_u.get_rect()
                                            contin.x, contin.y = 1050,695
                                            dis.blit(contin_u, [1050, 695])
                                # Wait for user to view and move on from turn order results
                                else:
                                    contin_u = click_font_1.render("Continue ->", True, wh)
                                    contin = contin_u.get_rect()
                                    contin.x, contin.y = 1050,695
                                    dis.blit(contin_u, [1050, 695])
                                    if contin.collidepoint(pygame.mouse.get_pos()):
                                        dis.fill(blk, rect=(1050, 695, 200, 200))
                                        contin_c = click_font_2.render("Continue ->", True, red)
                                        dis.blit(contin_c, [1050, 695])
                                    else:
                                        dis.fill(blk, rect=(1050, 695, 200, 200))
                                        contin_u = click_font_1.render("Continue ->", True, wh)
                                        dis.blit(contin_u, [1050, 695]) 
                                    if event7.type == pygame.MOUSEBUTTONUP and contin.collidepoint(pygame.mouse.get_pos()):
                                        dis.fill(blk, rect=(595, 40, 1000, 1000))
                                        loop7 = False 
                            pygame.display.update()
      
                pygame.display.update()
                # Show standings after all ties eliminated
                dis.fill(blk, rect=(592, 100, 650, 552))
                center_text = pygame.font.SysFont("cambria", 36).render("Game #" + str(game) + " Over!", True, wh)
                dis.blit(center_text,center_text.get_rect(center=[900, 175]))
                v_align = 1 ; rank = 1
                p_score_for_determ = player_scores.copy()
                for n in range(0,num_players):
                    if num_players != 1:
                        popped_player = player_scores.index(max(p_score_for_determ))
                        popped_score = player_scores[popped_player]
                        popped_name = player_names[popped_player]
                        p_score_for_determ.pop(p_score_for_determ.index(max(p_score_for_determ)))
                        if popped_name != "":
                            center_text = welcome_font_1.render(str(rank) + ".) " + str(popped_name) + " (" + str(popped_score) + " Points)", True, p_colors[player_names.index(popped_name)])
                            dis.blit(center_text,center_text.get_rect(center=(900, 240 + (v_align*45))))
                    else:
                        center_text = welcome_font_1.render(str(player1) + ": " + str(player_scores[0]) + " Points", True, p_colors[0])
                        dis.blit(center_text,center_text.get_rect(center=(900, 240 + (v_align*45))))   
                    v_align += 1 if v_align != 1 else 2
                    rank += 1

                dis.blit(player_font_3.render("Cumulative Scores:", True, wh), [600, 622])
                if num_players > 0:
                    dis.blit(player_font_2.render("P1: " + str(player1 + ": " + str(MD1['p1_g1_GRAND'] + MD1['p1_g2_GRAND'] + MD1['p1_g3_GRAND'])), True, p1_color), [600, 650])
                if num_players > 1:
                    dis.blit(player_font_2.render("P2: " + str(player2 + ": " + str(MD2['p2_g1_GRAND'] + MD2['p2_g2_GRAND'] + MD2['p2_g3_GRAND'])), True, p2_color), [600, 672])
                if num_players > 2:
                    dis.blit(player_font_2.render("P3: " + str(player3 + ": " + str(MD3['p3_g1_GRAND'] + MD3['p3_g2_GRAND'] + MD3['p3_g3_GRAND'])), True, p3_color), [600, 694])
                if num_players > 3:
                    dis.blit(player_font_2.render("P4: " + str(player4 + ": " + str(MD4['p4_g1_GRAND'] + MD4['p4_g2_GRAND'] + MD4['p4_g3_GRAND'])), True, p4_color), [600, 716])
   
                if num_players != 1:
                    for i in range(0,len(MD_FILLS)):
                        dis.fill(blk, rect = MD_FILLS[i])
                    scorecard = "************************************************************************************************"
                    dis.fill(blk, rect=(10, 88, 580, 9)) ; dis.fill(blk, rect=(10, 706, 580, 9))
                    dis.fill(blk, rect=(8, 88, 9, 629)) ; dis.fill(blk, rect=(580, 88, 9, 629))
                    dis.blit(sc_font.render(scorecard, True, wh), [11, 84])
                    dis.blit(sc_font.render(scorecard, True, wh), [13, 700])
                    scorecard = "    _____________________      __________________     ____________     ____________     ____________"
                    ty = [85,90,350,355,360,365,639.5,644.5,649.5,654.5]
                    for i in ty:
                        dis.blit(sc_font.render(scorecard, True, wh), [15, i])
                    dis.fill(blk, rect=(15, 97.5, 15, 608)) ; dis.fill(blk, rect=(162.5, 97.5, 15, 608))
                    dis.fill(blk, rect=(292.5, 97.5, 15, 608)) ; dis.fill(blk, rect=(384, 97.5, 15, 608))
                    dis.fill(blk, rect=(475.5, 97.5, 15, 608)) ; dis.fill(blk, rect=(567, 97.5, 15, 608))
                    for s in range(1,42):
                        value = sc_font.render(" ||", True, wh)
                        if s < 20 or s > 21:
                            if s < 41:
                                dis.blit(value, [15, 82.5 + s*15]) ; dis.blit(value, [162.5, 82.5 + s*15])
                                dis.blit(value, [292.5, 82.5 + s*15]) ; dis.blit(value, [384, 82.5 + s*15])
                                dis.blit(value, [475.5, 82.5 + s*15]) ; dis.blit(value, [567, 82.5 + s*15])
                        value = sc_font.render("*", True, wh)
                        dis.blit(value, [10, 77.5 + s*15]) ; dis.blit(value, [10, 85 + s*15])
                        dis.blit(value, [582, 77.5 + s*15]) ; dis.blit(value, [582, 85 + s*15])

                # Wait for user to play again
                pygame.display.update() ; time.sleep(2.25)
                result_u = click_font_5.render("Play again? --->", True, wh)
                result = result_u.get_rect()
                result.x, result.y = 1015,685
                dis.blit(result_u, [1015, 685])
                loop6 = True
                while loop6:
                    for event6 in pygame.event.get():
                        if event6.type == pygame.QUIT:
                            loop6 = False ; pygame.quit() ; sys.exit()
                                                
                        if result.collidepoint(pygame.mouse.get_pos()):
                            dis.fill(blk, rect=(1015, 685, 170, 50))
                            result_c = click_font_6.render("Play again? --->", True, red)
                            dis.blit(result_c, [1015, 685])
                        else:
                            dis.fill(blk, rect=(1015, 685, 170, 50))
                            result_u = click_font_5.render("Play again? --->", True, wh)
                            dis.blit(result_u, [1015, 685])
                           
                        if event6.type == pygame.MOUSEBUTTONUP and result.collidepoint(pygame.mouse.get_pos()):
                            dis.fill(blk, rect=(350, 24, 900, 15)) ; dis.fill(blk, rect=(592, 50, 700, 700)) # Reset whole screen
                            # Reset some declared variables from earlier
                            game += 1
                            p1_score = 0; p2_score = 0; p3_score = 0; p4_score = 0
                            yb1 = 0 ; yb2 = 0 ; yb3 = 0; bb = 0
                            player_scores = [0, 0, 0, 0]
                            loop = False ; loop6 = False ; pass3 = True
                            if num_players == 1:
                                player_outofturns = [False] ; player_scores = [0]
                            elif num_players == 2:
                                player_outofturns = [False, False] ; player_scores = [0, 0]
                            elif num_players == 3:
                                player_outofturns = [False, False, False] ; player_scores = [0, 0, 0]
                            elif num_players == 4:
                                player_outofturns = [False, False, False, False] ; player_scores = [0, 0, 0, 0]
                            if game == 4:
                                dis.fill(blk, rect=(0, 0, 1200, 750)) # Reset whole screen
                                loop = False
                                loop_3game = False # All three games FINALLY over! Go back to unending while loop.
                    pygame.display.update()
            pygame.display.update()
    pygame.display.update()

##### END #####
