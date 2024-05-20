import re
from openai import OpenAI
from Navigate_dataset import get_examples
import pytholog as pl
import subprocess
from threading import Timer
import time
import argparse



prompt_examples = """In the following problems, our goal is to follow the instructions given and calculate the distance of our final position relative to our starting position. We do this by following the given instructions step by step, and then return the distance of the final position from the starting point as an integer after the last instruction (use round to convert float to int) in the end. 

"Take 1 step. Take 2 steps. Take 3 steps. Turn around. Take 6 steps. Turn left."

"Take 1 step." - We move 1 step forward.
"Take 2 steps." - We move 2 steps forward. So far, we’ve moved 3 steps forward in total.
"Take 3 steps." - We move 3 steps forward. We’ve moved 6 steps forward in total now.
"Turn around." - We turn around 180 degrees. Our direction is now opposite to the original direction.
“Take 6 steps." - We move 6 steps in the opposite direction. Thus, now we’ve moved back to your original position.
“Turn left." - We turn left but don't move. 

So, our final position is the same as our starting position. Therefore, the distance of our final position relative to our starting position is 0. The answer is /boxed/0.


"Always face forward. Take 3 steps right. Take 7 steps right. Take 4 steps right. Take 8 steps backward."

"Always face forward." - We are instructed to keep our orientation constant. 
"Take 3 steps right." - We move 3 steps to the right. 
"Take 7 steps right." - We move 7 steps to the right. So now we’ve moved 10 steps to the right.
"Take 4 steps right." - We move 4 steps to the right. We’ve moved 14 steps to the right in total.
"Take 8 steps backward." - We move 8 steps backward. Thus, now we’ve moved 14 steps to the right and 8 backwards from our original position.

Therefore, our final position is 14 steps to the right and 8 steps to the south of the starting point. Using the pythagorean theorem we can calculate the distance, which is round(sqrt(14^2 + 8^2)) = 16. The answer is /boxed/16.


“Turn left. Turn left. Take 6 steps. Take 3 steps. Turn around. Take 1 step. Take 3 steps. Take 5 steps.”

"Turn left." - We turn left but don't move.
"Turn left." - We turn left again but still don't move. Now we are facing the opposite direction from the start.
"Take 6 steps." - We move 6 steps backwards.
"Take 3 steps." - We move 3 steps in the same direction. So far, we’ve moved 9 steps backwards.
"Turn around." - We turn around 180 degrees. Our direction is now the original direction.
“Take 1 step." - We move 1 step forward. Thus, now we’ve moved 8 steps backwards.
“Take 3 steps." - We move 3 steps forward. Thus, now we are 5 steps back from our starting position.
“Take 5 steps." - We move 5 steps forward. Thus, now we’ve moved back to our original position.

So, our final position is the same as our starting position. Therefore, the distance of our final position relative to our starting position is 0. The answer is /boxed/0.


“Always face forward. Take 4 steps forward. Take 9 steps backward. Take 3 steps left. Take 10 steps backward. Take 6 steps forward. Take 8 steps forward. Take 1 step forward. Take 10 steps right. Take 7 steps left.”

"Always face forward." - We are instructed to keep our orientation constant. 
"Take 4 steps forward." - We move 4 steps forward.
"Take 9 steps backward." - We move 9 steps backward. So now we’ve moved 5 steps backward from our original position.
"Take 3 steps left." - We move 3 steps to the left. Now we are 5 steps backward and 3 steps to the left from our original position.
"Take 10 steps backward." - We move 10 steps backward. We are now 15 steps backward and 3 steps to the left from our original position.
"Take 6 steps forward." - We move 6 steps forward. So now we are 9 steps to the back and 3 steps to the left from our original position.
"Take 8 steps forward." - We move 8 steps forward. We are now 1 step to the back and 3 steps to the left from our original position.
"Take 1 step forward." - We move 1 step forward. Thus, now we are 3 steps to the left from our original position.
"Take 10 steps right." - We move 10 steps to the right. We are 7 steps to the right from our original position currently.
"Take 7 steps left." - We move 7 steps to the left. Thus, now we are 5 steps back from our starting position.

Therefore, the final position is the same as our starting position. Therefore, the distance of our final position relative to our starting position is 0. The answer is /boxed/0.

Follow the instructions below step by step in the same format. The answer must be an integer indicating our distance from the starting position. The final answer must be reported immediately after the phrase ‘/boxed/’

#####

"""


