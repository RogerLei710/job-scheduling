import random
import pprint
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy
import time
from itertools import permutations


class ExactSolution:
    """
    Build branch and bound algorithm to optimally solve two dimensional strip packing problem
    """
    def __init__(self, W):
        """
        :param W: Specify the maximum amount of resource
        """
        self.W = W
        self.jobs = []
        self.jobs_sorted = []
        self.optimal_height = float('inf')
        self.optimal_jobs = []
        self.solve_time = 0

    def gen_uniform_jobs(self, num, res_low, res_high, time_low, time_high):
        """
        Generate uniform jobs according to four parameters, and save them into self.jobs
        :param num: The number of jobs waited to schedule.
        :param res_low: The smallest amount of resource that a job may request.
        :param res_high: The biggest amount of resource that a job may request.
        :param time_low: The smallest amount of time that a job may request.
        :param time_high: The biggest amount of time that a job may request.
        :return: None
        """
        self.jobs = []
        for i in range(num):
            job = {'x': 0, 'y': 0}
            job['width'] = random.randrange(res_low, res_high + 1)
            job['height'] = random.randrange(time_low, time_high)
            self.jobs.append(job)

    def exact_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Get permutations from self.jobs
        # Note that this would generate n! sequences, which take an incredibly long time to solve.
        perm = permutations(self.jobs)
        for seq in perm:
            self.pack_jobs(0, seq)
        self.solve_time = time.time() - start_time

    def random_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # No sorting. Pack jobs directly.
        self.pack_jobs(0, self.jobs)
        self.solve_time = time.time() - start_time

    def height_first_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing height.
        self.jobs_sorted = sorted(self.jobs, key=lambda job: job['height'], reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def height_width_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing height then width.
        self.jobs_sorted = sorted(
            self.jobs,
            key=lambda job: (job['height'], job['width']),
            reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def width_first_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing width.
        self.jobs_sorted = sorted(self.jobs, key=lambda job: job['width'], reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def width_height_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing height then width.
        self.jobs_sorted = sorted(
            self.jobs,
            key=lambda job: (job['width'], job['height']),
            reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def reverse_width_height_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing height then width.
        self.jobs_sorted = sorted(
            self.jobs,
            key=lambda job: (job['width'], job['height']))
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def area_first_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing area.
        self.jobs_sorted = sorted(self.jobs, key=lambda job: job['width'] * job['height'], reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def area_height_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing area then height.
        self.jobs_sorted = sorted(
            self.jobs,
            key=lambda job: (job['width'] * job['height'], job['height']),
            reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def area_width_model(self):
        self.optimal_height = float('inf')
        start_time = time.time()
        # Sort jobs according to non-increasing area then width.
        self.jobs_sorted = sorted(
            self.jobs,
            key=lambda job: (job['width'] * job['height'], job['width']),
            reverse=True)
        self.pack_jobs(0, self.jobs_sorted)
        self.solve_time = time.time() - start_time

    def pack_jobs(self, i, all_jobs):
        # early return if the packing is already higher than the current optimal height
        if i is not 0:
            highest_job = max(
                all_jobs[:i],
                key=lambda job: job['y'] + job['height'])
            overall_height = highest_job['y'] + highest_job['height']
            if overall_height >= self.optimal_height:
                return

            # Have packed all the jobs.
            if i is len(all_jobs):
                self.optimal_height = overall_height
                self.optimal_jobs = copy.deepcopy(all_jobs)
                return

        # in_jobs could be empty [] when i is 0
        in_jobs = all_jobs[:i]
        # out_jobs could be empty [] when i is len-1
        # get the minimum width of the out jobs
        out_jobs = all_jobs[i:]
        if len(out_jobs) is not 0:
            out_min_width = min(out_jobs, key=lambda job: job['width'])['width']
        else:
            out_min_width = 0
        # sort jobs in the bin and get corner points
        jobs_ordered_yx = self.sort_in_jobs(in_jobs)
        corners = self.two_dim_corners(jobs_ordered_yx, out_min_width)
        # try corner points recursively and obey depth first rule
        for corner in corners:
            if corner[0] + all_jobs[i]['width'] <= self.W:
                all_jobs[i]['x'] = corner[0]
                all_jobs[i]['y'] = corner[1]
                # try to pack the next job, call itself recursively
                self.pack_jobs(i + 1, all_jobs)

    def two_dim_corners(self, in_jobs, out_min_width):
        """
        find corner points in the current bin
        :param in_jobs: jobs in the bin
        :param out_min_width: the minimum width of the unpacked jobs
        :return: corner points in set
        """
        # if no job is scheduled, corner is (0,0) and return
        if len(in_jobs) is 0:
            corners = [(0, 0)]
            return corners

        # Phrase 1: identify the extreme items, e0, e1, ..., em-1
        ex_jobs = []
        x_max = m = 0
        for j in range(len(in_jobs)):
            # j = 0, 1, ...., l-1
            if in_jobs[j]['x'] + in_jobs[j]['width'] > x_max:
                m = m + 1
                x_max = in_jobs[j]['x'] + in_jobs[j]['width']
                ex_jobs.append(in_jobs[j])
        # Phrase 2: determine the corner points
        corners = [(0, ex_jobs[0]['y'] + ex_jobs[0]['height'])]
        for j in range(1, m):
            corner = (ex_jobs[j - 1]['x'] + ex_jobs[j - 1]['width'],
                      ex_jobs[j]['y'] + ex_jobs[j]['height'])
            corners.append(corner)
        corners.append( (ex_jobs[m - 1]['x'] + ex_jobs[m - 1]['width'], 0) )
        # Phrase 3: remove infeasible corner points
        for corner in corners:
            if corner[0] + out_min_width > self.W:
                corners.remove(corner)
        return corners

    def sort_in_jobs(self, in_jobs):
        """
        Order the jobs in the bin according to their end-points (y + height)
        :param in_jobs: jobs in the bin
        :return: ordered jobs
        """
        if len(in_jobs) is 0:
            return in_jobs
        jobs_ordered_yx = sorted(
            in_jobs,
            key=lambda job: (job['y'] + job['height'], job['x'] + job['width']),
            reverse=True)

        return jobs_ordered_yx

    def print_jobs(self):
        print('Generated jobs are: ')
        pp = pprint.PrettyPrinter(width=80)
        pp.pprint(self.jobs)

    def print_solution(self):
        print('\nOptimal height is:', self.optimal_height, end='. ')
        print('Optimal jobs are: ')
        pp = pprint.PrettyPrinter(width=80)
        pp.pprint(self.optimal_jobs)

    def draw_solution(self):
        fig, ax = plt.subplots(1)
        for job in self.optimal_jobs:
            x, y, w, h = job['x'], job['y'], job['width'], job['height']
            rect = Rectangle(
                (x, y), w, h, facecolor='red', alpha=0.5, edgecolor='black')
            ax.add_patch(rect)

        plt.ylim((0, self.optimal_height + 5))
        plt.xlim((0, self.W))
        plt.show()


# solution = ExactSolution(W=8)
# solution.gen_uniform_jobs(8, res_low=1, res_high=4, time_low=1, time_high=5)

# solution.jobs.append({'x': 0, 'y': 0, 'width': 2, 'height': 2})
# solution.jobs.append({'x': 0, 'y': 0, 'width': 1, 'height': 1})
# solution.jobs.append({'x': 0, 'y': 0, 'width': 4, 'height': 3})
# solution.jobs.append({'x': 0, 'y': 0, 'width': 4, 'height': 1})

# solution.exact_model()
# solution.print_jobs()
# solution.print_solution()
# solution.draw_solution()


def compare_models(W, num, res_low, res_high, time_low, time_high, iter):
    solution = ExactSolution(W=W)
    # height early stop
    exact_time = exact_height = 0
    random_time = random_height = 0
    HF_time = HF_height = 0
    HW_time = HW_height = 0
    WF_time = WF_height = 0
    WH_time = WH_height = 0
    AF_time = AF_height = 0
    AH_time = AH_height = 0
    AW_time = AW_height = 0
    RWH_time = RWH_height = 0

    for i in range(iter):
        solution.gen_uniform_jobs(num, res_low, res_high, time_low, time_high)

        # solution.exact_model()
        # exact_time += solution.solve_time
        # exact_height += solution.optimal_height

        # solution.random_model()
        # random_time += solution.solve_time
        # random_height += solution.optimal_height

        # solution.height_first_model()
        # HF_time += solution.solve_time
        # HF_height += solution.optimal_height
        #
        # solution.height_width_model()
        # HW_time += solution.solve_time
        # HW_height += solution.optimal_height
        #
        # solution.width_first_model()
        # WF_time += solution.solve_time
        # WF_height += solution.optimal_height

        solution.width_height_model()
        WH_time += solution.solve_time
        WH_height += solution.optimal_height

        # solution.area_first_model()
        # AF_time += solution.solve_time
        # AF_height += solution.optimal_height
        #
        # solution.area_height_model()
        # AH_time += solution.solve_time
        # AH_height += solution.optimal_height
        #
        # solution.area_width_model()
        # AW_time += solution.solve_time
        # AW_height += solution.optimal_height

        solution.reverse_width_height_model()
        RWH_time += solution.solve_time
        RWH_height += solution.optimal_height

    print('Maximum resource: {}. Number of jobs: {}. Times of iteration: {}.'.format(W, num, iter))
    print('Resource low bound: {}. Resource high bound: {}.'.format(res_low, res_high))
    print('Time low bound: {}. Time high bound: {}.\n'.format(time_low, time_high))

    # print('Exact solution took {0:.5f}s. Sum of optimal heights is {1}'.format(exact_time, exact_height))
    # print('Random solution took {0:.5f}s. Sum of heights is {1}'.format(random_time, random_height))
    # print('Height First solution took {0:.5f}s. Sum of heights is {1}'.format(HF_time, HF_height))
    # print('Height then Width solution took {0:.5f}s. Sum of heights is {1}'.format(HW_time, HW_height))
    # print('Width First solution took {0:.5f}s. Sum of heights is {1}'.format(WF_time, WF_height))
    print('Width then Height solution took {0:.5f}s. Sum of heights is {1}'.format(WH_time, WH_height))
    # print('Area First solution took {0:.5f}s. Sum of heights is {1}'.format(AF_time, AF_height))
    # print('Area then Height solution took {0:.5f}s. Sum of heights is {1}'.format(AH_time, AH_height))
    # print('Area then Width solution took {0:.5f}s. Sum of heights is {1}'.format(AW_time, AW_height))
    print('Reverse Width then Height solution took {0:.5f}s. Sum of heights is {1}'.format(RWH_time, RWH_height))


compare_models(W=8, num=10, res_low=1, res_high=4, time_low=1, time_high=10, iter=10000)
