import curses
from curses import wrapper
import time 
import random
from pynput import keyboard
 
def startScrn(stdscr):
    stdscr.clear()
    stdscr.addstr(1,56,"Welcome to the Typing Speed test!")
    stdscr.addstr(2,60,"Press any key to continue")
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    with open('text.txt',"r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()
    


def wpmTest(stdscr):
    target_text = load_text()
    curr_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    
   
    while True:
        timeElasped = max(time.time() - start_time, 1)


        wpm = len(curr_text) / timeElasped
        wpm = round((wpm * 60)/5)


        stdscr.clear()
        display_text(stdscr, target_text, curr_text,wpm)
        stdscr.refresh()
        
        if "".join(curr_text) == target_text:
            stdscr.nodelay(False)
            break




        try:
            key = stdscr.getkey()
        except:
            continue

        if key == keyboard.Key.esc:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()
        elif len(curr_text) < len(target_text):
             curr_text.append(key)
    
    stdscr.addstr(2,0, "You completed the test! Press any key to continue!")
    stdscr.getkey()


        

def display_text(stdscr, target_text, curr_text, wpm):
    stdscr.addstr(target_text)
    stdscr.addstr(1,0, f"WPM: {wpm}")

    for i, char in enumerate(curr_text):
        correct = target_text[i]
        color = curses.color_pair(3)

        if(char != correct):
            color = curses.color_pair(2)

        stdscr.addstr(0,i,char, color)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE , curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW , curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN , curses.COLOR_BLACK)
    
    while(True):
        startScrn(stdscr)
        wpmTest(stdscr)
        

wrapper(main)