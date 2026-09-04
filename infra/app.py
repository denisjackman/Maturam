#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.leaderboard_stack import MaturamLeaderboardStack


app = cdk.App()
MaturamLeaderboardStack(app, "MaturamLeaderboardStack",
    # Deploy to whatever account/region the AWS CLI default profile points at.
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION", "eu-west-2"),
    ),
    )

app.synth()
