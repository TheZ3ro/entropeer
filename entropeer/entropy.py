import math
import json
import re

from functools import partial

BASE64_CHARS = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = b"1234567890abcdefABCDEF"

def entropy(data, iterator=range(256)):
    """
    return the shannon entropy value for a given string
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    originally by Ero Carrera (blog.dkbza.org)
    """
    if not data:
        return 0
    if isinstance(data, str):
        data = data.encode()

    seen = dict(((x, 0) for x in iterator))
    for byte in data:
        seen[byte] += 1

    entropy = 0
    for x in iterator:
        p_x = float(seen[x]) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

class FileEntropy(object):
    rules = set()
    block_size = 1024

    @staticmethod
    def get_strings_of_set(word, char_set, threshold=20):
        """
        return all strings in word with length > threshold that contain only characters in char_set (from trufflehog)
        """
        count = 0
        letters = b""
        strings = []

        if isinstance(word, str):
            word = word.encode()
        if isinstance(char_set, str):
            char_set = char_set.encode()

        for char in word:
            if char in char_set:
                letters += bytes((char,))
                count += 1
            else:
                if count > threshold:
                    strings.append(letters)
                letters = b""
                count = 0
        if count > threshold:
            strings.append(letters)
        return strings

    @staticmethod
    def add_rule(rule):
        FileEntropy.rules.add(re.compile(rule))

    @staticmethod
    def load_rules_from_file(filename):
        try:
            with open(filename, "r") as f:
                rules = json.loads(f.read())
                for rule in rules:
                    FileEntropy.add_rule(rules[rule])
        except (IOError, ValueError) as e:
            print(e)
            raise Exception("Error reading rules file")

    def __init__(self, filename):
        self.filename = filename

    def find_entropy(self, binary=False):
        if binary:
            return self.find_binary_entropy()
        else:
            return self.find_text_entropy()

    def find_text_entropy(self):
        """
        step through a text file line by line, split it by words and get entropy
        """
        with open(self.filename, 'r', encoding='utf8') as f:
            for line_counter, line in enumerate(f, 1):
                for word in line.split():
                    for string in self.find_block_entropy(word):
                        yield (self.filename, line_counter, line.strip(), string)

    def find_binary_entropy(self):
        """
        step through a text file line by line, split it by words and get entropy
        """
        with open(self.filename, 'rb') as f:
            for chunk in iter(partial(f.read, FileEntropy.block_size), b''):
                for string in self.find_block_entropy(chunk):
                    yield (self.filename, '', string, string)

    def find_block_entropy(self, block):
        """
        find b64/hex blobs and measure their entropy.
        """
        base64_strings = FileEntropy.get_strings_of_set(block, BASE64_CHARS)
        hex_strings = FileEntropy.get_strings_of_set(block, HEX_CHARS)
        for string in base64_strings:
            b64_entropy = entropy(string, BASE64_CHARS)
            if b64_entropy > 4.5:
                yield string
        for string in hex_strings:
            hex_entropy = entropy(string, HEX_CHARS)
            if hex_entropy > 3.0:
                yield string

    def find_regex(self, binary=False):
        """
        step through a file line by line matching rules in regex formats.
        """
        with open(self.filename, encoding='utf8') as f:
            for line_counter, line in enumerate(f, 1):
                for rule in FileEntropy.rules:
                    for found_string in rule.findall(line):
                        yield (self.filename, line_counter, line.strip(), found_string)
