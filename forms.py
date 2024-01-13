from wtforms import Form, StringField, SelectField

class SportEquipmentSearchForm(Form):
    choices = [('SportEquipment', 'SportEquipment')]
    select = SelectField('Search for sport equipment:', choices=choices)
    search = StringField('')