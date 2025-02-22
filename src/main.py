from ui.MainMenu import MainMenu

DIRECTORY = "ledger/"

def main():
    """Main function to start the program"""
    main_menu = MainMenu(DIRECTORY)
    main_menu.run()

if __name__ == "__main__":
    main()
