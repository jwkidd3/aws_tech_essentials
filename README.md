# AWS Technical Essentials

**Course Length:** 1 Day

## Course Description

AWS Technical Essentials introduces you to essential AWS services and common solutions. The course covers the fundamental AWS concepts related to compute, database, storage, networking, monitoring, and security. You will start working in AWS through hands-on course experiences. The course covers the concepts necessary to increase your understanding of AWS services, so that you can make informed decisions about solutions that meet business requirements. Throughout the course, you will gain information on how to build, compare, and apply highly available, fault tolerant, scalable, and cost-effective cloud solutions.

## Course Objectives

- Describe terminology and concepts related to AWS services
- Navigate the AWS Management Console
- Articulate key concepts of AWS security measures and AWS Identity and Access Management (IAM)
- Distinguish among several AWS compute services, including Amazon Elastic Compute Cloud (Amazon EC2), AWS Lambda, Amazon Elastic Container Service (Amazon ECS), and Amazon Elastic Kubernetes Service (Amazon EKS)
- Understand AWS database and storage offerings, including Amazon Relational Database Service (Amazon RDS), Amazon DynamoDB, and Amazon Simple Storage Service (Amazon S3)
- Explore AWS networking services
- Access and configure Amazon CloudWatch monitoring features

## Intended Audience

- Individuals responsible for articulating the technical benefits of AWS services to customers
- Individuals interested in learning how to get started with AWS
- SysOps administrators
- Solutions architects
- Developers

## Prerequisites

- IT experience
- Basic knowledge of common data center architectures and components (servers, networking, databases, applications, and so on)
- No prior cloud computing or AWS experience required

## Course Outline

### Module 1: Introduction to Amazon Web Services
- Introduction to AWS Cloud
- Security in the AWS Cloud
- Hosting the employee directory application in AWS
- **Hands-On Lab:** Introduction to AWS Identity and Access Management (IAM)

### Module 2: AWS Compute
- Compute as a service in AWS
- Introduction to Amazon Elastic Compute Cloud
- Amazon EC2 instance lifecycle
- AWS container services
- What is serverless?
- Introduction to AWS Lambda
- Choose the right compute service
- **Hands-On Lab:** Launch the Employee Directory Application on Amazon EC2

### Module 3: AWS Networking
- Networking in AWS
- Introduction to Amazon Virtual Private Cloud (Amazon VPC)
- Amazon VPC routing
- Amazon VPC security
- **Hands-On Lab:** Create a VPC and Relaunch the Corporate Directory Application in Amazon EC2

### Module 4: AWS Storage
- AWS storage types
- Amazon EC2 instance storage and Amazon Elastic Block Store (Amazon EBS)
- Object storage with Amazon S3
- Choose the right storage service
- **Hands-On Lab:** Create an Amazon S3 Bucket

### Module 5: Databases
- Explore databases in AWS
- Amazon Relational Database Service
- Purpose-built databases
- Introduction to Amazon DynamoDB
- Choose the right AWS database service
- **Hands-On Lab:** Implement and manage Amazon DynamoDB

### Module 6: Monitoring, Optimization, and Serverless
- Monitoring
- Optimization
- Alternate serverless employee directory application architecture
- **Hands-On Lab:** Configure High Availability for Your Application

### Module 7: Course Summary

## Course Materials

### Presentations
| Module | File |
|--------|------|
| 1 — Introduction to AWS | `presentations/module-01-introduction-to-aws.html` |
| 2 — AWS Compute | `presentations/module-02-aws-compute.html` |
| 3 — AWS Networking | `presentations/module-03-aws-networking.html` |
| 4 — AWS Storage | `presentations/module-04-aws-storage.html` |
| 5 — Databases | `presentations/module-05-databases.html` |
| 6 — Monitoring, Optimization & Serverless | `presentations/module-06-monitoring-optimization-serverless.html` |
| 7 — Course Summary | `presentations/module-07-course-summary.html` |

### Labs
Each lab ships in two formats: a Reveal.js deck for projecting, and a Markdown copy for handouts, printing, or the LMS.

