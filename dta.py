# Defining color codes
black = "\033[0;30m"
red = "\033[0;31m"
bred = "\033[1;31m"
green = "\033[0;32m"
bgreen = "\033[1;32m"
yellow = "\033[0;33m"
byellow = "\033[1;33m"
blue = "\033[0;34m"
bblue = "\033[1;34m"
purple = "\033[0;35m"
bpurple = "\033[1;35m"
cyan = "\033[0;36m"
bcyan = "\033[1;36m"
white = "\033[1;37m"
bwhite = "\033[0;37m"
magenta = "\033[0;35m"
bmagenta = "\033[1;35m"
orange = "\033[38;5;208m"  # Bright orange
bright_red = "\033[91m"
bright_green = "\033[92m"
bright_yellow = "\033[93m"
bright_blue = "\033[94m"
bright_magenta = "\033[95m"
bright_cyan = "\033[96m"
bright_white = "\033[97m"
nc = "\033[00m" 
bright_light_blue = "\033[1;38;2;173;216;230m"
saffron = "\033[38;2;255;153;51m"  # Saffron (orange)
navy_blue = "\033[38;2;0;0;128m" 

nc = "\033[00m"  # No color (reset)

version = str("1.0 Beta")
import os
clear = ('cls' if os.name == 'nt' else 'clear')
con_inf = f'{byellow}[{bmagenta}!{byellow}] {nc}'
con_pls = f'{bgreen}[{bmagenta}+{bgreen}] {nc}'
con_mns = f'{bred}[{bmagenta}-{bred}] {nc}'
con_ai = f'{bgreen}[{bmagenta}⁜{bgreen}] {nc}'
print(con_inf+con_pls+con_mns)

logo = f'''{saffron}
███████╗ ███╗   ███╗ ██╗ ██╗   ██╗   ██╗
██╔════╝ ████╗ ████║ ██║ ██║   ╚██╗ ██╔╝
{bright_white}█████╗   ██╔████╔██║ ██║ ██║    ╚████╔╝ 
{bright_green}██╔══╝   ██║╚██╔╝██║ ██║ ██║     ╚██╔╝  
███████╗ ██║ ╚═╝ ██║ ██║ ███████╗ ██║   
╚══════╝ ╚═╝     ╚═╝ ╚═╝ ╚══════╝ ╚═╝
{bpurple} v{version}{bcyan} By @dkyivyansh{nc}
'''

def print_color_names():
    color_dict = {
        "Black": black,
        "Red": red,
        "Bright Red": bred,
        "Green": green,
        "Bright Green": bgreen,
        "Yellow": yellow,
        "Bright Yellow": byellow,
        "Blue": blue,
        "Bright Blue": bblue,
        "Purple": purple,
        "Bright Purple": bpurple,
        "Cyan": cyan,
        "Bright Cyan": bcyan,
        "White": white,
        "Bright White": bwhite,
        "Magenta": magenta,
        "Bright Magenta": bmagenta,
        "Orange": orange,
        "Bright Red Alt": bright_red,
        "Bright Green Alt": bright_green,
        "Bright Yellow Alt": bright_yellow,
        "Bright Blue Alt": bright_blue,
        "Bright Magenta Alt": bright_magenta,
        "Bright Cyan Alt": bright_cyan,
        "Bright White Alt": bright_white,
        "Saffron": saffron,
        "Navy Blue (Ashoka Chakra)": navy_blue,
        "bright_light_blue" : bright_light_blue
    }

    for color_name, color_code in color_dict.items():
        print(f"{color_code}{color_name}{nc}")

