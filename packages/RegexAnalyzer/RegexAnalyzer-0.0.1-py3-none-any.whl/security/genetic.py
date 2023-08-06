# Builtin imports
import time
import sys
import base64
from tqdm import tqdm 
import string as String 
import matplotlib.pyplot as plt

# Internal imports
import config
import root_pb2
from mutations import single_char_mutate, mult_mutate, crossover_mutate, trim_mutate
from timing import match_time, match_time, slowest_average_match_time, slowest_total_match_time
from seeding import generate_seeds, get_tokens


def cull(regex, generation, number_of_survivors):
    """
    Culls the least desireable inputs
    Only keeps the [number_of_survivors] slowest in the generation 
    """
    dict = {}
    ordered_generation = []
    for input in generation:
        if input != "":
            dict[input] = match_time(regex, input)
    sorted_inputs = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)
    for input in sorted_inputs:
        ordered_generation.append(input[0])
    # Keep slowest
    keepers = ordered_generation[:number_of_survivors]
    return keepers


def pump(regex, input):
    # print("PUMP:", input)
    trim = list(input)
    slowest_string = input
    slowest_so_far = 0

    for i in range(1, len(input) - 2):
        prime = trim[0:i - 1] + trim[i + 1:]
        if prime != '':
            prime = "".join(prime)
            time_taken_prime = match_time(regex, prime)
            if time_taken_prime >= slowest_so_far:
                slowest_so_far = time_taken_prime
                slowest_string = prime
    string = slowest_string
    m = 0
    i_star = 0
    j_star = 0
    for i in range(0, len(string) - 1):
        for j in range(i + 1, len(string) - 2):
            prime = string[0:i - 1] + string[i:j] * 2 + string[j + 1:]
            if match_time(regex, prime) >= m:
                m = match_time(regex, prime)
                i_star = i
                j_star = j
    k = (config.max_len - len(string)) // (j_star - i_star + 1)
    # creating pump section of final_string
    # print("K", k)
    pumped_string = ""
    if k > 1:
        pumped_string = "".join(string[i_star:j_star])
    final_string = "".join(string[0:i_star - 1] + pumped_string * k + string[j_star + 1:])
    # print("PUMP OUT:", final_string)
    return final_string


def generator(i, iterations, timed_out):
    while i<iterations and timed_out == False:
        yield


def evaluate_regex(regex_protobuf: root_pb2.Expression, iterations) -> root_pb2.Output:
    evolutionary_track = []
    potential_generation = []
    regex = regex_protobuf.raw
    tokens = get_tokens(regex_protobuf)
    generation = generate_seeds(tokens)
    allowed_characters = String.printable 
    output = root_pb2.Output()

    i = 0
    timed_out = False 
    # for _ in tqdm(generator(i, iterations, timed_out)):
    # for i in tqdm(range(iterations)):
    while i<iterations and timed_out == False:

        # --- MUTATE --- 
        for j in range(len(generation) - 1):
            new_mutation = single_char_mutate(generation[j], allowed_characters, 3)
            new_crossover, new_crossover_2 = crossover_mutate(generation[j], generation[j + 1])
            rand_mutation = mult_mutate(generation[j], allowed_characters) 
            potential_generation.append(new_mutation)
            potential_generation.append(new_crossover)
            potential_generation.append(new_crossover_2)
            potential_generation.append(rand_mutation)

        potential_generation = potential_generation + generation # add the old generation 
        potential_generation.append(mult_mutate(generation[-1], allowed_characters))
        potential_generation.append(single_char_mutate(generation[-1], allowed_characters, 3))

        # check for timeout 
        current_worst_string, current_worst_time = slowest_total_match_time(regex, generation)
        evolutionary_track.append(current_worst_time)
        if current_worst_time == config.timeout:
            timed_out = True 
            print("Your regex took longer than", config.timeout, "seconds to match", current_worst_string)

        # print results for testing 
        if (i % 100 == 0):
            print("----- Generation", str(i), "-----")
            print("  ", current_worst_string)
            print("  ", current_worst_time)

        # --- PUMP ---
        # if i % 1000 == 0 and i != 0:
        #     for input in generation:
        #         if input != '':
        #             potential_generation.append(pump(regex, input))

        # --- CULL --- 
        if timed_out==False:
            generation = cull(regex, potential_generation, config.number_of_survivors)
            potential_generation = []

        i += 1 

    # --- FINAL PUMP --- 
    print("----- Pumping -----")
    worst_strings_list = []
    worst_times_list = []
    for string in tqdm(generation):
        # only pump if you haven't timed out 
        if timed_out == False:
            string = pump(regex, string)
        worst_strings_list.append(string)
        worst_times_list.append(match_time(regex, string))


    # TODO 
    # These are just example outputs, showing how you guys can use the Output functionality

    for i in range(len(worst_strings_list)):
        a = output.annotations.add()
        a.entity = worst_strings_list[i]
        a.note = f"This string gave the expression a run time of {worst_times_list[i]} seconds"

    if timed_out==True:
        output.status = "No vulnerability found"
        # Also optional
        output.score = 0
    else: 
        output.status = "Vulnerability found"
        output.score = 1

    return output, evolutionary_track



"""
regex_samples = ['h.*?.*?j', '^(?=hello)[a-z]{5}', '^<\!\-\-(.*)+(\/){0,1}\-\->$'] # for testing
"""

def main():
    expr_raw = base64.b64decode(sys.argv[1])
    e = root_pb2.Expression()
    e.ParseFromString(expr_raw)
    iterations = 1000
    tokens = get_tokens(e)
    # print(tokens)
    # print(generate_seeds(tokens))
    output, evolution = evaluate_regex(e, iterations)
    print(output)
    # print(base64.b64encode(output.SerializeToString()).decode('utf-8'))

    if len(evolution) > 2:
        plt.plot(evolution)
        plt.xlabel("Generation")
        plt.ylabel("Slowest input (seconds)")
        # plt.title(expr_raw)
        plt.show()


if __name__ == "__main__":
    main()
