from scrapy.http import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from AmazonScraper.items import DetailsItem


class AmazonSpider(CrawlSpider):
    name = "amazon"
    allowed_urls = ["amazon.com"]
    start_urls = [
            "http://www.amazon.com/books-used-books-textbooks/b/ref=nav_shopall_bo?ie=UTF8&node=283155",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths = "(//div[@class='categoryRefinementsSection']/ul/li)"), callback="sort_books"),
    )

    #sort books by the number of their reviews
    def sort_books(self, response):
        sorted_form = FormRequest.from_response(
            response,
            formxpath="//form[@id='searchSortForm']", #xpath of form
            formdata={"sort":"review-count-rank"}, #id of select node("sort") and value of "Most Reviews"("review-count-rank")
            clickdata={"value":"Go"}, #the button we "click"
            callback=self.parse_category #the method we execute on the sorted page
        )
        yield sorted_form

    def parse_category(self, response):
        links = response.xpath("//a[@class='a-link-normal s-access-detail-page  a-text-normal']/@href")
        for link in links:
            url = response.urljoin(link.extract())
            yield Request(url, callback=self.parse_book_page)

    def parse_book_page(self,response):
        details = DetailsItem()
        details["title"] = response.xpath("(//span[@id='productTitle' or @id='ebooksProductTitle']/text())").extract()
        details["file_size"] = response.xpath( self.getxpath_by_text('File Size:') ).extract()
        details["print_length"] = response.xpath( self.getxpath_by_text('Print Length:') ).extract()
        details["paperback"] = response.xpath( self.getxpath_by_text("Paperback:") ).extract()
        details["publisher"] = response.xpath( self.getxpath_by_text("Publisher:") ).extract()
        details["language"] = response.xpath( self.getxpath_by_text("Language:") ).extract()
        details["isbn_10"] = response.xpath( self.getxpath_by_text("ISBN-10:") ).extract()
        details["isbn_13"] = response.xpath( self.getxpath_by_text("ISBN-13:") ).extract()
        details["dimensions"] = response.xpath( self.getxpath_by_text("Product Dimensions:") ).extract()
        details["weight"] = response.xpath( self.getxpath_by_text("Shipping Weight:") ).extract()
        details["average_customer_review"] = response.xpath("//span[@class='crAvgStars']/span/a/span/@title").extract()
        yield details

    def getxpath_by_text(self, text):
        item_xpath_start = "//div[@class='content']/ul/li/b[contains(.,'"
        item_xpath_end = "')]/parent::li/text()"
        xpath = item_xpath_start+text+item_xpath_end
        return xpath
