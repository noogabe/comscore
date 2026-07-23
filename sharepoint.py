import os
import requests

from msal import ConfidentialClientApplication
from dotenv import load_dotenv


load_dotenv()


class SharePoint:

    def __init__(self):

        self.tenant_id = os.getenv(
            "SHAREPOINT_TENANT_ID"
        )

        self.client_id = os.getenv(
            "SHAREPOINT_CLIENT_ID"
        )

        self.client_secret = os.getenv(
            "SHAREPOINT_CLIENT_SECRET"
        )

        self.drive_id = os.getenv(
            "SHAREPOINT_DRIVE_ID"
        )

        self.folder = os.getenv(
            "SHAREPOINT_FOLDER"
        )

        self.authority = (
            f"https://login.microsoftonline.com/"
            f"{self.tenant_id}"
        )

        self.scope = [
            "https://graph.microsoft.com/.default"
        ]


    def get_token(self):

        app = ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )


        response = app.acquire_token_for_client(
            scopes=self.scope
        )


        token = response.get(
            "access_token"
        )


        if not token:
            raise Exception(
                f"Erro ao gerar token SharePoint: {response}"
            )


        return token



    def upload_file(self, file_path):

        token = self.get_token()


        filename = os.path.basename(
            file_path
        )


        upload_url = (
            "https://graph.microsoft.com/v1.0/"
            f"drives/{self.drive_id}"
            f"/root:/{self.folder}/{filename}"
            ":/content"
        )


        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        }


        with open(
            file_path,
            "rb"
        ) as file:

            response = requests.put(
                upload_url,
                headers=headers,
                data=file
            )


        if response.status_code not in [
            200,
            201
        ]:
            raise Exception(
                "Erro ao enviar arquivo para SharePoint: "
                f"{response.text}"
            )


        print(
            f"Arquivo enviado para SharePoint: {filename}"
        )


        return response.json()