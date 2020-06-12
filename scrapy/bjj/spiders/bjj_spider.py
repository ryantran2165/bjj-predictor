import scrapy
from ..items import BjjItem

class BjjSpider(scrapy.Spider):
    name = 'bjj'
    start_urls = [
        'https://www.bjjheroes.com/a-z-bjj-fighters-list'
    ]

    def parse(self, response):
        table = response.css("tbody.row-hover")
        rows = table.css("tr")

        for i in range(0, len(rows)):
            row = table.css("tr.row-" + str(i + 2))
            href = row.css("td.column-1 a::attr(href)").get()

            item = BjjItem()
            item['id'] = href[4:]
            item['first_name'] = row.css("td.column-1 a::text").get()
            item['last_name'] = row.css("td.column-2 a::text").get()
            item['nickname'] = row.css("td.column-3 a::text").get()

            # Team may or may not have link
            if row.css("td.column-4 a::text"):
                item['team'] = row.css("td.column-4 a::text").get()
            else:
                item['team'] = row.css("td.column-4::text").get()

            # Go to actual fighter page and get stats
            yield scrapy.Request(response.urljoin(href), callback=self.parse_fighter, meta={'item': item}, dont_filter=True)

    def parse_fighter(self, response):
        # Only include fighters with a history
        if response.css("div.fighter_info_plug"):
            # Retrieve the item
            item = response.meta['item']

            # Wins
            wins_text = response.css("div.wrapper_canvas span.t_wins em::text").get()
            item['wins'] = int(wins_text.split()[0])

            # Wins by submission
            win_dividers = response.css("div.wrapper_canvas ul.divs li.divider")
            item['wins_by_sub'] = int(win_dividers[2].css("div.points_info span.per_no::text").get())

            # Losses
            losses_text = response.css("div.wrapper_canvas_lose span.t_wins em::text").get()
            item['losses'] = int(losses_text.split()[0])

            # Losses by submission
            loss_dividers = response.css("div.wrapper_canvas_lose ul.divs li.divider")
            item['losses_by_sub'] = int(loss_dividers[2].css("div.points_info span.per_no_lose::text").get())

            # Get all tables, possibly including the conquered/conceded tables
            tables = response.css("tbody")

            # Get the history table's rows
            rows = tables[-1].css("tr")

            # Create empty history
            item['history'] = []

            # Go through every table row
            for row in rows:
                # Skip first td because it's weird for some reason
                table_datas = row.css("td")[1:]

                # Only include fights versus opponents with a page link
                if table_datas[0].css("a"):
                    # Get only the number part of the url
                    opponent_id = table_datas[0].css("a::attr(href)").get()[4:]
                    opponent_name = table_datas[0].css("a::text").get()
                    win_loss = table_datas[1].css("::text").get()

                    # Win/loss method may or may not have a link
                    if table_datas[2].css("a"):
                        method = table_datas[2].css("a::text").get()
                    else:
                        method = table_datas[2].css("::text").get()

                    competition = table_datas[3].css("::text").get()
                    weight = table_datas[4].css("::text").get()
                    stage = table_datas[5].css("::text").get()
                    year = table_datas[6].css("::text").get()

                    item['history'].append({
                        "opponent_id": opponent_id,
                        "opponent_name": opponent_name,
                        "win_loss": win_loss,
                        "method": method,
                        "competition": competition,
                        "weight": weight,
                        "stage": stage,
                        "year": year
                    })

            yield item
