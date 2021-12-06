
class SimpleTranslator:

    INDEX_ENGLISH = 0
    INDEX_CHINESE_SIMPLIFIED = 1

    def __init__(self, filepath: str, choosen_lang: int):
        self.matching_dict = {}
        fs = open(filepath, 'r', encoding="utf-8")

        while True:
            ln = fs.readline()
            if ln == "":
                break

            ln = ln.strip()
            if ln == "":
                continue

            lnsp = ln.split("\t")
            self.matching_dict[lnsp[0]] = lnsp[choosen_lang]

        fs.close()

    def Translate(self, pending_str: str) -> str:
        v = self.matching_dict.get(pending_str)
        if v is None:
            v = pending_str
        
        return v
