import os
from datetime import datetime
import time
import logging
import json
import boto3
from botocore.exceptions import ClientError


#########################################################################
#
# Class S3Client:
#
# This class manages connections to an Amazon S3 server
#
#########################################################################


class S3Client:
    _accessKeyId = ""
    _secretKey = ""
    _client = None

    def __init__(self, accessKeyId, secretKey):
        self._accessKeyId = accessKeyId
        self._secretKey = secretKey

        logger = logging.getLogger("botocore")
        logger.setLevel(logging.ERROR)

        self._client = boto3.client(
            "s3",
            aws_access_key_id=self._accessKeyId,
            aws_secret_access_key=self._secretKey,
        )

    def fileExists(self, bucketName, s3Dir, fileName):
        fileNames = self.getFilenames(bucketName, s3Dir, fileName)

        if len(fileNames) > 0:
            return True

        return False

    def deleteFiles(self, bucketName, s3Dir, filePrefix):
        fileNames = self.getFilenames(bucketName, s3Dir, filePrefix)

        for fileName in fileNames:
            self._client.delete_object(Bucket=bucketName, Key=fileName)

    def uploadFile(self, sourceFile, bucketName, s3Dir, s3BaseFilename):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=self._accessKeyId,
            aws_secret_access_key=self._secretKey,
        )

        key = s3Dir

        if s3Dir.endswith("/") is False:
            key = key + "/"

        key = key + s3BaseFilename

        s3_client.upload_file(sourceFile, bucketName, key)

    def copy_file_to_bucket(self, sourceBucket, sourceKey, destBucket, destKey):
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=self._accessKeyId,
            aws_secret_access_key=self._secretKey,
        )

        copy_source = {"Bucket": sourceBucket, "Key": sourceKey}
        bucket = s3.Bucket(destBucket)
        bucket.copy(copy_source, destKey)

    def getFilenames(self, bucketName, dir, prefix, extension=None):
        filePrefix = dir

        if filePrefix.endswith("/") is False:
            filePrefix = filePrefix + "/"

        filePrefix = filePrefix + prefix

        print(f"Checking s3://{bucketName}/{filePrefix} for files....")

        objs = self._client.list_objects_v2(Bucket=bucketName, Prefix=filePrefix)

        fileKeys = []

        if "Contents" not in objs.keys():
            return fileKeys

        for obj in objs["Contents"]:
            if obj["Key"][-1:] != "/":
                if extension is not None and obj["Key"].endswith(extension) is False:
                    continue
                fileKeys.append({"filename": obj["Key"], "moddate": obj["LastModified"]})

        return fileKeys

    def readFile(self, s3Bucket, key, format="text"):
        obj = self._client.get_object(Bucket=s3Bucket, Key=key)
        file_content = obj["Body"].read().decode("utf-8")
        if format == "json":
            contents = json.loads(file_content)
        else:
            contents = file_content
        return contents

    def getDirectories(self, bucketName, dir, prefix):
        filePrefix = dir

        if filePrefix.endswith("/") is False:
            filePrefix = filePrefix + "/"

        filePrefix = filePrefix + prefix

        objs = self._client.list_objects_v2(Bucket=bucketName, Prefix=filePrefix)

        fileKeys = []

        if "Contents" not in objs.keys():
            return fileKeys

        for obj in objs["Contents"]:
            if obj["Key"][-1:] == "/":
                continue

            fileKeys.append(obj["Key"])

        return fileKeys

    def download(self, bucketName, fileKey, outputDir, extension=""):
        outputFilename = outputDir
        if outputFilename.endswith(os.path.sep) is False:
            outputFilename = outputFilename + os.path.sep
        fileParts = fileKey.split("/")
        outputFilename = outputFilename + fileParts[len(fileParts) - 1]
        if extension != "" and not outputFilename.endswith(extension):
            outputFilename += extension

        self._client.download_file(bucketName, fileKey, outputFilename)

        return outputFilename

    def move(self, sourceBucketName, sourceFullFileKey, destFullFileKey):
        copy_source = {"Bucket": sourceBucketName, "Key": sourceFullFileKey}

        self._client.copy(copy_source, sourceBucketName, destFullFileKey)
        self._client.delete_object(Bucket=sourceBucketName, Key=sourceFullFileKey)

    def createDirectory(self, bucketName, s3Dir):
        newDir = s3Dir

        if newDir.endswith("/") is False:
            newDir = newDir + "/"

        self._client.put_object(Bucket=bucketName, Key=newDir)


