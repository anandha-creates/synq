# SYNQ – Secure Cloud-Based Task Management Platform

## Project Overview

SYNQ is a secure cloud-based task management platform developed using Flask and deployed on Amazon Web Services (AWS). The project demonstrates the implementation of cloud infrastructure, cybersecurity, networking, DevOps, monitoring, and logging concepts in a real-world web application.

The platform allows users to securely manage tasks while leveraging AWS services such as EC2, RDS, S3, CloudWatch, SNS, and Application Load Balancer (ALB).

---

## Features

* User Registration and Authentication
* Secure Password Hashing using bcrypt
* Role-Based Access Control (Admin/User)
* Task Creation, Update, and Deletion
* MySQL Database Integration
* Dockerized Deployment
* Nginx Reverse Proxy
* HTTPS Secure Communication
* CloudWatch Monitoring and Logging
* SNS Email Notifications
* Automated Backup Storage in Amazon S3
* API Rate Limiting
* Fail2Ban Protection
* Security Headers and XSS Protection

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Backend

* Python
* Flask
* SQLAlchemy ORM

### Database

* Amazon RDS MySQL

### Cloud Services

* Amazon EC2
* Amazon RDS
* Amazon S3
* Application Load Balancer (ALB)
* Amazon CloudWatch
* Amazon SNS

### DevOps Tools

* Docker
* Docker Compose
* GitHub
* GitHub Actions

---

## AWS Infrastructure

The project is deployed on a custom AWS infrastructure consisting of:

* Custom VPC (10.0.0.0/16)
* Public and Private Subnets
* Internet Gateway
* NAT Gateway
* Bastion Host
* Application Server (EC2)
* Amazon RDS MySQL Database
* Amazon S3 Backup Storage
* CloudWatch Monitoring
* SNS Notifications

---

## Security Features

* bcrypt Password Hashing
* HTTPS (SSL/TLS)
* SQL Injection Prevention using SQLAlchemy ORM
* Cross-Site Scripting (XSS) Protection
* API Rate Limiting
* Role-Based Access Control
* Security Headers
* SSH Key-Based Authentication
* Fail2Ban Brute Force Protection

---

## Monitoring and Logging

The monitoring system includes:

* Application Log Collection using CloudWatch Logs
* Failed Login Tracking using Metric Filters
* CloudWatch Alarms
* SNS Email Notifications
* Server Performance Monitoring
* Security Event Monitoring

---

## Repository Structure

```text
SYNQ/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
├── static/
├── backups/
├── scripts/
└── README.md
```

## Deployment Workflow

```text
GitHub Repository
        ↓
GitHub Actions (CI/CD)
        ↓
Docker Build
        ↓
Amazon EC2
        ↓
Docker Container
        ↓
Flask Application
        ↓
Amazon RDS MySQL
```

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/SYNQ.git
cd SYNQ
```

### Build and Run Application

```bash
docker compose up -d --build
```

### Access Application

```text
https://synq.duckdns.org
```

---

## Project Objectives

* Deploy a secure web application on AWS.
* Implement cloud networking and infrastructure services.
* Apply cybersecurity best practices.
* Implement monitoring and alerting mechanisms.
* Demonstrate DevOps and containerization concepts.
* Manage backups and cloud storage securely.

---

## Project :-

Summer Internship Capstone Project

SYNQ – Secure Cloud-Based Task Management Platform
