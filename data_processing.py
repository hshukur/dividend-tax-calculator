import datetime
import requests

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
        # print(f"The FX rate for {self.new_date} was {usd_fx_rate}")
        return usd_fx_rate