class SecretManager:
    """AWS Secrets Manager class"""

    @staticmethod
    def get_secret(secretName: str, awsAccessKeyId: str, awsSecretKey: str, regionName: str):
        """Get the Secret from AWS"""
        """Attributes:"""
        secret_name = secretName
        region_name = regionName

        # Create a Secrets Manager client
        session = boto3.session.Session(
            aws_access_key_id=awsAccessKeyId,
            aws_secret_access_key=awsSecretKey,
            region_name=regionName,
        )
        client = session.client(service_name="secretsmanager", region_name=region_name)

        secret = []

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                secret = json.loads(get_secret_value_response["SecretString"])
            else:
                pass
        except ClientError as e:
            raise e

        return secret


class ParameterStore:
    @staticmethod
    def get_parameter_store_value(key, withDecryption=False):
        ssm = boto3.client("ssm", region_name="us-east-1")

        parameter = ssm.get_parameter(Name=key, WithDecryption=withDecryption)

        if parameter is None or "Parameter" not in parameter.keys():
            return ""

        return parameter["Parameter"]["Value"]


class CloudWatch:
    @staticmethod
    def format_dimension(dimensionName, dimensionValue):
        return {"Name": dimensionName, "Value": dimensionValue}

    @staticmethod
    def write_metric_data(regionName, metricNamespace, dimensions, metricName, metricUnit, metricValue):
        cloudwatch = boto3.client("cloudwatch", region_name=regionName)

        cloudwatch.put_metric_data(
            MetricData=[
                {
                    "MetricName": metricName,
                    "Dimensions": dimensions,
                    "Unit": metricUnit,
                    "Value": metricValue,
                },
            ],
            Namespace=metricNamespace,
        )


class CloudWatchLogs:
    def write_log(self, logGroupName, regionName, msg, sequenceToken=None):
        client = boto3.client("logs", region_name=regionName)

        logStreamName = "log-stream-{}".format(datetime.today().strftime("%Y%m%d"))

        try:
            response = client.create_log_stream(logGroupName=logGroupName, logStreamName=logStreamName)
        except Exception:
            pass

        currentTime = int(round(time.time() * 1000))

        if sequenceToken is None:
            try:
                response = client.describe_log_streams(
                    logGroupName=logGroupName,
                    logStreamNamePrefix=logStreamName,
                    orderBy="LogStreamName",
                    descending=True,
                    limit=1,
                )
            except Exception as e:
                logging.error(e)

            if "uploadSequenceToken" in response["logStreams"][0].keys():
                sequenceToken = response["logStreams"][0]["uploadSequenceToken"]

        try:
            if sequenceToken is not None:
                response = client.put_log_events(
                    logGroupName=logGroupName,
                    logStreamName=logStreamName,
                    logEvents=[
                        {"timestamp": currentTime, "message": msg},
                    ],
                    sequenceToken=sequenceToken,
                )
            else:
                response = client.put_log_events(
                    logGroupName=logGroupName,
                    logStreamName=logStreamName,
                    logEvents=[
                        {"timestamp": currentTime, "message": msg},
                    ],
                )
        except (
            client.exceptions.InvalidSequenceTokenException,
            client.exceptions.DataAlreadyAcceptedException,
        ) as e:
            msg = str(e)
            logging.info("Log exception: {}".format(msg))
            parts = msg.split(":")
            sequenceToken = parts[len(parts) - 1].strip()
            logging.info("Log next token: {}".format(sequenceToken))
            self.write_log(logGroupName, msg, sequenceToken)


class AWSLogger:
    _regionName = "us-east-1"
    _logGroupName = ""

    def __init__(self, logGroupName, regionName):
        self._logGroupName = logGroupName
        self._regionName = regionName

    def log(self, loggingLevel, appLevel, msg):
        outputMsg = ""

        if appLevel < 1:
            outputMsg = msg
        else:
            outputMsg = "{}>{}".format("".ljust((appLevel) * 4, "-"), msg)

        if loggingLevel == logging.DEBUG:
            logging.debug(outputMsg)
        elif loggingLevel == logging.INFO:
            logging.info(outputMsg)
        elif loggingLevel == logging.WARNING:
            logging.warning(outputMsg)
        elif loggingLevel == logging.ERROR:
            logging.error(outputMsg)
        else:
            logging.error(outputMsg)

        if loggingLevel == logging.DEBUG:
            return

        cloudWatchLogs = CloudWatchLogs()

        cloudWatchLogs.write_log(self._logGroupName, self._regionName, msg)
