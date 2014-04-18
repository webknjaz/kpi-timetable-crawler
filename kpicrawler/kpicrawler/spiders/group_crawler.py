#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest
from scrapy.http import Request

from kpicrawler.items import KpiGroupItem


class KPIGroupSpider(CrawlSpider):
    """Spider for KPI groups"""

    name="GroupsCrawler"
    allowed_domains = ["rozklad.kpi.ua", ]
    start_urls = ["http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"]

    def parse_start_url(self, response):
        """Initial request"""

        #self.log('wk===========')
        ##self.log(dir(response))
        #self.log(response.body)
        #self.log('wk===========')
        req = Request(url='http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx/GetGroups',
                           method='POST', encoding='utf-8',
                           body=json.dumps({
                               "prefixText": "%"
                           }),
                           headers={
                               "Content-Type": "application/json; charset=UTF-8"
                           },
                           callback=self.iterate_groups_list)
        req.meta['orig_resp'] = response
        yield req

        #yield FormRequest(url='http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx/GetGroups',
        #                   method='POST', encoding='utf-8',
        #                   formdata={
        #                       "prefixText": "ІК-"
        #                   },
        #                   headers={
        #                       "Content-Type": "application/json; charset=UTF-8"
        #                   },
        #                   callback=self.iterate_groups_list)

    def iterate_groups_list(self, response):
        """docstring for navigate_tabs"""

        response.meta['orig_resp']
        for g in json.loads(response.body)['d']:
            req = FormRequest.from_response(response.meta['orig_resp'],
                                            formdata={
                                                'ctl00$MainContent$ctl00$txtboxGroup': g
                                            },
                                            callback=self.add_gid)
            req.meta['group_item'] = KpiGroupItem()
            req.meta['group_item']['name'] = g
            req.meta['dont_redirect'] = True
            req.meta['handle_httpstatus_list'] = [302]
            #self.log(req.meta['group_item'])
            yield req
            #yield req.meta['group_item']
            #yield g

    def add_gid(self, response):
        """docstring for add_gid"""

        try:
            response.meta['group_item']['id'] = \
                                            response.headers['Location'][31:]
        except:
            self.log('wk==================================================================')
            self.log('wk==================================================================')
            self.log('wk==================================================================')
            self.log('wk==================================================================')
            self.log('wk==================================================================')
            self.log('Failed. Headers are:')
            self.log(response.headers)
        yield response.meta['group_item']
