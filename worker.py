import re
from collections import Counter
import Pyro4

@Pyro4.expose
class WordCountWorker(object):
    def count_words_in_range(self, file_path: str, start_byte: int, end_byte: int) -> dict:
        counter = Counter()
        pattern = re.compile(r'[a-zA-Z0-9]+')
        
        with open(file_path, 'rb') as f:
            f.seek(start_byte)
            if start_byte != 0:
                f.readline()
            
            while True:
                curr_pos = f.tell()
                if curr_pos >= end_byte:
                    break
                
                line = f.readline()
                if not line:
                    break
                
                text_line = line.decode('utf-8', errors='ignore')
                words = pattern.findall(text_line.lower())
                counter.update(words)
                
        return dict(counter)
