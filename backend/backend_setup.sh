#!/bin/bash

# Create main project directory
mkdir -p saas-lead-finder/backend
cd saas-lead-finder/backend

# Create app directory and main files
mkdir -p app
touch app/__init__.py app/main.py app/config.py

# Create subdirectories
mkdir -p app/models app/routes app/services app/utils app/integrations

# Create __init__.py files
touch app/models/__init__.py app/routes/__init__.py app/services/__init__.py app/utils/__init__.py app/integrations/__init__.py

# Create basic files
touch app/models/user.py app/models/lead.py app/models/campaign.py app/models/subscription.py
touch app/routes/auth.py app/routes/leads.py app/routes/campaigns.py app/routes/subscriptions.py
touch app/services/twitter_service.py app/services/linkedin_service.py app/services/email_finder_service.py app/services/dm_sender_service.py
touch app/utils/helpers.py app/utils/rate_limiter.py
touch app/integrations/lemonsqueezy.py

# Create requirements.txt
touch requirements.txt

# Create Dockerfile
touch Dockerfile

echo "Backend directory structure created successfully!"