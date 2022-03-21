# BERT NER

BERT named entity recognition (NER) with an emphasis on fine-tuning using my [NER labeler tool](https://github.com/brandonrobertz/ner-labeler) and ease-of-use (Docker). Forked from Kamal Raj's [original repo](https://github.com/kamalkraj/BERT-NER).

## Requirements

- `python3`
- `pip3 install -r requirements.txt`

## Training

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

More information about getting prepared for fine-tuning BERT NER models can be found in `data-notes-fine-tuning.md`.

# Pre-Trained Models

- [BERT-BASE](https://1drv.ms/u/s!Auc3VRul9wo5hghurzE47bTRyUeR?e=08seO3)
- [BERT-LARGE](https://1drv.ms/u/s!Auc3VRul9wo5hgr8jwhFD8iPCYp1?e=UsJJ2V)

To use one of the models, download it and then set the `--output_dir` argument to the path containing the directory with the model in it as found in the archive. The bert large model is found in a directory called `out_large`.

Average relative results:

```
                     precision    recall  f1-score   support
Bert-Base Test          0.9065    0.9209    0.9135      5648
Bert-Base Validation    0.9456    0.9534    0.9495      5942
Bert-Large Test         0.9121    0.9232    0.9174      5648
Bert-Large Validation   0.9531    0.9606    0.9568      5942
```

# Inference via CLI/Script

```python
from bert import Ner

model = Ner("out_base/")

output = model.predict("Steve went to Paris")

print(output)
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
```

# Inference via REST-API

BERT NER model deployed as rest api

```bash
python api.py
```

API will be live at `0.0.0.0:8000` endpoint `predict`

#### cURL request

` curl -X POST http://0.0.0.0:8000/predict -H 'Content-Type: application/json' -d '{ "text": "Steve went to Paris" }'`

Output

```json
{
    "result": [
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
}
```
