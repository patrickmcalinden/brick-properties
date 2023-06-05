# Real Estate Data Integration and Visualization

## Project Summary

The Real Estate Data Integration and Visualization project aims to retrieve the latest property listing data from Realty Mole Property's API, transform it into a DataFrame, and upload it to a BigQuery database. The uploaded data is then visualized on a Grafana dashboard. The project is automated to run on a weekly basis, ensuring that the data is always up to date.

## How It Works

### Retrieving Data

The project uses the `fetch_and_upload_data()` function to make an API call to Realty Mole Property's API. The function specifies the city and state for which property listings are requested. The API response, in JSON format, is retrieved and stored.

### DataFrame Transformation

The retrieved JSON data is transformed into a pandas DataFrame using the `make_df_and_upload()` function. The function converts specific columns to datetime format and prepares the data for uploading to BigQuery.

### Uploading to BigQuery

The transformed DataFrame is uploaded to a BigQuery database using the Google Cloud Python SDK. The function creates a BigQuery table if it doesn't already exist and defines the schema for the data. The DataFrame is then loaded into the table.

### Automated Execution

The project is scheduled to run on a weekly basis using a scheduler or a job orchestration tool. Each execution triggers the `hello_pubsub()` function, which starts the data retrieval and upload process.

### Visualization with Grafana

Once the data is stored in BigQuery, it can be accessed by Grafana for visualization. Grafana can be configured to connect to the BigQuery database and create visualizations and dashboards based on the property listing data.

By following this process, the project ensures that the latest property listing data is regularly retrieved, transformed, uploaded to BigQuery, and made available for visualization on a Grafana dashboard.

### Future

## Changes

Developing a more robust solution to handle duplicated data and add historical prices to a separate table, ensuring that a property is accurately marked as sold and that further calculations such as 'Days to Sell' and 'Selling Price' are added to a history table.
