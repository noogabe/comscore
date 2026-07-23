import json
import time
from pathlib import Path

import pandas as pd
import requests

from constants import (
    ComScore,
    DataSource,
    GEO,
    Measure,
    MediaSet,
    MediaSetType,
    Target,
    TargetType,
    TimePeriod,
    TimeType,
)

from media import Media


class Comscore:
    PRODUCT = "mmx"
    REPORT = "keymeasures"

    def __init__(self):
        self.base_url = ComScore.URL_BASE
        self.headers = ComScore.HEADER
        self.output_dir = Path("files")
        self.output_dir.mkdir(exist_ok=True)


    def _key_measures(self, period=None):

        body = {
            "Parameter": []
        }

        body["Parameter"].append(
            ComScore.parameter(DataSource.KEY, DataSource.MULTI_PLATFORM)
        )

        body["Parameter"].append(
            ComScore.parameter(TargetType.KEY, TargetType.SIMPLE)
        )

        body["Parameter"].append(
            ComScore.parameter(GEO.KEY, GEO.BRAZIL)
        )

        body["Parameter"].append(
            ComScore.parameter(TimeType.KEY, TimeType.MONTHS)
        )

        body["Parameter"].append(
            ComScore.parameter(MediaSetType.KEY, MediaSetType.SAVED_MEDIA_LISTS)
        )

        body["Parameter"].append(
            ComScore.parameter(MediaSet.KEY, MediaSet.RANKING_PORTAIS)
        )

        medias = [
            Media.DIARIO_DO_NORDESTE,

            Media.DIARIO_DO_NORDESTE_HOMEPAGE,
            Media.DIARIO_DO_NORDESTE_EDITORIAS,
            Media.DIARIO_DO_NORDESTE_PONTO_PODER,
            Media.DIARIO_DO_NORDESTE_CEARA,
            Media.DIARIO_DO_NORDESTE_CEARA_2,
            Media.DIARIO_DO_NORDESTE_CULINARIA,
            Media.DIARIO_DO_NORDESTE_E_HIT,
            Media.DIARIO_DO_NORDESTE_JOGADA,
            Media.DIARIO_DO_NORDESTE_MEIO_AMBIENTE,
            Media.DIARIO_DO_NORDESTE_METRO,
            Media.DIARIO_DO_NORDESTE_NEGOCIOS,
            Media.DIARIO_DO_NORDESTE_OPINIAO,
            Media.DIARIO_DO_NORDESTE_PAPO_CARREIRA,
            Media.DIARIO_DO_NORDESTE_REGIAO,
            Media.DIARIO_DO_NORDESTE_SEGURANCA,
            Media.DIARIO_DO_NORDESTE_SER_SAUDE,
            Media.DIARIO_DO_NORDESTE_ULTIMA_HORA,
            Media.DIARIO_DO_NORDESTE_VERSO,
            Media.DIARIO_DO_NORDESTE_ZOEIRA,

            Media.G1_CEARA,

            Media.TOTAL_INTERNET,

            Media.ABRIL_VEJA,
            Media.AGAZETA_COM_BR,
            Media.BBC_BRASIL,
            Media.CATRACALIVRE_COM_BR,
            Media.CNN_BRASIL_COM_BR,
            Media.CORREIOBRAZILIENSE_COM_BR,
            Media.ESTADAO,
            Media.FOLHA_DE_S_PAULO,

            Media.GAZETADOPOVO_COM_BR,
            Media.GCMAIS_COM_BR,
            Media.GZH,
            Media.JORNAL_EXTRA,
            Media.JORNAL_O_GLOBO,
            Media.JOVEMPAN_COM_BR,
            Media.METROPOLES_COM,
            Media.NE10,
            Media.OPOPULAR_COM_BR,

            Media.OPOVO_COM_BR,
            Media.OTEMPO_COM_BR,
            Media.PODER360_COM_BR,
            Media.VALOR_ECONOMICO,

            Media.NSCTOTAL_COM_BR,
            Media.DIARIODEPERNAMBUCO_COM_BR,
            Media.G1_BAHIA,
            Media.G1_PERNAMBUCO,
            Media.A_TARDE,
            Media.TRIBUNADONORTE_COM_BR,

            Media.IMIRANTE,
            Media.LIBERAL_COM_BR,
            Media.ACRITICA_COM,
            Media.EXAME_COM,
            Media.JC_ONLINE,
            Media.D24AM_COM,

            Media.CORREIO_24_HORAS_OLD,
            Media.CORREIO_24_HORAS,
            Media.EM_COM_BR,
        ]

        for media in medias:
            body["Parameter"].append(
                ComScore.parameter(Media.KEY, media)
            )

        measures = [
            Measure.TOTAL_UNIQUE_VISITORS_VIEWERS_TOTAL_POPULATION,

            Measure.TOTAL_DIGITAL_POPULATION_IXI,
            Measure.TOTAL_DIGITAL_POPULATION_IXII,
            Measure.TOTAL_DIGITAL_POPULATION_IXIII,
            Measure.TOTAL_DIGITAL_POPULATION_IXIIII,
            Measure.TOTAL_DIGITAL_POPULATION_IXIIIII,
            Measure.TOTAL_DIGITAL_POPULATION_IXIIIIII,

            Measure.REACH_TOTAL_POPULATION,
            Measure.TOTAL_VIEWS_TOTAL_POPULATION,
            Measure.TOTAL_VISITS_TOTAL_POPULATION,
            Measure.PAGE_VIEWS_TOTAL_POPULATION,
            Measure.TOTAL_MINUTES_TOTAL_POPULATION,
            Measure.AVERAGE_MINUTES_PER_VISITOR_TOTAL_POPULATION,
        ]


        for measure in measures:
            body["Parameter"].append(
                ComScore.parameter(Measure.KEY, measure)
            )

        body["Parameter"].append(
            ComScore.parameter(Target.KEY, Target.BRAZIL)
        )

        if period:
            body["Parameter"].append(
                ComScore.parameter(TimePeriod.KEY, period)
            )

        return body


    def get_period(self):

        body = self._key_measures()

        url = (
            f"{self.base_url}"
            f"{self.PRODUCT}/"
            f"{self.REPORT}/"
            "DiscoverParameterValues/timePeriod"
        )

        response = requests.post(
            url,
            json=body,
            headers=self.headers
        )

        try:
            data = response.json()

            periods = {}

            for item in data["EnumValue"]:
                periods[item["Id"]] = item["Value"]

            return periods

        except Exception:
            return {
                "error": "Não foi possível buscar períodos da Comscore",
                "response": response.text
            }

    def create_job(self, period):

        body = self._key_measures(period)

        url = (
            f"{self.base_url}"
            f"{self.PRODUCT}/"
            f"{self.REPORT}/"
            "Report"
        )

        response = requests.post(
            url,
            json=body,
            headers=self.headers
        )

        try:
            data = response.json()

            job_id = data.get("JobId")

            if not job_id:
                return {
                    "error": "Comscore não retornou JobId",
                    "response": data
                }

            return {
                "job_id": job_id
            }

        except Exception:
            return {
                "error": "Erro ao criar Job na Comscore",
                "response": response.text
            }


    def wait_job(self, job_id):

        url = (
            f"{self.base_url}"
            f"{self.PRODUCT}/"
            f"{self.REPORT}/"
            f"Report/{job_id}"
        )

        while True:

            response = requests.get(
                url,
                headers=self.headers
            )

            try:
                data = response.json()

            except Exception:
                return {
                    "error": "Erro ao consultar Job da Comscore",
                    "response": response.text
                }

            status = data.get("Status")

            if status == 0:
                print("Comscore na fila...")
                time.sleep(3)
                continue

            if status == 1:
                print("Comscore processando...")
                time.sleep(3)
                continue

            if status == 2:
                print("Comscore finalizado!")
                return data

            return {
                "error": "Job retornou status inesperado",
                "status": status,
                "response": data
            }

    def build_dataframe(self, response):
        dataF = []

        table = response["REPORT"]["TABLE"][0]

        for row in table["THEAD"] + table["TBODY"]:
            dataRow = []

            for th in row["TH"]:
                dataRow.append(th["Value"])

            for td in row["TD"]:
                dataRow.append(td["Value"])

            dataF.append(dataRow)

        return pd.DataFrame(dataF)
    
    def get_file_period(self, period_name):

        months = {
            "janeiro": "01",
            "jan": "01",
            "january": "01",

            "fevereiro": "02",
            "fev": "02",
            "february": "02",

            "março": "03",
            "mar": "03",
            "march": "03",

            "abril": "04",
            "abr": "04",
            "april": "04",

            "maio": "05",
            "mai": "05",
            "may": "05",

            "junho": "06",
            "jun": "06",
            "june": "06",

            "julho": "07",
            "jul": "07",
            "july": "07",

            "agosto": "08",
            "ago": "08",
            "august": "08",

            "setembro": "09",
            "set": "09",
            "september": "09",

            "outubro": "10",
            "out": "10",
            "october": "10",

            "novembro": "11",
            "nov": "11",
            "november": "11",

            "dezembro": "12",
            "dez": "12",
            "december": "12",
        }

        value = period_name.lower()

        month = None

        for name, number in months.items():
            if name in value:
                month = number
                break

        year = None

        for part in period_name.split():
            if part.isdigit() and len(part) == 4:
                year = part
                break

        if not year or not month:
            raise Exception(
                f"Período inválido retornado pela Comscore: {period_name}"
            )

        return f"{year}.{month}"

    def save_csv(self, dataframe, period_name):

        file_period = self.get_file_period(period_name)

        filename = f"files/{file_period}.csv"

        dataframe.insert(
            loc=0,
            column="Month",
            value=period_name
        )

        dataframe.to_csv(
            filename,
            encoding="utf-8"
        )

        print(f"Arquivo salvo: {filename}")

        return filename

    def generate_csv(self):
        print("Buscando períodos da Comscore...")
        periods = self.get_period()

        if "error" in periods:
            print(periods)
            return None

        for period_id, period_name in periods.items():

            year = int(period_name.split()[-1])

            if year < 2026:
                continue

            file_period = self.get_file_period(period_name)
            filename = self.output_dir / f"{file_period}.csv"

            if filename.exists():
                print(f"{filename.name} já existe. Pulando...")
                continue

            print(f"Gerando dados do período: {period_name}")

            job = self.create_job(period_id)

            if "error" in job:
                print(job)
                return None

            response = self.wait_job(job["job_id"])

            if "error" in response:
                print(response)
                return None

            dataframe = self.build_dataframe(response)

            if dataframe.empty:
                print("Nenhum dado retornado.")
                return None

            self.save_csv(dataframe, period_name)

            return filename

        print("Todos os arquivos a partir de 2026 já foram gerados.")
        return None