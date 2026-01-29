import boto3
from botocore.exceptions import ClientError

GRUPO = "imat3a13"
CRYPTO = "aave"

DATABASE_NAME = f"trade_data_{GRUPO}"
CRAWLER_NAME = f"crawler_{CRYPTO}_{GRUPO}"

S3_PATH = "s3://mi-bucket-datos-aave-2026/"
IAM_ROLE = "AWSGlueServiceRoleDefault"

TABLE_PREFIX = f"{CRYPTO}_"

glue = boto3.client("glue")   #me meto al cliente

#Creo base datos
def create_database():
    try:
        glue.create_database(
            DatabaseInput={
                "Name": DATABASE_NAME,
                "Description": "Datos históricos de cripto Aave"
            }
        )
        print(f"Base de datos creada: {DATABASE_NAME}")
    except glue.exceptions.AlreadyExistsException:
        print(f"La base de datos ya existe: {DATABASE_NAME}")

#Crear Crawler
def create_crawler():
    try:
        glue.create_crawler(
            Name=CRAWLER_NAME,
            Role=IAM_ROLE,
            DatabaseName=DATABASE_NAME,
            Targets={
                "S3Targets": [
                    {"Path": S3_PATH}
                ]
            },
            TablePrefix=TABLE_PREFIX,
            SchemaChangePolicy={   #Me lo ha dado Chat por si cambiara la estructura del S3
                "UpdateBehavior": "UPDATE_IN_DATABASE",
                "DeleteBehavior": "LOG"
            }
        )
        print(f"Crawler creado: {CRAWLER_NAME}")
    except glue.exceptions.AlreadyExistsException:
        print(f"El crawler ya existe: {CRAWLER_NAME}")

#EJECUTAR CRAWLER
def run_crawler():
    try:
        glue.start_crawler(Name=CRAWLER_NAME)
        print(f"Crawler ejecutándose: {CRAWLER_NAME}")
    except ClientError as e:
        if "CrawlerRunningException" in str(e):
            print("El crawler ya está en ejecución")
        else:
            raise e

#MAIN
if __name__ == "__main__":
    create_database()
    create_crawler()
    run_crawler()
