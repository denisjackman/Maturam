import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.leaderboard_stack import MaturamLeaderboardStack


def test_leaderboard_table_created():
    app = core.App()
    stack = MaturamLeaderboardStack(app, "MaturamLeaderboardStack")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::DynamoDB::Table", {
        "TableName": "MaturamLeaderboard",
        "BillingMode": "PAY_PER_REQUEST",
    })


def test_api_routes_and_functions_created():
    app = core.App()
    stack = MaturamLeaderboardStack(app, "MaturamLeaderboardStack")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::ApiGatewayV2::Route", 2)
    template.resource_count_is("AWS::Lambda::Function", 2)
