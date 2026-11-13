import sys
from src.view.TerminalView import TerminalView
from src.linker.LinkElements import LinkElements

class Application:
    def __init__(self):
        self.__initCalculatorElements()

    def __initCalculatorElements(self):
        linker = LinkElements(mainWindow=None)
        linker.linkViews()
        linker.linkControllers()
        linker.linkModels()
        linker.registerEvents()
        linker.initElements()


if __name__ == "__main__":
    try:
        Application()
    except (SystemExit, KeyboardInterrupt):
        pass