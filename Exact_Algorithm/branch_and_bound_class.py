import random
import pprint

class ExactSolution():
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
		self.min_height = float('inf')

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

		# pp = pprint.PrettyPrinter(width=80)
		# pp.pprint(self.jobs)
		self.__sort_jobs()

	def __sort_jobs(self):
		"""
		Sort jobs according to non-increasing volumes (areas), in order to gain best performance
		in branch and bound algorithm.
		:return: None
		"""
		self.jobs_sorted = sorted(self.jobs, key=lambda job: job['width'] * job['height'], reverse=True)

	def two_dim_corners(self, in_jobs, out_min_width):
		"""
		find corner points in the current bin
		:param in_jobs: jobs in the bin
		:param out_min_width: the minimum width of the unpacked jobs
		:return: corner points in set
		"""
		# if no job is scheduled, corner is (0,0) and return
		if len(in_jobs) is 0:
			corners = {(0, 0)}
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
		corners = {(0, ex_jobs[0]['y'] + ex_jobs[0]['height'])}
		for j in range(1, m):
			corner = (ex_jobs[j-1]['x'] + ex_jobs[j-1]['width'], ex_jobs[j]['y'] + ex_jobs[j]['height'])
			corners.add(corner)
		corners.add( (ex_jobs[m-1]['x'] + ex_jobs[m-1]['width'], 0) )
		# Phrase 3: remove infeasible corner points
		for corner in corners:
			if corner['x'] + out_min_width > self.W:
				corners.remove(corner)
		return corners

	def sort_in_jobs(self, in_jobs):
		"""
		Order the jobs in the bin according to their end-points
		:param in_jobs: jobs in the bin
		:return: ordered jobs
		"""
		if len(in_jobs) is 0:
			return in_jobs
		jobs_ordered_y = sorted(in_jobs, key=lambda job: job['y'] + job['height'], reverse=True)
		jobs_ordered_yx = sorted(jobs_ordered_y, key=lambda job: job['x'] + job['width'], reverse=True)
		return jobs_ordered_yx

	def run_model(self):
		# for i in range(len(self.jobs_sorted)):
		self.step_i(0)

	def step_i(self, i):
		# in_jobs could be empty [] when i is 0
		in_jobs = self.jobs_sorted[:i]
		# out_jobs could be empty [] when i is len-1
		# get the minimum width of the out jobs
		out_jobs = self.jobs_sorted[i + 1:]
		if len(out_jobs) is not 0:
			out_min_width = min(out_jobs)
		else:
			out_min_width = 0
		# sort jobs in the bin and get corner points
		jobs_ordered_yx = self.sort_in_jobs(in_jobs)
		corners = self.two_dim_corners(jobs_ordered_yx, out_min_width)
		# try corner points recursively and obey depth first rule


solution = ExactSolution(W=8)
solution.gen_uniform_jobs(20, res_low=1, res_high=4, time_low=1, time_high=5)
solution.run_model()
