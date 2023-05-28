[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![Linkedin: hatamshukur](https://img.shields.io/badge/LinkedIn-informational?logo=linkedin)](https://www.linkedin.com/in/hatamshukur/)


# Dividend Tax Calculator
<img src="https://github.com/hshukur/dividend-tax-calculator/blob/master/app_gui.png" alt="Alt text" width=500 title="Optional title">

Please make sure to read this before using the application.

## What is this tool?
This tool can help to calculate the amonut of tax you need to pay as a tax resident of Poland for dividends received from stocks owned in United States of America.

## Installation process
### Prerequisites
Make sure you have Python and Git installted on your laptop or PC.
* Installing Python: https://www.python.org/downloads/
* Installing GIt: https://github.com/git-guides/install-git

**Step 1.** Open a command prompt on your laptop or PC.

**Step 2.** Clone the repository using Git by running the following command:
```bash
git clone https://github.com/hshukur/dividend-tax-calculator
```

**Step 3.** Change into the project directory using the cd command:
```bash
cd dividend-tax-calculator/
```

**Step 4.** Install the required Python packages:
```bash
pip install -r requirements.txt
```

**Step 5.** Now you can run the application using the following command:
```bash
python main.py
```

## How is tax being calculated?
The tax calculator tool assumes that you have a valid W-8BEN form submitted.

Which means that you are already paying 15% tax in USA and only need to pay the 4% tax in Poland.

When you specify a year you want to calculate the tax for, 
the tool goes to [Investor Relations](https://investor.cisco.com/stock-information/dividends-and-splits/default.aspx)
and checks how many times dividends were paid that year and what was the payment date.

After that's done the user is asked to provide the amount of dividends they received for each payment date.

Once the submit button is clicked, this logic is used:
1. Calculate 19%, 15%, 4% of each dividend amount specified
2. Calculate a day prior the specified transaction date
3. Get the USD FX rate from NBP (National Bank of Poland) for the date calculated in step 2
    - If there is no information present on NBP for that day (i.e. non-business day), go back to step 2.
5. Calculate the gain, total tax, tax paid in the USA, and tax to be paid in Poland.
6. Present the data for each entry and in total

## Is my data being sent somewhere?
No, the data you provide is processed locally and not being sent anywhere.
  
## Important Notice
The tax calculator tool assumes that you have a valid W-8BEN form submitted.

The tool is intended for informational purposes only and should not be considered a substitute for professional tax advice.

Tax laws and regulations can vary by jurisdiction and may change over time. 

By using this tax calculator tool, you acknowledge and agree that the author(s) and contributors are not responsible for any consequences, losses, or damages resulting from the use of the tool.

Please use this tax calculator tool responsibly and seek professional advice when needed.
