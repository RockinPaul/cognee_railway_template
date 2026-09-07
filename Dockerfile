# Cognee backend API for Railway. Upgrade cognee by bumping this tag.
FROM cognee/cognee:1.5.4

# Railway injects PORT; the upstream entrypoint listens on HTTP_PORT.
ENTRYPOINT ["sh", "-c", "export HTTP_PORT=${PORT:-8080}; exec /app/entrypoint.sh"]
