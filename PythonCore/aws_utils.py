import boto3
import pandas as pd
from datetime import datetime
from PythonCore.slack_alert import send_slack_alert
from PythonCore.env_vars import get_env_var


def upload_to_aws(data, bucket_name):
    """Upload data to AWS S3."""
    token = get_env_var('TOKEN')
    file_name = f"DAR{token}YieldFile_{datetime.utcnow().strftime('%Y%m%d')}.csv"
    df = pd.DataFrame(data)

    # Parse the bucket name to get the object key
    bucket_name_parts = bucket_name.split('/', 1)
    bucket_name = bucket_name_parts[0]
    object_key = bucket_name_parts[1] + file_name

    try:
        aws_access_key_id = get_env_var('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = get_env_var('AWS_SECRET_ACCESS_KEY')
        aws_region_name = get_env_var('AWS_REGION')

        aws_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name
        )

        # Upload the file to S3
        s3 = aws_session.resource('s3')
        s3.Object(bucket_name, object_key).put(Body=df.to_csv(index=False))

        return f"Data successfully written to {bucket_name}/{object_key}"

    except Exception as e:
        send_slack_alert(f"Error occurred while uploading to AWS: {e}")
        raise
