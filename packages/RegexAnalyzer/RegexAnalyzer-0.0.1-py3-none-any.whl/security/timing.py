# timing functions for the genetic algorithm
# Jan 2022
import re
import time
import statistics
import multiprocessing

import config 


def do_match(regex, regex_input, pipe):
    time_started = time.process_time()
    regex.match(regex_input)
    time_ended = time.process_time()
    pipe.send(time_ended - time_started)


def match_time(regex, regex_input, iterations: int = 2, timeout: int = config.timeout):
    """
    Determine how long a string takes to match
    """
    times = []
    compiled_regex = re.compile(regex)
    for _ in range(iterations):
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=do_match, args=((compiled_regex, regex_input, child_conn, )))
        p.start()
        p.join(timeout=timeout)
        if p.is_alive():
            time_taken = timeout
            # print("TIMEOUT:", regex_input)
            p.kill()
        else:
            time_taken = parent_conn.recv()
        times.append(time_taken)

    # print("difference in time", total_time1, total_time2, abs(total_time1 - total_time2))
    return statistics.mean(times)


# def match_time(regex, regex_input):
#     """
#     Old version for testing 
#     """
#     compiled_regex = re.compile(regex)
#     times = [] 
#     for i in range(10):
#         time_started = time.process_time()
#         compiled_regex.match(regex_input)
#         time_ended = time.process_time()
#         times.append(time_ended-time_started)
#     return statistics.mean(times)


# returns time taken per character
# TODO 
def average_match_time(regex, input):
    time_taken = match_time(regex, input)
    average_time = time_taken / len(input)
    return average_time


# returns slowest individual in a generation based on average matching time (per letter)
def slowest_average_match_time(regex, generation):
    slowest_time = 0
    slowest_string = ""
    for finalist in generation:
        time_taken = match_time(regex, finalist)
        if time_taken > slowest_time:
            slowest_string = finalist
            slowest_time = time_taken
    slowest_string = "".join(slowest_string)
    return slowest_string, slowest_time


# returns slowest individual in a generation based on total matching time 
def slowest_total_match_time(regex, generation):
    slowest_time = 0
    slowest_string = ""
    for finalist in generation:
        time_taken = match_time(regex, finalist)
        if time_taken >= config.timeout:
            return finalist, config.timeout 
        elif time_taken > slowest_time:
            slowest_string = finalist
            slowest_time = time_taken
    return slowest_string, slowest_time


# an alternate to fittest_individual_total
# not currently in use
def slowest_individual(regex, generation):
    dict = {}
    ordered_generation = []
    for input in generation:
        if input != "":
            dict[input] = match_time(regex, input)
    sorted_inputs = sorted(dict.items(), key=lambda kv: kv[1])
    slowest_item = sorted_inputs[-1][0]
    slowest_time = sorted_inputs[-1][1]
    return (slowest_item, slowest_time)
