# AWS CLOUD DATA WAREHOUSE
This project continues a previous work on [data modeling of a company's songs and logs data in postgreSQL database](https://gitlab.com/offor20/data_modeling_with_postgreSQL). The company has made tremendous growth and decided to migrate their data and operations to the cloud. They have uploaded their data in two Amazon S3 storage directories holding their JSON logs on user activity and JSON metadata of songs in their music app. This project aims at building an Extraction, Transformation and Loading (ETL) pipeline of the company's data by doing the following:
* Extracting the data from the S3 storage
* Staging the data in an Amazon Redshift (cloud)
* Processing the data by creating a star schema consisting of a fact table and a set of dimensional tables in the Redshift.
* Running some queries and comparing the results with the expectations of the company's analytics team.