def get_oai_reponse(final_prompt, model):
    if model == "GPT4":
        model = "gpt-4"
    elif model == "GPT3.5":
        model = "gpt-3.5-turbo"
    response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": final_prompt
        }
    ],
    temperature=0,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    response = response.choices[0].message.content
    
    return response
        

def get_llm_solution(problem, model):
    final_prompt = prompt_examples.replace("#####", '"' + problem + '"')
    
    # Try to get openai's response 5 times, then give up
    tries = 5
    while tries >= 0:
        try:
            response = get_oai_reponse(final_prompt, model)
            break
        except:
            if tries == 0:
                raise 
            else:
                # Wait a few seconds before retrying 
                time.sleep(6) 
                tries -= 1
                continue
    
    try:
        answer_index = response.index("/boxed/") + 7
        number_str = response[answer_index:]
        answer_llm_list = re.findall(r'\d+', number_str)
        if answer_llm_list:
            correct_format = True
            answer_llm = answer_llm_list[0]
            if response[answer_index] == "-":
                answer_llm = "-" + answer_llm
        else:
            correct_format = False

    except ValueError:
        correct_format = False
    
    if not correct_format:    
        answer_llm = -1
        
    return correct_format, response, answer_llm
    
    
def main():
    parser = argparse.ArgumentParser(description='This script evaluates the end-to-end text-based performance of GPT4 or GPT3.5 Turbo on the Navigate task (modified to ask for final distance).')
    parser.add_argument('OAI_key', type=str, help='Your OpenAI API key.')
    parser.add_argument('model', type=str, choices=['GPT4', 'GPT3.5'], help='Name of the model you want to do inference on, either GPT4 or GPT3.5.')
    parser.add_argument('--print', type=str, choices=['True', 'False'], default='True', nargs='?', help='If set to True, the script will print a statemnt about the result of each call to the model')

    args = parser.parse_args()
    
    global client
    client = OpenAI(
    api_key=args.OAI_key,
    )
    model = args.model
    global print_progress
    print_progress = args.print

    log_file = f"{model}_navigate_text.txt"
    problem_num = 1000
    ignore_num = 10
    
    problems = get_examples("train", ignore_num, problem_num)
    count_correct = 0
    incorrect_format = {}
    incorrect_ids_difficulty = {}
    
    for id, problem in problems.items():
        correct_format, complete_answer, answer_llm = get_llm_solution(problem["Instructions"], model)
        if not correct_format:
            incorrect_format[id] = complete_answer
            
        if answer_llm == str(problem["Distance"]):
            count_correct += 1
            if print_progress:
                print(str(count_correct) + " out of " + str(id + 1 - ignore_num) + " is correct.")
            
            f = open(log_file, "a")
            f.write(str(id) + "\n" + str(problem) + "\n")
            f.write(str(complete_answer)+ "\n")
            f.write("Correct LLM asnwer: " + str(answer_llm) + "\n")
            f.write("problem difficulty: " + str(problem["Difficulty"])+ "\n\n\n\n")
            f.close()

        else:
            if print_progress:
                print("incorrect llm_solution: " + str(answer_llm) + "  actual_solution " + str(problem["Distance"]))
            incorrect_ids_difficulty[id] = {"Difficulty": problem["Difficulty"], "Type": problem["Inst_type"]}
        
            f = open(log_file, "a")
            f.write(str(id) + "\n" + str(problem) + "\n")
            f.write(str(complete_answer)+ "\n")
            f.write("LLM asnwer extracted: " + str(answer_llm) + "\n")
            f.write("Actual asnwer: " + str(problem["Distance"]) + "\n")
            f.write("problem difficulty: " + str(problem["Difficulty"])+ "\n\n\n\n")
            f.close()
    
    #log problems that were not solved due to incorrect formatting
    f = open(log_file, "a")   
    f.write("\n" + "-"*50 + "\n")
    f.write("Incorrect formats")
    f.write("\n" + "-"*50 + "\n")
    for id in incorrect_format:
        f.write(str(id) + " ")
        f.write(str(incorrect_format[id]) + "\n")
        
    #ids of problems that got incorrect solutions
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("Incorrect ids and the difficulty of the problem")
    f.write("\n" + "-"*50 + "\n")
    for i, s in incorrect_ids_difficulty.items():
        f.write(str(i) + " : " + str(s) + "\n")


    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("stats")
    f.write("\n" + "-"*50 + "\n")
    f.write(str(problem_num - ignore_num - len(incorrect_ids_difficulty)) + " out of " + str(problem_num - ignore_num) + " is correct.")
    f.close()
    
    
main()


    
