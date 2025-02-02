import boto3

ce = boto3.client('ce')

def get_service_wise_cost(start_date, end_date):
    """Fetches cost per AWS service."""
    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    service_costs = {}
    total_cost = 0

    for service in response['ResultsByTime'][0]['Groups']:
        service_name = service['Keys'][0]
        service_cost = float(service['Metrics']['UnblendedCost'].get('Amount', 0.0))
        service_costs[service_name] = service_cost
        total_cost += service_cost

    return service_costs, total_cost
