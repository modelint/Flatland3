""" flatland_db.py """
from pyral.database import Database
from pyral.rtypes import Attribute, Mult as DBMult
from pyral.relvar import Relvar
from collections import namedtuple

Header = namedtuple('Header', ['attrs', 'ids'])



relvars = {
    'metadata': Header(attrs=[Attribute(name='Name', type='string')], ids={1: ['Name']}),
    'title_block_pattern': Header(attrs=[Attribute(name='Name', type='string')], ids={1: ['Name']}),
    'compartment_box': Header(attrs=[
        Attribute(name='ID', type='int'),
        Attribute(name='Pattern', type='string'),
        Attribute(name='Orientation', type='string'),
        Attribute(name='Distance', type='double'),
        Attribute(name='Up', type='int'),
        Attribute(name='Down', type='int'),
    ], ids={1: ['ID', 'Pattern']}),
    'data_box': Header(attrs=[
        Attribute(name='ID', type='int'),
        Attribute(name='Pattern', type='string'),
        Attribute(name='H_align', type='string'),
        Attribute(name='V_align', type='string'),
        Attribute(name='Style', type='string'),
    ], ids={1: ['ID', 'Pattern']}),
    'sheet_size_group': Header(attrs=[Attribute(name='Name', type='string')], ids={1: ['Name']}),
    'sheet': Header(attrs=[
        Attribute(name='Name', type='string'),
        Attribute(name='Group', type='string'),
        Attribute(name='Height', type='string'),
        Attribute(name='Width', type='string'),
        Attribute(name='Size_group', type='string'),
    ], ids={1: ['Name']}),
    'frame': Header(attrs=[
        Attribute(name='Name', type='string'),
        Attribute(name='Sheet', type='string'),
        Attribute(name='Orientation', type='string'),
    ], ids={1: ['Name', 'Sheet', 'Orientation']}),
    'title_block_placement': Header(attrs=[
        Attribute(name='Frame', type='string'),
        Attribute(name='Sheet', type='string'),
        Attribute(name='Orientation', type='string'),
        Attribute(name='Title_block_pattern', type='string'),
        Attribute(name='Sheet_size_group', type='string'),
        Attribute(name='X', type='int'),
        Attribute(name='Y', type='int'),
    ], ids={1: ['Frame', 'Sheet', 'Orientation']}),
    'box_placement': Header(attrs=[
        Attribute(name='Frame', type='string'),
        Attribute(name='Sheet', type='string'),
        Attribute(name='Orientation', type='string'),
        Attribute(name='Title_block_pattern', type='string'),
        Attribute(name='Box', type='int'),
        Attribute(name='X', type='int'),
        Attribute(name='Y', type='int'),
        Attribute(name='Width', type='double'),
        Attribute(name='Height', type='double'),
    ], ids={1: ['Frame', 'Sheet', 'Orientation', 'Title_block_pattern', 'Box']}),
    'box_text_line': Header(attrs=[
        Attribute(name='Metadata', type='string'),
        Attribute(name='Box', type='int'),
        Attribute(name='Title_block_pattern', type='string'),
        Attribute(name='Order', type='int'),
    ], ids={
        1: ['Metadata', 'Box', 'Title_block_pattern'],
        2:['Box', 'Title_block_pattern', 'Order']}
    ),
    'open_field': Header(attrs=[
        Attribute(name='Metadata', type='string'),
        Attribute(name='Frame', type='string'),
        Attribute(name='Sheet', type='string'),
        Attribute(name='Orientation', type='string'),
        Attribute(name='x_position', type='int'),
        Attribute(name='y_position', type='int'),
        Attribute(name='Y', type='int'),
        Attribute(name='max_width', type='int'),
        Attribute(name='max_height', type='int'),
    ], ids={1: ['Metadata', 'Frame', 'Sheet', 'Orientation']}),
}

class FlatlandDB:
    """

    """
    db_name = 'flatland'
    db = None
    relvar_names = None

    @classmethod
    def create_db(cls):
        """

        """
        # Create a TclRAL session with an empty tclral
        cls.db = Database.open_session(name='flatland')
        for n,h in relvars.items():
            Relvar.create_relvar(db=cls.db_name, name=n, attrs=h.attrs, ids=h.ids)
        cls.relvar_names = Database.names(db='flatland')


