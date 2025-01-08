# Senate Trading Visualization Application

## Project Description

### Senate Trading Visualization Tool Aligned with Your Investment Preferences

This project aims to create a data visualisation tool to analyse U.S. senators' trading patterns using scraped data from [TrendSpider](https://trendspider.com/markets/congress-trading) and stock market performance data from APIs like [Yahoo Finance](https://finance.yahoo.com). The tool will feature interactive charts to explore popular investment sectors, trends, and profit standings among senators. Additionally, a "Senator To Watch Tool" will allow users to find senators with similar investment profiles as theirs. Designed as a Streamlit-based application, this project provides an engaging way to gain insights into U.S. senator trading activities and help answer if some insider trading is involved.

## Project Setup

Follow the steps in **terminal** below to set up the repository and run the project locally:

*The shown commands are for **PowerShell**, use the adequate commands depending on your system*

### 1. Clone the Repository

```sh
mkdir <project-directory>  # Replace `<project-directory>` with the new folder name
cd <project-directory>
git clone <repository-url>  # Replace `<repository-url>` with the repository URL from GitHub
```

### 2. Set Up a Virtual Environment and activate it

```sh
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in the terminal prompt.

*To leave the virtual environment, use the `deactivate` command*

### 3. Install Dependencies

```sh
cd <repository>
pip install -r requirements.txt  # Install dependencies for project
pip install -r requirements_dev.txt  # Install dependencies for testing
```

If you would also like to run the tests for the project, install development dependencies.

```sh
pip install -r requirements_dev.txt  # Install dependencies for testing
```

### 4. Run the project

```sh
streamlit run 🏠_Home.py
```

## How to code and contribute

Please follow the convention below to keep the work organised and maintain readable code.

### Branches

Please create a new branch using the following convention to contribute to the project. For example *I would like to create a new graph for a visualisation app, so I will make a `devel/feature/<name of graph>` branch from the current version `devel` where I will work on it. When I am done, I merge it with `devel` and destroy the branch I created*

#### Description

- **main** - Functional version of the project - *get updates from the devel when there are more than of new things in devel*
- **publish** - Project deployment on web-site - *Auto-deploy branch to Heroku webhosting. Make sure to merge the main without any redundant files*
- **devel** - Prepare to update primary - *purpose to test the new thing and make sure everything is fine*
- **devel/feature/...** - Adding new functionality to the program - *man can be creative here to play*

### Commits

When committing, try to give a useful message to help identify what happened. Merging and committing are not restricted.

A quick guide to git:

```sh
git status  # shows what is in the working space
git add <specific file> or .  # chose to prepare things to commit
git commit -m "<write message here>"  # committing things
git push  # send it to the remote repository (to be visible for other contributors)

git fetch or pull  # update repository
git branches  # show all branches
git checkout <branch name>  # switching between branches
```

Before committing the code, make sure it is well-described and formatted. A helpful thing to keep the exact formatting of code is to use `flake8 <name of file.py>` in the console to see formatting errors.

### Tests

When creating a function, it is good to develop tests to ensure it does not break old ones when adding new things. We will use **pytest**. More info [Testing in Python](https://naucse.python.cz/lessons/intro/testing/)

### Streamlit

The visualization app we will create in **Streamlit** and **Plotly** More info and ispiration [Streamlit](https://streamlit.io/gallery) and [Plotly](https://plotly.com/python/)

### Requirements

When adding a new package, please include it in the requirements and use `pip freeze > requirements.txt`. For testing package use with testing include it in `requirements_dev.txt`
