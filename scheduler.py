from apscheduler.schedulers.blocking import BlockingScheduler

from comscore import Comscore
from sharepoint import SharePoint
from datetime import datetime


def execute():

    print("=" * 80)
    print(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] Iniciando rotina Comscore")

    try:
        comscore = Comscore()
        filename = comscore.generate_csv()

        if filename:
            print(f"Arquivo gerado: {filename}")

            sharepoint = SharePoint()
            print("Enviando arquivo para o SharePoint...")
            sharepoint.upload_file(filename)
            print("Upload concluído com sucesso.")

        else:
            print("Nenhum arquivo novo para enviar.")
    
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        raise

    finally:
        print(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] Rotina finalizada")
        print("=" * 80)


scheduler = BlockingScheduler(timezone="America/Sao_Paulo")

scheduler.add_job(
    execute,
    "cron",
    day="21-25",
    hour="8,15",
    minute=30,
)