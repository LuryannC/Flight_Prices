# Flight_Prices
This bot was created solely for research purposes and should not be sold or distributed. Feel free to change the source code but, however, please always refer to me.

Bot to find flight details in the provided dates and export as a XLSX file.

Site scrapped:
  - http://www.skyscanner.net


# How to run

Clone the repository and install the requirements.
``` CMD
git clone https://github.com/LuryannC/Flight_Prices.git && cd Flight_Prices
pip install -r requirements.txt
```
To finally run:
``` CMD
python.exe .\Start.py
```

The results are stored in ```./Flight_Prices/data/(filename).xlxs```

# How long it takes to get the data

The bot was defined to take 1min to get the data and output it into a file.
It was set this way due the website protection against bot, as once deteceted it will bring the captcha every time an element is clicked and soft lock your IP for a few minutes.
