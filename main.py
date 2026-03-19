from pathlib import Path

from random_generator import get_random_data
from participants_lists_generator import get_participants_lists
from xlsx_minimal_writer import get_minimal_xlsx
from xlsx_writer import get_xlsx

DATA_DIRECTORY = Path("data")

data = get_random_data(50, 500, (8, 12), 80, (50, 50))
#minimal_xlsx = get_minimal_xlsx(data, DATA_DIRECTORY)
xlsx = get_xlsx(data, DATA_DIRECTORY)
# participants_lists = get_participants_lists(data)
# for schulung, juleis in participants_lists.items():
#     print(f"Schulung {schulung.id:<10}: {", ".join(str(j.id) for j in juleis)}")

# todo: Add logging
# todo: Verify that reading and writing does not change the outcome
