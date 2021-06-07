import curses, logging.config, threading, click
from time import sleep
from .interfaces import TextAccumulator, OptionWindow
from .textgenerator import TextGenerator
from random import randint

highlighted_slot_index = 0

def draw_menu(stdscrr, option_window, global_text_accumulator):
    stdscr = curses.initscr()
    height, width = stdscr.getmaxyx()
    curses.resizeterm(50, 200)
    # Start colors in curses
    stdscr.refresh()
    curses.start_color()

    new_box = curses.newwin(1, width, height-2, 0)
    new_box.attron(curses.color_pair(1))
    new_box.attron(curses.A_BOLD)
    new_box.addnstr(0, 0, "UP/DOWN Selects text. RIGHT Adds selected text block to game. LEFT Removes rightmost character from the game. q exits.", width-1)
    new_box.attroff(curses.color_pair(1))
    new_box.attroff(curses.A_BOLD)
    new_box.refresh()



    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    option_window.set_screen(stdscr)
    global_text_accumulator.set_screen(stdscr)

    t = threading.Thread(name ='daemon', target=input_thread, args=(stdscr, option_window, global_text_accumulator))
    t.setDaemon(True)
    t.start()

    while t.is_alive():
        option_window.attempt_to_generate_new_option_at_text_ticker_location(global_text_accumulator.generate_add_text_candidate())
        sleep(1)

        option_window.focus_option_at_key(option_window.highlight_ticker)
        for box in option_window.options.values():
            box.refresh()
        stdscr.refresh()

def input_thread(stdscr, option_window, global_text_accumulator):
    curses.curs_set(0)
    k = 0
    
    while (k != ord('q')):
        highlighted_slot_index = option_window.highlight_ticker
        if k == curses.KEY_DOWN:
            option_window.remove_focus()
            highlighted_slot_index = (highlighted_slot_index + 2) % 16
            option_window.focus_option_at_key(highlighted_slot_index)
        if k == curses.KEY_UP:
            option_window.remove_focus()
            highlighted_slot_index = (highlighted_slot_index - 2) % 16
            option_window.focus_option_at_key(highlighted_slot_index)
        if k == curses.KEY_RIGHT:
            if option_window.options.get(highlighted_slot_index).text != "LOADING...":
                current_text = option_window.options.get(highlighted_slot_index).text
                global_text_accumulator.add_text(current_text)
                option_window.set_screen(stdscr)
                current_slot_index = 0
                option_window.highlight_ticker = 0
        if k == curses.KEY_LEFT:
            global_text_accumulator.backspace()
            option_window.set_screen(stdscr)
            current_slot_index = 0
            option_window.highlight_ticker = 0

    
        for box in option_window.options.values():
            box.refresh()
        stdscr.refresh()
        # Wait for next input
        k = stdscr.getch()
    
@click.command()
@click.option('--path', default='model/', help='Path to a local pytorch model.')
@click.option('--name', default='gyre/200wordrpgmodel', prompt='Enter The Model Name', help='Name of the huggingface model.')
def play(path: str, name: str):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })
    option_window = OptionWindow()
    text_generator = TextGenerator(model_path = path, model_name = name)
    text_accumulator = TextAccumulator(text_generator)
    curses.wrapper(draw_menu, option_window = option_window, global_text_accumulator = text_accumulator)

def main():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })
    option_window = OptionWindow()
    text_generator = TextGenerator(model_path = path, model_name = name)
    global_text_accumulator = TextAccumulator(text_generator)
    curses.wrapper(draw_menu, option_window = option_window, global_text_accumulator = global_text_accumulator)

if __name__ == "__main__":
    main()
