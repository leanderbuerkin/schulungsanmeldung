
from allocator import allocate
from config import DATA_DIRECTORY
from random_problem_generator import generate_random_problem

problem = generate_random_problem(DATA_DIRECTORY, 5, 50, (8, 12), 80, (1, 50))
allocate(problem)