| Lab | Deck | Markdown |
|-----|------|----------|
| 1 — IAM | `labs/lab-01-iam.html` | `labs/lab-01-iam.md` |
| 2 — EC2 | `labs/lab-02-ec2.html` | `labs/lab-02-ec2.md` |
| 3 — VPC | `labs/lab-03-vpc.html` | `labs/lab-03-vpc.md` |
| 4 — S3 | `labs/lab-04-s3.html` | `labs/lab-04-s3.md` |
| 5 — DynamoDB | `labs/lab-05-dynamodb.html` | `labs/lab-05-dynamodb.md` |
| 6 — High Availability | `labs/lab-06-high-availability.html` | `labs/lab-06-high-availability.md` |

All presentations and labs are Reveal.js single-file HTML — open directly in a browser.
PDF exports sit next to each lab deck in `labs/`, and the module exports are in `pdfs/`.

**The HTML decks are the source of truth.** After editing a lab deck, regenerate its Markdown copy so the two do not drift:

```bash
python3 tools/html2md.py      # requires: pip install beautifulsoup4
```

## Shared AWS Account — Resource Naming

All students in a delivery share one AWS account, so every resource a student creates must carry a unique suffix. Assign each student a short ID on day one — `user1` through `userN` — and have them substitute it wherever the labs show `<ID>`.

| Lab | Resource | Name |
|-----|----------|------|
| 1 | IAM user | `lab-user-<ID>` |
| 1 | IAM group | `EC2-Admins-<ID>` |
| 1 | IAM policy | `S3ScopedReadPolicy-<ID>` |
| 2 | EC2 instance | `employee-directory-app-<ID>` |
| 2 | Key pair | `employee-dir-key-<ID>` |
| 2 | Security group | `employee-directory-app-sg-<ID>` |
| 3 | VPC wizard name tag | `employee-directory-<ID>` → creates `employee-directory-<ID>-vpc` |
| 3 | EC2 instance | `employee-directory-app-vpc-<ID>` |
| 4 | S3 bucket | `employee-directory-app-bucket-<ID>-<RANDOM>` |
| 5 | DynamoDB table | `Employees-<ID>` |
| 6 | Load balancer | `employee-directory-alb-<ID>` |
| 6 | ALB security group | `employee-directory-alb-sg-<ID>` |
| 6 | Target group | `employee-directory-tg-<ID>` |
| 6 | Launch template | `employee-directory-lt-<ID>` |
| 6 | Auto Scaling group | `employee-directory-asg-<ID>` |

Notes:

- **Keep IDs to six characters or fewer.** AWS caps load balancer and target group names at 32 characters, and `employee-directory-alb-` already consumes 23.
- **S3 needs two layers.** Bucket names are unique across all of AWS, so Lab 4 keeps a random component on top of the student ID.
- **Lab 3's VPC wizard does the heavy lifting.** The name-tag auto-generation value propagates to the subnets, route tables, and internet gateway, so one field labels the whole network stack with the student's ID.
- **Lab 1's custom policy is scoped per student.** The resource ARN embeds `<ID>`, so a student's policy cannot read a classmate's bucket.

### Instructor pre-flight for a shared account

The course runs entirely in **us-east-1**. Set the console Region picker there and stay in it —
every lab after Lab 1 builds on resources from the previous labs, and those are invisible from
any other Region. No Cloud9 or CLI is needed; the labs are console-only plus EC2 user data.

#### Quota headroom in us-east-1

Verified on the lab account; the per-student column is what each student consumes across all six labs.

| Quota | Limit | Per student | Headroom |
| --- | --- | --- | --- |
| VPCs per Region | 35 | 1 (Lab 3) | ~35 students |
| Internet gateways per Region | 35 | 1 (Lab 3 wizard) | ~35 students |
| Elastic IPs per Region | 30 | 0 — no lab allocates one | n/a |
| Running On-Demand Standard vCPUs | 2208 | 4 (Labs 2, 3, and 2 × Lab 6) | not a constraint |

VPCs and internet gateways are the binding limits, so this account comfortably covers a class of
30. Both are adjustable and already raised above the AWS defaults of 5 — re-check them with
`aws service-quotas get-service-quota --service-code vpc --quota-code L-F678F1CE --region us-east-1`
before a larger delivery, and request an increase well ahead of class if you need one.

- **Clean-up is per student.** Have each student filter the console by their own ID at the end of every lab; sweep for orphans by ID after class.
