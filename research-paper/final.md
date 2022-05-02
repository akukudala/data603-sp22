# Amazon S3 & Athena - Interact, Encrypt and Query
![](https://github.com/akukudala/homework_603/blob/main/aws-security-issues.png)
## Introduction

<p>Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability,
data availability, security, and performance. This means customers of all sizes and industries can use it to store and protect
any amount of data for a range of use cases, such as data lakes, websites, cloud-native applications, backups, archive,
 machine learning, and analytics.
Amazon S3 stores data for millions of customers all around the world. Data on Amazon S3 is 
spread across multiple devices and availability zones within a region automatically.
Amazon S3 provides a storage management and administration capability that is highly flexible.
S3 provides various data protection requirements which helps application owners keep their data secure at all times.</p>
But, does everyone know?
<br>
<br>
<p>Although s3 has been across the most vulnerable AWS service due to misconfiguration by the application owners, 
if configured as per security best practices, S3 can be used as a most reliable data lake because it can be easily integrated with data analytic tools (Ex: Athena, quick sight).
In this article, let us explore how our bigdata can be securely maintained in S3. This documentation has sample code which can be considered as a beginner guide to interact with AWS service Amazon S3. This article will also provide details on how to create a bucket, loading data file, to enable encryption and how to use Athena to interact with S3.</p>

# Table of contents

 1. [Interact with AWS Amazon S3](#store1)</br>
 
    1.1 [How does Amazon S3 store data?](#store)</br>
    1.2 [Interacting With AWS Services](#interactaws)</br>
    1.3 [Interacting with S3](#interacts3)</br>
    1.4 [Creating an S3 bucket](#creates3)</br>
 
 2. [Loading data into an S3 Bucket](#bucket1)</br>      
 3. [Encrypting the data](#encrypt1)</br>
 
    3.1 [Enabling Encryption on S3 Bucket & getting confirmation](#encrypt2)</br>
    3.2 [Get Details of Encryption](#encrypt3)</br>
    3.3 [Access control - authorization](#authorization)</br>
 4. [Using Athena to interact with S3 objects](#athena1) </br>
 
    4.1 [Athena Introduction](#athena2)</br>
    4.2 [Create table using the csv data](#athena3)</br>
    4.3 [Query the desired data](#athena4)</br>
 5. [Conclusion](#conclusion)</br>
 6. [Sources](#sources)</br>


## 1. Interact with AWS Amazon S3 <a name="store1"></a>
### 1.1 How does Amazon S3 store data? <a name="store"></a>
The Amazon S3 stores data as objects within buckets. An object consists of a file and optionally any metadata that describes that file. 
To store an object in Amazon S3, the user can upload the file that he/she wants to store in the bucket.
<p>A bucket is a container (web folder) for objects (files) which performs a Persisting function 
(Persisting refers to any time data is written to non-volatile storage, including but not limited to writing the data to back-end storage, 
shared/cloud storage, hard drive, or storage media). Every Amazon S3 object is contained in a bucket. 
Buckets form the top-level namespace for Amazon S3, and bucket names are global. 
This means that bucket names must be unique across all AWS accounts, 
much like Domain Name System (DNS) domain names, not just within your own account.
</p>

### 1.2 Interacting With AWS Services  <a name="interactaws"></a>

* We can interact with AWS services either through console or through AWS CLI. In this scenario, we will interact with S3 using **AWS CLI**. 
* Below figure explains the interaction with Amazon S3 bucket. We are going to create S3 bucket from AWS CLI and query using Athena.
<p align="center">
  <img src="https://github.com/akukudala/homework_603/blob/main/S2Cli.png" width="700" />
</p>


### 1.3 Interacting with S3 <a name="interacts3"></a>

* Before even we interact with S3 using CLI, we would require IAM user credentials.
* In AWS management console, click on IAM and create a new user
* Add a new user with programmatic access and attach the permission policies you need for s3 and Athena
* The policy you'll need is Amazon Athena full access or a custom policy with full
access to Athena and lists read/write permissions to the source S3 bucket.
* More information can be found in the below link:
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console

### 1.4 Creating an S3 bucket : <a name="creates3"></a>

* Once we have configured the CLI with AWS credentials, we will now create an S3 bucket. 
* Command - **aws s3api create-bucket —bucket bucket name**
* Here, we are creating aks_s3 bucket. While choosing the region, we can select the Region closest to where our clients will be accessing or is located.

```
 Data_lake % aws s3api create-bucket --bucket aks_s3 --region us-east-1
{
    "Location": "/aks_s3"
}
```
* Command: **aws s3 ls** can be used to list out all the buckets in our AWS account.

```
aws s3 ls                                                                       
2022-03-31 12:29:02 aks_s3
2022-03-31 12:28:19 akshitha-test
```
## 2. Loading data into an S3 Bucket  <a name="bucket1"></a>
* In this scenario, we are uploading a csv file which is taken from 
[kaggle](https://www.kaggle.com/datasets/hishaamarmghan/list-of-top-data-breaches-2004-2021).
* Command: **aws S3 cp** can be used to upload files into specific s3 buckets , in the below code we are uploading files into aks_s3 bucket which we created in the previous step.
```
aws s3 cp DataBreaches\(2004-2021\).csv s3://aks_s3
upload: ./DataBreaches(2004-2021).csv to s3://aks_s3/DataBreaches(2004-2021).csv
```
* We uploaded a CSV file in this example, take note of the column names and data types in the table.
* Set the permissions and properties you need.
* Before heading to AWS Athena from AWS management console, we shall enable the encryption.
* All the objects in S3 can be listed using **aws s3 ls bucket-name** command.

```
aws s3 ls s3://aks_s3                           
2022-03-31 12:36:54      16665 DataBreaches(2004-2021).csv
```
## 3. Encrypt the data <a name="encrypt1"></a>
Encrypt data at rest to mitigate potential issues with data leakage. This helps reduce risk by encrypting the information rendering it unreadable to the attacker without a key. The key should be stored in a different location than the data itself.

### 3.1 Enabling Encryption on S3 Bucket & getting confirmation <a name="encrypt2"></a>

* Data security is most important aspect when it comes to handling critical data [PII etc].
* Command: **aws s3api put-bucket-encryption —bucket bucket-name** is used to enable default encryption on S3 bucket. 

```
aws s3api put-bucket-encryption --bucket aks_s3 --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
```


### 3.2 Get Details of Encryption <a name="encrypt3"></a>
* Command: **aws s3api get-bucket-encryption —bucket bucket-name**
```
aws s3api get-bucket-encryption --bucket aks_s3
{
    "ServerSideEncryptionConfiguration": {
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                },
                "BucketKeyEnabled": false
            }
        ]
    }
}
```
### 3.3 Access control - authorization <a name="authorization"></a>
When authorization is not implemented correctly and completely, a malicious user can perform actions such as read, write, modify data, access a host or call a service API for which they do not have permissions.
If successful, this activity can expose customer data or impact service availability; resulting in a loss of customer trust.

Authorization refers to the function of specifying access rights/privileges to resources, such as data or APIs. Authorization is a component of access control, to be performed after authentication.
Authorization should be sufficiently granular to achieve the principle of least required privileges. Periodic base-lining of authorization groups, or IAM policies must be performed regularly to ensure least privilege remains in effect, group members still require access to the service and policies are current.

S3 Provides wide range of capabilities to restrict Access : 

* Access to S3 can be controlled using [bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-iam-policies.html) and [ACLs](https://docs.aws.amazon.com/AmazonS3/latest/dev/S3_ACLs_UsingACLs.html).
* Data owners can implement [role-based access control](https://en.wikipedia.org/wiki/Role-based_access_control) to enforce separation of duties. Create multiple roles for multiple functions. For example, you may define separate roles with read-only access, write-only access, etc.
* If we want another AWS account to access S3 buckets it can done using cross-account access, use [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html) to delegate access to another account .
## 4. Using Athena to interact with S3 objects<a name="athena1"></a>
Athena is serverless interative query system. so there is no infrastructure to manage, and you pay only for the queries that you run. It also supports variety of formats like csv, json, Avro, ORC (columnar) and Parquet (columnar) which are recommenble in Bigdata storage. 
Amazon Athena is a service that makes it easy to create and analyze data in Amazon S3 using open standards. </br>
Athena is easy to use. Simply point to your data in Amazon S3 and start querying using SQL. Most results are delivered within seconds. With Athena, there’s no need for complex ETL jobs to prepare your data for analysis. This makes it easy for anyone with SQL skills to quickly analyze large-scale datasets. 
### 4.1 Why Athena got Popular? <a name="athena2"></a>
* Athena is used by Data Analysts to query large S3 data sets
* Only pay for querying the data. It is $5 per TB data scanned. No charge for DDL and failed Queries.
* One of the best ways to save the cost, we can create Columnar formats (Parquet and ORC) and by using Partitions.
* Quickly queries Unstructured, Semi Structured and Structured Data. Uses Presto (It is a distributed SQL query engine for BigData).


### 4.2 Create table using the csv data<a name="athena3"></a>
* Create a new database (if you have not set up one)
* Give your table a name and add your path inside the S3 bucket and folder
* Indicate data format as CSV and add the column names and data types using bulk-add option for your table.
* Go to athena service through AWS management console & click on explore query editor to the right.
* As shown in the below image click on create table from S3 bucket data source.
<p align="center">
  <img src="https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%203.26.15%20PM.png" width="450" />
</p>

* Select the input location of dataset,  this would be the **s3 location/bucket-name**. Athena provide a browse s3 functionality which simplifies locating the s3 bucket. 
* Once all the required fields are filled out click on create table.

### 4.3 Query the desired data <a name="athena4"></a>
* Once tables are created successfully we can query the desired data, below are few examples :
* In the below example, I am querying the counting the number of records per year using the **group by** statement along with **having** statement to apply a condition.
 ``` sql
select sum(records) Total_Records, year from datalakev1 group by year having year>2015 order by year asc;
``` 

![](https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%206.13.27%20PM.png)

* In the below example, I am querying the most used method for hacking. The data can be retrieved using the **group by** statement on method column. 
``` sql
select count(method) count, method from datalakev1 group by method order by 1 desc;
```
![](https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%206.15.56%20PM.png)

## 5. Conclusion <a name="conclusion"></a>
Amazon S3 encrypts your data at the object level as it writes it to disks in its data centers and decrypts it for you when you access it.
As long as you authenticate your request and you have access permissions, there is no difference in the way you access encrypted or unencrypted objects.
Amazon Athena allows you to analyze data in S3 using standard SQL, without the need to manage any infrastructure. You can also access Athena via a business intelligence tool, by using the JDBC driver. Athena charges you on the amount of data scanned per query. As was evident from this article, converting your data into open source formats not only allows you to save costs, but also improves performance.
Any SQL developer can start working on S3 bucket data through Athena. 
We  can use the Amazon [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html) feature to reduce cost/scaling issues.
Consider the below example for to compare performance with the data processed: CSV, GZip, and Parquet files.
|Raw CSV	|GZip CSV |Compressed Parquet |
|--------|---------|-------------------|
|No compression, just a plain set of CSV files|Simple CSV files compressed using GZip to compress them.|We converted to the CSV file to parquet using Spark. The same process could also be done with (AWS Glue)|
|12 ~55MB files (one for each month)|12 ~10MB Gzipped CSV files (one for each month)|12 ~8MB Parquet file using the default compression (Snappy)|
|Total dataset size: ~666MBs|Total dataset size: ~126MBs|Total dataset size: ~84MBs ||

Thanks to Apache Parquet’s columnar format, AWS Athena is reads only the columns that are needed from the query. This reduces the query time by more than 50+% and reduces the query price by 98%.

## 6. Sources <a name="sources"></a>

* Amazon S3: https://aws.amazon.com/pm/serv-s3/?trk=fecf68c9-3874-4ae2-a7ed-72b6d19c8034&sc_channel=ps&sc_campaign=acquisition&sc_medium=ACQ-P|PS-GO|Brand|Desktop|SU|Storage|S3|US|EN|Text&s_kwcid=AL!4422!3!488982706722!e!!g!!s3&ef_id=CjwKCAjwopWSBhB6EiwAjxmqDVZhQqzk-utK6i34xptNzA7MVWoo_nRYSj5jfzxiuxaCc1qt1MLokBoCMnsQAvD_BwE:G:s&s_kwcid=AL!4422!3!488982706722!e!!g!!s3
* Athena: https://aws.amazon.com/athena/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc
* Creating IAM User/Roles: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console
* AWS CLI: https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html
* Athena basics tutorial: https://www.youtube.com/watch?v=8VOf1PUFE0I
* Image https://www.scnsoft.com/blog/aws-security-issues
