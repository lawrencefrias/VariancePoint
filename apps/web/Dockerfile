FROM node:22-alpine
WORKDIR /app
COPY apps/web/package.json apps/web/package-lock.json /app/
RUN npm ci
COPY apps/web /app
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
