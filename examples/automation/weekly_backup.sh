#!/bin/bash
# Weekly backup script for ISO 27001 data
# Setup with cron: 0 2 * * 1 /path/to/weekly_backup.sh

set -e

BACKUP_DIR="$HOME/iso27001-backups"
DATE=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="iso27001_backup_$DATE.tar.gz"
RETENTION_DAYS=90  # Keep backups for 90 days

echo "📦 ISO 27001 Weekly Backup - $(date)"
echo "======================================="

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create archive
echo "1. Creating archive..."
tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" \
    -C "$HOME" \
    .iso27001/ \
    --exclude='*.tmp' \
    --exclude='*.log'

ARCHIVE_SIZE=$(du -h "$BACKUP_DIR/$ARCHIVE_NAME" | cut -f1)
echo "   ✓ Archive created: $ARCHIVE_NAME ($ARCHIVE_SIZE)"

# Optional: Upload to cloud storage
# Uncomment and configure for your cloud provider

# AWS S3
# echo "2. Uploading to S3..."
# aws s3 cp "$BACKUP_DIR/$ARCHIVE_NAME" s3://my-bucket/iso27001-backups/

# Google Cloud Storage
# echo "2. Uploading to GCS..."
# gsutil cp "$BACKUP_DIR/$ARCHIVE_NAME" gs://my-bucket/iso27001-backups/

# Azure Blob Storage
# echo "2. Uploading to Azure..."
# az storage blob upload \
#     --account-name mystorageaccount \
#     --container-name iso27001-backups \
#     --file "$BACKUP_DIR/$ARCHIVE_NAME" \
#     --name "$ARCHIVE_NAME"

# Clean old backups (older than RETENTION_DAYS)
echo "2. Cleaning old backups (>$RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "iso27001_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
REMAINING=$(ls -1 "$BACKUP_DIR"/iso27001_backup_*.tar.gz 2>/dev/null | wc -l)
echo "   ✓ Backups remaining: $REMAINING"

# Create backup manifest
echo "3. Creating manifest..."
cat > "$BACKUP_DIR/backup_manifest_$DATE.txt" << MANIFEST
Backup Date: $(date)
Archive: $ARCHIVE_NAME
Size: $ARCHIVE_SIZE
Files:
$(tar -tzf "$BACKUP_DIR/$ARCHIVE_NAME" | head -20)
...
MANIFEST

echo
echo "✓ Backup completed successfully"
echo "  Archive: $BACKUP_DIR/$ARCHIVE_NAME"
echo "  Size: $ARCHIVE_SIZE"
