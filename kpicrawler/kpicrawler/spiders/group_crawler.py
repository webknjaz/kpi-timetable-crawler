#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class implements crawler of all student groups @ the NTUU 'KPI'.
Developed by Sviatoslav Sydorenko.
"""

from bs4 import BeautifulSoup
import json

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import FormRequest
from scrapy.http import Request

from kpicrawler.items import KpiGroupItem


class KPIGroupSpider(CrawlSpider):
    """Spider for KPI groups"""

    name = "GroupsCrawler"
    allowed_domains = ["rozklad.kpi.ua", ]
    start_urls = ["http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx"]

    def parse_start_url(self, response):
        """Initial request"""

        req = Request(url='http://rozklad.kpi.ua/Schedules'
                          '/ScheduleGroupSelection.aspx/GetGroups',
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

        #yield FormRequest(url='http://rozklad.kpi.ua/Schedules'
        #                      '/ScheduleGroupSelection.aspx/GetGroups',
        #                   method='POST', encoding='utf-8',
        #                   formdata={
        #                       "prefixText": "ІК-"
        #                   },
        #                   headers={
        #                       "Content-Type":
        #                           "application/json; charset=UTF-8"
        #                   },
        #                   callback=self.iterate_groups_list)

    def iterate_groups_list(self, response):
        """docstring for navigate_tabs"""

        for group in json.loads(response.body)['d']:
            req = FormRequest.from_response(response.meta['orig_resp'],
                                            formdata={
                                                'ctl00$MainContent'
                                                '$ctl00$txtboxGroup': group
                                            },
                                            callback=self.add_gid)
            req.meta['group_item'] = KpiGroupItem()
            req.meta['group_item']['name'] = group
            req.meta['dont_redirect'] = True
            req.meta['handle_httpstatus_list'] = [302]
            yield req

    def add_gid(self, response):
        """docstring for add_gid"""

        try:
            response.meta['group_item']['id'] = \
                                            response.headers['Location'][31:]
            yield response.meta['group_item']
        except KeyError:
            # If there's no HTTP redirect in response, then groups with such
            # name exist in several departments;
            # let's process this case in subroutine
            for group_item in self.grep_groups(response):
                yield group_item

    def grep_groups(self, response):
        """
        Adding 'full_name' to `response.meta['group_item']`
        as it's meant to be unique
        """
        soup = BeautifulSoup(response.body)
        for group_link in soup.table.find_all('a', href=True):
            group_item = response.meta['group_item']
            group_item['full_name'] = group_link.text
            group_item['id'] = group_link['href'][20:]
            yield group_item

    def log(self, message_obj, **kwargs):
        """
        Override default method to make possible logging of non-string objects
        """

        try:
            message = str(message_obj)
        except:
            message = message_obj

        super(KPIGroupSpider, self).log(message, **kwargs)
