from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as integrations,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class MaturamLeaderboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Single-table design: one partition ("GLOBAL") holds every score.
        # Sort key is "{score:010d}#{timestamp}#{uuid}" - zero-padding the
        # score means a plain sort-key query (ScanIndexForward=False, Limit=N)
        # returns the top N scores directly, no GSI or scan required.
        table = dynamodb.Table(
            self, "LeaderboardTable",
            table_name="MaturamLeaderboard",
            partition_key=dynamodb.Attribute(
                name="pk", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="sk", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            # DESTROY while the table is still empty/throwaway during
            # development. Switch to RETAIN once it holds scores worth
            # keeping across a `cdk destroy`.
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Shared secret the game sends as `x-api-key` when submitting a
        # score. Read-only (top scores) stays open; only writes are gated.
        # Generated randomly at deploy time - never appears in source or
        # the CloudFormation template in plaintext.
        api_secret = secretsmanager.Secret(
            self, "SubmitScoreApiSecret",
            description="Shared secret the Maturam game sends as x-api-key to submit a score",
        )

        common_env = {"TABLE_NAME": table.table_name}

        submit_score_fn = lambda_.Function(
            self, "SubmitScoreFunction",
            runtime=lambda_.Runtime.PYTHON_3_13,
            handler="submit_score.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                **common_env,
                "API_SECRET_ARN": api_secret.secret_arn,
            },
            timeout=Duration.seconds(10),
        )
        table.grant_write_data(submit_score_fn)
        api_secret.grant_read(submit_score_fn)

        top_scores_fn = lambda_.Function(
            self, "TopScoresFunction",
            runtime=lambda_.Runtime.PYTHON_3_13,
            handler="top_scores.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment=common_env,
            timeout=Duration.seconds(10),
        )
        table.grant_read_data(top_scores_fn)

        http_api = apigwv2.HttpApi(
            self, "LeaderboardApi",
            api_name="MaturamLeaderboardApi",
        )

        http_api.add_routes(
            path="/scores",
            methods=[apigwv2.HttpMethod.POST],
            integration=integrations.HttpLambdaIntegration(
                "SubmitScoreIntegration", submit_score_fn
            ),
        )
        http_api.add_routes(
            path="/scores/top",
            methods=[apigwv2.HttpMethod.GET],
            integration=integrations.HttpLambdaIntegration(
                "TopScoresIntegration", top_scores_fn
            ),
        )

        CfnOutput(self, "ApiUrl", value=http_api.api_endpoint)
        CfnOutput(self, "ApiSecretArn", value=api_secret.secret_arn)
