"""
Level designs for Brick Breaker game.
Each level is defined as a list of rows, where:
- Each row is a string of characters
- Each character represents a brick type:
  - ' ' (space): No brick
  - '#': Normal brick (1 health)
  - '2', '3', etc.: Stronger bricks (2, 3 health)
  - L : Slow ball powerup (1 health)
  - F : Fast ball powerup (1 health)
  - M : Multiball powerup (1 health)
  - + : Extra life powerup (1 health)
"""

LEVEL_DESIGNS = [
    # Level 1 - Basic pattern with some powerups
    [
        "     ##########     ",
        "    ############    ",
        "    ####M##L####    ",
        "     #####+MLF#     "
    ],
    
    # Level 2 - Slightly harder with more powerups
    [
        " ############  ",
        " #222#222F222#  ",
        " #############  ",
        " ##    +    ##  ",
        " #############  ",
        " #222F222L222#  ",
        " ############  "
    ],
    
    # Level 3 - Wall pattern
    [
        "##############",
        "#22222#22M2222#",
        "#2####2####2###2#",
        "#2#  #2#  #2# #2#",
        "#2#  #+#  #M# #2#",
        "#2####2####2###2#",
        "#22222F22L2222#",
        "##############"
    ],
]