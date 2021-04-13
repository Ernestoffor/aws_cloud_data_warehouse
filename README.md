# AWS CLOUD DATA WAREHOUSE
This project continues a previous work on [data modeling of a company's songs and logs data in postgreSQL database](https://gitlab.com/offor20/data_modeling_with_postgreSQL). The company has made tremendous growth and decided to migrate their data and operations to the cloud. They have uploaded their data in two Amazon S3 storage directories holding their JSON logs on user activity and JSON metadata of songs in their music app. The exact locations of the data are:
* Song data: s3://udacity-dend/song_data
* Log data: s3://udacity-dend/log_data
    *Log data json path: s3://udacity-dend/log_json_path.json

This project aims at building an Extraction, Transformation and Loading (ETL) pipeline of the company's data by doing the following:
* Extracting the data from the S3 storage
* Staging the data in an Amazon Redshift (cloud)
* Processing the data by creating a star schema consisting of a fact table and a set of dimensional tables in the Redshift.
* Running some queries and comparing the results with the expectations of the company's analytics team.

<p>
The simplified architecture of the the project is as shown in the diagram below. The green arrows depict operations performed in this project. Data is copied from S3 into two staging tables in Amazon Redshift. Each of the staging tables represents each of the two different data sources/directories in S3. Then,  extraction, transformation and loading are performed on te staged data to produce a star schema comprising one fact table called songplays and four dimensional tables, namely: songs, artists, users and time tables. The tables' fields and their data types are given in the sql_queries.py file.
![DWH Architecture](/images/dwh_achitect.png)
</p>
## Getting Started
Find below the requirements cum preconditions for successfully running and testing of the project. 
### Prerequisites
In order to have full insights into the project's implementations and have it up and running, the following software packages and accounts are necessary:
* Python 3
* Amazon account with I AM Role and User Credentials
* An Available Amazon Redshift Cluster preferably located in US-West-2 region.

### Installations:
Python can be installed by following the instructions in the links below:
    * [Python 3 on MacOS.](https://docs.python-guide.org/starting/install3/osx/#install3-osx)
    * [Python 3 on Linux.](https://docs.python-guide.org/starting/install3/linux/#install3-linux)
    * [Python 3 on Windows.](https://docs.python-guide.org/starting/install3/win/#install3-windows)
### Sign up or Login to AWS Account
* [Create or sign in to an AWS account (My Account) here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
* Once you are signed in to AWS navigate to [I AM Dashboard](https://console.aws.amazon.com/iam/), select **Roles** followed by **Create role**. Choose Redshift as a type of trusted entity under **AWS service**. Attach AmazonS3ReadOnlyAccess policy to the I am Role. 
* [Create I AM User here](https://console.aws.amazon.com/iam/) by choosing **Users**. Under access type use: **Programmatic access**.

