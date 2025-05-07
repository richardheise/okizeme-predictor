# Imagem base com Node.js 22 Alpine
FROM node:22-alpine

# Instala pnpm globalmente
RUN corepack enable && corepack prepare pnpm@latest --activate

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência
COPY pnpm-lock.yaml package.json ./

# Instala dependências de produção
RUN pnpm install --prod

# Copia o restante da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "build/index.js"]

