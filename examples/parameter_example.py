from cadquery import Workplane, Vector
from pyqtgraph.parametertree import Parameter


####BOX EXAMPLE####

#param() will check if Parameter.name() is already loaded and return the Parameter if found 

parameter = param(
    Parameter(
        name='box',
        children=[
            {'name': 'Height', 'type': 'float', 'value': 1},
            {'name': 'Width', 'type': 'float', 'value': 1},
            {'name': 'Depth', 'type': 'float', 'value': 1},
        ]
    )
)

h = parameter['Height']
w = parameter['Width']
d = parameter['Depth']

box = Workplane().box(w,d,h)
show_object(box,param=parameter)


####SPHERE EXAMPLE####

sphere_param = param(
    Parameter(
        name='sphere',
        children=[
            {'name': 'Height', 'type': 'float', 'value': 1},
        ]
    )
)

h=sphere_param['Height']

sphere = Workplane().center(2,0).sphere(h/2)
show_object(sphere, param=sphere_param)


####CUSTOM PARAMETER####

from pyqtgraph.parametertree.parameterTypes import GroupParameter
class ComboParameter(GroupParameter):
    def __init__(self, **opts):
        GroupParameter.__init__(self, **opts)
    
        self.addChildren(
            [
                { 'name': 'Shape', 'type': 'list', 'value': 'box', 'limits': ['box', 'sphere'] },
                { 'name': 'Width', 'type': 'float', 'value': 1.0, 'suffix': 'mm' },
                { 'name': 'Depth', 'type': 'float', 'value': 1.0,  'suffix': 'mm'},
                { 'name': 'Height', 'type': 'float', 'value': 1.0, 'suffix': 'mm'},
            
            ]
        )
        
        self.shape = self.param('Shape')
        self.width = self.param('Width')
        self.depth = self.param('Depth')
        
        self.shape.sigValueChanged.connect(self.shape_changed)
    
    def shape_changed(self):
        if self.shape.value() == 'box':
            self.width.setOpts(visible=True)
            self.depth.setOpts(visible=True)
        elif self.shape.value() == 'sphere':
            self.width.setOpts(visible=False)
            self.depth.setOpts(visible=False)

def build(param):
    result = Workplane()

    shape = param['Shape']
    h = param['Height']
    w = param['Width']
    d = param['Depth']
    
    if shape == 'sphere':
        result = result.sphere(h/2)
    elif shape == 'box':
        result = result.box(w,d,h)
        
    return result
    
c1_param = param(ComboParameter(name='c1'))
combo1 = build(c1_param).translate(Vector(4,0,0))
show_object(combo1,param=c1_param)

c2_param = param(ComboParameter(name='c2'))
combo2 = build(c2_param).translate(Vector(6,0,0))
show_object(combo2,param=c2_param)


###HELLO WORLD####

from PyQt5.QtGui import QFontInfo
class TextParameter(GroupParameter):
    def __init__(self, **opts):
        GroupParameter.__init__(self, **opts)
    
        self.addChildren(
            [   
                {'name': 'Value', 'type': 'str', 'value': 'Hello World'},
                {'name': 'Height', 'type': 'float', 'value': 1.0, 'suffix': 'mm'},
                {'name': 'Text Size', 'type': 'float', 'value': '2.0', 'suffix': 'pts'},
                {'name': 'Font', 'type': 'font', 'value': 'Arial'},
                {
                    'name': 'Kind', 
                    'type': 'list',
                    'limits': ['regular', 'bold', 'italic'], 
                    'value': 'regular'
                },
                {
                    'name': 'H Align', 
                    'type': 'list', 
                    'limits': ['center', 'left', 'right'], 
                    'value': 'left'
                },
                {
                    'name': 'V Align', 
                    'type': 'list',
                    'limits': ['center', 'top', 'bottom'] ,  
                    'value': 'center'
                },

            ]
        )

t = param(TextParameter(name='text'))
props = (t['Value'],t['Text Size'],t['Height'],False,False,True,
         QFontInfo(t['Font']).family(),None,t['Kind'],t['H Align'],t['V Align'])

text = Workplane().center(8,0).text(*props)
show_object(text, param=t)















