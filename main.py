import sys,os
import curses
from textgenerator import TextGenerator
import logging.config
import textwrap
from random import randint
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
text_boxes = {}
global_text_generator = TextGenerator()

def draw_box(slot, text, highlighted):
        new_box = curses.newwin(2, 75, slot, 55)
        if highlighted:
            new_box.attron(curses.color_pair(3))
            new_box.attron(curses.A_BOLD)
        new_box.addstr(1, 2, textwrap.fill(text, 75))
        if highlighted:
            new_box.attroff(curses.color_pair(3))
            new_box.attroff(curses.A_BOLD)
        return new_box

def draw_menu(stdscrr):
    stdscr = curses.initscr()
    height, width = stdscr.getmaxyx()
    
    curses.curs_set(0)
    k = 0
    stdscr.timeout(1500)

    # Start colors in curses
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_text = global_text_generator.create_textblock()
    slots = [1, 3, 5, 7, 9, 11]
    current_slot_index = 0
    highlighted_slot_index = 0
    # Loop where k is the last character pressed
    while (k != ord('q')):
        if k == ord('d'):

            highlighted_slot_index = (highlighted_slot_index + 1) % len(slots)
        elif k == ord('a'):
            highlighted_slot_index = (highlighted_slot_index - 1) % len(slots)


        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(0, 0, current_text)
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)
        
        # Draw a new textbox if this slot isn't highlighted
        if highlighted_slot_index != current_slot_index:
            new_text = global_text_generator.create_textblock()
            new_box = draw_box(slots[current_slot_index], new_text, False)
            text_boxes[current_slot_index]=new_box

        else:
            pass
        for box in text_boxes.values():
        #    box_y, box_x =  box.getbegyx()
        #    if box_y < 2:
        #        box.clear()
        #        box.refresh()
        #        text_boxes.remove(box)
        #    else:
        #        box.mvwin(box_y - 2, box_x)
            box.refresh()
        current_slot_index = (current_slot_index + 1) % len(slots)
        stdscr.refresh()
        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()