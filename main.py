"""
Preference Categories:
Flatten, assign and count rejections[schulung] = ...
Second run: out of the same categorie choose the Schulung with the least rejections
Repeat till nothing changes anymore.
"""

# todo: Add tests (is really everything unchanged after writing and reading xlsx)

from pathlib import Path

from generators import complete_data, generate_participants_list, generate_random_input_data



DATA_DIRECTORY = Path("data")

input_data = generate_random_input_data(50, 500, 80, 8, 12, 50, 50)

data = complete_data(input_data)

generate_participants_list(data, DATA_DIRECTORY)
