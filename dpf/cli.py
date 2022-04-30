import csv
from argparse import ArgumentParser

from dpf.db.models import CircResultOrm
from sqlalchemy.orm import Session

from dpf.db.database import engine, Base

DATASET_URL = 'https://www.data.gouv.fr/fr/datasets/r/29d9cba6-5a2f-455b-8f41-9040a6efc4ca'


def comma_string_to_float(s: str):
    return float(s.replace(',', '.'))


def parse_line(line):
    code_dept = line[0]
    code_circ = line[2]
    # name_cic = line[3]
    # inscrits = line[5]
    # voters = line[8]
    # blank = line[10]
    # cast = line[16]
    candidates = {
        'ARTHAUD': comma_string_to_float(line[25]),
        'ROUSSEL': comma_string_to_float(line[32]),
        'MACRON': comma_string_to_float(line[39]),
        'LASSALE': comma_string_to_float(line[46]),
        'LE PEN': comma_string_to_float(line[53]),
        'ZEMMOUR': comma_string_to_float(line[60]),
        'MELENCHON': comma_string_to_float(line[67]),
        'HIDALGO': comma_string_to_float(line[74]),
        'JADOT': comma_string_to_float(line[81]),
        'PECRESSE': comma_string_to_float(line[88]),
        'POUTOU': comma_string_to_float(line[95]),
        'DUPONT-AIGNANT': comma_string_to_float(line[102]),
    }
    circ_results = []
    for name, percentage in candidates.items():
        circ_result = CircResultOrm(
            code_dept=code_dept,
            code_circ=code_circ,
            candidate=name,
            percentage=percentage,
        )
        circ_results.append(circ_result)
    return circ_results


def update_db_cmd(args):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open(args.data_path, encoding='iso-8859-15') as f:
        f.readline()
        reader = csv.reader(f.readlines(), delimiter=';', quotechar='"')
    with Session(engine) as session:
        for row in reader:
            session.add_all(parse_line(row))
        session.commit()


def main():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(required=True)

    update_db_parser = sub_parsers.add_parser('update-db')
    update_db_parser.add_argument('data_path')
    update_db_parser.set_defaults(func=update_db_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
