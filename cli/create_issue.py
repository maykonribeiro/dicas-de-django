import click
import requests
from decouple import config


## como executar esse codigo
'''
# https//docs.github.com/en/rest/reference/issues#create-an-issue

python clin/create_issue.py \
--title='' \
--body='' \
--labels='feature'
'''

# O repositório para adicionar a issue
REPO_OWNER = config('REPO_OWNER')
REPO_NAME = config('REPO_NAME')
TOKEN = config('TOKEN')


# criando a função para escrever o texto no arquivo
def write_file(filename, number, title, description, labels):
    labels = ', '.join(labels).strip()
    with open(filename, 'a') as f:
        f.write(f'\n---\n\n')
        f.write(f'[] {number} - {title}\n')
        f.write(f'   {labels}\n\n')

        if description:
            f.write(f'    {description}')

        f.write(f"    make lint; git add . ; git commit -m '{title}. close #{number}'; git push\n")

@click.command()
@click.option('--title', prompt='Title', help='Digite o titulo')
@click.option('--body', prompt='Description', help='Digite a descrição')
@click.option('--assignee', prompt='Assignee', help='Digite o nome da pessoa a ser associada')
@click.option('--labels', prompt='Labels', help='Digite as labels')

def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    '''
        Cria issue no github.com
    '''
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
    headers = {
        "Authorization": f"token {TOKEN}"
    }
    labels = labels.split(',')

    # cria a issue
    issue = {
        "title": title,
        "body": body,
        "labels": labels 
    }

    if assignee:
        issue['assignees'] = [assignee]

    # adiciona a issue no repositorio
    req = requests.post(url, headers=headers, json=issue)    

    if req.status.code == 201:
        print(f'Issue criada com sucesso "{title}"')
        number = req.json()['number']
        description = body

        filename = 'C:\\Users\\2107031\\Documents\\ordem-de-servico\\tarefas.txt'
        write_file(filename, number, title, description, labels)

    else:
        print(f'nao foi possivel criar a issue "{title}"')



