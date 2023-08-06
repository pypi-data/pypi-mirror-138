# LeafNLP - A package for domain specific natural language processing

This repository contains pipes and models of LeafNLP.

## Installation
Just simply run

```pip install leafnlp```

to install LeafNLP.

## Usage

```
from leafnlp.NER.BERT import ModelNER

ner_model = ModelNER(model_param="model_ner_bert_conll2003")

input_text = [{"text": "The storm hits New York."}]
output = ner_model.annotate(input_text)
```

## Available Models

|PL|Task|Model|model_param|Note|
|-|-|-|-|-|
|NER|NER|BERT|model_ner_bert_conll2003||
|NER|ED|BERT|model_ed_bert_maven2020||

- NER: Named Entity Recogonition.
- ED: Event Detection.

## Citation

If you use LeafNLP in your research, please cite 

```
Will be here.
```


## Acknowledgements
LeafNLP is maintained by the Leaf-AI-LAB at Stevens Institute of Technology.