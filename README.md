# U.S. Senator's Trading Visualization

## Project Description

### U.S. Senator's Trading Visualization with Alignment to Your Investment Preferences

This project aims to build a data visualization tool to analyze U.S. senator's trading activities, utilizing data scraped from [TrendSpider](https://trendspider.com/markets/congress-trading) and market performance data from APIs like [Yahoo Finance](https://finance.yahoo.com). The application features interactive charts to uncover insights such as popular investment sectors, trading trends, and profit standings among senators. Additionally, a **Align Your Investment Strategy** feature helps users identify senators with investment strategies that align with their own. Built on Streamlit, the project provides a transparent and engaging way to explore senator's trading behaviors and investigate the possibility of insider trading.

## Project Setup

Follow the steps in **terminal** below to set up the repository and run the project locally:

> *The shown commands are for **PowerShell**, use the appropriate commands depending on your operating system!*

### 1. Clone the Repository

```sh
mkdir <project-directory>  # Replace `<project-directory>` with folder name of your choice
cd <project-directory>
git clone <repository-url>  # Replace `<repository-url>` with the repository URL from GitHub
```

*Alternatively, depending on your preference, you can clone this repository securely using SSH, offering a seamless and encrypted connection tailored to your workflow.*

### 2. Python Compatibility

To successfully run this project, please make sure you have **Python 3.10** or greater.

### 3. Set Up a Virtual Environment and Activate It

```sh
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in the CLI.

*To leave the virtual environment, use the `deactivate` command.*

### 4. Install Dependencies

```sh
cd <repository>
pip install -r requirements.txt  # Install dependencies for project to run
```

If you would like to run the tests for the project using **pytest** and **flake8**, install the required testing dependencies:

```sh
pip install -r requirements_test.txt  # Install dependencies for testing the project
```

### 5. Run the project

```sh
streamlit run main.py
```

### Tests

To run the **Tests** for the project, please navigate to the root directory of the project and follow the instructions below:

- **Flake8**: The project follows the PEP8 formatting guidelines, except for `E501` (due to text displaying and data manipulation). To run *flake8*, execute the following command in the root directory:

```sh
flake8
```

- Pytest - For the project, tests are implemented with *pytest* in the **Tests** directory. To run *pytest*, execute the following command in the root directory:

```sh
pytest
```

## Details

### Data

The data for this project is sourced from multiple regularly updated platforms to ensure accurate and comprehensive insights into U.S. senator's trading activities:

- **[TrendSpider](https://trendspider.com/markets/congress-trading)**:  
  Scraped tables containing the most recent trading activities of U.S. senators, updated daily with disclosures. This data includes details on the financial instruments being traded, transaction types, and trends among senators and political affiliations.
  
- **[Yahoo Finance](https://finance.yahoo.com/)**:  
  API for fetching real-time and historical market data, including stock prices, performance trends, and metadata about financial instruments. This data complements the trading activities, enabling deeper analysis of market performance and senator trades.

- **[Wikipedia](https://en.wikipedia.org/)**:  
  API used to gather biographical information about U.S. senators, such as their profiles, political affiliations, and voting behavior. This context helps to enrich the analysis by linking trading habits with political backgrounds.

### Inspiration

The motivation behind this project originates from widespread discussions online about whether politicians can leverage insider knowledge gained from their work in legislation to influence market outcomes. I was inspired by the presence of trading bots that mirror politician's portfolios, further fueling concerns about potential conflicts of interest. Additionally, there is a prevailing belief that politicians might achieve disproportionate profits due to insider trading.  

This project aims to help answer these questions by providing insights and transparency into the trading activities of U.S. senators, allowing a clearer understanding of whether these concerns are justified.

### Further Improvements

- **SQLite Database Implementation**:  
  Introducing an SQLite database would enhance data storage and retrieval efficiency, allowing faster queries and better management of large datasets.

- **Better API Call Handling**:  
  Optimizing API calls for faster downloads and providing a better user experience with a progress bar is crucial. This can include:
  - Using asynchronous requests.
  - Implementing caching for frequent queries.
  - Opting for faster and more reliable APIs.  
  However, the project relies on multiprocessing techniques for data retrieval, which inherently limits opportunities to present meaningful progress updates to the user.

- **Adding More Information Sources**:  
  Integrating additional data sources like legal and market news would provide richer context. Correlating senator's trading activities with legislative updates and market shifts would offer deeper insights and a more comprehensive view.

- **Automatic Data Updates & Web Hosting Optimization**:  
  Automating data updates via scheduled tasks (e.g., cron jobs) or webhooks ensures the application always has the latest data. Optimizing web hosting by:
  - Reducing memory usage.
  - Improving load times.
  - Enhancing scalability.  
  These optimizations would boost performance and handle more users efficiently.

These improvements would make the project more efficient, scalable, and insightful for users, enhancing both its performance and the quality of the analysis.
