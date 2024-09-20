import instaloader
import pytz  # Importa a biblioteca para ajustar o fuso horário
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import time
import colorama
from colorama import Fore, Back, Style

# Inicializa o instaloader
L = instaloader.Instaloader()

# Inicializa o colorama (necessário no Windows)
colorama.init(autoreset=True)

# Faça login
L.login('usuario_instagram', 'senha_instagram')

def verificar_stories(usuario):
    """Verifica se a conta do Instagram especificada postou algum story."""
    perfil = instaloader.Profile.from_username(L.context, usuario)
    stories = L.get_stories(userids=[perfil.userid])
    
    for story in stories:
        for item in story.get_items():
            utc_time = item.date_utc
            fuso_horario_sao_paulo = pytz.timezone('America/Sao_Paulo')

            if utc_time.tzinfo is None:
                # Caso não tenha informações sobre o fuso horário, adiciona o fuso horário UTC
                utc_time = pytz.utc.localize(utc_time)

            # Converte o horário UTC para o fuso horário local (UTC-3)
            local_time = utc_time.astimezone(fuso_horario_sao_paulo)
            hora_postada = local_time.strftime('%H:%M:%S')

            # Verifica se o horário é diferente da ultima hora de stories postado para ter um destaque
            if hora_postada != '00:00:00':
                # Exibe o horário ajustado e colorido em verde
                print( Fore.GREEN + f"Novo Story encontrado de {usuario} - Postado em " + f"{hora_postada}")
            else:
                # Exibe o horário ajustado e colorido em vermelho
                print(f"Novo Story encontrado de {usuario} - Postado em " + Fore.RED + f"{hora_postada}")
            
            return True  # Retorna True se encontrar stories
    return False  # Nenhum story encontrado

def monitorar_instagram():
    """Monitora a conta do Instagram e envia notificações se houver novos stories."""
    while True:
        usuario = 'conta_a_ser_monitorada'
        print(f"Monitorando stories...")

        if verificar_stories(usuario):
            assunto = 'Novo Story no Instagram!'
            mensagem = f'O usuário {usuario} postou um novo story!'
            
            # Envia notificações

if __name__ == "__main__":
    monitorar_instagram()
