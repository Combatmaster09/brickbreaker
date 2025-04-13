"""
Level designs for Brick Breaker game.
Each level is defined as a list of rows, where:
- Each row is a string of characters
- Each character represents a brick type:
  - ' ' (space): No brick
  - '#': Normal brick (1 health)
  - '2', '3', etc.: Stronger bricks (2, 3 health)
  - 'S': Special brick (power-up)
"""

LEVEL_DESIGNS = [
    # Level 1 - Basic pattern
    [
        "     ##########     ",
        "    ############    ",
        "    ############    ",
        "     ##########     "
    ],
    
    # Level 2 - Slightly harder
    [
        "  ##############  ",
        "  #2222222222222#  ",
        "  #2############2#  ",
        "  #2#          #2#  ",
        "  #2############2#  ",
        "  #2222222222222#  ",
        "  ##############  "
    ],
    
    # Level 3 - Wall pattern
    [
        "##################",
        "#22222222222222222#",
        "#2#####2#####2####2#",
        "#2#   #2#   #2#  #2#",
        "#2#   #2#   #2#  #2#",
        "#2#####2#####2####2#",
        "#22222222222222222#",
        "##################"
    ],
    
]