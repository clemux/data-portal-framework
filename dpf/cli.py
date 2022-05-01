import csv
from argparse import ArgumentParser

from sqlalchemy.orm import Session

from dpf.lib.db import engine, Base

from dpf.modules import covid, elections

DATASET_URL = 'https://www.data.gouv.fr/fr/datasets/r/29d9cba6-5a2f-455b-8f41-9040a6efc4ca'





def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(required=True)



    elections_parser = subparsers.add_parser('elections')
    elections.cli.register_subparsers(elections_parser)

    covid_parser = subparsers.add_parser('covid')
    covid.cli.register_subparsers(covid_parser)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
