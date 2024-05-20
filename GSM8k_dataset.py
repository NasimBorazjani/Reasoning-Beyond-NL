import json
import os
import re
import random

random.seed(0)

def read_jsonl(path: str):
    with open(path) as fh:
        lines = fh.readlines()[14:]
        random.shuffle(lines)
        return {i : json.loads(lines[i]) for i in range(len(lines)) if lines[i]}
    

ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")
INVALID_ANS = "[invalid]"

def extract_answer(completion):
    match = ANS_RE.search(completion)
    if match:
        match_str = match.group(1).strip()
        match_str = match_str.replace(",", "")
        return match_str
    else:
        return INVALID_ANS
    

def get_problems(split):
    path = os.path.join("grade-school-math/grade_school_math/data", f"{split}.jsonl")
    examples = read_jsonl(path)
    problems = {}

    for id, ex in examples.items():
        ex.update(question=ex["question"] + "\n")
        ex.update(answer=extract_answer(ex["answer"]))
        problems[id] = ex

    print(f"{len(problems)} {split} problems")
    return problems

 




