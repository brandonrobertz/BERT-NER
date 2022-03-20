Source: https://skimai.com/how-to-fine-tune-bert-for-named-entity-recognition-ner/

    3) Labels
    In CoNLL-2002/2003 datasets, there are have 9 classes of NER tags:
        O, Outside of a named entity
        B-MIS, Beginning of a miscellaneous entity right after another miscellaneous entity
        I-MIS, Miscellaneous entity
        B-PER, Beginning of a person’s name right after another person’s name
        I-PER, Person’s name
        B-ORG, Beginning of an organisation right after another organisation
        I-ORG, Organisation
        B-LOC, Beginning of a location right after another location
        I-LOC, Location

Source: https://www.irjet.net/archives/V7/i6/IRJET-V7I61165.pdf

    Here is a demo from CoNLL 2003
          U.N. NNP I-NP I-ORG
          official NN I-NP O
          Ram NNP I-NP I-PER
          heads VBZ I-VP O
          for IN I-PP O
          Baghdad NNP I-NP I-LOC
    In the above example, the first word on every line is a
    word from the corpus, second is part-of-speech (POS) tag,
    the third is syntactic chunk tag and fourth is the name
    entity tag for that word. Every line in the dataset follows
    this pattern [word] [POS tag] [chunk tag] [NER tag].
    Entities are annotated with ORG (organization), LOC
    (location), PER (person), and MISC (miscellaneous), O
    (other). The chunk tags and the named entity tags have
    the format I-TYPE which means that the word is inside a
    phrase of type TYPE. Only if two phrases of the same type
    immediately follow each other, the first word of the
    second phrase will have tag B-TYPE to show that it starts a
    new phrase. A word with tag O is not part of a phrase.


Source: https://spacy.io/usage/linguistic-features/#updating-biluo

        IOB Scheme
        
            I – Token is inside an entity.
            O – Token is outside an entity.
            B – Token is the beginning of an entity.
        
        BILUO Scheme
        
            B – Token is the beginning of a multi-token entity.
            I – Token is inside a multi-token entity.
            L – Token is the last token of a multi-token entity.
            U – Token is a single-token unit entity.
            O – Token is outside an entity.

For fine-tuning training, we just need data in the BIO format, so just the
token and the NER tag. Here's an example of the German-language legal case
NER task:

Source: https://blog.codecentric.de/en/2020/12/ner-with-little-data-transformers-to-the-rescue/

         1. an O
         2. Kapitalgesellschaften O
         3. ( O
         4. § B-GS
         5. 17 I-GS
         6. Abs. I-GS
         7. 1 I-GS
         8. und I-GS
         9. 2 I-GS
        10. EStG I-GS
        11. ) O

Okay enough NER token and classification descriptions. Now for fine tuning.

A few things need to be done.

1) Tag training data

I need to convert my OCR'd case documents into streams of NER labeled tokens.
This will get us a stream of tokens and NER tags. I'll need to add new
labels for the officer subject phrases.

        Label   Description
        ------- ---------------------------------
        B-OFF   Begin subject officer, e.g. "Officer John Smith"
        I-OFF   Inner subject officer
        B-DATE  Begin date, e.g. "Dec 24, 2021"
        I-DATE  Inner date
        B-OUT   Begin outcome, e.g. "Written Reprimand"
        I-OUT   Inner outcome
        B-ALEG  Begin allgation, e.g. "Misuse of property"
        I-ALEG  Inner allegation

TODO: I have tagged sequences like this (in a `ner-data.json`):

    "file_data" [{
      "name": "path/to/file.ext",
      "data": [
        {
          "id":123,
          "text":"Wednesday",
          "label":"DDATE"
        },
        {
          "id":124,
          "text":",
          ",
          "label":"DDATE"
        },
        {
          "id":125,
          "text":"&nbsp"
        },
        {
          "id":126,
          "text":"November",
          "label":"DDATE"
        },
        {
          "id":127,
          "text":"&nbsp"
        },
        {
          "id":128,
          "text":"13",
          "label":"DDATE"
        },
        {
          "id":129,
          "text":",
          ",
          "label":"DDATE"
        },
        {
          "id":130,
          "text":"&nbsp"
        },
        {
          "id":131,
          "text":"2019",
          "label":"DDATE"
        },
        {
          "id":132,
          "text":"&nbsp"
        },
        {
          "id":133,
          "text":"4",
          "label":"DDATE"
        },
        {
          "id":134,
          "text":":",
          "label":"DDATE"
        },
        {
          "id":135,
          "text":"46",
          "label":"DDATE"
        },
        {
          "id":136,
          "text":":",
          "label":"DDATE"
        },
        {
          "id":137,
          "text":"30",
          "label":"DDATE"
        },
        {
          "id":138,
          "text":"&nbsp"
        },
        {
          "id":139,
          "text":"PM",
          "label":"DDATE"
        },
        {
          "id":140,
          "text":"&nbsp"
        },
        {
          "id":141,
          "text":"LINE-BREAK"
        }
      ]
    }, ...]

And will need to parse them, doing the following:

- skipping whitespace-only, `&nbsp` and `LINE-BREAK` tokens
- stripping token text
- converting tags to B- and I- prefixed tags, based on sequences

2) We need to compute the new full tokens list:

    cat test.txt train.txt valid.txt | cut -d " " -f 2 | grep -v "^$"| sort | uniq > labels.txt

3) Train

    python run_ner.py \
            --data_dir=data/ \
            --bert_model=bert-large-cased \
            --task_name=ner \
            --output_dir=out_large \
            --max_seq_length=128 \
            --num_train_epochs 5 \
            --do_train \
            --do_eval \
            --warmup_proportion=0.1
