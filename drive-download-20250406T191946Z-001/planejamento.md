# Plano de Implementação Corrigido

## Passo 1: Adicionar o campo responsible_name ao modelo Account

1. Edite o arquivo `apps/accounts/models.py` para adicionar o campo `responsible_name`:
   ```python
   # Adicionar o campo
   responsible_name = models.CharField(_("Responsável"), max_length=100, blank=True, null=True)
   
   # Modificar o default para issue_date
   issue_date = models.DateField(_("Data de Emissão"), default=timezone.now)
   
   # Tornar description opcional
   description = models.CharField(_("Descrição"), max_length=255, blank=True)
   ```

2. Execute a migração:
   ```
   python manage.py makemigrations accounts --name 'add_responsible_name_field'
   python manage.py migrate
   ```

## Passo 2: Migrar os dados do campo responsible para responsible_name

1. Salve o arquivo `migrate_responsible_data.py` na raiz do seu projeto com o conteúdo fornecido
2. Execute o script diretamente:
   ```
   python migrate_responsible_data.py
   ```

## Passo 3: Atualizar os formulários e templates

1. Atualize o arquivo `apps/accounts/forms.py` para usar o novo campo `responsible_name` e implementar as melhorias de usabilidade
2. Atualize o template `templates/accounts/form.html` para exibir o novo campo e adicionar o datalist e formatação do valor original
3. Atualize o template `templates/accounts/detail.html` para exibir o novo campo `responsible_name`
4. Atualize a view de lista para filtrar pelo novo campo `responsible_name`

## Passo 4: Tornar o campo responsible opcional (para compatibilidade com registros existentes)

1. Edite novamente o arquivo `apps/accounts/models.py` para tornar o campo `responsible` opcional:
   ```python
   responsible = models.ForeignKey(
       User,
       verbose_name=_("Responsável (Antigo)"),
       on_delete=models.PROTECT,
       related_name='accounts',
       null=True,
       blank=True
   )
   ```

2. Execute a migração:
   ```
   python manage.py makemigrations accounts --name 'make_responsible_optional'
   python manage.py migrate
   ```

## Passo 5: Atualizar serviços e views para usar o novo campo

1. Atualize o arquivo `apps/accounts/services.py` para usar o campo `responsible_name` ao gerar parcelas recorrentes
2. Certifique-se que o arquivo `apps/accounts/views.py` inclui todas as funções necessárias, incluindo as relacionadas a pagamentos e recebimentos

## Passo 6 (Futuro): Remover o campo responsible quando não for mais necessário

Após todos os ajustes e garantir que o sistema está funcionando corretamente, você pode remover o campo `responsible` criando uma nova migração.