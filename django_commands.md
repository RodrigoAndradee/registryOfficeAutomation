# Comandos para usar no DJango

### 🔧 Comandos gerais

| Comando              | Descrição                                                           |
| -------------------- | ------------------------------------------------------------------- |
| runserver            | Inicia o servidor de desenvolvimento (127.0.0.1:8000)               |
| migrate              | Aplica as migrações pendentes ao banco de dados                     |
| makemigrations       | Cria novas migrações a partir das alterações no modelo              |
| createsuperuser      | Cria um superusuário para acessar o admin                           |
| shell                | Abre um shell interativo (IPython se instalado)                     |
| check                | Verifica se há problemas de configuração no projeto                 |
| startapp \<nome>     | Cria uma nova aplicação Django                                      |
| startproject \<nome> | Cria um novo projeto Django (geralmente feito fora do manage.py)    |
| collectstatic        | Coleta todos os arquivos estáticos para o diretório STATIC_ROOT     |
| flush                | Apaga todos os dados do banco e reinicializa como após as migrações |
| loaddata \<fixture>  | Carrega dados a partir de arquivos JSON, XML, YAML                  |
| dumpdata             | Exporta os dados do banco como JSON (útil para backups ou fixtures) |

### 🧪 Testes e depuração

| Comando                           | Descrição                                                            |
| --------------------------------- | -------------------------------------------------------------------- |
| test                              | Roda os testes automatizados                                         |
| test \<app>                       | Roda os testes de uma app específica                                 |
| dbshell                           | Abre um shell para o banco de dados configurado                      |
| showmigrations                    | Mostra as migrações aplicadas e pendentes                            |
| sqlmigrate \<app> <nome_migração> | Mostra o SQL que será executado por uma migração                     |
| diffsettings                      | Mostra as diferenças entre suas configurações e as padrões do Django |
