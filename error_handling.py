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
    def __init__(self, number, date):
        self.number = number
        self.date = date

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
        if float(self.number) <= 0:
            return True
        return False

    def check_txn_date(self):
        """
        Check if the uses provided a valid transaction dates

        Returns
        -------
        bool
            True if the date is not valid or earlier than 2 January 2002
            False otherwise
        """
        split_list = self.date.split("-")
        try:
            expected_date = datetime.date(int(split_list[0]), int(split_list[1]), int(split_list[2]))
        except (ValueError, IndexError):
            return True
        if expected_date < datetime.date(2002, 1, 2):
            return True
        return False
