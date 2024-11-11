""" pop_sheet_subsys.py - Populate the sheet subsystem classes """

# System
from typing import NamedTuple
from pathlib import Path

# Model Integration
from pyral.relvar import Relvar
from pyral.transaction import Transaction
from mi_config.config import Config


class SheetData(NamedTuple):
    standard: str
    height: float
    width: float
    size_group: str

class DividerInstance(NamedTuple):
    Box_above: int
    Box_below: int
    Pattern: str
    Compartment_box: int
    Partition_distance: float
    Partition_orientation: str

class DataBoxInstance(NamedTuple):
    ID: int
    Pattern: str
    H_align: str
    V_align: str
    Style: str

class RegionInstance(NamedTuple):
    Data_box: int
    Title_block_pattern: str
    Stack_order: int

class BoxInstance(NamedTuple):
    ID: int
    Pattern: str

class TitleBlockPatternInstance(NamedTuple):
    Name: str

class SheetInstance(NamedTuple):
    Name: str
    Height: float
    Width: float
    Units: str
    Size_group: str

class SheetSizeGroupInstance(NamedTuple):
    Name: str


# SheetInstance = namedtuple('SheetInstance', 'Name Height Width Units Size_group')
# SheetSizeGroupHeader = namedtuple('SheetSizeGroupHeader', 'Name')

app = "flatland"  # Client name supplied to flatland services


class SheetSubsysDB:
    """
    Laod all Sheet Subsystem yaml data into the database
    """

    config_path = Path(__file__).parent.parent / "configuration"

    @classmethod
    def pop_title_blocks(cls):
        """
        Populate all Title Block Patterns
        """
        tbp_spec = {'titleblock': None}
        c = Config(app_name=app, lib_config_dir=cls.config_path, fspec=tbp_spec)
        tblocks = c.loaded_data['titleblock']
        for tbp in tblocks:
            for name, v in tbp.items():
                # Populate each Title Block Pattern in a single transaction
                tr_name = name.replace(' ', '_')  # Use the tbp name for the transaction name for easy debugging
                Transaction.open(db=app, name=tr_name)

                # Populate a single Title Block Pattern instance
                tbp_inst = [TitleBlockPatternInstance(Name=name)]
                Relvar.insert(db=app, relvar='Title_Block_Pattern', tuples=tbp_inst, tr=tr_name)

                # Populate Box
                # Collect all the box IDs for both data and compartment boxes
                comp_box_ids = {c['ID'] for c in v['compartment boxes']}
                data_box_ids = {d['ID'] for d in v['data boxes']}
                all_box_ids = comp_box_ids | data_box_ids
                boxes = [BoxInstance(ID=i, Pattern=name) for i in all_box_ids]
                Relvar.insert(db=app, relvar='Box', tuples=boxes, tr=tr_name)

                # Populate the single Envelope Box
                Relvar.insert(db=app, relvar='Envelope_Box', tuples=[boxes[0]], tr=tr_name)

                # Populate Compartment Boxes
                cboxes = [b for b in boxes if b.ID in comp_box_ids]
                Relvar.insert(db=app, relvar='Compartment_Box', tuples=cboxes, tr=tr_name)

                # Populate Section Boxes (all Compartment Boxes that are not the Envelope Box
                sboxes = [b for b in boxes if b.ID in comp_box_ids and b.ID != 1]
                Relvar.insert(db=app, relvar='Section_Box', tuples=sboxes, tr=tr_name)

                # Populate the Dividers
                dividers = []
                for c in v['compartment boxes']:
                    (above, below) = (c.get('Up'), c.get('Down')) if c['Orientation'] == 'H' else (c.get('Right'), c.get('Left'))
                    dividers.append(
                        DividerInstance(Box_above=above, Box_below=below, Pattern=name, Compartment_box=c['ID'],
                                        Partition_distance=c['Distance'], Partition_orientation=c['Orientation'])
                    )
                Relvar.insert(db=app, relvar='Divider', tuples=dividers, tr=tr_name)

                # Populate the Data Boxes
                dboxes = [
                    DataBoxInstance(ID=d['ID'], Pattern=name,
                                    V_align=d['V align'], H_align=d['H align'],
                                    Style=d['Style']) for d in v['data boxes']
                ]
                Relvar.insert(db=app, relvar='Data_Box', tuples=dboxes, tr=tr_name)

                # Populate the Partitioned Boxes (all Data and Section Boxes)
                pboxes = sboxes + [BoxInstance(ID=i, Pattern=name) for i in data_box_ids]
                Relvar.insert(db=app, relvar='Partitioned_Box', tuples=pboxes, tr=tr_name)
                # Populate the Regions
                regions = [
                    RegionInstance(Data_box=d['ID'], Title_block_pattern=name, Stack_order=r)
                    for d in v['data boxes']
                    for r in range(1, d['Regions'] + 1)
                ]
                Relvar.insert(db=app, relvar='Region', tuples=regions, tr=tr_name)

                Transaction.execute(db=app, name=tr_name)


    @classmethod
    def pop_sheets(cls):
        """
        Populate all Sheet Size Group and Sheet class data
        """
        sheet_spec = {'sheet': SheetData}
        c = Config(app_name=app, lib_config_dir=cls.config_path, fspec=sheet_spec)
        sheets = c.loaded_data['sheet']
        # get a set of group names
        size_group_names = {s.size_group for s in sheets.values()}
        sgroup_instances = [SheetSizeGroupInstance(Name=n) for n in size_group_names]
        Transaction.open(db=app, name="sgroup")
        Relvar.insert(db=app, relvar='Sheet_Size_Group', tuples=sgroup_instances, tr="sgroup")
        sheet_instances = [SheetInstance(Name=k, Height=v.height, Width=v.width, Size_group=v.size_group,
                                         Units='in' if v.standard == "us" else 'cm')
                           for k, v in sheets.items()]
        Relvar.insert(db=app, relvar='Sheet', tuples=sheet_instances, tr="sgroup")
        Transaction.execute(db=app, name="sgroup")
