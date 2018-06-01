# -*- coding: utf-8 -*-
import scrapy


class DoctorfieldsSpider(scrapy.Spider):
    name = 'doctorFields'

    custom_settings = {
        'ITEM_PIPELINES': {
            'neurologist.pipelines.FieldPipeline': 301,
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
                callback=self.parseField
            )

    def parseField(self, response):
        fields = response.xpath('/html/body/div[1]/div/div/div[2]/main/div/div[3]//div//text()').re(r'.*:')
        yield {'fields': fields}
