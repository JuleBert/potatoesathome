# game_of_live/forms.py
from django import forms


class GameOfLiveForm(forms.Form):
    size_choices = (('512','512'),
                    ('1024','1024'),
                    ('2048','2048'),
                    )
    type_choices1 = (('block','block'),
                    ('beehive','beehive'),
                    ('loaf','loaf'),
                    ('boat','boat'),
                    ('tub','tub'),
                    ('big_square','big_square'),
                    ('double_tub','double_tub'),
                    ('blinker','blinker'),
                    ('toad','toad'),
                    ('beacon','beacon'),
                    ('tripol','tripol'),
                    ('pentadecathlon','pentadecathlon'),
                    ('pulsar','pulsar'),
                    ('glider','glider'),
                    ('lwss','lwss'),
                    ('mwss','mwss'),
                    ('hwss','hwss'),
                    ('giant','giant'),
                    )
    
    type_choices2 = (('r_pentomino','r_pentomino'),
                    ('die_hard','die_hard'),
                    ('acorn','acorn'),
                    ('surprise','surprise'),
                    ('gosper_glider_gun','gosper_glider_gun'),
                    ('block_laying_engine_1','block_laying_engine_1'),
                    ('block_laying_engine_2','block_laying_engine_2'),
                    ('block_laying_engine_3','block_laying_engine_3'),
                    )
    
    size = forms.ChoiceField(choices=size_choices)
    square_size = forms.IntegerField()
    steps = forms.IntegerField()
    type_1 = forms.ChoiceField(choices=type_choices1)
    x_position_1 = forms.IntegerField()
    y_position_1 = forms.IntegerField()
    type_2 = forms.ChoiceField(choices=type_choices1)
    x_position_2 = forms.IntegerField()
    y_position_2 = forms.IntegerField()
    '''
    class Meta:
        model = Time_Entry
        fields =  ['description', 'project_id']
        widgets = {
            'current_day': DateInput()
        }
        labels = {
            'description': _('Beschreibung'),
            'project_id': _('Projekt'),
            'start_time': _('Start'),
            'end_time': _('Ende'),
        }
        help_texts = {
            'description': _('Was habe ich gemacht´?'),
        }
        error_messages = {
            'description': {
                'max_length': _('Die Beschreibung ist zu lang.'),
            },
        }
        '''