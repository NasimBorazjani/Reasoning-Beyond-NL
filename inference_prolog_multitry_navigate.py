import re
from openai import OpenAI
from Navigate_dataset import get_examples
import pytholog as pl
import subprocess
from threading import Timer
import time
import argparse

prompt = """In the following problems, our goal is to follow the instructions given and calculate the distance of our final position relative to our starting position. To solve these problems, we encode the current direction and coordinates after each instruction in prolog language. The direction is encoded as degrees in our system. right is encoded as +90 in our system, left as 270, forward as 0 degrees, and backwards as 180. It’s important that if the instruction is about turning then we calculate the direction relative to our previous direction. Coordinates are encoded as X and Y position, and coordinates change only when we take steps.​ Our starting X and Y coordinates are always 0 and the starting direction is at 0 degrees. To update the coordinates we record the number of steps taken and our current direction at the time of the instruction, and then call the proccess_coordinates function. 

%If our direction is 0, then we are moving forward or in the positive X direction
process_coordinates(0, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old + Steps,
Y_new = Y_old}.


%If our direction is 90 degrees, then we are moving to the right or in the positive Y direction
process_coordinates(90, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old,
Y_new = Y_old + Steps}.


%If our direction is 0, then we are moving backwards or in the negative X direction
process_coordinates(180, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old - Steps,
Y_new = Y_old}.


%If our direction is 270 degrees, then we are moving to the left or in the negative Y direction
process_coordinates(270, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old,
Y_new = Y_old - Steps}.

After updating the coordinates and direction with the last instruction, we calculate the distance of our current position (which is the final position) to the starting point by calling the “distance” function. This function uses the pythagorean theorem on the final X and Y coordinates to calculate the distance. 

distance(X, Y, Distance) :-
Distance is round(sqrt(X ** 2 + Y ** 2)).


Follow these instructions. Return the distance of the final position from the starting position as a rounded integer.

"Take 1 step. Take 2 steps. Take 3 steps. Turn around. Take 6 steps. Turn left."

follow_instructions(Distance) :-
Direction_time0 is 0,
X_time0 is 0,
Y_time0 is 0,
%our first instruction is to take a step, so direction doesn't change relative to the starting direction and the number of steps is 1.
Direction_time1 is Direction_time0,
Steps_time1 is 1,
process_coordinates(Direction_time1, Steps_time1, X_time0, Y_time0, X_time1, Y_time1),
%Take 2 steps, direction doesn't change relative to previous direction.
Direction_time2 is Direction_time1,
Steps_time2 is 2,
process_coordinates(Direction_time2, Steps_time2, X_time1, Y_time1, X_time2, Y_time2),
%Take 3 steps, so direction doesn't change again.
Direction_time3 is Direction_time2,
Steps_time3 is 3,
process_coordinates(Direction_time3, Steps_time3, X_time2, Y_time2, X_time3, Y_time3),
%fourth instruction is to turn around, so we have to change the direction by 180 degrees relative to the previous direction. Coordinates don't change.
Direction_time4 is (Direction_time3 + 180) mod 360,
X_time4 is X_time3,
Y_time4 is Y_time3,
%fifth instruction is to take 6 steps, so direction doesn't change.
Direction_time5 is Direction_time4,
Steps_time5 is 6,
process_coordinates(Direction_time5, Steps_time5, X_time4, Y_time4, X_time5, Y_time5),
%Lastly turn left, so change the direction by 270 degrees relative to the previous direction. Coordinates don't change.
Direction_time6 is (Direction_time5 + 270) mod 360,
X_time6 is X_time5,
Y_time6 is Y_time5,
%After the last instruction, calculate the distance from the starting position
distance(X_time6, Y_time6, Distance).



"Always face forward. Take 3 steps right. Take 7 steps right. Take 4 steps right. Take 8 steps backward."

follow_instructions(Distance) :-
%We’re told to always face forward, so the direction of our steps are independent of our direction in the previous step. We pay attention to the direction given in each instruction: left, right, forward, backward
Direction_time0 is 0,
X_time0 is 0,
Y_time0 is 0,
%Take 3 steps to the right, so the direction is to the right which is 90 degrees, and the number of steps is 3.
Direction_time1 is 90,
Steps_time1 is 3,
process_coordinates(Direction_time1, Steps_time1, X_time0, Y_time0, X_time1, Y_time1),
%Take 7 steps right; the direction is to the right again, or +90 degrees.
Direction_time2 is 90,
Steps_time2 is 7,
process_coordinates(Direction_time2, Steps_time2, X_time1, Y_time1, X_time2, Y_time2),
%Take 4 steps, direction to the right again.
Direction_time3 is 90,
Steps_time3 is 4,
process_coordinates(Direction_time3, Steps_time3, X_time2, Y_time2, X_time3, Y_time3),
%Last instruction is to take 8 steps backwards, thus the direction at time 4 is backwards which is 180 degrees.
Direction_time4 is 180,
Steps_time4 is 8,
process_coordinates(Direction_time4, Steps_time4, X_time3, Y_time3, X_time4, Y_time4),
%After the last instruction, calculate the distance from the starting position
distance(X_time4, Y_time4, Distance).


“Turn left. Turn left. Take 6 steps. Take 3 steps. Turn around. Take 1 step. Take 3 steps. Take 5 steps.”

follow_instructions(Distance) :-
Direction_time0 is 0,
X_time0 is 0,
Y_time0 is 0,
%The first instruction is to turn left, so our direction changes by 270 degrees relative to the starting direction. Coordinates don’t change.
Direction_time1 is (Direction_time0 + 270) mod 360,
X_time1 is X_time0,
Y_time1 is Y_time0,
%Turn left. So our direction changes by -90 again relative to the previous direction. Coordinates don’t change.
Direction_time2 is (Direction_time1 + 270) mod 360,
X_time2 is X_time1,
Y_time2 is Y_time1,
%Take 6 steps; the direction doesn't change relative to the previous direction.
Direction_time3 is Direction_time2,
Steps_time3 is 6,
process_coordinates(Direction_time3, Steps_time3, X_time2, Y_time2, X_time3, Y_time3),
%Take 3 steps; the direction doesn't change relative to the previous direction.
Direction_time4 is Direction_time3,
Steps_time4 is 3,
process_coordinates(Direction_time4, Steps_time4, X_time3, Y_time3, X_time4, Y_time4),
%Fifth instruction is to turn around, so our direction changes by 180 degrees relative to the previous direction. Coordinates don’t change.
Direction_time5 is (Direction_time4 + 180) mod 360,
X_time5 is X_time4,
Y_time5 is Y_time4,
%Then take 1 step; the direction doesn't change relative to the previous direction
Direction_time6 is Direction_time5,
Steps_time6 is 1,
process_coordinates(Direction_time6, Steps_time6, X_time5, Y_time5, X_time6, Y_time6),
%Take 3 steps; the direction doesn't change
Direction_time7 is Direction_time6,
Steps_time7 is 3,
process_coordinates(Direction_time7, Steps_time7, X_time6, Y_time6, X_time7, Y_time7),
%Lastly take 5 steps; the direction doesn't change again
Direction_time8 is Direction_time7,
Steps_time8 is 5,
process_coordinates(Direction_time8, Steps_time8, X_time7, Y_time7, X_time8, Y_time8),
%After the last instruction, calculate the distance from the starting position
distance(X_time8, Y_time8, Distance).


“Always face forward. Take 4 steps forward. Take 9 steps backward. Take 3 steps left. Take 10 steps backward. Take 6 steps forward. Take 8 steps forward. Take 1 step forward. Take 10 steps right. Take 7 steps left.”

follow_instructions(Distance) :-
%We’re told to always face forward, so the direction of our steps are independent of our direction in the previous step.
Direction_time0 is 0,
X_time0 is 0,
Y_time0 is 0,
%Take 4 steps forward; the direction is forward or 0 degrees.
Direction_time1 is 0,
Steps_time1 is 4,
process_coordinates(Direction_time1, Steps_time1, X_time0, Y_time0, X_time1, Y_time1),
%Take 9 steps backwards; the direction is backwards or 180 degrees.
Direction_time2 is 180,
Steps_time2 is 9,
process_coordinates(Direction_time2, Steps_time2, X_time1, Y_time1, X_time2, Y_time2),
%Take 3 steps left, direction is to the left or 270 degrees.
Direction_time3 is 270,
Steps_time3 is 3,
process_coordinates(Direction_time3, Steps_time3, X_time2, Y_time2, X_time3, Y_time3),
%Take 10 steps backwards, thus the direction at time 4 is backwards or 180 degrees.
Direction_time4 is 180,
Steps_time4 is 10,
process_coordinates(Direction_time4, Steps_time4, X_time3, Y_time3, X_time4, Y_time4),
%Take 6 steps forwards; the direction is forwards or 0 degrees.
Direction_time5 is 0,
Steps_time5 is 6,
process_coordinates(Direction_time5, Steps_time5, X_time4, Y_time4, X_time5, Y_time5),
%Then take 8 step forward; the direction is 0 degrees
Direction_time6 is 0,
Steps_time6 is 8,
process_coordinates(Direction_time6, Steps_time6, X_time5, Y_time5, X_time6, Y_time6),
%Take 1 steps forward; the direction is 0 degrees
Direction_time7 is 0,
Steps_time7 is 1,
process_coordinates(Direction_time7, Steps_time7, X_time6, Y_time6, X_time7, Y_time7),
%Take 10 steps right; the direction is to the right or 90 degrees
Direction_time8 is 90,
Steps_time8 is 10,
process_coordinates(Direction_time8, Steps_time8, X_time7, Y_time7, X_time8, Y_time8),
%Lastly take 7 steps left; the direction is to the left or 270 degrees
Direction_time9 is 270,
Steps_time9 is 7,
process_coordinates(Direction_time9, Steps_time9, X_time8, Y_time8, X_time9, Y_time9),
%After the last instruction, calculate the distance from the starting position
distance(X_time9, Y_time9, Distance).


Follow the instructions below in the same format by encoding the direction and X and Y after each instruction as prolog statements step by step. The completion must be an executable prolog function that starts with ‘follow_instructions(Distance) :-’ and ends with a ‘.’

#####


"""
prolog_code = """:- use_module(library(clpq)).

:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    follow_instructions(At_first_pos),
    write(At_first_pos),
    halt.

process_coordinates(0, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old + Steps,
Y_new = Y_old}.

process_coordinates(90, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old,
Y_new = Y_old + Steps}.

process_coordinates(180, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old - Steps,
Y_new = Y_old}.

process_coordinates(270, Steps, X_old, Y_old, X_new, Y_new) :-
{X_new = X_old,
Y_new = Y_old - Steps}.

distance(X, Y, Distance) :-
Distance is round(sqrt(X ** 2 + Y ** 2)).

"""

