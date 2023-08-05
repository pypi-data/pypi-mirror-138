from . import clidle

if __name__ == "__main__":
    from curses import wrapper
    wrapper(clidle.clidle_main)
