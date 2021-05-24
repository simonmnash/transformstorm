import curses, os, textwrap
from .textgenerator import TextGenerator



class TextAccumulator():
    def __init__(self):
        self.complete_text = ""
        self.text_generator = TextGenerator()
        
    def set_screen(self, stdscr):
        self.screen = stdscr

    def add_text(self, text):
        height, width = self.screen.getmaxyx()
        self.complete_text = self.complete_text + text
        new_box = curses.newwin(height-5, 60, 0, 75)
        new_box.attron(curses.color_pair(2))
        new_box.attron(curses.A_BOLD)
        new_box.addnstr(0, 0, textwrap.fill(self.complete_text, 100), width)
        new_box.attroff(curses.color_pair(2))
        new_box.attroff(curses.A_BOLD)
        new_box.refresh()
    def backspace(self):
        height, width = self.screen.getmaxyx()
        self.complete_text = self.complete_text[:-1]
        new_box = curses.newwin(height-5, 60, 0, 75)
        new_box.attron(curses.color_pair(2))
        new_box.attron(curses.A_BOLD)
        new_box.addnstr(0, 0, textwrap.fill(self.complete_text, 100), width)
        new_box.attroff(curses.color_pair(2))
        new_box.attroff(curses.A_BOLD)
        new_box.refresh()
    def generate_add_text_candidate(self):
        return self.text_generator.create_textblock(self.complete_text)


class TextBox():
    def __init__(self, slot, text, highlighted = False):
        self.text = text
        self.slot = slot
        self.highlighted = highlighted
        self.box = self.draw()
    
    def draw(self):
        new_box = curses.newwin(2, 75, self.slot, 0)
        if self.highlighted:
            new_box.attron(curses.color_pair(3))
            new_box.attron(curses.A_BOLD)
        new_box.addstr(1, 2, textwrap.fill(self.text, 75))
        if self.highlighted:
            new_box.attroff(curses.color_pair(3))
            new_box.attroff(curses.A_BOLD)
        return new_box

    def focus(self):
        self.highlighted = True
        self.box = self.draw()
        return self
    
    def unfocus(self):
        self.highlighted = False
        self.box = self.draw()
        return self
    
    def toggle_highlight(self):
        if self.highlighted:
            self.highlighted = False
        else:
            self.highlighted = True
        self.box = self.draw()
        self.box.refresh()

    def refresh(self):
        self.box.refresh()

class OptionWindow():
    def __init__(self):
        self.options = {}
        # highlight ticker determines which option is currently highlighted.
        self.highlight_ticker = 0
        # text generation ticker determines which option is next in line for replacement.
        self.text_generation_ticker = 0

    def set_screen(self, stdscr):
        self.screen = stdscr
        height, width = stdscr.getmaxyx()
        for slot in range(0, 12, 2):
            self.add_new_option(slot, "LOADING...", slot==0)

    def add_new_option(self, new_option_location, new_option_text, highlighted):
        new_text_box = TextBox(new_option_location, new_option_text, highlighted)
        self.options[new_option_location] = new_text_box

    def attempt_to_generate_new_option_at_text_ticker_location(self, new_option_text):
        if self.text_generation_ticker == self.highlight_ticker and self.options[self.text_generation_ticker].text != "LOADING...":
            pass
        else:
            self.add_new_option(self.text_generation_ticker, new_option_text, False)
        self.text_generation_ticker = (self.text_generation_ticker + 2) % 12

    def remove_focus(self):
        for option in self.options.values():
            self.options[option.slot] = option.unfocus()

    def focus_option_at_key(self, key_to_focus):
        if self.options.get(key_to_focus):
            self.highlight_ticker = key_to_focus
            self.options[key_to_focus] = self.options[key_to_focus].focus()
