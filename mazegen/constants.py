
# Constants for cells' direction
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000


# Color palettes
lesbian_palette = {
    'walls': 0xF79553,
    'solution': 0xCC5E9E,
    'ft': 0xF7F7F7,
    'entry': 0xCE2B00,
    'exit': 0x9D015E
}
bisexual_palette = {
    'walls': 0x9D015E,
    'solution': 0x083EAA,
    'ft': 0x9E5499,
    'entry': 0x67BED9,
    'exit': 0xF7F7F7
}
gay_palette = {
    'walls': 0x25CFAA,
    'solution': 0x4F48CA,
    'ft': 0xFFFFFF,
    'entry': 0x98EAC3,
    'exit': 0x7BADE3
}
trans_palette = {
    'walls': 0x5BCEFA,
    'solution': 0xF5A9B8,
    'ft': 0xFFFFFF,
    'entry': 0xFCE5EA,
    'exit': 0x5BCEFA
}
COLOR_PALETTE = [lesbian_palette, bisexual_palette, gay_palette, trans_palette]
