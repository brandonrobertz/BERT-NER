#!/usr/bin/env python
import sys
import json

from bert import Ner

# import nltk
# nltk.download('punkt')

model = Ner("out_large/")

output = model.predict(" ".join(sys.argv[1:]))

print(json.dumps(output, indent=2))
'''
    [
        {
            "confidence": 0.9981840252876282,
            "tag": "B-PER",
            "word": "Steve"
        },
        {
            "confidence": 0.9998939037322998,
            "tag": "O",
            "word": "went"
        },
        {
            "confidence": 0.999891996383667,
            "tag": "O",
            "word": "to"
        },
        {
            "confidence": 0.9991968274116516,
            "tag": "B-LOC",
            "word": "Paris"
        }
    ]
'''
