from django import forms


class OpportunityRankingForm(forms.Form):
    def __init__(self, choices=None, *args, **kwargs):
        super(OpportunityRankingForm, self).__init__(*args, **kwargs)
        self.fields["office"] = forms.ChoiceField(label="MC", choices=choices, required=False)
    start_date = forms.DateField(label="Start date", widget=forms.SelectDateWidget(years=[2016, 2017, 2018]), required=False)
    end_date = forms.DateField(label="End date", widget=forms.SelectDateWidget(years=[2016, 2017, 2018]), required=False)
    program = forms.ChoiceField(label="Program", choices=[(1, "GV"), (2, "GT"), (5, "GE")])
