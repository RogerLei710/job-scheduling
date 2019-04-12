import random
import pprint

class ExactSolution():
	"""
	Build branch and bound algorithm to optimally solve two dimensional strip packing problem
	"""
	def __init__(self, res_max):
		"""
		:param res_max: Specify the maximum amount of resource
		"""
		self.res_max = res_max
		self.jobs = []
		self.jobs_sorted = []

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
		for i in range(num):
			job = {'x': 0, 'y': 0}
			job['width'] = random.randrange(res_low, res_high + 1)
			job['height'] = random.randrange(time_low, time_high)
			self.jobs.append(job)

		# pp = pprint.PrettyPrinter(width=80)
		# pp.pprint(self.jobs)

	def sort_jobs(self):
		"""
		Sort jobs according to non-increasing volumes (areas), in order to gain best performance
		in branch and bound algorithm.
		:return: None
		"""
		self.jobs_sorted = sorted(self.jobs, key=lambda job: job['width'] * job['height'], reverse=True)

	def two_dim_corners(self):
		pass


solution = ExactSolution(8)
solution.gen_uniform_jobs(20, res_low=1, res_high=4, time_low=1, time_high=5)
