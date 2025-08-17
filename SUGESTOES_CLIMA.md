# Sistema de Sugestões Baseadas no Clima

Este sistema integra informações meteorológicas com sugestões inteligentes para suas tarefas, ajudando você a planejar melhor suas atividades baseado nas condições climáticas.

## Como Funciona

O sistema analisa o tipo de atividade (interno/externo) e o clima atual da cidade para gerar sugestões personalizadas e relevantes.

## Tipos de Atividade Suportados

### Atividades Externas
- `externo`, `outdoor`, `ar livre`, `rua`, `exercício`, `esporte`

### Atividades Internas  
- `interno`, `casa`, `home`, `indoor`, `escritório`, `trabalho`

### Atividades de Concentração
- `estudo`, `leitura`, `concentração`

## Condições Climáticas Analisadas

- **Chuva/Tempestade**: Sugere atividades internas
- **Tempo Nublado**: Bom para atividades que não precisam de sol direto
- **Céu Limpo/Ensolarado**: Ideal para atividades externas
- **Temperatura**: Considera temperaturas extremas (muito baixa/alta)
- **Vento**: Alerta sobre ventos fortes
- **Umidade**: Informação adicional sobre conforto

## Endpoints Disponíveis

### 1. Criar Tarefa com Sugestão Automática
```
POST /todo/
```
A sugestão é gerada automaticamente baseada no clima atual.

### 2. Obter Sugestão de Clima
```
GET /todo/sugestao-clima/{activity_type}/{city}
```
Obtém uma sugestão para um tipo de atividade e cidade específicos.

**Exemplo:**
```
GET /todo/sugestao-clima/externo/São Paulo
```

### 3. Atualizar Sugestão de uma Tarefa
```
PUT /todo/{todo_id}/sugestao-clima
```
Atualiza a sugestão de uma tarefa específica baseada no clima atual.

### 4. Atualizar Todas as Sugestões
```
PUT /todo/atualizar-sugestoes-clima
```
Atualiza as sugestões de todas as tarefas do usuário.

## Exemplos de Sugestões

### Para Atividades Externas em Dia de Chuva
```
🌧️ Está chovendo em São Paulo! Sugestão: Considere fazer uma tarefa em casa. 
Atividades internas como organização, leitura, exercícios em casa ou projetos 
caseiros seriam ideais.
```

### Para Atividades Internas em Dia Ensolarado
```
☀️ Tempo limpo e ensolarado em São Paulo (25°C)! Mesmo fazendo uma tarefa 
em casa, você pode aproveitar a luz natural. Considere abrir as janelas 
para ventilação!
```

### Para Estudo em Dia Nublado
```
☁️ Tempo nublado em São Paulo (20°C). Luz suave ideal para leitura e estudo. 
Aproveite a tranquilidade!
```

## Configuração Necessária

Certifique-se de que a `API_KEY` do OpenWeatherMap está configurada no arquivo `config.py`:

```python
API_KEY = "sua_chave_da_api_aqui"
```

## Benefícios

1. **Planejamento Inteligente**: Sugestões baseadas em dados meteorológicos reais
2. **Conforto**: Evita atividades externas em condições climáticas desfavoráveis
3. **Produtividade**: Aproveita melhor as condições climáticas para cada tipo de atividade
4. **Segurança**: Alerta sobre condições extremas (temperatura, vento)
5. **Flexibilidade**: Permite atualizar sugestões conforme o clima muda

## Uso no Frontend

O frontend pode usar estas sugestões para:
- Mostrar alertas visuais sobre o clima
- Sugerir tipos de atividades apropriadas
- Exibir informações meteorológicas junto com as tarefas
- Permitir que o usuário atualize sugestões manualmente
