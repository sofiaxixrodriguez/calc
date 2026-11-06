from PyQt6.QtWidgets import QApplication
import sys
from src.view.TerminalView import TerminalView
from src.linker.LinkElements import LinkElements
from src.widget.MainWindow import MainWindow


class Application:
    def __init__(self):

        app = QApplication(sys.argv)
        self.mainWindow = MainWindow()
        self.__initDocumentViewerElements()
        sys.exit(app.exec_())

    def __initDocumentViewerElements(self):
        documentViewerLinker = LinkElements(self.mainWindow)
        documentViewerLinker.linkViews()
        documentViewerLinker.linkControllers()
        documentViewerLinker.linkModels()
        documentViewerLinker.registerEvents()
        documentViewerLinker.initElements()


if __name__ == "__main__":
    Application()
