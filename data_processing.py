import datetime
import requests
import mechanize
from bs4 import BeautifulSoup

class DataProcessor:
    """
    Class is used to process the data provided and make API call to NPB (National Bank of Poland)

    Attributes
    ----------
    provided_date : str
        The transaction date provided by the user
        Date expected to be in YYYY-MM-DD format (ISO "8601 standard")
    delta : int
        Number of days used when calculating a new date
    new_date : str
        new date which will be added after applying delta to provided_date

    Methods
    -------
    increase_delta_by_one()
        Increases self.delta by one
    day_before_transaction()
        Calculates the new date based on delta
    api_call_to_nbp()
        Makes API call to NBP
    get_data_from_nbp()
        Glues all above 3 methods together
    """
    def __init__(self, provided_date):
        self.provided_date = provided_date
        self.delta = 1
        self.new_date = ""
        self.div_payment_data = {}

    def get_div_payment_dates(self):
        URL = "https://investor.cisco.com/stock-information/dividends-and-splits/default.aspx"
        user_agent_header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

        web_browser = mechanize.Browser()
        web_browser.addheaders = [('User-agent', user_agent_header)]
        web_browser.open(URL)
        web_page_content = web_browser.response().read()

        soup = BeautifulSoup(web_page_content, "html.parser")
        payment_date_td = soup.find_all('td', {'data-heading': 'Payment Date'})

        div_payment_dates = []
        for each in payment_date_td:
            new_each = each.span.get_text(strip=True).split("/")
            div_payment_dates.append(new_each)

        for each_date in div_payment_dates:
            month, day, year = each_date
            if year in self.div_payment_data:
                self.div_payment_data[year].append([year, month, day])
            else:
                self.div_payment_data[year] = [[year, month, day]]
        return self.div_payment_data[self.provided_date]

    # def get_specific_year_data(self):
    #
    #     print(self.final_dictionary)
    #     b = self.final_dictionary[self.provided_date]
    #     print(b)
    #
    #     return b

    def increase_delta_by_one(self):
        """
        Increases self.delta by one
        """
        self.delta += 1

    def day_before_transaction(self):
        """
        Calculates the new date based on delta

        Returns
        -------
        str
            new_delta_date - the date after delta calculation
        """
        split_list = self.provided_date.split("-")
        provided_date = datetime.date(int(split_list[0]), int(split_list[1]), int(split_list[2]))
        new_delta_date = (provided_date - datetime.timedelta(days=self.delta)).isoformat()
        return new_delta_date

    def day_before_transaction_new(self, input_date):
        provided_date = datetime.date(int(input_date[0]), int(input_date[1]), int(input_date[2]))
        print(f"{provided_date}")
        new_delta_date = (provided_date - datetime.timedelta(days=self.delta)).isoformat()
        print(f"new {new_delta_date}")
        return new_delta_date

    def api_call_to_nbp(self):
        """
        Makes API call to NBP to get the USD FX rate for provided date
        NBP API documentation: http://api.nbp.pl/en.html

        Returns
        -------
        object
            The Response object, which contains a server’s response to an HTTP request.
        """
        nbp_api_url = "http://api.nbp.pl/api/exchangerates/rates/A/USD"
        request_url = f"{nbp_api_url}/{self.new_date}/"
        request_headers = {'Accept': 'application/json'}
        return requests.get(url=request_url, headers=request_headers, timeout=5)

    def get_data_from_nbp(self):
        """
        Gets user-provided date, calculates delta, makes API call to NBP
        API will return 404 in the case of lack of data for a correctly determined time interval
        That can happen if we are trying to get the FX rate for a non-business day
        In that case the while loop is invoked

        Returns
        -------
        str
            FX rate for USD
        """
        recv_404 = True
        self.new_date = self.day_before_transaction()
        data_from_nbp = self.api_call_to_nbp()
        # print(data_from_nbp.status_code)

        if data_from_nbp.status_code == 400:
            # print(data_from_nbp.status_code)
            return 400
        if data_from_nbp.status_code == 404:
            # print(data_from_nbp.status_code)
            while recv_404:
                self.increase_delta_by_one()
                self.new_date = self.day_before_transaction()
                data_from_nbp = self.api_call_to_nbp()
                if data_from_nbp.status_code == 200:
                    # print(data_from_nbp.status_code)
                    recv_404 = False

        usd_fx_rate = data_from_nbp.json()["rates"][0]["mid"]
        print(f"The FX rate for {self.new_date} was {usd_fx_rate}")
        return usd_fx_rate

    def get_data_from_nbp_new(self, input_date):
        """
        Gets user-provided date, calculates delta, makes API call to NBP
        API will return 404 in the case of lack of data for a correctly determined time interval
        That can happen if we are trying to get the FX rate for a non-business day
        In that case the while loop is invoked

        Returns
        -------
        str
            FX rate for USD
        """

        recv_404 = True

        self.new_date = self.day_before_transaction_new(input_date)
        data_from_nbp = self.api_call_to_nbp()
        # print(data_from_nbp.status_code)

        if data_from_nbp.status_code == 400:
            # print(data_from_nbp.status_code)
            return 400
        if data_from_nbp.status_code == 404:
            # print(data_from_nbp.status_code)
            while recv_404:
                self.increase_delta_by_one()
                self.new_date = self.day_before_transaction()
                data_from_nbp = self.api_call_to_nbp()
                if data_from_nbp.status_code == 200:
                    # print(data_from_nbp.status_code)
                    recv_404 = False

        usd_fx_rate = data_from_nbp.json()["rates"][0]["mid"]
        print(f"The FX rate for {self.new_date} was {usd_fx_rate}")
        return usd_fx_rate
