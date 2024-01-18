**This project contains dependencies that are intended for personal use only.**

Please check https://pypi.org/project/yfinance/

---

# Trading Experiments

Make back-tests easier for technical-based trading strategies!
Simply create a Jupyter notebook in the project directory and start using the
provided APIs!

Repository structure:
* `configuration/` contains configuration files used for downloading market data
* `reporting/` contains the APIs to report data as graphs or logs
* `trading/` contains the main library (mostly for technical indicators) and is
             suitable for one-day-resolution data
* `data*/` contains data that could be used by notebooks
* `generate_data.py` downloads market data
* `preprocess_*.py` preprocesses the downloaded data and generates intermediate
                    forms which could be easily parsed
* `notebook_*.ipynb` are the notebooks

Naming conventions:
* Every file may have a `main` and can be used for sanity-checking
* `n_days` `ptnd` means including data from `n` days ago to the current day
* `a` denotes an array of `[trading_day] -> [value]`
* `db` denotes a dictionary of `[ticker_name] -> a`

# Dependencies

```sh
pip install notebook
pip install plotly
pip install pprint
pip install yfinance
```

# Demo

Please create a `txt` file with ticker names (one ticker symbol per line).
Running out of idea? Try https://github.com/datasets/s-and-p-500-companies/blob/main/data/constituents.csv

```sh
python generate_data.py --out-dir "data240117qqq" --config "configuration/my-tickers.txt"
python preprocess_my_data.py --in-dir "data240117qqq"
jupyter notebook # then open notebook_inspect_my_data.ipynb and play around!
```
