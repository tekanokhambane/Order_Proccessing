# Deployement and setup of Order processing django

## Testing




## Deployment

1. **Installing AWS CLI:**
   - Set up a new user and group in AWS IAM with limited access.
   - Install AWS CLI using Python's virtual environment:
     ```bash
     virtualenv venv -p python
     source venv/bin/activate
     python -m pip install awscli
     aws --version
     ```

2. **Building Container Images:**
   - Build Docker images for the Django app:
     ```bash
     docker build -t django_process -f /backend/Dockerfile_data .
     docker build -t django -f /backend/Dockerfile .
     ```

3. **Pushing Images to ECR:**
   - Create an ECR repository and push the Docker images:
     ```bash
     aws ecr create-repository --repository-name myproject
     docker tag django_precess <registry_ID>.dkr.ecr.<region>.amazonaws.com/order_processing:data
     docker tag django <registry_ID>.dkr.ecr.<region>.amazonaws.com/order_processing:app
     docker push <registry_ID>.dkr.ecr.<your_region>.amazonaws.com/order_processing:data
     docker push <registry_ID>.dkr.ecr.<your_region>.amazonaws.com/order_processing:app
     ```

4. **Creating Infrastructure on AWS:**
   - I Used CloudFormation to create the VPC stack, execution role, load balancer, security group, task definition, Postgres RDS, S3 bucket, and manage secrets in Parameter Store.


   ```bash
   cd conf
   aws cloudformation create-stack --stack-name vpc --template-body file://vpc.yaml --capabilities CAPABILITY_NAMED_IAM

   aws cloudformation create-stack --stack-name roles --template-body file://roles.yaml --capabilities CAPABILITY_NAMED_IAM

   ## use the 'data' image
   aws cloudformation create-stack --stack-name lb-sg-task --template-body file://lb_sg_task.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=ImageUrl,ParameterValue='<your registry ID>.dkr.ecr.<your region>.amazonaws.com/myproject:data'

   aws cloudformation create-stack --stack-name rds-s3 --template-body file://rds_s3.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=BucketName,ParameterValue=$(head /dev/urandom | tr -dc a-z0-9 | head -c10)

   aws ssm put-parameter --overwrite --name /Prod/DjangoSecret --type SecureString --value <SECRET_KEY value>

   aws cloudformation create-stack --stack-name service --template-body file://service.yaml --capabilities CAPABILITY_NAMED_IAM

   aws cloudformation delete-stack --stack-name service

## use the 'app' image this time

   aws cloudformation update-stack --stack-name lb-sg-task --template-body file://lb_sg_task.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=ImageUrl,ParameterValue='<your registry ID>.dkr.ecr.<your region>.amazonaws.com/myproject:app'

   aws cloudformation create-stack --stack-name service --template-body file://service.yaml --capabilities CAPABILITY_NAMED_IAM

## Use Lambda
   Once the images, roles and other services are complete. You can reuse the container with services like lambda function 
   ```

   

5. **Updating ENV Variables in Parameter Store:**
   - Update the Django SECRET_KEY as a SecureString type in the Parameter Store:
     ```bash
     aws ssm put-parameter --overwrite --name /Prod/DjangoSecret --type SecureString --value <SECRET_KEY value>
     ```

6. **Running ECS Services:**
   - Run the ECS service with the container image that sets up the DB and static files.
   - Launch the ECS service using the container image that launches the Django app.


