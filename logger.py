
from time import gmtime, strftime, time

from config import DATA_DIRECTORY, GENERATE_LOGS

with open(DATA_DIRECTORY/"time_needed_per_process.md", "w") as f:
    f.write("# Elapsed Times\n\n")

time_at_last_log = time()

def log_time(process_name: str) -> None:
    if not GENERATE_LOGS:
        return
    global time_at_last_log
    with open(DATA_DIRECTORY/"time_needed_per_process.md", "a") as f:
        f.write(f"{strftime("%H:%M:%S", gmtime(time()-time_at_last_log))}  {process_name}\n")
    time_at_last_log = time()
