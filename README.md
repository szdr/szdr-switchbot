# szdr-switchbot
switchbot APIを叩いてDBに格納

## デプロイ

```
$ gcloud functions deploy szdr-switchbot \
--gen2 \
--runtime=python311 \
--region=asia-northeast1 \
--entry-point=main \
--trigger-topic=szdr-switchbot \
--env-vars-file .env.yaml
```