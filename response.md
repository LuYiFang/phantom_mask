# Response
## A. Required Information
### A.1. Requirement Completion Rate
- [x] List all pharmacies open at a specific time and on a day of the week if requested.
  - Implemented at /pharmacies API.
- [x] List all masks sold by a given pharmacy, sorted by mask name or price.
  - Implemented at /pharmacies/{pharmacy_id}/masks API.
- [x] List all pharmacies with more or less than x mask products within a price range.
  - Implemented at /pharmacies_by_count_and_range API.
- [x] The top x users by total transaction amount of masks within a date range.
  - Implemented at /top_user_amount API.
- [x] The total number of masks and dollar value of transactions within a date range.
  - Implemented at /transactions/summary API.
- [x] Search for pharmacies or masks by name, ranked by relevance to the search term.
  - Implemented at /search API.
- [x] Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.
  - Implemented at /purchase API.
### A.2. API Document
#### Method 1: View Deployed Swagger UI 
1. Open [swagger](redoc-static.html) in your browser to view the API documentation.

#### Method 2: Run Swagger UI Locally 
1. Navigate to the `/api` directory in your terminal.
2. Run the FastAPI application locally to view the documentation: 
   Start your FastAPI application: 

```
uvicorn main:app --host "0.0.0.0" --reload 
```

3. Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the API documentation.

### A.3. Import Data Commands
Please run these two script commands to migrate the data into the database.

```bash
python ETL.py
```
## B. Bonus Information

### B.1. Test Coverage Report

I wrote down the 20 unit tests for the APIs I built. Please check the test coverage report at [here](htmlcov/index.html). You can open this in your browser to view the detailed results.

You can run the test script by using the command below:

```bash
pytest ./api/test_main.py
```

Generate Coverage report

```bash
pytest --cov=api --cov-report=html
```



### B.2. Dockerized
Please check my Dockerfile at [here](Dockerfile) / docker-compose.yml at at [here](docker-compose.yml). 

On the local machine, please follow the commands below to build it.

```bash
$ docker-compose build
$ docker-compose up -d

$ docker exec -it phantom-mask-api bash
$ python ETL.py
```

## C. Other Information

### C.1. ERD

My ERD [erd-link](#erd-link).

### C.2. Technical Document

For frontend programmer reading, please check this [technical document](redoc-static.html) to know how to operate those APIs. You can open this in your browser to view the detailed results.

- --
