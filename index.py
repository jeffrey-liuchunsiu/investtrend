import json

import json
import matt_supertrend as mst

def handler(event, context):

    # Event contains the data passed to the lambda function
    data = event

    symbol = data.get('symbol', "BTC-USD")
    investment = data.get('investment', 10000000)
    commission = data.get('commission', 0)
    start_date = data.get('start_date', "2023-1-1")
    end_date = data.get('end_date', "2023-10-1")
    interval = data.get('interval', '1d')
    atr = data.get('atr')
    multiplier = data.get('multiplier')

    strategy = mst.Supertrend
    backtest = mst.backtest_supertrend

    fy_df = mst.get_yf_df(symbol, start_date, end_date, interval)

    atr_period, multiplier, ROI = mst.find_optimal_parameter(fy_df, strategy, backtest, investment, commission, atr, multiplier)

    result = {
        'Best Parameter Set': {
            'ATR Period': atr_period,
            'Multiplier': multiplier,
            'ROI': f'{ROI}%'
        }
    }

    # Instead of returning a flask response, you just return the data and the status code.
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
    # return {
    #     'statusCode': 200,
    #     'body': json.loads(response.content)
    # }
# # Load environment variables from .env file
# load_dotenv("./.env")

# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# print('aws_access_key_id: ', aws_access_key_id)
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
# print('aws_secret_access_key: ', aws_secret_access_key)
# region_name = os.getenv('AWS_REGION')
# print('region_name: ', region_name)


# def handler(event, context):
    
#     my_session = boto3.session.Session(
#                           aws_access_key_id="AKIAWFODOPGFGGIEVY7C", 
#                           aws_secret_access_key="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", 
#                           )
#     # Create a Boto3 client for ECS
#     ecs_client = my_session.client('ecs',region_name=region_name)

#     # Define the parameters for running the Fargate task
#     task_definition = 'amplify-investtrendv2-dev-234900-testinvesttrendscheduleroi:3'
#     cluster = 'amplify-investtrendv2-dev-234900-NetworkStack-9EI9N1KBHGPK-Cluster-cjkHTEpdI4fc'
#     launch_type = 'FARGATE'
#     network_configuration = {
#         'awsvpcConfiguration': {
#             'subnets': ['subnet-0a590e02d8dae90a5','subnet-0e6dbe8b7b3e8426c','subnet-0ebb9cc774cc49bb0'],
#             'securityGroups': ['sg-0f45b0a00e60b6d71'],
#             'assignPublicIp': 'ENABLED'
#         }
#     }

#     # Start the Fargate task
#     response = ecs_client.run_task(
#         taskDefinition=task_definition,
#         cluster=cluster,
#         launchType=launch_type,
#         networkConfiguration=network_configuration
#     )

#     # Process the response
#     if response['failures']:
#         # Handle failures if any
#         print(f"Failed to start Fargate task: {response['failures']}")
#     else:
#         # Fargate task started successfully
#         print("Fargate task started successfully")

#     # Return a response
#     return {
#         'statusCode': 200,
#         'body': 'Fargate task triggered successfully'
#     }
  