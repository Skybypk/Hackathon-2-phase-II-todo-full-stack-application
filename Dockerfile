# Root-level Dockerfile for multi-service deployment
# This Dockerfile will not be used directly but serves as documentation
# for how to properly containerize the full application

# NOTE: For Render deployment, you typically deploy each service separately
# The current render.yaml has been updated to use the individual Dockerfiles
# in the backend/ and frontend/ directories.

# For a complete Docker-compose approach on Render, you would need to:
# 1. Use Render's native service definitions (as in the current render.yaml)
# 2. OR create a single container that runs both services
# 3. OR use Render's connected services feature

# The current approach in render.yaml is the recommended way for multi-service
# applications on Render - defining each service separately.