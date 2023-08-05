import PySimpleGUI as sg

# Demo of how columns work      
# window has on row 1 a vertical slider followed by a COLUMN with 7 rows      
# Prior to the Column element, this layout was not possible      
# Columns layouts look identical to window layouts, they are a list of lists of elements.

window = sg.Window('Columns')                                   # blank window

# Column layout      
col = [[sg.Text('col Row 1')],      
       [sg.Text('col Row 2'), sg.Input('col input 1')],      
       [sg.Text('col Row 3'), sg.Input('col input 2')],      
       [sg.Text('col Row 4'), sg.Input('col input 3')],      
       [sg.Text('col Row 5'), sg.Input('col input 4')],      
       [sg.Text('col Row 6'), sg.Input('col input 5')],      
       [sg.Text('col Row 7'), sg.Input('col input 6')]]

layout = [[sg.Slider(range=(1,100), default_value=10, orientation='v', size=(8,20)), sg.Column(col)],      
          [sg.In('Last input')],      
          [sg.OK()]]

# Display the window and get values      
# If you're willing to not use the "context manager" design pattern, then it's possible      
# to collapse the window display and read down to a single line of code.      
event, values = sg.Window('Compact 1-line window with column').Layout(layout).Read()

sg.Popup(event, values, line_width=200)
