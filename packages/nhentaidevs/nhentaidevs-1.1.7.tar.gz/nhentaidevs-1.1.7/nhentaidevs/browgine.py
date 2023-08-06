from . import *

class Browgine:

    def __init__(self, code, path=None, *args) -> None:
        self.code = code
        self.raw = request.get("https://nhentai.net/g/" + str(self.code))
        self.soup = BeautifulSoup(self.raw, "html.parser")
    
