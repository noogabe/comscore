from comscore import Comscore
from sharepoint import SharePoint

def main():

    comscore = Comscore()
    filename = comscore.generate_csv()

    if filename:

        sharepoint = SharePoint()
        sharepoint.upload_file(
            filename
        )

if __name__ == "__main__":
    main()