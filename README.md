# Project Setup

Follow these steps to set up the repository and run the project locally:

## 1. Clone the Repository

```sh
mkdir project-directory
cd project-directory
git clone <repository-url>  # Replace `<repository-url>` with the repository URL
```

## 2. Set Up a Virtual Environment

```sh
python -m venv .venv
```

### Activate the Virtual Environment

```sh
.venv\Scripts\activate
```

### Confirm the Virtual Environment is Active

You should see `(.venv)` in the terminal prompt. To deactivate, use:

```sh
deactivate
```

## 3. Install Dependencies

```sh
cd <repository>
pip install -r requirements.txt  # Install dependencies from requirements.txt
```

## Before Commit

Make sure to run:

```sh
pylint file.py
```

## Branches

- **main** - Functional version
- **devel** - Prepare to update main
- **devel/feature/...** - Adding new functionality
- **devel/fix/...** - Fixing issues

Merge and push freely.
