""" pop_connector_subsys.py - Populate the connector subsystem classes """

# Model Integration
from pyral.relvar import Relvar
from pyral.transaction import Transaction

# Flatland
from flatland.names import app
from flatland.configuration.configDB import ConfigDB
from flatland.database.instances.connector_subsystem import *


class ConnectorSubsysDB:
    """
    Load all Connector Subsystem yaml data into the database
    """

    @classmethod
    def populate(cls):
        """
        Populate the connector subsystem by breaking it down into multiple focused database transactions
        (so if something goes wrong, the scope of the affected transaction is as tight as possible)
        """
        # Order of these function invocations is important since each successive call populates
        # references to data populated in the previous call.
        cls.pop_clayout_spec()
        cls.pop_stem_type()
        cls.pop_stem_notation()

    @classmethod
    def pop_stem_type(cls):
        """
        """
        notation_data = ConfigDB.item_data['notation']
        ctype_data = ConfigDB.item_data['connector_type']
        for dtype in ctype_data:
            for dtype_name, ctype_dict in dtype.items():
                full_dtype_name = f"{dtype_name} diagram"
                for ctype_name, v in ctype_dict.items():
                    tr_name = f"ctype_name"
                    Transaction.open(db=app, name=tr_name)
                    ctype_i = ConnectorTypeInstance(Name=ctype_name,
                                                    Diagram_type=dtype_name,
                                                    About=v['about'],
                                                    Geometry=v['geometry'])
                    Relvar.insert(db=app, relvar='Connector_Type', tuples=[ctype_i], tr=tr_name)
                    stype_instances = []
                    for stem_type, sv in v['stem types'].items():
                        stype_instances.append(
                            StemTypeInstance(Name=stem_type, Diagram_type=dtype_name,
                                             About=sv['about'], Connector_type=ctype_name)
                        )
                        stem_sem_i=[
                            StemSemanticInstance(Name=ss_name, Diagram_type=dtype_name) for ss_name in sv['semantics']
                        ]
                        Relvar.insert(db=app, relvar='Stem_Semantic', tuples=stem_sem_i, tr=tr_name)
                        stem_sig_i=[
                            StemSignificationInstance(Stem_type=stem_type, Semantic=ss_name, Diagram_type=dtype_name)
                            for ss_name in sv['semantics']
                        ]
                        Relvar.insert(db=app, relvar='Stem_Signification', tuples=stem_sig_i, tr=tr_name)

                        pass

    @classmethod
    def pop_stem_notation(cls):
        """
        """
        pass

    @classmethod
    def pop_clayout_spec(cls):
        """
        """
        layout_data = ConfigDB.item_data['layout_specification']
        stand_layout = layout_data[0]['standard']
        spec_instance = ConnectorLayoutSpecificationInstance(
            Name='standard',
            Default_stem_positions=stand_layout['default stem positions'],
            Default_rut_positions=stand_layout['default rut positions'],
            Default_new_path_row_height=stand_layout['default new path row height'],
            Default_new_path_col_width=stand_layout['default new path col width'],
        )
        Relvar.insert(db=app, relvar='Connector_Layout_Specification', tuples=[spec_instance])

