try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import re

LETTER_NUMBER_RE = re.compile(r"\w?\d+")
CONTRACTNO_RE = re.compile(r"\w?\d{5,}")


class DocumentProcessor:

    def retrieveContractNumber(self, filename):
        im = Image.open(filename)
        im = im.convert('L').resize([3 * _ for _ in im.size], Image.BICUBIC)
        im = im.point(lambda p: p > 150 and p + 150)
        # im.save("temp2.png", "png")

        ocr_text = pytesseract.image_to_string(im, lang='nld')

        return self.extract_number(ocr_text)

    # custom:

    def process_basic(self, line):
        return self.remove_non_number(line)

    def remove_non_number(self, text):
        list = LETTER_NUMBER_RE.findall(text)
        if list:
            return list[0]
        return False

    def extract_number(self, raw):
        string_list = raw.split('\n')

        # print(string_list)

        for line in string_list:
            low = line.lower()

            if "contract" in low or 'ingnummer' in low:  # contractnummer,  INGnummer/len-ingnummer
                contract_no = self.process_basic(line)
                if contract_no:
                    return contract_no
                else:
                    continue

            elif "contrac" in low:
                # todo: improve fuzzy match
                contract_no = self.process_basic(line)
                if contract_no:
                    return contract_no
                else:
                    continue

        # else, raw find:
        matches = CONTRACTNO_RE.findall(raw)
        if matches:
            # todo: maybe at some other index?
            return matches[0]

        return "not found"
