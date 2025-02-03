**AWS-Cost-Sentinel**

**Workflow:-**

Event-Bridge ---> Lambda(Collects the cost data from cost explorer) ---> S3 && SNS Notification.

**Step1**:-  Create a lambda function & a layer which contains the helper function( gets total cost & service wise cost) and attach that layer to lambda function.

**Step2**:-  Attach the appropriate permissions to lambda for accessing S3, SNS.

**Step3**:-  Schedule a job in the **Event-Bridge** which triggers the lambda function on daily or monthly basis.

**Step4**:-  Create a S3 bucket for storing the cost-reports for further analysis.

**Step5**:-  Create **SNS** topic and ultimately put the bucket name, sns arn and other requored information in the lambda code.

**Working**:-

Scheduler in the **Event-Bridge** triggers **Lambda**, then lambda will collect the **total_cost** and **servicewise_cost**for highly costed services from the **Cost_explorer**. Alert will be sent by SNS if cost exceeds the budget and same will be stored in **S3** for further analysis.
