# Lab 6: Configure High Availability

*AWS Technical Essentials*

> Wherever you see `<ID>`, substitute the student ID your instructor assigned you (for example `user7`).

---

## ⚡ Lab 6: Configure High Availability

*AWS Technical Essentials — Load Balancing, Auto Scaling & Self-Healing*

**Instructor notes:** Welcome to Lab 6 — the capstone lab. This ties together VPC, EC2, IAM roles, load balancing, and Auto Scaling. Ensure all students have the VPC and security group from Lab 3.

---

## 🏷️ Resource Names for This Lab

Replace `<ID>` with your assigned student ID (for example `user7`).

| Resource | Name |
| --- | --- |
| Application Load Balancer | `employee-directory-alb-<ID>` |
| ALB security group | `employee-directory-alb-sg-<ID>` |
| Target group | `employee-directory-tg-<ID>` |
| Launch template | `employee-directory-lt-<ID>` |
| Auto Scaling group | `employee-directory-asg-<ID>` |
| *Reused from earlier labs* | `employee-directory-<ID>-vpc`, `employee-directory-app-sg-<ID>`, `employee-dir-key-<ID>` |

> **⚠️ 32-character limit:** AWS caps load balancer and target group names at 32 characters. Keep your ID to six characters or fewer.

**Instructor notes:** This lab creates the most resources, and the ALB, target group and ASG dropdowns will be crowded with every student's entries. Stress that they select by their own ID at every step — attaching your ASG to a classmate's target group is the classic failure here, and it is hard to spot because the app still loads.

---

## 📋 Lab Overview

### 🎯 Objectives

- Create an Application Load Balancer
- Create a Launch Template
- Configure an Auto Scaling Group
- Test self-healing
- View CloudWatch metrics

### 📝 Lab Details

- **Duration:** ~25 minutes
- **Capstone:** Lab 6 of 6

**Instructor notes:** This is the most complex lab. Students build a production-style architecture with load balancing, auto scaling, and self-healing. Emphasize that this is what real-world AWS deployments look like.

---

## ✅ Prerequisites

> **Before starting:** Verify these resources from previous labs exist.

- **VPC:** `employee-directory-<ID>-vpc` with 2 public subnets in different AZs
- **Security Group:** `employee-directory-app-sg-<ID>`
- **IAM Role:** EmployeeDirectoryAppRole
- **Key Pair:** `employee-dir-key-<ID>`

> **💡 Tip:** Terminate any running EC2 instances from earlier labs to stay within limits.

**Instructor notes:** Have students verify each resource exists. If anything is missing, they need to recreate it. This lab creates its own instances via the Launch Template and ASG. Previous EC2 instances are not needed.

---

## 🔧 Create the Application Load Balancer

1. Navigate to **EC2** → **Load Balancers** (left nav)
2. Click **Create load balancer** → **Application Load Balancer** → **Create**

| Setting | Value |
| --- | --- |
| Name | `employee-directory-alb-<ID>` |
| Scheme | **Internet-facing** |
| VPC | **`employee-directory-<ID>-vpc`** |
| Availability Zones | Check **both** public subnets |

Create a **new security group** for the ALB:

- Name: `employee-directory-alb-sg-<ID>`
- Inbound rule: **HTTP / 80** from `0.0.0.0/0`

**Instructor notes:** The ALB needs its own security group that allows HTTP from anywhere. Students need to create the SG in a new tab, then return and refresh the SG list. Make sure they select both public subnets for multi-AZ availability.

---

## 🔧 Create Target Group and Finish ALB

Under **Listeners and routing**, click **Create target group**:

| Setting | Value |
| --- | --- |
| Target type | **Instances** |
| Name | `employee-directory-tg-<ID>` |
| Protocol / Port | HTTP / 80 |
| VPC | `employee-directory-<ID>-vpc` |
| Health check path | `/` |

1. Click **Next**, skip registering targets, click **Create target group**
2. Return to the ALB tab, **refresh**, select **`employee-directory-tg-<ID>`**
3. Click **Create load balancer**

> **✅ Expected:** ALB created. Status will show **Provisioning** for a few minutes.

**Instructor notes:** The target group is empty for now — the Auto Scaling Group will register instances automatically. Health check on / will verify Apache is responding. The ALB takes 2-3 minutes to provision.

