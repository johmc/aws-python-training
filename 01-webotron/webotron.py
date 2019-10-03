#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites with AWS
Automates Process

"""

import boto3
import click

from bucket import BucketManager

session = boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)

#s3 = session.resource('s3')
client = session.client('s3')

@click.group()
def cli():
	"""Webotron deploys websites to AWS"""
	pass

@cli.command('list-buckets')
def list_buckets():
	"""List all s3 buckets"""
	for bucket in bucket_manager.all_buckets():
		print(bucket)


@cli.command('create-bucket')
@click.argument('bucket_name')
def create_bucket(bucket_name, region):
	"""Create a S3 bucket"""
	s3.create_bucket(
		Bucket=bucket_name, 
		CreateBucketConfiguration={'LocationConstraint': session.region_name})
	print("Successfuly created a S3 Bucket")
	print("Automatically listing S3 Buckets...")
	for bucket in s3.buckets.all():
		print(bucket)


@cli.command('delete-bucket')
@click.argument('bucket_name')
def delete_bucket(bucket_name):
	"""Delete S3 Bucket"""
	client.delete_bucket(Bucket=bucket_name)
	print("Successfuly deleted")
	print("Automatically listing S3 Buckets...")
	for bucket in s3.buckets.all():
		print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
	"""List objects in an s3 bucket"""
	for obj in bucket_manager.all_objects(bucket):
		print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
	"""Create and configure S3 bucket"""
	s3_bucket = bucket_manager.init_bucket(bucket)
	bucket_manager.set_policy(s3_bucket)
	bucket_manager.configure_website(s3_bucket)

	return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
	"""Sync contents of PATHNAME to BUCKET"""
	bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
	cli()
