from django.shortcuts import render, redirect
from vanilla import TemplateView, FormView

from .forms import OpportunityRankingForm

from pyexpa.pyexpa.api import ExpaApi


class FilterOpportunities(FormView):
    template_name = "opportunity_ranking/form.html"

    def get_form(self, data=None, files=None, *args, **kwargs):
        ex_api = ExpaApi(token='e316ebe109dd84ed16734e5161a2d236d0a7e6daf499941f7c110078e3c75493')
        mc_list = ex_api.make_query(['lists', 'mcs'])
        choices = [(mc['id'], mc['name']) for mc in mc_list]
        return OpportunityRankingForm(choices=choices, data=data, files=files, *args, **kwargs)

    def form_valid(self, form):
        post_data = self.request.POST
        query_params = {
            'filters[for]': 'people',
            'filters[is_pop_user]': 'false',
            'filters[programmes]': post_data['program'],
            'filters[statuses]': 'open',
        }
        if start_date_day in post_data and start_date_month in post_data and start_date_year in post_data:
            query_params['start_date'] = "%s-%s-%s" % (post_data['start_date_day'], post_data['start_date_month'], post_data['start_date_year'], )
        if end_date_day in post_data and end_date_month in post_data and end_date_year in post_data:
            query_params['end_date'] = "%s-%s-%s" % (post_data['end_date_day'], post_data['end_date_month'], post_data['end_date_year'], )
        if office in post_data:
            query_params['filters[committee]'] = post_data['office']

        raise Exception("was")


# Create your views here.
