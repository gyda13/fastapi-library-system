from .BaseException import NotFoundException

class BookNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("Book")