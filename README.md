# Sistema de Estoque

Um web app completo para gestão de estoque com funcionalidades de busca, cadastro e upload de planilhas.

## Funcionalidades

### 🔍 Busca de Produtos
- Busca por código ou descrição do produto
- Exibição detalhada do estoque por filial (Ceará, Santa Catarina, São Paulo)
- Visualização do total geral, reservas e disponibilidade

### ➕ Cadastro de Produtos
- Formulário completo para cadastro de novos produtos
- Cálculo automático do total baseado no estoque das filiais
- Validação de dados obrigatórios

### 📊 Upload de Planilhas
- Upload de arquivos CSV com dados de estoque
- Processamento automático com inserção e atualização de produtos
- Suporte ao formato padrão com colunas: COD, NOME DO PRODUTO, MARCA, CEARÁ, SANTA CATARINA, SÃO PAULO, TOTAL, RESERVA

### 📱 Interface Responsiva
- Design adaptável para desktop e mobile
- Interface moderna com componentes shadcn/ui
- Navegação por abas intuitiva

## Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local
- **Pandas** - Processamento de dados CSV
- **Flask-CORS** - Suporte a requisições cross-origin

### Frontend
- **React** - Biblioteca JavaScript para UI
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS utilitário
- **shadcn/ui** - Componentes de interface
- **Lucide React** - Ícones

## Estrutura do Projeto

```
estoque-app/
├── src/
│   ├── models/
│   │   └── produto.py          # Modelo de dados do produto
│   ├── routes/
│   │   └── produto.py          # Rotas da API
│   ├── static/                 # Frontend compilado
│   └── main.py                 # Aplicação principal
├── venv/                       # Ambiente virtual Python
└── requirements.txt            # Dependências Python

estoque-frontend/
├── src/
│   ├── components/
│   │   ├── BuscaProduto.jsx    # Componente de busca
│   │   ├── CadastroProduto.jsx # Componente de cadastro
│   │   └── UploadPlanilha.jsx  # Componente de upload
│   └── App.jsx                 # Componente principal
└── dist/                       # Build de produção
```

## Como Executar

### Desenvolvimento

1. **Backend (Flask)**:
   ```bash
   cd estoque-app
   source venv/bin/activate
   python src/main.py
   ```

2. **Frontend (React)**:
   ```bash
   cd estoque-frontend
   npm run dev
   ```

### Produção

1. **Build do Frontend**:
   ```bash
   cd estoque-frontend
   npm run build
   cp -r dist/* ../estoque-app/src/static/
   ```

2. **Executar Aplicação**:
   ```bash
   cd estoque-app
   source venv/bin/activate
   python src/main.py
   ```

A aplicação estará disponível em `http://localhost:5000`

## API Endpoints

### Produtos
- `GET /api/produtos/buscar?termo={termo}` - Busca produtos por código ou nome
- `POST /api/produtos` - Cadastra novo produto
- `PUT /api/produtos/{cod}` - Atualiza produto existente
- `POST /api/produtos/upload` - Upload de planilha CSV
- `GET /api/produtos` - Lista produtos com paginação

## Formato da Planilha CSV

A planilha deve conter as seguintes colunas:
- **COD** - Código do produto (obrigatório)
- **NOME DO PRODUTO** - Nome/descrição do produto
- **MARCA** - Marca do produto
- **CEARÁ** - Quantidade em estoque no Ceará
- **SANTA CATARINA** - Quantidade em estoque em Santa Catarina
- **SÃO PAULO** - Quantidade em estoque em São Paulo
- **TOTAL** - Total geral (calculado automaticamente)
- **RESERVA** - Quantidade reservada

### Exemplo de CSV:
```csv
COD,NOME DO PRODUTO,MARCA,CEARÁ,SANTA CATARINA,SÃO PAULO,TOTAL,RESERVA
1234,Câmera Digital,Sony,10,15,20,45,5
5678,Tripé Profissional,Manfrotto,5,8,12,25,2
```

## Recursos Implementados

✅ Busca por código e descrição  
✅ Cadastro de produtos com validação  
✅ Upload e processamento de planilhas CSV  
✅ Interface responsiva para desktop e mobile  
✅ Cálculo automático de totais  
✅ Tratamento de erros nos dados  
✅ Feedback visual para o usuário  
✅ Design moderno e profissional  

## Próximos Passos

Para expandir o sistema, considere implementar:
- Autenticação de usuários
- Histórico de movimentações
- Relatórios de estoque
- Alertas de estoque baixo
- Integração com códigos de barras
- Backup automático dos dados

## Suporte

Para dúvidas ou problemas, consulte a documentação do código ou entre em contato com a equipe de desenvolvimento.

