from huggingface_hub import snapshot_download 
snapshot_download(
        repo_id="SivakumarP/PhishingURLDetection",
    local_dir="./models",
)