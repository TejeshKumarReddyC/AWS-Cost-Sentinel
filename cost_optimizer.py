import boto3
import json
import datetime


ce = boto3.client('ce')
sns = boto3.client('sns')
s3 = boto3.client('s3')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:412381766568:myfsns"
S3_BUCKET = "pdff1-tkr"
COST_THRESHOLD = 0.5

def lambda_handler(event, context):
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
        )
    total_cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
    report = {
        "total_cost": total_cost,
        "start_date": start_date,
        "end_date": end_date,
    }
    report_json = json.dumps(report)
    s3.put_object(Bucket=S3_BUCKET, Key=f"cost-report-{end_date}.json", Body=report_json)
    
    if total_cost > COST_THRESHOLD:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"AWS cost alert, your monthly cost is {total_cost:.2f}!",
            Subject="AWS cost alert"
            )
    return {"statusCode": 200, "body": "Cost analysis completed"}
    
        
