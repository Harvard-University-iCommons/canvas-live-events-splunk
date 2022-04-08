# canvas-live-events-splunk

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- canvas_event_handler - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

The application receives live event data from Canvas and sends it to Splunk. It consists of an SQS queue where events are received,
a dead-letter queue to store events that were not processed successfully, and a Lambda function to package and deliver the events to Splunk.

To get started, you will need:
* An AWS account where you have permission to create Lambda functions, SQS queues, S3 buckets, Security Groups. This account should have a VPC and at least one subnet in it where your Lambda function can run.
* A Splunk account and a Splunk HEC (HTTP Event Collector) url and token.
* A Canvas instance where you have an administrator role and can configure Live Events.

## Prepare the configuration file

This repository includes a sample configuration file called `samconfig.toml.sample`. Copy this file to a file called `samconfig.toml` and edit it to match your environment:
* The configuration defaults to the 'us-east-1' region; if your environment is not in that region, you will need to change all references to 'us-east-1' to the region you are using.
* Fill in appropriate values in the last line of the file, `parameter_overrides`:
** provide your Splunk HEC URL and token
** provide your VPC ID
** provide a comma-separated list (can be just one) of subnet IDs in your VPC where your Lambda function can run

## Deploy the application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, using the configuration parameters in `samconfig.toml` as defaults. You can change the values to match your environment. If you answer `Y` to "Save arguments to configuration file" you won't need to re-enter the values the next time you run `sam deploy`.

When the deployment is complete, the CLI will print the URL corresponding to your SQS queue. You can use this URL to configure Canvas Live Events.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name canvas-live-events-splunk
```
