import re


def clean_schedule(input_file: str, output_file: str) -> str:
    """
    Clean extra data from eclipse file and create handled file .inc

    :param input_file: file name with extra data
    :param output_file: handled file name

    :return: cleaned file
    """
    with open(file=input_file, mode='r', encoding='utf-8') as input_data:
        schedule = input_data.read()

    pre_clean = re.sub(r"--.+\n", r"\n", schedule)
    cleaned_schedule = re.sub(r"\s*\n+", "\n", pre_clean)

    with open(file=output_file, mode='w', encoding='utf-8') as output_data:
        output_data.write(cleaned_schedule)

    return cleaned_schedule
