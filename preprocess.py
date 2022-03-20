#!/usr/bin/env python
import os
import sys

from pytorch_transformers import BertTokenizer
from transformers import AutoTokenizer


if len(sys.argv) != 3:
    print("USAGE: preprocess.py INPUT_DIRECTORY EXTENSION")
    print()
    print("This builds a tokenized dataset from a directory of documents.")
    print("Example usage: ./preprocess.py ../pdfs/ .ocr-txt")
    print()
    print("INPUT_DIRECTORY - Path to a directory with text documents")
    print("EXTENSION - Use files with this extension")


# path to documents
doc_path = sys.argv[1]
# extension of files to build dataset from
doc_ext = sys.argv[2] # ".ocr-txt"

# model_name_or_path = sys.argv[2]
# max_len = int(sys.argv[3])

# typically bert-large-cased
# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
# max_len -= tokenizer.num_special_tokens_to_add()


def tokenize_file(filename, tokenizer=None):
    tokens = []
    with open(filename, "rt") as f_p:
        for line in f_p:
            line = line.strip()

            if not line:
                continue

            for t in tokenizer.tokenize(line):
                print(f"{t} O")
                tokens.append(t)
    return tokens


if __name__ == "__main__":
    tokens = []
    tokenizer = BertTokenizer.from_pretrained("bert-large-cased", do_lower_case=False)
    for basedir, subdirs, filenames in os.walk(doc_path):
        for filename in filenames:
            if not filename.endswith(doc_ext):
                continue
            tokens.extend(tokenize_file(
                os.path.join(basedir, filename), tokenizer=tokenizer
            ))
