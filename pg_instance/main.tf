
terraform {
  required_version = "1.9.5"

  backend "s3" {}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.65.0"
    }
  }
}

locals {
  postgres_identifier    = "openinfra"
  postgres_user_name     = "openinfra"
  postgres_user_password = "openinfraday.2025"
  postgres_db_password   = "openinfraday.2025"
}


variable "pipeline_vault_role" {
  description = "Vault role name to use to be authenticate."
}
variable "vault_addr" {
  description = "The vault address (endpoint)."
}
# MANDATORY
variable "pipeline_vault_backend" {
  description = "Vault PATH backend to be authenticate."
}
# Input Variables
variable "region" {
  description = "Region in which AWS Resources to be created"
  type        = string
  default     = "eu-west-1"
}

// PROVIDERS
provider "vault" {
  address = var.vault_addr
}

data "vault_aws_access_credentials" "creds" {
  backend = var.pipeline_vault_backend
  role    = var.pipeline_vault_role
  type    = "sts"
}

provider "aws" {
  region     = var.region
  access_key = data.vault_aws_access_credentials.creds.access_key
  secret_key = data.vault_aws_access_credentials.creds.secret_key
  token      = data.vault_aws_access_credentials.creds.security_token
}


data "aws_vpc" "vpc" {
 filter {
  name = "tag:Name"
  values = ["my-app-vpc"]
 }
}
data "aws_subnets" "default_subnets" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.vpc.id] # Replace 'your_vpc_name' with the actual name of your VPC data source
  }
  tags = {
    tier = "Public"
  }
}


# data "aws_subnet" "public_subnet" {
#  id = data.aws_subnets.default_subnets.ids[0] // this will fetch first subnet
# }

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = data.aws_subnets.default_subnets.ids

  tags = {
    Name = "RDS subnet group"
  }
}

// POSTGRES
resource "aws_security_group" "allow_postgres_traffic" {
  name        = "allow_postgres"
  description = "Allow Postgres traffic"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    description = "allow Postgres"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow postgres"
  }
}

resource "aws_db_instance" "pg_db_test" {
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "14"
  instance_class         = "db.t3.micro"
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  identifier             = local.postgres_identifier
  username               = local.postgres_user_name
  password               = local.postgres_db_password
  publicly_accessible    = true
  parameter_group_name   = "default.postgres14"
  vpc_security_group_ids = [aws_security_group.allow_postgres_traffic.id]
  skip_final_snapshot    = true
}
