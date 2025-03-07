from ui.MainMenu import MainMenu
from control.MainFileManager import MainFileManager

LEDGERS_DIRECTORY = "ledger/"

def main():
    """Main function to start the program"""
    main_file_manager = MainFileManager(LEDGERS_DIRECTORY)
    main_menu = MainMenu(main_file_manager)
    main_menu.run()

if __name__ == "__main__":
    main()
