from itertools import permutations
import random


def gen_uniform_jobs(num, res_low, res_high, time_low, time_high):
    jobs = []
    for i in range(num):
        job = {'x': 0, 'y': 0}
        job['width'] = random.randrange(res_low, res_high + 1)
        job['height'] = random.randrange(time_low, time_high)
        jobs.append(job)

    perm = permutations(jobs)
    for seq in perm:
        print(seq[0]['width'])
    pass


gen_uniform_jobs(num=4, res_low=1, res_high=4, time_low=1, time_high=5)