---

## 📄 Create a Launch Template

1. Navigate to **EC2** → **Launch Templates**
2. Click **Create launch template**

| Setting | Value |
| --- | --- |
| Name | `employee-directory-lt-<ID>` |
| AMI | **Amazon Linux 2023** |
| Instance type | **t2.micro** |
| Key pair | **`employee-dir-key-<ID>`** |
| Security group | **`employee-directory-app-sg-<ID>`** |

Under **Advanced details**:

- IAM instance profile: **EmployeeDirectoryAppRole**
- User data — paste the script on the next slide

**Instructor notes:** The launch template defines the blueprint for all instances created by Auto Scaling. Same security group and IAM role as before. The user data script includes the stress tool for later testing.

---

## 📄 Launch Template — User Data

Paste into the **User data** field:

```bash
#!/bin/bash -ex
yum update -y
yum install -y httpd stress
systemctl start httpd
systemctl enable httpd
EC2_INSTANCE_ID=$(ec2-metadata -i | cut -d" " -f2)
EC2_AZ=$(ec2-metadata -z | cut -d" " -f2)
echo "<!DOCTYPE html>
<html><head><title>Employee Directory</title>
<style>body{font-family:Arial,sans-serif;max-width:800px;margin:50px auto;padding:20px}
h1{color:#1a365d}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:12px;text-align:left}
th{background:#2b6cb0;color:white}tr:nth-child(even){background:#f7fafc}</style></head>
<body><h1>Employee Directory</h1>
<p>Instance: $EC2_INSTANCE_ID | AZ: $EC2_AZ</p>
<table><tr><th>Name</th><th>Department</th><th>Location</th></tr>
<tr><td>John Smith</td><td>Engineering</td><td>Seattle</td></tr>
<tr><td>Jane Doe</td><td>Marketing</td><td>New York</td></tr>
<tr><td>Bob Johnson</td><td>Sales</td><td>Austin</td></tr></table>
</body></html>" > /var/www/html/index.html
```

1. Click **Create launch template**

**Instructor notes:** This script is similar to Lab 2 but adds the stress tool and embeds the Instance ID and AZ in the page. When students refresh the ALB DNS, they will see different instance IDs, proving load balancing works. No manual edits needed — the script detects instance metadata automatically.

---

## 📊 Create Auto Scaling Group

1. Navigate to **EC2** → **Auto Scaling Groups**
2. Click **Create Auto Scaling group**
3. Name: `employee-directory-asg-<ID>`
4. Launch template: **`employee-directory-lt-<ID>`**
5. Click **Next**
6. VPC: **`employee-directory-<ID>-vpc`**
7. Subnets: Select **both** public subnets
8. Click **Next**

**Instructor notes:** The ASG uses the launch template to know what kind of instances to create. Selecting both subnets means instances will be distributed across AZs for high availability.

---

## 📊 ASG — Attach to ALB

1. Select **Attach to an existing load balancer**
2. Choose **Choose from your load balancer target groups**
3. Select **`employee-directory-tg-<ID>`**
4. Health check type: Check **Turn on Elastic Load Balancing health checks**
5. Click **Next**

| Setting | Value |
| --- | --- |
| Desired capacity | **2** |
| Min | **2** |
| Max | **4** |

6. Click **Next** through remaining pages, then **Create Auto Scaling group**

**Instructor notes:** Attaching the ASG to the target group means new instances are automatically registered with the ALB. ELB health checks mean unhealthy instances get replaced. Desired=2 means 2 instances launch immediately, one in each AZ.

---

## 🌐 Verify — Test the ALB

1. Go to **EC2** → **Instances** — confirm 2 new instances are **Running**
2. Go to **Load Balancers** → select your ALB
3. Copy the **DNS name**
4. Open in a browser: `http://<ALB_DNS_NAME>`
5. Refresh the page several times

> **✅ Expected:** The Employee Directory page loads. Refreshing shows different **Instance IDs** and **AZs** — the ALB is distributing traffic.

**Instructor notes:** It takes 2-3 minutes for instances to pass health checks and be registered. If the page does not load, check: ALB status is Active, target group shows healthy targets, instances are in Running state. The instance ID changes on refresh prove load balancing is working.

---

## 🔨 Test Self-Healing