def get_oai_reponse(final_prompt, model, temp):
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
    temperature=temp,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    response = response.choices[0].message.content
    
    return response
        

def get_llm_solution(problem, model, prompt_examples, temp):
    final_prompt = prompt_examples.replace("#####", '"' + problem + '"')
    
    # Try to get openai's response 5 times, then give up
    tries = 5
    while tries >= 0:
        try:
            response = get_oai_reponse(final_prompt, model, temp)
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
        code_begin_index = response.index("follow_instructions(Distance)")
        code_end_index = response.index("Distance).")
        code_llm = response[code_begin_index:code_end_index + 14]
        code = prolog_code + code_llm
        f = open("result_navigate.pl", "w")
        f.write(code)
        f.close()    
        correct_format = True

    except ValueError:
        correct_format = False
        code_llm = response
        
    return correct_format, code_llm
    

def run_llm_prolog_result():
    kill = lambda process: process.kill()
    cmd = ['swipl', 'result_navigate.pl']
    ping = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cancelled  = False
    #kill prolog if it takes more than 2 secs, would be due to failed initialization, ie the problem did not return a result
    my_timer = Timer(2, kill, [ping])
    try:
        my_timer.start()
        stdout, stderr = ping.communicate()
    finally:
        my_timer.cancel()
        if stderr.decode('ascii'):
            cancelled = True
        
    prolog_solution = stdout.decode('ascii')
    return prolog_solution, cancelled
    
     
