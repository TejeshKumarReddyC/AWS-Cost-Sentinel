import boto3
import json
import datetime
from helper.cost import get_service_wise_cost

ce = boto3.client('ce')
sns = boto3.client('sns')
s3 = boto3.client('s3')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:412381766568:myfsns"
S3_BUCKET = "pdff1-tkr"
COST_THRESHOLD = 0.5
SERVICE_THRESHOLD = 0.2

def lambda_handler(event, context):
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    service_costs, total_cost = get_service_wise_cost(start_date, end_date)
    
    s3.put_object( Bucket=S3_BUCKET, Key=f"cost-report-{end_date}.json", Body=json.dumps({"total_cost": total_cost, "service_costs": service_costs}))
    
    if total_cost > COST_THRESHOLD:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"AWS cost alert, your monthly cost is {total_cost:.2f}!",
            Subject="AWS cost alert"
            )
    alert = ""
    for service, cost in service_costs.items():
        if cost > SERVICE_THRESHOLD:
            alert += f"AWS cost alert, your monthly cost is {service}: ${cost:.2f} exceeded {SERVICE_THRESHOLD}\n"
            
    if alert:       
        sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=alert,
        Subject="AWS cost alert"
        )
            
    return {"statusCode": 200, "body": "Cost analysis completed"}
    
        