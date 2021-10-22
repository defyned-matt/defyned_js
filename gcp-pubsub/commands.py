project = "defyned-data"
dataset = "?"

commands = f"""
# Create Dataset
bq mk --dataset {project}:bq_poc

# Create Table
bq mk -t bq_poc.txn_msg year:STRING,month:STRING,sales:FLOAT


# Create Service Account
gcloud iam service-accounts create svc-cloudrun-api --display-name "Cloud Run Streaming API"

# Add Roles to Service Account
gcloud projects add-iam-policy-binding {project} \
         --member serviceAccount:svc-cloudrun-api@{project}.iam.gserviceaccount.com \
         --role roles/bigquery.admin

gcloud projects add-iam-policy-binding {project} \
         --member serviceAccount:svc-cloudrun-api@{project}.iam.gserviceaccount.com \
         --role roles/pubsub.editor

gcloud projects add-iam-policy-binding {project} \
         --member serviceAccount:svc-cloudrun-api@{project}.iam.gserviceaccount.com \
         --role roles/storage.admin

gcloud projects add-iam-policy-binding {project} \
         --member serviceAccount:svc-cloudrun-api@{project}.iam.gserviceaccount.com \
         --role roles/run.admin

# Build and Upload App to Container Registry
gcloud builds submit --tag gcr.io/{project}/stream-analytics

# Download App Image from Container Registry and Deploy
gcloud run deploy --image gcr.io/{project}/stream-analytics \
         --service-account svc-cloudrun-api@{project}.iam.gserviceaccount.com \
         --platform managed

# Create PubSub Topic
gcloud pubsub topics create pubsub-topic

# Create PubSub Subscription with Service Account
gcloud pubsub subscriptions create pubsub-subscription \
         --topic pubsub-topic \
         --push-endpoint=https://stream-analytics-la7ldrpbna-ue.a.run.app/ \
         --push-auth-service-account=svc-cloudrun-api@{project}.iam.gserviceaccount.com

"""