def final_record(log_file, incorrect_format, incorrect_ids, problem_num, 
                 ignore_num, reached_max_tries, reached_max_tries_ids, repeat_max,
                 corrected_after_multiple_try, incorrect_after_multiple_try, 
                 temp_at_max, total_number_calls, count_correct):
    #log problems that were not solved due to incorrect formatting
    f = open(log_file, "a")   
    f.write("\n" + "-"*50 + "\n")
    f.write("Incorrect formats"+ "\n")
    for id in incorrect_format:
        f.write(str(id))
        f.write(str(incorrect_format[id]) + "\n")
        
    #ids of problems that got incorrect solutions
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("Incorrect ids" + "\n")
    f.write(str(incorrect_ids))
    
    #number of times prolog still didn't run after repeat max calls
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("Number of max tries"+ "\n")
    f.write(str(repeat_max))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Number of times prolog didn't run after repeat max tries"+ "\n")
    f.write(str(reached_max_tries))
   
    f.write("\n" + "-"*50 + "\n")
    f.write("Problem ids that prolog didn't run after max tries"+ "\n")
    f.write(str(reached_max_tries_ids))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Problem number that got correct solution after many tries"+ "\n")
    f.write(str(corrected_after_multiple_try))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Problem number with incorrect solution after many tries"+ "\n")
    f.write(str(incorrect_after_multiple_try))
    
    f.write("\n" + "-"*50 + "\n")
    f.write("Tempreture at the max repeat call number"+ "\n")
    f.write(str(temp_at_max))
    

    #total number of calls to LLM
    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("total number of calls to LLM"+ "\n")
    f.write(str(total_number_calls))

    f.write("\n\n")
    f.write("\n" + "-"*50 + "\n")
    f.write("stats"+ "\n")
    f.write(str(count_correct) + " out of " + str(problem_num - ignore_num) + " is correct.")
    f.close()
   
   
