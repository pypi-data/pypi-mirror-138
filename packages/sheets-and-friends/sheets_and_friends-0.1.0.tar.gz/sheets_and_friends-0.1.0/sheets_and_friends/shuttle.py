import logging
import pprint

import click
import click_log

import pandas as pd

from linkml_runtime.linkml_model import (
    SchemaDefinition,
    # SlotDefinition,
    # Example,
    # EnumDefinition,
    # PermissibleValue,
    # Annotation
)

from linkml_runtime.utils.schemaview import SchemaView

# from linkml_runtime.dumpers import yaml_dumper


logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--destination_model", type=click.Path(exists=True), required=True)
@click.option("--config_tsv", type=click.Path(exists=True), required=True)
def do_shuttle(destination_model, config_tsv):
    """
    Gets slots, listed in config_tsv, from source_model and puts them in destination_model
    :param destination_model:
    :param config_tsv:
    :return:
    """

    shuttle = Shuttle()
    shuttle.tsv_file = config_tsv
    shuttle.destination_model = destination_model
    shuttle.get_slots_from_tsv()
    shuttle.prepare_dest_schema()
    shuttle.get_unique_source_files()
    shuttle.prep_transactions_dict()
    shuttle.prep_views_dict()
    shuttle.confirm_slots()


if __name__ == '__main__':
    do_shuttle()


class Shuttle:
    def __init__(self):
        self.views_dict = {}
        self.sources_first = {}
        self.source_schema_files = None
        self.destination_class_name = None
        self.destination_schema: SchemaDefinition = None
        self.destination_model = None
        self.slots_lod = None
        self.slots_frame: pd.DataFrame = None
        self.tsv_file = None

    def get_slots_from_tsv(self):
        slots_frame = pd.read_csv(self.tsv_file, sep="\t")
        self.slots_lod = slots_frame.to_dict(orient='records')

    def prepare_dest_schema(self):
        current_view = SchemaView(self.destination_model)
        self.destination_schema = current_view.schema

    def get_unique_source_files(self):
        schema_files = [i['source file or URL'] for i in self.slots_lod]
        schema_files = list(set(schema_files))
        schema_files.sort()
        self.source_schema_files = schema_files

    def prep_transactions_dict(self):
        self.sources_first = {}
        for i in self.slots_lod:
            source_designator = i['source file or URL']
            if source_designator not in self.sources_first:
                self.sources_first[source_designator] = {}
                self.sources_first[source_designator]['transactions'] = []
            self.sources_first[source_designator]['transactions'].append(i)

    def prep_views_dict(self):
        self.views_dict = {}
        for k, v in self.sources_first.items():
            temp = SchemaView(k)
            self.views_dict[k] = temp

    def confirm_slots(self):
        for k, v in self.sources_first.items():
            print(k)
            current_view = self.views_dict[k]
            for i in v['transactions']:
                print(i)
                # class_name = 'soil MIMS'
                current_slot = current_view.induced_slot(slot_name=i['slot'], class_name=i['source class'])
                print(current_slot)
