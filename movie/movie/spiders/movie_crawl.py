import scrapy
class MovieSpider(scrapy.Spider):
    name = "movie"
    start_urls = [f"https://www.boxofficemojo.com/year/{1990 + i}" for i in range (33)]
    def parse(self,response):
        for data in response.css("tr")[1:300]:
            next_page = data.css("td.a-text-left.mojo-field-type-release.mojo-cell-wide a.a-link-normal").attrib["href"]
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse_data_page)
    def parse_data_page(self,response):
        movie = response.css("div.a-fixed-left-grid-col.a-col-right h1.a-size-extra-large::text").get()
        for grosses in response.css(".mojo-performance-summary-table"):
            domestic = grosses.css("div:nth-child(2) > span:nth-child(3) > span:nth-child(1)::text").get()
            international = grosses.css("div:nth-child(3) > span:nth-child(3) > a:nth-child(1) > span:nth-child(1)::text").get()
            worldwild = grosses.css("div:nth-child(4) > span:nth-child(3) > a:nth-child(1) > span:nth-child(1)::text").get()
        for data in response.css(".mojo-summary-values"):
            distributor = data.css("div:nth-child(1) > span:nth-child(2)::text").get()
            opening = data.css("div:nth-child(2) > span:nth-child(2) > span:nth-child(1)::text").get()
            if data.css("div:nth-child(3) > span:nth-child(1)::text").get() == "Budget":
                budget = data.css("div:nth-child(3) > span:nth-child(2) > span:nth-child(1)::text").get()
            if data.css("div:nth-child(4) > span:nth-child(1)::text").get() == "Release Date":
                release_date = data.css("div:nth-child(4) > span:nth-child(2) > a:nth-child(1)::text").get()
            if data.css("div:nth-child(5) > span:nth-child(1)::text").get() == "MPAA":
                MPAA = data.css("div:nth-child(5) > span:nth-child(2)::text").get()
            if data.css("div:nth-child(6) > span:nth-child(1)::text").get() == "Running Time":
                running_time = data.css("div:nth-child(6) > span:nth-child(2)::text").get()
            if data.css("div:nth-child(7) > span:nth-child(1)::text").get() == "Genres":
                genres = data.css("div.a-section:nth-child(7) > span:nth-child(2)::text").get()
        yield{
            "Movies":movie,
            "Domestic":domestic,
            "International":international,
            "Worldwild":worldwild,
            "Distributor":distributor,
            "Opening":opening,
            "Budget":budget,
            "Release_Date":release_date,
            "MPAA":MPAA,
            "Runing_Time":running_time,
            "Genres":genres
        }
