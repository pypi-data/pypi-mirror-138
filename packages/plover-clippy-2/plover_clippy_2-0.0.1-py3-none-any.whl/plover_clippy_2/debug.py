list(tails([1, 2, 3, 4, 5]))
[[5], [4, 5], [3, 4, 5], [2, 3, 4, 5], [1, 2, 3, 4, 5]]


# problem with KA*PD
old = []
new = [Action(text='south', trailing_space=' ', word='south')]
# pass filter
english  = south
stroked  = ['SOUT']
suggestions  = [('SOUT',), ('SO*UT',)]
phrase = ('south', ['SOUT'], [('SOUT',), ('SO*UT',)])
english  = south
translations  = [Translation(('PHROLG',) : "{PLOVER:TOGGLE}"),
 Translation(('SOUT',) : "south")]
stroke = Stroke(SOUT : ['S-', 'O-', '-U', '-T'])
old = []
new = [Action(prev_attach=True, prev_replace='south', text='So
uth', trailing_space=' ', word='south')]
# pass filter
english  = South
stroked  = ['KA*PD']
suggestions  = [('SOUT',), ('SO*UT',)]
phrase = ('South', ['KA*PD'], [('SOUT',), ('SO*UT',)])
english  = South
english  = South
translations  = [Translation(('PHROLG',) : "{PLOVER:TOGGLE}"),
 Translation(('SOUT',) : "south"), Translation(('KA*PD',) : "{
*-|}")]
stroke = Stroke(KA*PD : ['K-', 'A-', '*', '-P', '-D'])


# fun with advertise

old = [Action(text='add', trailing_space=' ', word='add')]
new = [Action(text='advertise', trailing_space=' ', word='adve
rtise')]
pass filter
english  = advertise
stroked  = ['AD', 'TAOEUS']
suggestions  = [('TEUZ',), ('TAOEUS',), ('AD', 'TAOEUS'), ('AD
', 'SRER', 'TAOEUZ')]
phrase = ('advertise', ['AD', 'TAOEUS'], [('TEUZ',), ('TAOEUS'
,), ('AD', 'TAOEUS'), ('AD', 'SRER', 'TAOEUZ')])
english  = advertise
stroked  = ['PHROLG', 'AD', 'TAOEUS']
suggestions  = [('TEUZ',), ('TAOEUS',), ('AD', 'TAOEUS'), ('AD
', 'SRER', 'TAOEUZ')]
phrase = ('advertise', ['PHROLG', 'AD', 'TAOEUS'], [('TEUZ',),
 ('TAOEUS',), ('AD', 'TAOEUS'), ('AD', 'SRER', 'TAOEUZ')])
translations  = [Translation(('PHROLG',) : "{PLOVER:TOGGLE}"),
 Translation(('AD', 'TAOEUS') : "advertise")]
stroke = Stroke(TAOEUS : ['T-', 'A-', 'O-', '-E', '-U', '-S'])


# annoying retrospective delete space

old = [Action(text='writer', trailing_space=' ', word='writer'
)]
new = [Action(next_attach=True, prev_attach=True, text='', wor
d='', word_is_finished=False), Action(prev_attach=True, text='
writer', trailing_space=' ', word='writer')]
pass filter
english  = typewriter
stroked  = ['TK-FPS']
suggestions  = [('TWRAOEUR',), ('TAOEUP', 'WREUR'), ('TAOEUP',
 'WRAOEURT'), ('TAOEUP', 'WREU', 'ER'), ('TAOEUP', 'WRAOEUT',
'ER'), ('TAOEUP', 'WRAOEUT', '*ER')]
phrase = ('typewriter', ['TK-FPS'], [('TWRAOEUR',), ('TAOEUP',
 'WREUR'), ('TAOEUP', 'WRAOEURT'), ('TAOEUP', 'WREU', 'ER'), (
'TAOEUP', 'WRAOEUT', 'ER'), ('TAOEUP', 'WRAOEUT', '*ER')])
english  = typewriter
stroked  = ['PHROLG', 'TK-FPS']
suggestions  = [('TWRAOEUR',), ('TAOEUP', 'WREUR'), ('TAOEUP',
 'WRAOEURT'), ('TAOEUP', 'WREU', 'ER'), ('TAOEUP', 'WRAOEUT',
'ER'), ('TAOEUP', 'WRAOEUT', '*ER')]
phrase = ('typewriter', ['PHROLG', 'TK-FPS'], [('TWRAOEUR',),
('TAOEUP', 'WREUR'), ('TAOEUP', 'WRAOEURT'), ('TAOEUP', 'WREU'
, 'ER'), ('TAOEUP', 'WRAOEUT', 'ER'), ('TAOEUP', 'WRAOEUT', '*
ER')])
translations  = [Translation(('PHROLG',) : "{PLOVER:TOGGLE}"),
 Translation(('TK-FPS',) : "type{^~|^}writer")]
stroke = Stroke(TK-FPS : ['T-', 'K-', '-F', '-P', '-S'])

