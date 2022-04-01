## Amazon S3 

<p>Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability,
data availability, security, and performance. This means customers of all sizes and industries can use it to store and protect
any amount of data for a range of use cases, such as data lakes, websites, cloud-native applications, backups, archive, machine learning, and analytics.
Amazon S3 stores data for millions of customers all around the world.</p>
<p>A bucket is a container (web folder) for objects (files) which performs a Persisting function 
(Persisting refers to any time data is written to non-volatile storage, including but not limited to writing the data to back-end storage, 
shared/cloud storage, hard drive, or storage media). Every Amazon S3 object is contained in a bucket. Buckets form the top-level namespace for Amazon S3, and bucket names are global. This means that bucket names must be unique across all AWS accounts, much like Domain Name System (DNS) domain names, not just within your own account.
</p>
Although s3 has been across the most vulnerable AWS service due to misconfiguration by the application owners, 
if configured as per security best practices, S3 can be used as a most reliable data lake because 
it can be easily integrated with data analytic tools (Ex: Athena, quick sight). In this session, let us try to understand the below.

* How to interact with AWS services & Amazon S3?
* How to enable encryption?
* How to use Athena to interact with S3?

### Interacting With AWS Services  

* Interacting with AWS services can be done in multiple ways either through console or through AWS CLI, In this scenario we will interact with S3 using AWS CLI & Athena using Management console. 



#### 

![](https://github.com/akukudala/homework_603/blob/main/S2Cli.png)


### Interacting with S3

* Before even we interact with S3 using CLI we would require IAM user credentials , to create IAM credentials we will use management console access , How to create IAM user credentials can be found here : https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console
* Once we have configure the CLI with AWS credentials below commands can be used to interact with S3

#### Creating an S3 bucket : 

* S3 bucket can be created using aws s3api create-bucket —bucket bucket name command, here we are creating akshitha-datalake-assignment bucket.

```
 Data_lake % aws s3api create-bucket --bucket akshitha-datalake-assignment --region us-east-1
{
    "Location": "/akshitha-datalake-assignment"
}
```

####  Listing all the buckets in you AWS Accounts

* aws s3 ls command can be used to list out all the buckets in our AWS account.

```
aws s3 ls                                                                       
2022-03-31 12:29:02 akshitha-datalake-assignment
2022-03-31 12:28:19 akshitha-test
```

#### Uploading CSV File into S3 Bucket

* AWS S3 cp command can be used to upload files into specific s3 buckets , in the below command we are uploading files into akshitha-datalake-assignment s3 bucket.

```
aws s3 cp DataBreaches\(2004-2021\).csv s3://akshitha-datalake-assignment
upload: ./DataBreaches(2004-2021).csv to s3://akshitha-datalake-assignment/DataBreaches(2004-2021).csv
```

#### Listing Objects in S3 Bucket

* All the objects in S3 can be listed using aws s3 ls bucket-name command , here we are listing out all the objects in the akshitha-datalake-assignment  s3 bucket.

```
aws s3 ls s3://akshitha-datalake-assignment                              
2022-03-31 12:36:54      16665 DataBreaches(2004-2021).csv
```

#### Enabling Encryption on S3 Bucket & getting confirmation

* Data security is most important aspect when it comes to handling critical data [PII etc] , aws s3api put-bucket-encryption —bucket bucket-name command is used to enable default encryption on S3 bucket. 

```
aws s3api put-bucket-encryption --bucket akshitha-datalake-assignment --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
```


#### Get Details of Encryption

```
aws s3api get-bucket-encryption --bucket akshitha-datalake-assignment 
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

## 

## Athena 

Amazon Athena is a service that makes it easy to create analyze data in Amazon S3 using open standards. Athena is serverless, so there is no infrastructure to manage, and you pay only for the queries that you run. Athena is easy to use. Simply point to your data in Amazon S3 and start querying using standard SQL. Most results are delivered within seconds. With Athena, there’s no need for complex ETL jobs to prepare your data for analysis. This makes it easy for anyone with SQL skills to quickly analyze large-scale datasets. 

### Using Athena to interact with S3 objects

* Go to athena service through AWS management console & click on explore query editor to the right.
* As shown in the below image click on create table from S3 bucket data source

![](https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%203.26.15%20PM.png)


* Select the input location of dataset,  this would be the s3 location/bucket-name as shown in the below image. Athena provide a browse s3 functionality which simplifies locating the s3 bucket. 
* Once all the required fields are filled out click on create table.

![](https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%203.57.32%20PM.png)

* Once tables are created successfully we can query the desired data, below are few examples :

![](https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%206.13.27%20PM.png)
![](https://github.com/akukudala/homework_603/blob/main/Screen%20Shot%202022-03-31%20at%206.15.56%20PM.png)

## Sources

* Amazon S3 :https://aws.amazon.com/pm/serv-s3/?trk=fecf68c9-3874-4ae2-a7ed-72b6d19c8034&sc_channel=ps&sc_campaign=acquisition&sc_medium=ACQ-P|PS-GO|Brand|Desktop|SU|Storage|S3|US|EN|Text&s_kwcid=AL!4422!3!488982706722!e!!g!!s3&ef_id=CjwKCAjwopWSBhB6EiwAjxmqDVZhQqzk-utK6i34xptNzA7MVWoo_nRYSj5jfzxiuxaCc1qt1MLokBoCMnsQAvD_BwE:G:s&s_kwcid=AL!4422!3!488982706722!e!!g!!s3
* Athena : https://aws.amazon.com/athena/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc
* Creating IAM User/Roles : https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console
* AWS CLI : https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html
* We  can use the Amazon [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html) feature to reduce cost/scaling issues

