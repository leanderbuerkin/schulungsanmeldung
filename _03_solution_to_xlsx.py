from openpyxl import Workbook

from data_structures import InputData, Parameters, Solution
from xlsx import get_new_workbook


def save_to_xlsx(solution: Solution):
    xlsx = get_new_workbook()
    _add_parameters(xlsx, solution.parameters)



def _add_parameters(xlsx: Workbook, parameters: Parameters):
    _add_input_data(xlsx, parameters.input_data)

def _add_input_data(xlsx: Workbook, input_data: InputData):
    def add_events():
        sheet = xlsx.create_sheet()
    add_events()
    add_seekers()
    add_ranked_wishes()