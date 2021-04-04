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
class TextAccumulator():
    def __init__(self):
        self.complete_text = ""
        self.text_generator = TextGenerator() 
    def add_text(self, text):
        self.complete_text = self.complete_text + text
    def generate_add_text_candidate(self):
        return self.text_generator.create_textblock(self.complete_text)

class TextBox():
    def __init__(self, slot, text, highlighted = False):
        self.text = text
        self.slot = slot
        self.highlighted = highlighted
        self.box = self.draw()
    
    def draw(self):
        new_box = curses.newwin(2, 75, self.slot, 55)
        if self.highlighted:
            new_box.attron(curses.color_pair(3))
            new_box.attron(curses.A_BOLD)
        new_box.addstr(1, 2, textwrap.fill(self.text, 75))
        if self.highlighted:
            new_box.attroff(curses.color_pair(3))
            new_box.attroff(curses.A_BOLD)
        return new_box

    def toggle_highlight(self):
        if self.highlighted:
            self.highlighted = False
        else:
            self.highlighted = True
        self.box = self.draw()
        self.box.refresh()

    def refresh(self):
        self.box.refresh()

global_text_accumulator = TextAccumulator()

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

    slots = [1, 3, 5, 7, 9, 11]
    current_slot_index = 0
    highlighted_slot_index = 0
    # Loop where k is the last character pressed
    while (k != ord('q')):
        highlighted_slot = slots[highlighted_slot_index]
        if k == ord('d'):
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, False)
                text_boxes[highlighted_slot_index]=new_box
            highlighted_slot_index = (highlighted_slot_index + 1) % len(slots)
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, True)
                text_boxes[highlighted_slot_index]=new_box
        elif k == ord('a'):
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, False)
                text_boxes[highlighted_slot_index]=new_box
            highlighted_slot_index = (highlighted_slot_index - 1) % len(slots)
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, False)
                text_boxes[highlighted_slot_index]=new_box

        if k == ord(' '):
            current_text = text_boxes.get(highlighted_slot_index).text
            global_text_accumulator.add_text(current_text)
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, 0, textwrap.fill(global_text_accumulator.complete_text, 50))
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)
        
        if highlighted_slot_index == current_slot_index:
            if text_boxes.get(current_slot_index):
                keep_text = text_boxes.get(current_slot_index).text
                new_box = TextBox(slots[current_slot_index], keep_text, True)
            else:
                new_box = TextBox(slots[current_slot_index], global_text_accumulator.generate_add_text_candidate(), True)
        else:
            new_box = TextBox(slots[current_slot_index], global_text_accumulator.generate_add_text_candidate(), False)
        text_boxes[current_slot_index]=new_box

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