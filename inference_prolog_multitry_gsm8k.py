import re
from openai import OpenAI
from GSM8k_dataset import get_problems
import pytholog as pl
import subprocess
from threading import Timer
import time
import argparse



prompt = """The goal is to solve math word problems by converting natural language statements of the problem to prolog statements. The numerical values of the entities in the statement are encoded in prolog variables with units or coefficients without units. The relationship between the variables and coefficients is expressed as a set of equalities in a function called “problem”. It is important to note that the goal is to describe the problem statements, not to solve the resulting linear equations.
Variable names are a brief description of the entity in the problem; and all variable names end with the unit of the entity. The name assigned to entities that have different numerical values must be different. Variables in an arithmetic statement in the “problem” function must have compatible units. 


"James writes a 3-page letter to 2 different friends twice a week.  How many pages does he write a year?",

problem(James_writes_pages_per_year) :-
{James_writes_pages = 3,
James_friends_number = 2,
James_writes_per_week = 2,
%James writes 3 pages to each of his 2 friends and he does this two times per week. So the total number of pages he write per week is:
James_writes_pages_per_week = James_writes_pages * James_friends_number * James_writes_per_week,
% We know that James writes the same number of pages each week for a year and there are 52 weeks in a year, thus the number of pages James writes per year is:
James_writes_pages_per_year = James_writes_pages_per_week * 52}.


"Albert is wondering how much pizza he can eat in one day. He buys 2 large pizzas and 2 small pizzas. A large pizza has 16 slices and a small pizza has 8 slices. If he eats it all, how many pieces does he eat that day?"

problem(Total_eaten_slices) :-
{Large_pizza_number = 2,
Small_pizza_number = 2,
Large_pizza_slices = 16,
Small_pizza_slices = 8,
%Albert bought 2 large pizzas, and we know that each of the large pizzas have 8 slices. Thus the total number of slices Albert eats from large pizzas is:
Total_large_pizza_slices = Large_pizza_number * Large_pizza_slices
%And the total number of slices Albert eats from small pizzas is:
Total_small_pizza_slices = Small_pizza_number * Small_pizza_slices
%Albert eats all of the slices from the large pizzas plus all of the slices from the small pizzas
Total_eaten_slices = Total_large_pizza_slices + Total_small_pizza_slices}.


"Mark has a garden with flowers. He planted plants of three different colors in it. Ten of them are yellow, and there are 80% more of those in purple. There are only 25% as many green flowers as there are yellow and purple flowers. How many flowers does Mark have in his garden?"

problem(Total_flowers_number) :-
{Yellow_flowers_number = 10,
%Number of purple flowers is 80% more than number of yellow flowers, which means if we subtract the number of yellow flowers from purple flowers, we get 80% of the number of yellow flowers
Purple_flowers_number - Yellow_flowers_number = 0.8 * Yellow_flowers_number,
%Number of green flowers is 25% of the number of yellow and purple flowers together.
Green_flowers_number = 0.25 * (Yellow_flowers_number + Purple_flowers_number),
% The flowers in Mark’s garden are composed of the yellow, purple and green flowers. Thus the total number of flowers in Mark’s garden is equal to the sum of the three flower counts. 
Total_flowers_number = Yellow_flowers_number + Purple_flowers_number + Green_flowers_number}.


"Ken created a care package to send to his brother, who was away at boarding school.  Ken placed a box on a scale, and then he poured into the box enough jelly beans to bring the weight to 2 pounds.  Then, he added enough brownies to cause the weight to triple.  Next, he added another 2 pounds of jelly beans.  And finally, he added enough gummy worms to double the weight once again.  What was the final weight of the box of goodies, in pounds?"

problem(Final_box_weight_time4_pounds) :-
{%The weight of the box with the jelly beans is 2 pounds initially (time1)
Jelly_box_weight_time1_pounds = 2,
%Ken added enough brownies to triple the weight of the box, so the weight of the box with the brownies added at time2 is described as:
Brownies_box_weight_time2_pounds = 3 * Jelly_box_weight_time1_pounds,
More_jelly_beans_pounds = 2,
%He added 2 more pounds of jelly beans, so the box weight at time3 is:
More_jelly_box_weight_time3_pounds = Brownies_box_weight_time2_pounds + More_jelly_beans_pounds,
%Finally he added enough gummy worms to double the total weight of the box once again. Thus the final weight of the box at time4 is:
Final_box_weight_time4_pounds = 2 * More_jelly_box_weight_time3_pounds}.


"Tina makes $18.00 an hour.  If she works more than 8 hours per shift, she is eligible for overtime, which is paid by your hourly wage + 1/2 your hourly wage.  If she works 10 hours every day for 5 days, how much money does she make?"

problem(Total_wage_dollars) :-
{Wage_dollars_per_hour = 18,
%Tina’s overtime pay is equal to her hourly wage + 1/2 her hourly wage
Overtime_wage_dollars_per_hour = Wage_dollars_per_hour + (Wage_dollars_per_hour * 1/2),
Regular_shift_hours_number = 8,
Shift_hours = 10,
%The number of hours Tina gets paid with overtime wage is the number hours she works after her regular 8 hour shift ends
Overtime_hours = Shift_hours - Regular_shift_hours_number,
%The total money she earns from working overtime is equal to her overtime wage per hour times the number of hours she works overtime.
Overtime_wage_per_day = Overtime_wage_dollars_per_hour * Overtime_hours,
Regular_wage_per_day = Wage_dollars_per_hour * Regular_shift_hours_number,
%The total money she earns each day is the sum of her regular shift earnings and overtime earnings.
Money_per_day = Regular_wage_per_day + Overtime_wage_per_day
Days_working_number = 5,
%We know that Tina works for 5 Days and she gets paid the same amount each day, thus the total amount of money she earns is described as:                                                                                                                           
Total_money_dollars = Days_working_number * (Regular_wage_per_day + Overtime_wage_per_day)}.


"Central Park had 8 more than half of the number of trash cans as in Veteran's Park.  Then one night, someone took half of the trash cans from Central Park and put them in Veteran's Park.  If originally there were 24 trash cans in Veteran's Park, how many trash cans are now in Veteran's Park?”

problem(Veterans_park_cans_now_number) :-
{Veterans_park_cans_original_number = 24,
%Originally, Central Park had 8 more than half of the initial number of trash cans in Veteran's Park, thus if we subtract 8 from the original (before the replacement) number of trash cans in Central park we get:
Central_park_cans_original_number - 8 = Veterans_park_cans_original_number / 2,
%Then one night, someone took half of the trash cans of Central Park
Trash_cans_taken_number = Central_park_cans_original_number / 2,
%The trash cans were removed from Central park. Thus the current number of trash cans in Central park is:
Central_park_cans_now_number = Central_park_cans_original_number - Trash_cans_taken_numbe,
%The person transferred the trash cans taken from Central park to the Veteren's park. Thus the current number of trash cans in Veteren's Park after the transfer is:
Veterans_park_cans_now_number = Veterans_park_cans_original_number + Trash_cans_taken_number}.


“Liz sold her car at 80% of what she originally paid. She uses the proceeds of that sale and needs only $4,000 to buy herself a new $30,000 car. How much cheaper is her new car versus what she originally paid for her old one?”

problem(Amount_new_car_is_cheaper_dollars) :-
{New_car_price_dollars = 30000,
Extra_money_needed_dollars = 4000,
% Liz sold her old car and used the money to buy a new car. She needed an additional $4000 to buy the new car. Thus the price of the new car is equal to the price she sold her old car for plus the additional $4000 she needed.
Old_car_sale_price_dollars = New_car_price_dollars - Extra_money_needed_dollars,
% We know that the money Liz got for selling her old car is 80% of the car's original price.
Old_car_sale_price_dollars = 0.8 * Old_car_original_price_dollars,
% We are told that her new car is cheaper than her old car. We can determine by how much her new car is cheaper by subtracting the price of ner new car from the original price of her old car.
Amount_new_car_is_cheaper_dollars = Old_car_original_price_dollars - New_car_price_dollars}.


"A deep-sea monster rises from the waters once every hundred years to feast on a ship and sate its hunger. Over three hundred years, it has consumed 847 people. Ships have been built larger over time, so each new ship has twice as many people as the last ship. How many people were on the ship the monster ate in the first hundred years?"

problem(First_ship_size) :-
{People_eaten_per_300_years = 847,
Ship_size_ratio = 2,
%The monster eats a ship every a hundred years, and we know that he ate 874 people in 300 years. Thus he ate the people aboard 3 ships during this time. Also we know that the size of the ships doubles every 100 years, thus the size of the ship the monster ate during the second 100 years is twice the size of the first ship he ate
Second_ship_size = First_ship_size * 2,
%And the size of the third ship is twice the size of the second ship
Third_ship_size = Second_ship_size * 2,
% The number of people the monster ate during the 300 years is equal to the sum of the number of the people aboard these three ships
People_eaten_per_300_years = First_ship_size + Second_ship_size + Third_ship_size}.


Solve the below problem in the same format by encoding the problem as prolog equalities step by step. Each equality either assigns a numerical value to a variable or describes the relationship between variables. Completion must end in ‘}.’

#####

"""
prolog_code = """:- use_module(library(clpq)).

:- initialization main.

:- set_prolog_flag(verbose, silent).

:-style_check(-singleton).

:-style_check(-discontiguous).

main :-
    problem(Answer),
    write(Answer),
    halt.

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
        code_begin_index = response.index("problem(")
        code_end_index = response.index("}.")
        code_llm = response[code_begin_index:code_end_index + 2]
        code = prolog_code + code_llm
        f = open("result.pl", "w")
        f.write(code)
        f.close()    
        correct_format = True

    except ValueError:
        correct_format = False
        code_llm = response
        
    return correct_format, code_llm
    

def run_llm_prolog_result():
    kill = lambda process: process.kill()
    cmd = ['swipl', 'result.pl']
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
                  reached_max_tries, reached_max_tries_ids, repeat_max,
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
    f.write(str(count_correct) + " out of " + str(problem_num) + " is correct.")
    f.close()
   
   
def record(id, log_file, prolog_solution, problem, code_llm, repeated = None, corrected = False):
    f = open(log_file, "a")
    f.write("ID: " + str(id) + "\n" + str(problem) + "\n")
    if repeated:
        f.write("repeated: " + str(repeated) + "\n")
    else:
        f.write("NOT repeated \n")
    if corrected:
        f.write("Corrected!!!" + "\n")
    f.write(str(code_llm)+ "\n")
    f.write("prolog run result: " + str(prolog_solution) + " problem answer: " + str(problem["answer"]) + "\n\n\n\n")
    f.close()
    

    
def main():
    parser = argparse.ArgumentParser(description='This script evaluates GPT4 or GPT3.5 Turbo on the GSM8k dataset, using our neurosymbolic Prolog augmented approach.')
    parser.add_argument('OAI_key', type=str, help='Your OpenAI API key.')
    parser.add_argument('model', type=str, choices=['GPT4', 'GPT3.5'], help='Name of the model you want to do inference on, either GPT4 or GPT3.5.')
    parser.add_argument('--print', type=str, choices=['True', 'False'], default='True', nargs='?', help='If set to True, the script will print a statement about the result of each call to the model')

    args = parser.parse_args()
    
    global client
    client = OpenAI(
    api_key=args.OAI_key,
    )
    model = args.model
    global print_progress
    print_progress = args.print

    log_file = f"{model}_multiTry_gsm8k_prolog.txt"
    repeat_max = 50
    total_number_calls = 0
    reached_max_tries = 0
    reached_max_tries_ids = []
    corrected_after_multiple_try = 0
    incorrect_after_multiple_try = 0
    temp_at_max = 0.4
    
    problems = get_problems("test")
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
            correct_format, code_llm = get_llm_solution(problem["question"], model, prompt, temp)
            total_number_calls += 1
            
            if correct_format:
                prolog_solution, cancelled = run_llm_prolog_result()
                if cancelled or "_" in prolog_solution or "r" in prolog_solution or "?" in prolog_solution:
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
        if prolog_solution == problem["answer"]:
            count_correct += 1
            if print_progress:
                print(str(count_correct) + " out of " + str(id + 1) + " is correct.")
            
            if repeated > 0:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated, corrected = True)
                corrected_after_multiple_try += 1
                if print_progress:
                    print("corrected after more than 1 try, total corected after multiple treis count: " + str(corrected_after_multiple_try))
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)


        else:
            if print_progress:
                print("incorrect llm_solution: " + str(prolog_solution) + "  actual_solution " + problem["answer"])
            incorrect_ids.append(id)
            record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)

            if repeated > 0:
                incorrect_after_multiple_try += 1
                if print_progress:
                    print("incorrect after more than 1 try, total incorrect after multiple treis count: " + str(incorrect_after_multiple_try))
            else:
                record(id, log_file, prolog_solution, problem, code_llm, repeated = repeated)


    final_record(log_file, incorrect_format, incorrect_ids, len(problems), 
                  reached_max_tries, reached_max_tries_ids, repeat_max,
                 corrected_after_multiple_try, incorrect_after_multiple_try, 
                 temp_at_max, total_number_calls, count_correct)
     
    print(str(count_correct) + " out of " + str(len(problems)) + " is correct.")        
     


main()


    
