import datetime

class ErrorChecker:
    """
     Class is used to error check user-provided date

     Attributes
     ----------
     number : float
         Number of dividends provided by a user
     date : str
         Transaction date provided by a user

     Methods
     -------
     check_div_amount()
         Check if the uses provided a valid dividend amount
     check_txn_date()
         Check if the uses provided a valid transaction date

     """
    def __init__(self, number=10.0, year="2022"):
        self.number = number
        self.year = year

    def check_div_amount(self):
        """
        Check if the uses provided a valid dividend amount

        Returns
        -------
        bool
            True if the number is not a valid float or is less than or equal to zero
            False otherwise
        """
        try:
            float(self.number)
        except ValueError:
            return True
        if float(self.number) < 0:
            return True
        return False

    def check_year(self):
        """
        Check if the uses provided a valid year information

        Returns
        -------
        bool
            True if the number is not a valid year, or it is before 2011
            False otherwise
        """
        try:
            int(self.year)
        except ValueError:
            return True
        if len(self.year) != 4:
            return True
        if int(self.year) < 2011:
            return True
        if int(self.year) > datetime.datetime.now().year:
            return True
        return False
