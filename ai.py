from openai import OpenAI

#Insira sua chave de api da openai
key_openai = ''

client = OpenAI(
    api_key = key_openai
)

# Função para ler o conteúdo de um arquivo
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Caminho para o arquivo .txt com o system (personalidade) do bot
file_path = 'system.txt'

# Leia o conteúdo do arquivo
system_message = read_file(file_path)

def responde(msg):
    try:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_message
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": msg
                }
            ]
            }
        ],
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.2
        )
        resposta = response.choices[0].message.content
        return (resposta)
    except Exception as e:
        return (e)
