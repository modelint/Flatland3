"""
relvars.py - Flatland DB relation variables (database schema)

This file defines all relvars (relational variables) for the Flatland database. In SQL terms,
this is the schema definition for the database. These relvars are derived from the Flatland domain
models.

Consult those models to understand all of these relvars and their constraints,
They should be available on the Flatland GitHub wiki.
"""
from pyral.rtypes import Attribute, Mult
from collections import namedtuple

# Here is a mapping from metamodel multiplcity notation to that used by the target TclRAL tclral
# When interacting with PyRAL we must supply the tclral specific value
mult_tclral = {
    'M': Mult.AT_LEAST_ONE,
    '1': Mult.EXACTLY_ONE,
    'Mc': Mult.ZERO_ONE_OR_MANY,
    '1c': Mult.ZERO_OR_ONE
}

Header = namedtuple('Header', ['attrs', 'ids'])
SimpleAssoc = namedtuple('SimpleAssoc', ['name', 'from_class', 'from_mult', 'from_attrs',
                                         'to_class', 'to_mult', 'to_attrs'])
AssocRel = namedtuple('AssocRel', ['name', 'assoc_class', 'a_ref', 'b_ref'])
Ref = namedtuple('AssocRef', ['to_class', 'mult', 'from_attrs', 'to_attrs'])
GenRel = namedtuple('GenRel', ['name', 'superclass', 'superattrs', 'subrefs'])

