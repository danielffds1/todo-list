# Sistema de Histórico de Tarefas

Este sistema rastreia todas as mudanças feitas nas tarefas, permitindo acompanhar a evolução de cada atividade.

## 📋 Funcionalidades

### 1. **Rastreamento Automático**
- ✅ Criação de tarefas
- ✅ Atualizações de campos
- ✅ Exclusão de tarefas
- ✅ Mudanças de status

### 2. **Informações Registradas**
- **Ação**: tipo de operação (created, updated, deleted)
- **Campo**: qual campo foi alterado
- **Valor Anterior**: valor antes da mudança
- **Novo Valor**: valor após a mudança
- **Data/Hora**: quando a mudança ocorreu
- **Usuário**: quem fez a alteração

## 🚀 Endpoints Disponíveis

### 1. **Histórico de uma Tarefa Específica**
```bash
GET /todo/{todo_id}/historico
```

**Exemplo:**
```bash
GET /todo/abc-123/historico
```

**Resposta:**
```json
[
    {
        "id": "hist-456",
        "todo_id": "abc-123",
        "user_id": "user-789",
        "action": "updated",
        "field_name": "status",
        "old_value": "pendente",
        "new_value": "em_andamento",
        "created_at": "2024-01-15T11:30:00"
    },
    {
        "id": "hist-455",
        "todo_id": "abc-123",
        "user_id": "user-789",
        "action": "created",
        "field_name": "tarefa_completa",
        "old_value": null,
        "new_value": "Tarefa criada: Estudar Python",
        "created_at": "2024-01-15T10:00:00"
    }
]
```

### 2. **Histórico Geral do Usuário**
```bash
GET /todo/historico/geral?limit=50
```

**Parâmetros:**
- `limit`: número máximo de registros (padrão: 50)

## 📊 Exemplos de Uso

### **Cenário 1: Criar uma Tarefa**
```bash
POST /todo/
{
    "title": "Estudar React",
    "description": "Aprender hooks",
    "status": "pendente",
    "activity_type": "interno",
    "city": "São Paulo"
}
```

**Histórico gerado:**
```json
{
    "action": "created",
    "field_name": "tarefa_completa",
    "new_value": "Tarefa criada: Estudar React"
}
```

### **Cenário 2: Atualizar Status**
```bash
PUT /todo/abc-123
{
    "status": "em_andamento"
}
```

**Histórico gerado:**
```json
{
    "action": "updated",
    "field_name": "status",
    "old_value": "pendente",
    "new_value": "em_andamento"
}
```

### **Cenário 3: Atualizar Múltiplos Campos**
```bash
PUT /todo/abc-123
{
    "title": "Estudar React Hooks",
    "description": "Aprender useState e useEffect",
    "status": "concluída"
}
```

**Histórico gerado:**
```json
[
    {
        "action": "updated",
        "field_name": "title",
        "old_value": "Estudar React",
        "new_value": "Estudar React Hooks"
    },
    {
        "action": "updated",
        "field_name": "description",
        "old_value": "Aprender hooks",
        "new_value": "Aprender useState e useEffect"
    },
    {
        "action": "updated",
        "field_name": "status",
        "old_value": "em_andamento",
        "new_value": "concluída"
    }
]
```

### **Cenário 4: Excluir Tarefa**
```bash
DELETE /todo/abc-123
```

**Histórico gerado:**
```json
{
    "action": "deleted",
    "field_name": "tarefa_completa",
    "old_value": "Tarefa: Estudar React Hooks",
    "new_value": null
}
```

## �� Configuração

### 1. **Executar Migração**
```bash
python migrate_database.py
```

### 2. **Verificar Tabela Criada**
```sql
SELECT name FROM sqlite_master WHERE type='table' AND name='todo_history';
```

## 💡 Benefícios

1. **Auditoria Completa**: Rastreia todas as mudanças
2. **Debugging**: Facilita identificar problemas
3. **Análise de Produtividade**: Mostra padrões de uso
4. **Recuperação**: Permite entender o que foi alterado
5. **Compliance**: Atende requisitos de auditoria

## �� Casos de Uso

- **Gestores**: Acompanhar progresso da equipe
- **Usuários**: Ver histórico de suas atividades
- **Suporte**: Investigar problemas reportados
- **Análise**: Estatísticas de uso do sistema

## Como Testar o Sistema de Histórico:

1. **Execute a migração:**
```bash
python migrate_database.py
```

2. **Crie uma tarefa:**
```bash
POST /todo/
{
    "title": "Teste Histórico",
    "description": "Testando o sistema",
    "status": "pendente",
    "activity_type": "interno",
    "city": "São Paulo"
}
```

3. **Verifique o histórico:**
```bash
GET /todo/{todo_id}/historico
```

4. **Atualize a tarefa:**
```bash
PUT /todo/{todo_id}
{
    "status": "em_andamento"
}
```

5. **Verifique o histórico novamente:**
```bash
GET /todo/{todo_id}/historico
```

Agora o sistema de histórico está completo e funcionando! Quer que eu implemente mais alguma funcionalidade?
