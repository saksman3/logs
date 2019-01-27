from django import forms

class EmailForm(forms.Form):
    Email_address = forms.EmailField(max_length=254)


class LogSearchForm(forms.Form):
#    class Meat:


    search_log =  forms.CharField(
                    required = False,
                    label='Search log',
                    widget=forms.TextInput(attrs={'placeholder': 'search here!'})
                  )
    search_logid_exact = forms.IntegerField(
                    required = False,
                    label='Search logID (exact match)!'
                  )

    search_logTime = forms.TimeField(
                    required = False,
                    label='search log time'
                  )


    search_logDate = forms.DateField(
                    required = False,
                    label='search log date',
                    widget = forms.DateInput(format="Y-m-d",attrs={'class': 'datepicker'})
                  )
