# AWS CLOUD DATA WAREHOUSE
This project is a continuation of a previous work on [data modeling of a company's songs and logs data in postgreSQL database](https://gitlab.com/offor20/data_modeling_with_postgreSQL). The company has made tremendous growth and decided to migrate their data and operations to the cloud. They have uploaded their data in two Amazon S3 storage directories holding their JSON logs on user activity and JSON metadata of songs in their music app. The exact locations of the data are:
* [Song data](s3://udacity-dend/song_data)
* [Log data](s3://udacity-dend/log_data)
    * [Log data json path](s3://udacity-dend/log_json_path.json)

This project aims at building an Extraction, Transformation and Loading (ETL) data pipeline of the company's data by doing the following:
* Extracting the data from the S3 storage
* Staging the data in an Amazon Redshift (cloud)
* Processing the data by creating a star schema consisting of a fact table and a set of four dimensional tables in the Redshift.
* Running some queries and comparing the results with the expectations of the company's analytics team.

<p>
The simplified architecture of the the project is as shown in the diagram below. The green arrows depict operations performed in this project. Data is copied from S3 into two staging tables in Amazon Redshift. Each of the staging tables represents each of the two different data sources/directories in S3. Then,  extraction, transformation and loading are performed on te staged data to produce a star schema comprising one fact table called songplays and four dimensional tables, namely: songs, artists, users and time tables. The tables' fields and their data types are given in the sql_queries.py file.

![DWH Architecture](/images/dwh_achitect.png)
</p>

## Getting Started
Find below the requirements cum preconditions for successfully running and testing of the project files. 
### Prerequisites
In order to have full insights into the project's implementations and have it up and running, the following software packages and accounts are necessary:
*   Python 3
* Amazon account with I AM Role and User Credentials
* An Available Amazon Redshift Cluster preferably located in US-West-2 region.

### Installations:
Python can be installed by following the instructions in the links below:
* [Python 3 on MacOS.](https://docs.python-guide.org/starting/install3/osx/#install3-osx)
*  [Python 3 on Linux.](https://docs.python-guide.org/starting/install3/linux/#install3-linux)
* [Python 3 on Windows.](https://docs.python-guide.org/starting/install3/win/#install3-windows)
### Sign up or Login to AWS Account
* [Create or sign in to an AWS account (My Account) here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
* Once you are signed in to AWS navigate to [I AM Dashboard](https://console.aws.amazon.com/iam/), select **Roles** followed by **Create role**. Choose Redshift as a type of trusted entity under **AWS service**. Attach AmazonS3ReadOnlyAccess policy to the I am Role. 
* [Create I AM User here](https://console.aws.amazon.com/iam/) by choosing **Users**. Under access type use: **Programmatic access**.
* [Launch an AWS Redshift Cluster](https://console.aws.amazon.com/redshift/) by filling out the necessary configuration details such as the following:
    * Redshift Identifier
    * Type and number of nodes
    * Select free trial for learning and development
    * Database necessary details are:
        * Database Name
        * Database Port which is 5439
        * Master user name
        * Master user password
    * Cluster Permissions: Under the IAM Roles select the IAM Role you created earlier and associate it with the cluster.

***It is advisable to delete a cluster after use to avoid exorbitant bills*** 

## Implementation Steps
* First and foremost, there are three key files for this project, namely:
    * sql_queries.py
    * create_tables.py
    * etl.py
* In the sql_queries.py file, **SQL  DROP TABLE** statements were defined for all the tables, followed by the **SQL CREATE TABLE** statements for all the tables with the table fields and their associated data types.
* COPY statements to copy the datasets from AWS S3 to staging tables in Redshift are defined in the sql_queries.py file. Also defined in the file are the **SQL INSERT** commands that would populate the individual fact and dimension tables using data from the staging tables. 
* The create_tables.py defines two functions that drop the tables if they exist and create all the tables anew respectively.
* In the etl.py file, the actual ETL data pipelines are implemented. Firstly, two functions, namely: load_staging_tables and insert_tables that respectively copy the original datasets from Amazon S3 to the staging tables in Redshift and populate the fact and dimensional tables. Secondly, the etl.py file defines a main function where the actual execution of all the previously defined functions in this file takes place. 

## Running the Code
The codes are to be ran in the following order:
``` python3 sql_queries.py
    python3 create_tables.py
    python3 etl.py 
```
## Authors
Ernest Offor Ugwoke - previous work [data modeling in postgreSQL](https://gitlab.com/offor20/data_modeling_with_postgreSQL)

## Acknowledgement
The author is grateful to the [Udacity data engineering team](www.udacity.com) for their guidance, supervision and supports.
