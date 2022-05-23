import numpy as np
import re
from typing import List, Tuple


def parse_schedule(cleaned_schedule: str, keywords: Tuple[str]) -> List[List[str]]:
    """
    Handled list of elements that ready to be transformed to the DataFrame

    :param cleaned_schedule: cleaned schedule text
    :param keywords: tuple fo keywords for search

    :return: prepared to be transformed to the DataFrame list of elements
    """
    keywords_blocks = extract_keyword_blocks(cleaned_schedule, keywords)
    schedule_list = []
    current_date = np.nan

    for block in keywords_blocks:
        if block[0] == 'DATES':
            for line in block[1:-1]:
                schedule_list.append([parse_keyword_DATE_line(line)] + [np.nan])
            current_date = parse_keyword_DATE_line(block[-1])
            current_index = keywords_blocks.index(block)
            if current_index != len(keywords_blocks) - 1:
                if keywords_blocks[current_index + 1][0] == 'DATES':
                    schedule_list.append([current_date] + [np.nan])
            else:
                if block[0] == 'DATES':
                    schedule_list.append([current_date] + [np.nan])

        if block[0] == 'COMPDAT':
            for line in block[1:]:
                schedule_list.append([current_date] + parse_keyword_COMPDAT_line(line))
        if block[0] == 'COMPDATL':
            for line in block[1:]:
                schedule_list.append([current_date] + parse_keyword_COMPDATL_line(line))

    return schedule_list


def extract_keyword_blocks(cleaned_schedule: str, keywords: Tuple[str]) -> List[Tuple[str]]:
    """
    Extract keyword's blocks from the schedule

    :param cleaned_schedule: handled schedule
    :param keywords: tuple of keywords that need to be parse

    :return: list of keyword blocks
    """
    list_of_blocks = re.split('\n/\n', cleaned_schedule)

    keyword_blocks = [tuple(i.splitlines()) for i in list_of_blocks]

    for block in keyword_blocks:
        if block[0] not in keywords:
            keyword_blocks.remove(block)

    return keyword_blocks


def extract_lines(keyword_block: Tuple[str]) -> Tuple[str, List[str]]:
    """
    Extract keyword's lines with keywords from the schedule

    :param keyword_block:

    :return: keyword and lines for it
    """
    keyword = keyword_block[0]
    lines = list(keyword_block[1:])

    return keyword, lines


def parse_keyword_DATE_line(current_date_line: str) -> str:
    """
    Parse a line related to a current DATA keyword block

    @param current_date_line: line related to a current DATA keyword block

    @return: list of parameters in a DATE line
    """
    return re.search(r'\d{2} [A-Z]{3} \d{4}', current_date_line).group(0)


def parse_keyword_COMPDAT_line(well_comp_line: str) -> List[str]:
    """
    Parse a line related to a current COMPDAT keyword block

    @param well_comp_line: line related to a current COMPDAT keyword block

    @return: list of parameters (+ NaN Loc. grid. parameter) in a COMPDAT line
    """
    well_comp_line = re.sub(r'\'', ' ', well_comp_line)
    well_comp_line = re.sub(r'\s+', ' ', well_comp_line)

    unpacked_well_comp_line = default_params_unpacking_in_line(well_comp_line)
    parameters_list = unpacked_well_comp_line.split()
    parameters_list[1:1] = [np.nan]

    return parameters_list[:-1]


def parse_keyword_COMPDATL_line(well_comp_line: str) -> List[str]:
    """
    Parse a line related to a current COMPDATL keyword block

    @param well_comp_line: line related to a current COMPDATL keyword block

    @return: list of parameters in a COMPDATL line
    """
    well_comp_line = re.sub(r'\'', ' ', well_comp_line)
    well_comp_line = re.sub(r'\s+', ' ', well_comp_line)

    unpacked_well_comp_line = default_params_unpacking_in_line(well_comp_line)
    parameters_list = unpacked_well_comp_line.split()

    return parameters_list[:-1]


def default_params_unpacking_in_line(line: str) -> str:
    """
    Unpacks default parameters set by the 'n*' expression

    @param line: line related to a current COMPDAT/COMPDATL keyword block

    @return: the unpacked line related to a current COMPDAT/COMPDATL keyword block
    """
    unpacked_line = line
    all_asterisks = re.findall(r' \d+\*', unpacked_line)

    for pattern in all_asterisks:
        actual_pattern = pattern[:-1]+'\*'
        unpacked_line = re.sub(actual_pattern, ' DEFAULT' * int(pattern[:-1]), unpacked_line)

    return unpacked_line
