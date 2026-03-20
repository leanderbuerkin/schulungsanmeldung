from pathlib import Path

from _0_input_data import StatsForRandomData, get_random_input_data
from _1_complete_data import RandomGenerator, XLSXReader, XLSXWriter
from _2_participants_list import ParticipantsLists, XLSXDrawer

DATA_DIRECTORY = Path("data")

# Allocating 500 JuLeis to 50 Schulungen with 10 slots takes 119 steps
# Allocating 400 JuLeis to 50 Schulungen with 10 slots takes 147 steps

def test_for_errors_by_converting_from_and_to_xlsx():
    stats_00 = StatsForRandomData(5, 50, (1, 1), (50, 50), 100)

    input_data = get_random_input_data(stats_00)
    complete_data = RandomGenerator.get_complete_data_from_input_data(input_data)
    
    # XLSXWriter.save_as_xlsx(complete_data, DATA_DIRECTORY/"minimal")
    # complete_data_written_and_read = XLSXReader.read_from_xlsx(DATA_DIRECTORY/"minimal"/"50_Schulungen_500_JuLeis.xlsx")

    XLSXDrawer.save_as_xlsx(complete_data, DATA_DIRECTORY/"detailed")
    # complete_data_drawn_and_read = XLSXReader.read_from_xlsx(DATA_DIRECTORY/"detailed"/"50_Schulungen_500_JuLeis.xlsx")

    # assert complete_data == complete_data_written_and_read, "Data is compromised after writing"
    # assert complete_data == complete_data_drawn_and_read, "Data is compromised after drawing"
    # assert ParticipantsLists(complete_data) == ParticipantsLists(complete_data_written_and_read), "Data is compromised after writing"
    # assert ParticipantsLists(complete_data) == ParticipantsLists(complete_data_drawn_and_read), "Data is compromised after drawing"

test_for_errors_by_converting_from_and_to_xlsx()