class FlatlandSchema:
    """
    The Flatland subsystem models are defined here

    """

    relvars = {
        'Sheet': {
            # Sheet subsystem relvars
            'Box': Header(attrs=[
                Attribute(name='ID', type='int'),
                Attribute(name='Pattern', type='string'),
            ], ids={1: ['ID', 'Pattern']}),
            'Box_Placement': Header(attrs=[
                Attribute(name='Frame', type='string'),
                Attribute(name='Sheet', type='string'),
                Attribute(name='Orientation', type='string'),
                Attribute(name='Box', type='int'),
                Attribute(name='Title_block_pattern', type='string'),
                Attribute(name='X', type='int'),
                Attribute(name='Y', type='int'),
                Attribute(name='Width', type='double'),
                Attribute(name='Height', type='double'),
            ], ids={1: ['Frame', 'Sheet', 'Orientation', 'Title_block_pattern', 'Box']}),
            'Compartment_Box': Header(attrs=[
                Attribute(name='ID', type='int'),
                Attribute(name='Pattern', type='string'),
                Attribute(name='Partition_distance', type='double'),
                Attribute(name='Partition_orientation', type='string'),
            ], ids={1: ['ID', 'Pattern']}),
            'Data_Box': Header(attrs=[
                Attribute(name='ID', type='int'),
                Attribute(name='Pattern', type='string'),
                Attribute(name='H_align', type='string'),
                Attribute(name='V_align', type='string'),
                Attribute(name='Style', type='string'),
            ], ids={1: ['ID', 'Pattern']}),
            'Envelope_Box': Header(attrs=[
                Attribute(name='ID', type='int'),
                Attribute(name='Pattern', type='string'),
            ], ids={1: ['ID', 'Pattern']}),
            'Field': Header(attrs=[
                Attribute(name='Metadata', type='string'),
                Attribute(name='Frame', type='string'),
                Attribute(name='Sheet', type='string'),
                Attribute(name='Orientation', type='string'),
                # Placement
                Attribute(name='x_position', type='int'),
                Attribute(name='y_position', type='int'),
                # Max area
                Attribute(name='max_width', type='int'),
                Attribute(name='max_height', type='int'),
                # TODO: Make use of TclRAL tuple data type to combine the above attributes
                # TODO: to match the model attributes
            ], ids={1: ['Metadata', 'Frame', 'Sheet', 'Orientation', 'x_position', 'y_position']}),
            'Frame': Header(attrs=[
                Attribute(name='Name', type='string'),
                Attribute(name='Sheet', type='string'),
                Attribute(name='Orientation', type='string'),
            ], ids={1: ['Name', 'Sheet', 'Orientation']}),
            'Metadata': Header(attrs=[Attribute(name='Name', type='string')], ids={1: ['Name']}),
            'Partitioned_Box': Header(attrs=[
                Attribute(name='ID', type='int'),
                Attribute(name='Pattern', type='string'),
            ], ids={1: ['ID', 'Pattern']}),
            'Region': Header(attrs=[
                Attribute(name='Data_box', type='int'),
                Attribute(name='Title_block_pattern', type='string'),
                Attribute(name='Stack_order', type='int'),
            ], ids={
                1: ['Data_box', 'Title_block_pattern', 'Stack_order']}
            ),
            'Scaled_Title_Block': Header(attrs=[
                Attribute(name='Title_block_pattern', type='string'),
                Attribute(name='Sheet_size_group', type='string'),
                Attribute(name='Height', type='string'),
                Attribute(name='Width', type='string'),
                # Block size
                Attribute(name='Margin_h', type='int'),
                Attribute(name='Margin_v', type='int'),
            ], ids={1: ['Title_block_pattern', 'Sheet_size_group']}),
            'Section_Box': Header(attrs=[
                Attribute(name='ID', type='int'),
                Attribute(name='Pattern', type='string'),
            ], ids={1: ['ID', 'Pattern']}),
            'Sheet': Header(attrs=[
                Attribute(name='Name', type='string'),
                # Size
                Attribute(name='Height', type='string'),
                Attribute(name='Width', type='string'),
                Attribute(name='Units', type='string'),
                Attribute(name='Size_group', type='string'),
            ], ids={1: ['Name']}),
            'Sheet_Size_Group': Header(attrs=[Attribute(name='Name', type='string')], ids={1: ['Name']}),
            'Title_Block_Field': Header(attrs=[
                Attribute(name='Metadata', type='string'),
                Attribute(name='Frame', type='string'),
                Attribute(name='Sheet', type='string'),
                Attribute(name='Orientation', type='string'),
                # Placement
                Attribute(name='x_position', type='int'),
                Attribute(name='y_position', type='int'),
                Attribute(name='Data_box', type='int'),
                Attribute(name='Title_block_pattern', type='string'),
                Attribute(name='Stack_order', type='int'),
            ], ids={1: ['Metadata', 'Frame', 'Sheet', 'Orientation', 'x_position', 'y_position']}),
            'Title_Block_Pattern': Header(attrs=[Attribute(name='Name', type='string')], ids={1: ['Name']}),
            'Title_Block_Placement': Header(attrs=[
                Attribute(name='Frame', type='string'),
                Attribute(name='Sheet', type='string'),
                Attribute(name='Orientation', type='string'),
                Attribute(name='Title_block_pattern', type='string'),
                Attribute(name='Sheet_size_group', type='string'),
                Attribute(name='X', type='int'),
                Attribute(name='Y', type='int'),
            ], ids={1: ['Frame', 'Sheet', 'Orientation']}),
        }
    }

    rels = {
        'Sheet': [
            SimpleAssoc(name='R300',
                        from_class='Frame', from_mult=mult_tclral['Mc'], from_attrs=['Sheet'],
                        to_class='Sheet', to_mult=mult_tclral['1'], to_attrs=['Name'],
                        ),
            AssocRel(name='R301', assoc_class='Scaled_Title_Block',
                     a_ref=Ref(to_class='Sheet_Size_Group', mult=mult_tclral['Mc'],
                               from_attrs=['Sheet_size_group'],
                               to_attrs=['Name']),
                     b_ref=Ref(to_class='Title_Block_Pattern', mult=mult_tclral['Mc'],
                               from_attrs=['Title_block_pattern'],
                               to_attrs=['Name'])
                     ),
            SimpleAssoc(name='R303',
                        from_class='Box', from_mult=mult_tclral['M'], from_attrs=['Pattern'],
                        to_class='Title_Block_Pattern', to_mult=mult_tclral['1'], to_attrs=['Name'],
                        ),
            AssocRel(name='R306', assoc_class='Title_Block_Field',
                     a_ref=Ref(to_class='Field', mult=mult_tclral['Mc'],
                               from_attrs=['Metadata', 'Frame', 'Sheet', 'Orientation', 'x_position', 'y_position'],
                               to_attrs=['Metadata', 'Frame', 'Sheet', 'Orientation', 'x_position', 'y_position'],
                               ),
                     b_ref=Ref(to_class='Region', mult=mult_tclral['1c'],
                               from_attrs=['Data_box', 'Title_block_pattern', 'Stack_order'],
                               to_attrs=['Data_box', 'Title_block_pattern', 'Stack_order'])
                     ),
            AssocRel(name='R307', assoc_class='Field',
                     a_ref=Ref(to_class='Metadata', mult=mult_tclral['Mc'],
                               from_attrs=['Metadata'],
                               to_attrs=['Name'],
                               ),
                     b_ref=Ref(to_class='Frame', mult=mult_tclral['Mc'],
                               from_attrs=['Frame', 'Sheet', 'Orientation'],
                               to_attrs=['Name', 'Sheet', 'Orientation'])
                     ),
            GenRel(name='308', superclass='Box', superattrs=['ID', 'Pattern'],
                   subrefs={
                       'Envelope_Box': ['ID', 'Pattern'],
                       'Section_Box': ['ID', 'Pattern'],
                       'Data_Box': ['ID', 'Pattern']
                   }),
            SimpleAssoc(name='R309',
                        from_class='Region', from_mult=mult_tclral['M'], from_attrs=['Data_box', 'Title_block_pattern'],
                        to_class='Data_Box', to_mult=mult_tclral['1'], to_attrs=['ID', 'Pattern'],
                        ),
            GenRel(name='R312', superclass='Compartment_Box', superattrs=['ID', 'Pattern'],
                   subrefs={
                       'Envelope_Box': ['ID', 'Pattern'],
                       'Section_Box': ['ID', 'Pattern'],
                   }),
            GenRel(name='R313', superclass='Partitioned_Box', superattrs=['ID', 'Pattern'],
                   subrefs={
                       'Envelope_Box': ['ID', 'Pattern'],
                       'Section_Box': ['ID', 'Pattern'],
                   }),
            AssocRel(name='R315', assoc_class='title_block_placement',
                     a_ref=Ref(to_class='frame', mult=mult_tclral['Mc'],
                               from_attrs=['Frame, Sheet, Orientation'],
                               to_attrs=['Name', 'Sheet', 'Orientation']),
                     b_ref=Ref(to_class='scaled_title_block', mult=mult_tclral['1c'],
                               from_attrs=['Title_block_pattern, Sheet_size_group'],
                               to_attrs=['Title_block_pattern, Sheet_size_group'])
                     ),
            SimpleAssoc(name='R316',
                        from_class='sheet', from_mult=mult_tclral['M'], from_attrs=['Size_group'],
                        to_class='sheet_size_group', to_mult=mult_tclral['1'], to_attrs=['Name'],
                        ),
            AssocRel(name='R318', assoc_class='box_placement',
                     a_ref=Ref(to_class='title_block_placement', mult=mult_tclral['Mc'],
                               from_attrs=['Frame, Sheet, Orientation'],
                               to_attrs=['Frame', 'Sheet', 'Orientation']),
                     b_ref=Ref(to_class='box', mult=mult_tclral['M'],
                               from_attrs=['Box, Title_block_pattern'],
                               to_attrs=['ID, Pattern'])
                     ),
        ]
    }