def record(id, log_file, prolog_solution, problem, code_llm, repeated = None, corrected = False):
    f = open(log_file, "a")
    f.write("ID: " + str(id) + "\n" + str(problem) + "\n")
    if repeated:
        f.write("repeated: " + str(repeated) + "\n")
    else:
        f.write("NOT repeated \n")
    if corrected:
        f.write("Corrected!!!!!" + "\n")
    f.write(str(code_llm)+ "\n")
    f.write("prolog run result: " + str(prolog_solution) + " actual_solution " + str(problem["Distance"]) + "\n\n\n\n")
    f.close()
    

    
def main():
    parser = argparse.ArgumentParser(description='This script evaluates GPT4 or GPT3.5 Turbo on the Navigate task using our neurosymbolic Prolog augmented approach.')
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

    log_file = f"{model}_multiTry_navigate_prolog.txt"
    
    problem_num = 1000
    ignore_num = 10
    repeat_max = 50
    total_number_calls = 0
    reached_max_tries = 0
    reached_max_tries_ids = []
    corrected_after_multiple_try = 0
    incorrect_after_multiple_try = 0
    temp_at_max = 0.4
    
    problems = get_examples("train", ignore_num, problem_num)
    count_correct = 0
    incorrect_format = {}
    incorrect_ids = []
    
    for id, problem in problems.items():
        
        repeated = 0
        #repeat if prolog didn't run
        while True:
            repeat = False
            #repeated 0 -> temp 0, repeated 50 -> temp 0.2
            temp = (temp_at_max * repeated)/repeat_max
            correct_format, code_llm = get_llm_solution(problem["Instructions"], model, prompt, temp)
            total_number_calls += 1
            
            if correct_format:
                prolog_solution, cancelled = run_llm_prolog_result()
                if (cancelled or "_" in prolog_solution or "r" in prolog_solution or
                    "?" in prolog_solution or not prolog_solution.isdigit()):
                    repeat = True
                    
            else:
                prolog_solution = None
                incorrect_format[id] = code_llm
                repeat = True

            #if format was correct and prolog ran then break
            if not repeat:
                break
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)
                if print_progress:
                    print("repeated: " + str(repeated) + " llm: " + str(prolog_solution))

                repeated += 1
                if repeated > repeat_max: 
                    reached_max_tries += 1
                    if print_progress:
                        print("reached max tries, total number of failed attmepts to run prolog: " + str(reached_max_tries))
                    reached_max_tries_ids.append(id)
                    break
                
        #prolog ran, check answer
        if int(prolog_solution) == problem["Distance"]:
            count_correct += 1
            if print_progress:
                print(str(count_correct) + " out of " + str(id + 1 - ignore_num) + " is correct.")
            
            if repeated > 0:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated, corrected = True)
                corrected_after_multiple_try += 1
                if print_progress:
                    print("corrected after more than 1 try, total corected after multiple treis count: " + str(corrected_after_multiple_try))
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)


        else:
            if print_progress:
                print("incorrect llm_solution: " + str(prolog_solution) + "  actual_solution " + str(problem["Distance"]))
            incorrect_ids.append(id)
            record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)

            if repeated > 0:
                incorrect_after_multiple_try += 1
                if print_progress:
                    print("incorrect after more than 1 try, total incorrect after multiple treis count: " + str(incorrect_after_multiple_try))
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)


    final_record(log_file, incorrect_format, incorrect_ids, problem_num, 
                 ignore_num, reached_max_tries, reached_max_tries_ids, repeat_max,
                 corrected_after_multiple_try, incorrect_after_multiple_try, 
                 temp_at_max, total_number_calls, count_correct)
    
    print(str(count_correct) + " out of " + str(problem_num - ignore_num) + " is correct.")

     


main()


    
