# Senate Trading Visualization Application

## Project Description

### Senate Trading Visualization Tool Aligned with Your Investment Preferences

This project aims to create a data visualization tool to analyze U.S. senators' trading patterns using scraped data from [TrendSpider](https://trendspider.com/markets/congress-trading/) and stock market performance data from APIs like [Alpha Vantage](https://www.alphavantage.co/). The tool will feature interactive charts to explore popular investment sectors, trends, and profit standings among senators. Additionally, a "Senator Matching Tool" will allow users to find senators with similar investment profiles. Designed as a Streamlit-based application, this project provides an engaging way to gain insights into U.S. senator trading activities and optimize personal investment strategies.

## Project Setup

Follow the steps in **terminal** below to set up the repository and run the project locally:

*The shown commands are for **powershell** but use the adacvate commands depending on your system*

### 1. Clone the Repository

```sh
mkdir <project-directory>  # Replace `<project-directory>` with the new folder name
cd <project-directory>
git clone <repository-url>  # Replace `<repository-url>` with the repository URL from github
```

### 2. Set Up a Virtual Environment and actiavte it

```sh
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in the terminal prompt.

*To leave the virtual enviroment use `deactivate` command*

### 3. Install Dependencies

```sh
cd <repository>
pip install -r requirements.txt  # Install dependencies from requirements.txt
```

### 4. create enviroment variables

```sh
copy .env.example .env
```

**Add the needed tokens for project as string to prepared variables**

### 5. Run the application TODO

```sh
python main.py  # Or your python runner
```

## How to code and contribute

To keep the work organize and maintain readable code pelase follow the convention below. Use **classses** when possible.(It is not compulsory)

### Branches

To start your contribution to the project please create a new branch with the following convention. For example *I would like to create a new graph to visualization app, so I will create `devel/feature/<name of graph>` branch from current version `devel` where I will work on it. When I am done I merge it with `devel` and destroy the branch I created*

#### Description

- **main** - Functional version of project - *get updates from the devel when there is more then then couple new things in devel*
- **devel** - Prepare to update main - *purpose to test the new thing and making sure every thing is fine*
- **devel/feature/...** - Adding new functionality to the program - *man can be creative here to play*

### Commits

When commiting try to give some usefull message to commit to better identification what heappend. The merging and committing is not restricted.

Quick guide to git:

```sh
git status  # show what is in working space
git add <specific file> or .  # chose prepare things to commit
git commit -m "<write meassege here>"  # committing things
git push  # send it to the remote repository (to be visible for others contributors)

git fetch or pull  # update repository
git branches  # show all branches
git checkout <branch name>  # switching between braches
```

Before commiting the code make sure is well describet and format. Usefull thing to keep same formatting of code is to use `pylint <name of file.py>` in console to see formatting errors.

### Tests

When creating function is good to create tests for it to make sure when adding new things it not break old ones. We will use **pytest**. More info [Testing in Python](https://naucse.python.cz/lessons/intro/testing/)

### Streamlit

The visualization app we will create in **Streamlit** and **Plotly** More info and ispiration [Streamlit](https://streamlit.io/gallery) and [Plotly](https://plotly.com/python/)

### Requirements

When adding new package, please include it also in requiremets or use `pip freeze > requirements.txt`.

### Might be helpfull

environ, unitmock,
