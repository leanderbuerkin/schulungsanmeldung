from config import DATA_DIRECTORY
from random_problem_generator import generate_random_problem
from allocator import allocate

problem = generate_random_problem(DATA_DIRECTORY, 5000, 100000, (8, 12), 80, (1, 50))
allocate(problem)
