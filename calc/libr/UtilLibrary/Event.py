class Event:
    def __init__(self):
        self.__listOfUsers = []

    def __del__(self):
        pass

    def register(self, *args):
        for userObj in args:
            if userObj not in self.__listOfUsers:
                self.__listOfUsers.append(userObj)

    def unregister(self, userObj):
        self.__listOfUsers.remove(userObj)

    def notifyAll(self):
        for objects in self.__listOfUsers:
            objects.onEventReceived(self)

    def getListOfUsers(self):
        return self.__listOfUsers
