# Apple Base Infra Terraform

## Basic Infrastructure Provisioning

The basic infrastructure (S3 bucket, Elasticachhe Redis, Reducto Container IAM Policy) is all defined in [terraform/modules/base](terraform/modules/base). This is what is worth applying as a first step.


## Sample Helm Chart

A sample helm chart is provided in [reducto-chart](reducto-chart). This chart is configured like our production chart, but with a dummy docker container.

### Dummy Docker Image

A dummy docker image with the relevant infrastructure code is provided in [sample-container](sample-container). This docker image is used in the provided HELM chart.

This image also contains and endpoint which connects to Apple's Textract, and can/should be used to verify that the boto3 authentication is working correctly.