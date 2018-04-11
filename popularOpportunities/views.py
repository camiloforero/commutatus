from django.shortcuts import render, redirect
from vanilla import TemplateView, FormView

from .forms import OpportunityRankingForm

from pyexpa.pyexpa.api import ExpaApi

import random


class FilterOpportunities(FormView):
    template_name = "opportunity_ranking/form.html"

    def get_form(self, data=None, files=None, *args, **kwargs):
        ex_api = ExpaApi(token='e316ebe109dd84ed16734e5161a2d236d0a7e6daf499941f7c110078e3c75493')
        mc_list = ex_api.make_query(['lists', 'mcs'])
        choices = [(mc['id'], mc['name']) for mc in mc_list]
        choices.insert(0, (0, '---------'))
        return OpportunityRankingForm(choices=choices, data=data, files=files, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        sdgs = [
            "No Poverty",
            'No Hunger',
            'Good Health and Wellness',
            'Quality Education',
            'Gender Equality',
            'Clean Water and Sanitation',
            'Renewable Energy',
            'Good Jobs and Economic Growth',
            'Innovation and Infrastructure',
            'Reduced Inequalities',
            'Sustainable Cities and Communities',
            'Responsible Consumption',
            'Climate Action',
            'Life Below Water',
            'Life on Land',
            'Peace and Justice',
            'Partnership for the Goals',
        ]
        programs = {'1': 'oGV', '2': 'oGT', '5': 'oGE'}
        post_data = self.request.POST
        context = self.get_context_data(**kwargs)
        query_params = {
            'filters[for]': 'people',
            'filters[is_pop_user]': 'false',
            'filters[programmes][]': [post_data['program']],
            'filters[statuses][]': ['open'],
            'per_page': 50,
            'page': 1,
        }
        if post_data['start_date_day'] != '0':
            query_params['filters[created][from]'] = "%s-%s-%s" % (post_data['start_date_day'], post_data['start_date_month'], post_data['start_date_year'], )
        if post_data['end_date_day'] != '0':
            query_params['filters[created][to]'] = "%s-%s-%s" % (post_data['end_date_day'], post_data['end_date_month'], post_data['end_date_year'], )
        if  post_data['office'] != '0':
            query_params['filters[committee]'] = post_data['office']

        ex_api = ExpaApi(token='e316ebe109dd84ed16734e5161a2d236d0a7e6daf499941f7c110078e3c75493')
        ops = ex_api.make_query(['opportunities'], query_params)
        ops_data = ops['data']

        if ops['paging']['total_pages'] > 1:
            pages = list(range(2, ops['paging']['total_pages'] + 1))
            random.shuffle(pages)
            for page in pages[:1]: #Takes 10 random pages out of the total amount of opportunities.
                query_params['page'] = page
                ops_data.extend(ex_api.make_query(['opportunities'], query_params)['data'])

        measure = None
        if post_data['program'] == '1':
            measure = 'SDG'
        else:
            measure = 'Background'
            # TODO send http response saying that this is not yet available
        popularity_count = {}
        for opportunity in ops_data:
            if opportunity['sdg_info'] is not None:
                sdg = opportunity['sdg_info']['sdg_target']['goal_index']
                if sdg in popularity_count:
                    popularity_count[sdg] += 1
                else:
                    popularity_count[sdg] = 1
        pop_order = sorted(popularity_count, key=popularity_count.get, reverse=True)
        pop_table = [{'measure': sdgs[x-1], 'amount': popularity_count[x]} for x in pop_order]
        context['measure'] = measure
        context['data'] = pop_table
        context['program'] = programs[post_data['program']]
        return render(self.request, 'opportunity_ranking/ranking_list.html', context)



# Create your views here.
