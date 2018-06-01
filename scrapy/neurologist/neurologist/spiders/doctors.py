# -*- coding: utf-8 -*-
import scrapy
import re

class DoctorsSpider(scrapy.Spider):
    name = 'doctors'
    titleKeys = {
        'Name:': 'name',
        'Background:': 'background',
        'Practice Name:': 'practice_name',
        'Phone Number:': 'phone_number',
        'FAX Number:': 'fax_number',
        'City:': 'city',
        'state:': 'state',
        'Zip code:': 'zip_code',
        'Country:': 'country',
        'Support Group Leader 1:': 'support_group_leader_1',
        'Support Group Leader:': 'support_group_leader_1',
        'Support Group Meeting Place 1:': 'support_group_meeting_place_1',
        'Support Group Meeting Place:': 'support_group_meeting_place_1',
        'Support Group Meeting Time 1:': 'support_group_meeting_time_1',
        'Support Group Meeting Time:': 'support_group_meeting_time_1',
        'Vitals.com Listing:': 'vitals.com_listings',
        'HealthGrades.com Listing:': 'healthGrades.com_listing',
        'WebMD.com Listing:': 'webMD.com_listing'
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'neurologist.pipelines.DoctorCsvPipeline': 300,
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            url=u'http://neuropathysupportnetwork.org/neuropathy-directories-2/?wpbdp_view=all_listings/',
            callback=self.parse
        )

    def parse(self, response):
        profils = response.xpath("/html/body/div[1]/div/div/div[2]/main/div/div[6]//div/div[@class='listing-title']/a/@href").extract()
        for profil in profils:
            yield scrapy.Request(
                url=profil,
                callback=self.parseProfil
            )

    def parseProfil(self, response):
        details = response.xpath("/html/body/div[1]/div/div/div[2]/main/div/div[@class='listing-details cf']//text()").re(r'^([^ \r\n].+)')
        result = {
            'name': '',
            'background': '',
            'practice_name': '',
            'phone_number': '',
            'fax_number': '',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': '',
            'support_group_leader_1': '',
            'support_group_leader_1': '',
            'support_group_meeting_place_1': '',
            'support_group_meeting_time_1': '',
            'vitals.com_listings': '',
            'healthGrades.com_listing': '',
            'webMD.com_listing': ''
        }
        key = None
        insCount = 0
        for detail in details:
            if detail in self.titleKeys:
                key = self.titleKeys[detail]
                insCount = 0
            else:
                detail = detail.replace(',', ' ')
                if insCount == 0:
                    result[key] = detail
                elif insCount > 0:
                    result[key] += " " + detail
                insCount += 1
        yield result
