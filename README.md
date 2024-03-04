# Zillow Scraper

The Zillow Scraper is a Python script designed to scrape real estate data from Zillow.com for multiple cities. It utilizes various techniques to extract property information from the Zillow website and save it into a structured format for further analysis.

## Features

- **Dynamic RapidAPI Key Rotation**: The scraper rotates through multiple RapidAPI keys to avoid rate limiting and ensure smooth scraping operations.
- **Time Interval Conversion**: It converts relative time intervals (e.g., "5 minutes ago") into a standardized format for easier analysis.
- **City-wise Data Scraping**: The scraper can retrieve real estate data for different cities specified in the script, enabling users to target specific locations of interest.
- **Error Handling**: The script includes error handling mechanisms to gracefully handle unexpected situations, such as missing data or network errors.
- **Data Export**: Scraped data is exported to a CSV file, making it convenient for users to analyze the results using tools like Excel or Python libraries like pandas.

## Tech Stack Used

The Zillow Scraper script utilizes a variety of technologies and libraries to achieve its functionality:

- **Python**: The core programming language used for scripting and automation.
- **HTTPX**: A modern, asynchronous HTTP client for Python used for making HTTP requests to the Zillow website and handling responses.
- **Pandas**: A powerful data manipulation library for Python used for structuring and analyzing the scraped real estate data.
- **Scrapy**: A fast, high-level web crawling and web scraping framework used for extracting structured data from HTML pages.
- **Parsel**: A library for extracting data from HTML and XML using XPath and CSS selectors, used in conjunction with Scrapy for parsing HTML content.
- **RapidAPI**: A platform that provides APIs for various purposes. The Zillow Scraper utilizes RapidAPI keys for making requests to the Zillow website to avoid rate limiting.
- **Git**: A version control system used for managing the source code of the project and facilitating collaboration.
- **GitHub**: A web-based hosting service for version control using Git. The Zillow Scraper project is hosted on GitHub, allowing for easy access, collaboration, and version tracking.
- **CSV Format**: The scraped real estate data is exported to CSV (Comma Separated Values) format, which is a simple and widely used file format for storing tabular data. This format enables easy import into spreadsheet software like Excel or analysis using Python's pandas library.

By leveraging this technology stack, the Zillow Scraper script is able to efficiently scrape real estate data from the Zillow website and provide it in a structured format for further analysis and use.

## Requirements

- Python 3.x
- Required Python packages: Mentioned in requirements.txt

## Usage

1. Clone the repository or download the script file (`zillow_scraper.py`) to your local machine.
2. Install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. Open the script file (`zillow_scraper.py`) and update the RapidAPI keys in the `ZillowScraper` class constructor, if necessary.
4. Customize the city URLs in the `city_urls` dictionary to include the cities you want to scrape data for.
5. Run the script:

   ```
   python zillow_scraper.py
   ```

6. After the scraping process is complete, the script will save the scraped data to a CSV file in the `results` folder.

## Contributing

Contributions are welcome! If you encounter any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Disclaimer

This script is intended for educational and research purposes only. Scraping data from websites may violate their terms of service, so use it responsibly and considerate of the website's policies.