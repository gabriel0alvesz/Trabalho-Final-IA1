class ReadDocs:

    def __init__(self):
        self.lines: list
    
    def ReadDoc(self, name_doc: str):
        with open(name_doc,'r') as f:
            self.lines = f.readlines()
    
    def Tokenizer(self) -> list:
        self.lines = [line.strip() for line in self.lines]
        return self.lines
    