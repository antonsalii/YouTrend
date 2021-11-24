from wtforms import Form, StringField, SelectField


class SearchForm(Form):
    choices = [
        ('day', 'Today'),
        ('week', 'This week'),
        ('month', 'This month'),
        ('year', 'This year'),
    ]
    select = SelectField('Time Period:', choices=choices)
    search = StringField('', render_kw={"placeholder": "Search"})

