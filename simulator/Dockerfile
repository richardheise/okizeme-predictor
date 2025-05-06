# Usa imagem oficial do Node.js
FROM node:22-alpine

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY package*.json ./

# Instala somente dependências de produção
RUN pnpm install --only=production

# Copia o restante do código (incluindo build/)
COPY . .

# Expõe a porta (ajuste conforme seu app)
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "build/index.js"]


