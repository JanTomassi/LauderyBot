from datetime import datetime, timedelta


class WashingMachine:
    def __init__(self, mtype: str):
        self.mtype = mtype
        self.start = datetime.now()
        self.end = timedelta()
        self.user = 0

    def setnewuse(self, end: timedelta, user: id):
        if self.hasFinished():
            self.start = datetime.now()
            self.user = user
            self.end = end
            return True
        else:
            return False

    def remaing(self) -> datetime:
        return self.start + self.end

    def hasFinished(self) -> bool:
        return self.remaing() < datetime.now()

    def currentUser(self) -> str:
        if HasFinished():
            self.user = "Nessuno"
        return self.user
