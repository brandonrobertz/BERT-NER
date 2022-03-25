#!/usr/bin/env python
import json
import os
import re
import sys


SKIP_WORDS = ["&nbsp", "LINE-BREAK"]
# number of non-labeled tokens before and after a sequence of labels to
# include, this reduces the sparsity of training data
CONTEXT = 30


def load_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def extract_data_labels(data):
    """
    Take data from the NER labeler tool and extract the labels as a set.
    """
    return set([l["label"] for l in data["labels"]])


def transform_document(file_data, labels):
    """
    Data structure from the NER labeler:

        [
          {
            "text":"2022",
            "label":"DDATE"
          },
          {
            "text":"June",
            "label":"DDATE"
          },
          {
            "text":"&nbsp"
          },
          {
            "text":"Last"
          },
          ...
        ]

    Output format (in German, from the legal NER project):

         an O
         Kapitalgesellschaften O
         ( O
         § B-GS
         17 I-GS
         Abs. I-GS
         1 I-GS
         und I-GS
         2 I-GS
         1EStG I-GS
         1) O
    """
    name = file_data["name"]
    words_data = file_data["data"]

    yield "-DOCSTART- O"

    # start each document with the words that make up the filename
    # this might help the model key in on the fact that the
    # subject of an investigation often ends up in the filename
    basename = os.path.splitext(os.path.basename(name))[0]
    filename_words = re.split('[^A-Za-z0-9]+', basename)
    for word in filename_words:
        if not word.strip():
            continue
        yield f"{word} O"

    prev_label = None
    blanks = 0
    for word_data in words_data:
        label = word_data.get("label")
        word = word_data["text"].strip()

        if not word or word in SKIP_WORDS:
            continue

        if not label:
            prev_label = None
            blanks += 1
            if CONTEXT is not None and blanks > CONTEXT:
                continue
            # O, aka Outside, is the default non-label
            yield f"{word} O"
            continue

        # we have a label
        blanks = 0

        # Inner vs Begin label
        prefix = "I" if prev_label == label else "B"
        prev_label = label
        yield f"{word} {prefix}-{label}"

        # use a blank line between sentences
        if word == ".":
            yield ""


if __name__ == "__main__":
    ner_filename = sys.argv[1]

    ner_data = load_data(ner_filename)
    labels = extract_data_labels(ner_data)
    for file_data in ner_data["file_data"]:
        if not file_data.get("has_labels"):
            continue
        for line in transform_document(file_data, labels):
            print(line)
        print()
