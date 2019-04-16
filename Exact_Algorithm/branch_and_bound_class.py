import random
import pprint
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy
import time

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

        self.volume_sort()

    def volume_sort(self):
        """
        Sort jobs according to non-increasing volumes (areas), in order to gain the best performance
        in branch and bound algorithm.
        :return: None
        """
        self.jobs_sorted = sorted(
            self.jobs,
            key=lambda job: (job['height'], job['width'] * job['height']),
            # key=lambda job: job['width'] * job['height'],
            reverse=True)

    def run_model(self):
        # for i in range(len(self.jobs_sorted)):
        self.optimal_height = float('inf')
        self.pack_jobs(0, self.jobs_sorted)

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

    def print_jobs(self):
        print('Generated jobs are: ')
        pp = pprint.PrettyPrinter(width=80)
        pp.pprint(self.jobs)

    def print_solution(self):
        print('\nOptimal height is:', solution.optimal_height, end='. ')
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


solution = ExactSolution(W=8)
# solution.gen_uniform_jobs(20, res_low=1, res_high=1, time_low=1, time_high=10)

solution.jobs.append({'x': 0, 'y': 0, 'width': 2, 'height': 2})
solution.jobs.append({'x': 0, 'y': 0, 'width': 1, 'height': 1})
solution.jobs.append({'x': 0, 'y': 0, 'width': 4, 'height': 3})
solution.jobs.append({'x': 0, 'y': 0, 'width': 4, 'height': 1})
solution.volume_sort()

# # height early stop
# total_time_1 = 0
# total_time_2 = 0
# for i in range(100):
#     start_time_1 = time.time()
#     solution.gen_uniform_jobs(20, res_low=1, res_high=1, time_low=1, time_high=10)
#     start_time_2 = time.time()
#     solution.run_model()
#     elapsed_time_1 = time.time() - start_time_1
#     elapsed_time_2 = time.time() - start_time_2
#     total_time_1 += elapsed_time_1
#     total_time_2 += elapsed_time_2
# print(total_time_1)
# print(total_time_2)

solution.run_model()
solution.print_jobs()
solution.print_solution()
solution.draw_solution()
