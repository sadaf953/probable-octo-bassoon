from forex_python.converter import CurrencyRates
from forex_python.exceptions import CurrencyRatesError

c = CurrencyRates()

def convert_currency(amount, from_currency, to_currency='INR'):
    """Converts specified currencies to INR with error handling."""
    supported_currencies = {'USD', 'GBP', 'AUD'}
    if from_currency not in supported_currencies:
      raise ValueError(f"Unsupported currency: {from_currency}. Only USD, GBP, and AUD are supported.")
    try:
        converted_amount = c.convert(amount, from_currency, to_currency)
        return converted_amount
    except CurrencyRatesError as e:
        return f"Currency conversion error: {e}. Please check currency codes."
    except Exception as e:
        return f"An unexpected error occurred: {e}"