"""
The first color in each pallete is the base color
The last color is the grayed out color
"""

tab_colors = [
    "tab:olive",
    "tab:green",
    "tab:orange",
    "tab:pink",
    "tab:purple",
    "tab:brown",
    "tab:gray",
    "tab:cyan",
    "tab:red",
]

colors = {
    "mkbhd_palette": ["tab:red"] + tab_colors + ["lightgray"],
    "base_palette": ["tab:blue"] + tab_colors + ["lightgray"],
    "vox_palette": ["white"] + tab_colors + ["#566a6b"],
    "innocent_palette": ["#244796"] + tab_colors + ["#9c9b92"],
}
