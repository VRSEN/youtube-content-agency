FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Install uv and Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install npm packages in readwise-reader-mcp
RUN cd readwise-reader-mcp && \
    npm install && \
    npm run build

# install py-mcp-youtube-toolbox dependencies
RUN cd py-mcp-youtube-toolbox && \
    pip install --no-cache-dir -r requirements.txt

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Install py-mcp-youtube-toolbox dependencies
RUN if [ -f py-mcp-youtube-toolbox/requirements.txt ]; then \
        pip install --no-cache-dir -r py-mcp-youtube-toolbox/requirements.txt; \
    fi

CMD python -u main.py