1. Go to **EC2** → **Instances**
2. Select one of the ASG instances
3. Click **Instance state** → **Terminate instance**
4. Watch the **Auto Scaling Groups** activity tab

> **✅ Expected:** Within 1-2 minutes, Auto Scaling launches a **replacement instance** to maintain the desired count of 2. The ALB continues serving traffic through the remaining healthy instance.

**Instructor notes:** This is the key demonstration of self-healing. The ASG detects the terminated instance, launches a replacement, and the ALB automatically registers it. Users experience no downtime because the other instance continues serving traffic. Check the Activity tab to see the scaling event.

---

## 📊 View CloudWatch Metrics

1. Go to **EC2** → select an instance → **Monitoring** tab
2. Review: CPU utilization, network in/out, status checks
3. Go to **Load Balancers** → select ALB → **Monitoring** tab
4. Review: request count, healthy host count, response time

> **💡 Key metrics:** The ALB **Healthy Host Count** dropped to 1 when you terminated an instance and returned to 2 when the replacement launched.

**Instructor notes:** CloudWatch metrics may take a few minutes to populate. Point out that these metrics are available automatically — no agent installation needed. In production, you would set CloudWatch Alarms to notify on unhealthy hosts or high error rates.

---

## 🗑 Clean Up — Step 1

> **⚠️ Delete in this order** to avoid dependency errors:

1. **Auto Scaling Group:** EC2 → Auto Scaling Groups → select → Delete (set desired/min to 0, then delete)
2. **Wait** for all ASG instances to terminate
3. **Load Balancer:** EC2 → Load Balancers → select → Delete
4. **Target Group:** EC2 → Target Groups → select → Delete

**Instructor notes:** Order matters. Delete the ASG first so it does not launch replacement instances. Wait for instances to fully terminate before deleting the ALB and target group. This can take 2-3 minutes.

---

## 🗑 Clean Up — Step 2

5. **Launch Template:** EC2 → Launch Templates → select → Delete
6. **Security Groups:** Delete `employee-directory-alb-sg-<ID>` and `employee-directory-app-sg-<ID>`
7. **VPC:** VPC → Your VPCs → select `employee-directory-<ID>-vpc` → Delete (this removes subnets, route tables, and IGW)
8. **Key Pair:** EC2 → Key Pairs → delete `employee-dir-key-<ID>`
9. **Any remaining EC2 instances** from earlier labs → Terminate

> **⚠️** If VPC deletion fails, check for remaining ENIs or instances. All dependencies must be removed first.

**Instructor notes:** The VPC delete action will automatically clean up subnets, route tables, and the internet gateway if there are no remaining dependencies. If it fails, look for lingering network interfaces or instances. Security groups must be deleted before the VPC.

---

## 🎉 Lab 6 Complete!

*High Availability Architecture Deployed*

**Instructor notes:** Congratulate students on completing the capstone lab and the entire course lab series.

---

## 🎯 Key Takeaways

### 🛠️ What You Built

- Application Load Balancer across 2 AZs
- Launch Template with bootstrap script
- Auto Scaling Group with self-healing
- CloudWatch monitoring

### 📚 Key Concepts

- **ALB** distributes traffic across AZs
- **ASG** maintains desired instance count
- **Self-healing** replaces failed instances
- **CloudWatch** provides monitoring

**Instructor notes:** This architecture represents the foundation of production AWS deployments. Review how all the services work together: VPC provides networking, ALB handles traffic distribution, ASG manages capacity and self-healing, CloudWatch provides visibility.

---

## 🏆 All Labs Complete!

*AWS Technical Essentials — You have built and deployed across IAM, EC2, VPC, S3, DynamoDB, ALB, and Auto Scaling*

**Instructor notes:** Final celebration slide. Students have completed all 6 labs covering the core AWS services. Encourage them to continue exploring with their own AWS accounts or through additional training.

---

## ❓ Questions?

*Final questions before we wrap up the course*

**Instructor notes:** Final Q&A. Common questions: How does scaling policy work? (Target tracking, step scaling, or scheduled.) What about HTTPS? (Add an SSL certificate to the ALB listener.) How do you do blue/green deployments? (Weighted target groups or CodeDeploy.) What is the next step for learning? (AWS Solutions Architect Associate certification.)

---
