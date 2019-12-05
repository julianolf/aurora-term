aurora-term
===========

Amazon Aurora Serverless interactive terminal.

Introduction
------------

The **aurora-term** app allows you to run SQL statements against `Aurora Serverless`_ databases without establishing a persistent connection, this is easily achieved thanks to the `Data-API`_.

Besides the non-persistent connection it works just as any other interactive terminal like `mysql-cli`_ and `psql`_.

Requirements
------------

- Python 3 and Pip.
- An AWS IAM user `authorized`_ to access the Data API (with the *AmazonRDSDataFullAccess* policy for example).
- Access key and secret access key properly configured for the same user (it can be done using the `aws-cli`_).

Installation
------------

The easiest and recommended way to install it is using Pip. ::

  pip install aurora-term

Usage
-----

Just specify the database cluster ARN, the secret manager ARN and the database name. ::

  aurora-term --cluster="arn:aws:rds:..." --secret="arn:aws:secretsmanager:..." mydb

**TIP:**

There are a few environment variables that might come in handy, you can set them to avoid the need to pass all the credentials when starting **aurora-term**.

- **AWS_PROFILE** Profile to be used.
- **RDS_CLUSTER_ARN** Aurora cluster ARN.
- **RDS_SECRET_ARN** Secret manager ARN.
- **RDS_DB_NAME** Database name.

e.g. ::

  export RDS_CLUSTER_ARN="arn:aws:rds:..."
  export RDS_SECRET_ARN="arn:aws:secretsmanager:..."

  aurora-term mydb

The interactive terminal looks like as follow. ::

  aurora-term (0.1.0)
  Type "help" or "?" for help.

  mydb=#

For more usage details. ::

  aurora-term -h


.. _Aurora Serverless: https://aws.amazon.com/rds/aurora/
.. _Data-API: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html
.. _mysql-cli: https://dev.mysql.com/doc/refman/5.5/en/mysql.html
.. _psql: https://www.postgresql.org/docs/current/app-psql.html
.. _authorized: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
.. _aws-cli: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html
