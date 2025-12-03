Azure DevOps Variable Group - sample variables

Create a Variable Group in Azure DevOps named `Azure-Variables` (the pipeline references this name).
Add the following variables (example values shown):

- `acrName` : `devopsassignacr.azurecr.io`    # ACR login server (used to form image names)
- `resourceGroupName` : `devopsassign-rg`     # Resource group where AKS and resources exist
- `aksClusterName` : `devopsassign-aks`       # AKS cluster name
- `app_insights_ikey` : <Application Insights instrumentation key>  # Stored as secret

Notes:
- Mark sensitive values (like `app_insights_ikey`) as secret in the Variable Group.
- The pipeline uses replacetokens (token format `$(` and `)`) to substitute these variables into the Kubernetes manifests before deploying.
- The CI matrix passes `serviceName` per job (api-gateway, user-service, order-service) during build/push.

Example usage in manifests:
- Image field in manifests should use `$(acrName)/<service>:<tag>` so the pipeline replaces `$(acrName)` with your ACR login server.
- In manifests where you need the App Insights key, use `$(app_insights_ikey)` and mark it secret in the Variable Group.

Once the Variable Group is created, link it to the pipeline (the YAML references `- group: Azure-Variables`).
