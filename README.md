
# Reliable Reasoning Beyond Natural Language


## Requirements

To install python requirements:

```setup
pip install -r requirements.txt
```

To install SWI-Prolog:
```setup
sudo apt-get install swi-prolog
```

To download the GSM8k dataset, clone the repository below in the project folder:
```
git clone https://github.com/openai/grade-school-math.git
```

## GSM8K

Models prompted with our Prolog in-context learning examples, using our neurosymbolic inference approach, achieve the following performance on the GSM8k dataset:

| Model name         | GSM8k Dataset | 
| ------------------ |---------------- | 
| GPT4 + Prolog      |     94%         |     
| GPT3.5 + Prolog    |     80.4%       | 

To reproduce these results and evaluate the models on the GSM8k dataset, using our neurosymbolic Prolog augmented approach, run:

```
python inference_prolog_multitry_gsm8k.py [-h] your_openai_api_key {GPT4,GPT3.5} 
```

## Navigate Dataset


Models prompted with our Prolog in-context learning examples, using our neurosymbolic inference approach, achieve the following performance on the Navigate dataset (modified to ask for the final distance):

| Model name         | Navigate Dataset | 
| ------------------ |---------------- | 
| GPT4 + Prolog      |     99.5%         |     
| GPT3.5 + Prolog    |     98.7%       | 

To reproduce these results and evaluate the models on the NLR dataset, using our neurosymbolic Prolog augmented approach, run:

```
python inference_prolog_multitry_navigate.py [-h] your_openai_api_key {GPT4,GPT3.5} 
```

Models prompted with Chain of Thought examples in text achieve the following performance on the Navigate dataset:

| Model name         | Navigate Dataset | 
| ------------------ |---------------- | 
| GPT4 + Prolog      |     88.5%         |     
| GPT3.5 + Prolog    |     57.1%       | 

To reproduce these results and evaluate the models' end to end performance on the Navigate dataset, run:

```
python inference_text_navigate.py [-h] your_openai_api_key {GPT4,GPT3.5} 
```


## NLR Dataset

Models prompted with our Prolog in-context learning examples, using our neurosymbolic inference approach, achieve the following performance on the NLR dataset:

| Model name         | Math Word problems | Constraint Satisfaction | Algorithmic Instructions |
| ------------------ |---------------- | -------------- |-------------- |
| GPT4 + Prolog      |     100%         |     100%      |   66.7%    |
| GPT3.5 + Prolog    |     50%         |      41.7%     |   16.7%    |

To reproduce these results and evaluate the models on the NLR dataset, using our neurosymbolic Prolog augmented approach, run:

```
python inference_prolog_multitry_nlr.py [-h] your_openai_api_key {GPT4,GPT3.5} {MWP,CS,AI} 
```

Models prompted with Chain of Thought examples in text achieve the following performance on the NLR dataset:

| Model name         | Math Word problems | Constraint Satisfaction | Algorithmic Instructions |
| ------------------ |---------------- | -------------- |-------------- |
| GPT4       |     0%         |     0%      |  0%    |
| GPT3.5     |     0%         |      0%     |   0%    |

To reproduce these results and evaluate the models' end to end performance on the NLR dataset, run:

```
python inference_text_nlr.py [-h] your_openai_api_key {GPT4,GPT3.5} {MWP,CS,AI} 
```


## License

CC BY-SA
