import boto3
from botocore.exceptions import NoCredentialsError


def uploadingFile(localfile, bucket, s3object):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(localfile, bucket, s3object)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = uploadingFile('./json_output_3.json', 'staging-for-load', '/dwh/vermeer/uploadedjsonfile_ayush.json')


# s3 = boto3.resource('s3')
# my_bucket = s3.Bucket('staging-for-load')
#
# for my_bucket_object in my_bucket.objects.all():
#     print(my_bucket_object)
