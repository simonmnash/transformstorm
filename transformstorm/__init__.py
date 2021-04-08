import sys,os
import curses
from textgenerator import TextGenerator
import logging.config
import textwrap
import threading
from time import sleep

from random import randint
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
text_boxes = {}
highlighted_slot_index = 0
slots = [0, 2, 4, 6, 8, 10]
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

def input_thread(stdscr):
    global current_slot_index
    global highlighted_slot_index
    global slots
    curses.curs_set(0)
    k = 0
    while (k != ord('q')):
        if k == curses.KEY_DOWN:
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, False)
                text_boxes[highlighted_slot_index]=new_box
            highlighted_slot_index = (highlighted_slot_index + 1) % len(slots)
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, True)
                text_boxes[highlighted_slot_index]=new_box
        if k == curses.KEY_UP:
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, False)
                text_boxes[highlighted_slot_index]=new_box
            highlighted_slot_index = (highlighted_slot_index - 1) % len(slots)
            if text_boxes.get(highlighted_slot_index):
                keep_text = text_boxes.get(highlighted_slot_index).text
                new_box = TextBox(slots[highlighted_slot_index], keep_text, True)
                text_boxes[highlighted_slot_index]=new_box

        if k == ord(' '):
            current_text = text_boxes.get(highlighted_slot_index).text
            global_text_accumulator.add_text(current_text)
            stdscr.attron(curses.color_pair(2))
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(0, 0, textwrap.fill(global_text_accumulator.complete_text, 50))
            stdscr.attroff(curses.color_pair(2))
            stdscr.attroff(curses.A_BOLD)
            for slot_index in range(0, len(slots)):
                if slot_index==0:
                    new_box = TextBox(slots[slot_index], global_text_accumulator.generate_add_text_candidate(), True)
                else:
                    new_box = TextBox(slots[slot_index], global_text_accumulator.generate_add_text_candidate(), False)
                text_boxes[slot_index]=new_box
            current_slot_index = 0
            highlighted_slot_index = 0
        for box in text_boxes.values():
            box.refresh()
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def draw_menu(stdscrr):
    stdscr = curses.initscr()

    height, width = stdscr.getmaxyx()

    # Start colors in curses
    stdscr.refresh()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_slot_index = 0
    
    for slot_index in range(0, len(slots)):
        if slot_index==0:
            new_box = TextBox(slots[slot_index], global_text_accumulator.generate_add_text_candidate(), True)
        else:
            new_box = TextBox(slots[slot_index], global_text_accumulator.generate_add_text_candidate(), False)
        text_boxes[slot_index] = new_box
    
    t = threading.Thread(name ='daemon', target=input_thread, args=(stdscr,))
    t.setDaemon(True)
    t.start()

    while True:
        if highlighted_slot_index == current_slot_index:
            if text_boxes.get(current_slot_index):
                keep_text = text_boxes.get(current_slot_index).text
                new_box = TextBox(slots[current_slot_index], keep_text, True)
            else:
                new_box = TextBox(slots[current_slot_index], global_text_accumulator.generate_add_text_candidate(), True)
        else:
            new_box = TextBox(slots[current_slot_index], global_text_accumulator.generate_add_text_candidate(), False)
        text_boxes[current_slot_index]=new_box
        current_slot_index = (current_slot_index + 1) % len(slots)
        sleep(1.5)


def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()