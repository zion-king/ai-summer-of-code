FROM quay.io/astronomer/astro-runtime:12.0.0


# Update package lists and install required build dependencies
USER root

# Install build-essential, Python dev headers, and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libhnswlib-dev \
    cmake \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to astro user
USER astro