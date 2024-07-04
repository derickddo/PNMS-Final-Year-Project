# Population Projection, Needs Assessment, and Map Prediction System (PNMS)

## Overview

PNMS is a comprehensive platform designed to aid development planners in Ghana with accurate population projections, needs assessment preparation, and facility prediction. By leveraging extensive demographic data and advanced predictive models, the platform aims to enhance strategic planning in key sectors such as health, education, and utilities.

## Features

- **Population Projection**: Calculate and project population growth for regions and districts using various methods.
- **Needs Assessment**: Evaluate resource requirements based on projected population data.
- **Map Prediction**: Visualize and predict facility needs on an interactive map.
- **User Authentication**: Seamless sign-up and login using third-party apps like Google.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Django Allauth
- Pandas
- GeoPy

<!-- ### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/derickddo/PNMS-Final-Year-Project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd final_year_project
    ```
3. Install the required dependencies:
    ```bash
    pip install pipenv
    ```
    ```bash
    pipenv shell
    ```
    ```bash
    pipenv install -r requirements.txt
    ```


4. Set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://localhost:8000`. -->

## Usage

1. **Population Projection**: Navigate to the Population Projection page, select the area (region/district), base year, and projected year to calculate the population.
2. **Needs Assessment**: Go to the Needs Assessment page, select the projected population data, and view the resource requirements by sector (Health, Education, Utilities).
3. **Map Prediction**: Use the interactive map to visualize facility needs and plan resource allocation effectively.
4. **User Authentication**: Sign up or log in using Google for a personalized experience.

## Project Structure

- `project_root/`
  - `core/`: Main project directory.
  - `data/`: Json and CSV population data
  - `pnms/`: Django app containing models, views, and templates.
  - `scripts/`: Scripts for mapping population data to database
  - `static/`: Static files (CSS, JavaScript, images).
  - `templates/`: HTML templates.
  - `theme/`: Tailwind configuration
  - `requirements.txt`: List of dependencies.



**Disclaimer**: This project is a part of the final year project requirements for the degree in Computer Science at KNUST.

