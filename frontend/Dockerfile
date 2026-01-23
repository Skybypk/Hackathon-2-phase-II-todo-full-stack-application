FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the Next.js application
RUN npm run build

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]