import json
import os
import re
import random
import math

random.seed(0)

def read_json(path: str):
    f = open(path)
    data = json.load(f)
    data_dict = {}
    random.shuffle(data['examples'])
    for i in range(len(data['examples'])):
        example = data['examples'][i]
        exmaple_dict = {}
        exmaple_dict["Instructions"] = example['input']
        exmaple_dict["Difficulty"] = example['n_sentences']
        exmaple_dict["Answer"] = example['target_scores']['True']
        exmaple_dict["Inst_type"] = example["inst_type"]
        data_dict[i] = exmaple_dict
    
    return data_dict
    

Test_split = 300
path = "/Users/nasimb/Desktop/prolog+gpt3/navigate_task.json"

  

def get_examples(split, igonre_lower_ids, number):
    examples = calculate_dist()
    if split == "test":
        return examples[-Test_split:]
    
    examples_cut = {}
    for id, ex in examples.items():
        if id >= igonre_lower_ids and id<number:
            examples_cut[id] = ex

    print(f"{len(examples_cut)} {split} problems")
    return examples_cut




def get_all_insstructions():
    examples = get_examples("train", 0, 500)
    instructions_set = set()
    for _, example in examples.items():
        inst = example["Instructions"].split(".")
        for e in inst:
            instructions_set.add(e)
    print(instructions_set)
    
    
    
def calculate_dist():
    examples = read_json(path)    
    for _, example in examples.items():
        vertical_c = 0
        horizontal_c = 0
        direction = 0
        instructions = example["Instructions"].split(".")
        for inst in instructions:
            if "Take" in inst:
                if "forward" in inst:
                    direction  = 0
                elif "right" in inst:
                    direction = 1
                elif "left" in inst:
                    direction = 3
                elif "backward" in inst:
                    direction = 2

                num_str = re.findall(r'\d+', inst)
                num_steps = list(map(int, num_str))[0]
                
                if direction == 0:
                    vertical_c += num_steps
                elif direction == 1:
                    horizontal_c += num_steps
                elif direction == 2:
                    vertical_c -= num_steps
                elif direction == 3:
                    horizontal_c -= num_steps


            elif "Turn left" in inst:
                direction = (direction - 1) % 4
            elif "Turn right" in inst:
                direction = (direction + 1) % 4
            elif "Turn around" in inst:
                direction = (direction + 2) % 4
        
        dist = round(math.sqrt((vertical_c ** 2 + horizontal_c ** 2)))
        example["Distance"] = dist
    
    return examples

