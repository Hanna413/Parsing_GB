import scrapy
from scrapy.http import HtmlResponse
from project_parser_hh.items import ProjectParserHhItem


class HhRuSpider(scrapy.Spider):

    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://spb.hh.ru/search/vacancy?area=76&search_field=name&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&items_on_page=20',
        'https://spb.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&items_on_page=20'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath("//div[@class='serp-item']//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for url_vacancy in urls_vacancies:
            yield response.follow(url_vacancy, callback=self.vacancy_parse)


    def clean_salary(self, vacancy_salary_text, min_salary=None, max_salary=None, currency_salary=None):
        list_salary = vacancy_salary_text.replace('\u202f', '').split()
        for i in range(len(list_salary) - 1):
            if list_salary[i] == 'от':
                min_salary = int(list_salary[i + 1])
            elif list_salary[i] == 'до':
                max_salary = int(list_salary[i + 1])
            elif list_salary[i] == '–':
                min_salary = int(list_salary[i - 1])
                max_salary = int(list_salary[i + 1])
                currency_salary = list_salary[-1]

        return min_salary, max_salary, currency_salary


    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        if vacancy_salary:
            vacancy_salary = vacancy_salary.text
            min_salary, max_salary, currency_salary = clean_salary(vacancy_salary)
        else:
            vacancy_salary = 'З/П не указана'
            min_salary, max_salary, currency_salary = None, None, None

        vacancy_url = response.url

        yield ProjectParserHhItem(
            name=vacancy_name,
            salary=vacancy_salary,
            min_salary = min_salary,
            max_salary = max_salary,
            currency = currency_salary,
            url=vacancy_url
        )
