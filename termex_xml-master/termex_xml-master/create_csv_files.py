from get_params_fields import get_max_fields
from csv import DictWriter
import csv


def create_blank_csv(fields: dict):

    for key in fields.keys():
        row = {}
        for field in fields[key]:
            row[field] = field

        with open(f"files/{key}.csv", "w", encoding='utf-8', newline='') as file:
            writer = DictWriter(file, fieldnames=fields[key])
            writer.writerow(row)
