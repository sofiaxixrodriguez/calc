class ObjectBuilder:
    def __init__(self):
        self.elementsMap: dict = {}

    def getElement(self, element: str):
        return self.elementsMap[element]
