import scrapy

class LanguageDailySpider(scrapy.Spider):
    name = 'common_german_words'
    start_urls = [
        'http://languagedaily.com/learn-german/vocabulary/common-german-words',
        'http://languagedaily.com/learn-german/vocabulary/most-common-german-words-2'
    ] + list([
        f'http://languagedaily.com/learn-german/vocabulary/common-german-words-{page}'
        for page in range(3, 13)
    ])

    def parse(self, response):
        for row in response.css('.jsn-article-content table tr'):
            columns = row.css('td ::text').extract()
            if 'Rank' not in columns[0]:
                yield {
                    'rank': int(columns[0].strip().replace('.', '')),
                    'german_word': columns[1].strip(),
                    'english_translation': columns[2].strip(),
                    'part_of_speech': columns[3].strip(),
                    'url': response.url
                }
