from typing import Any, Dict, List
import requests
from requests import HTTPError, RequestException
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import os
import shutil
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values
from redmail import EmailSender

try:
    from pycomunefirenze.working_dir import WorkingDir
except ModuleNotFoundError:
    from working_dir import WorkingDir

proxies = {
    "http": "http://proxyhttp.comune.intranet:8080",
    "https": "http://proxyhttp.comune.intranet:8080",
}


def general_request(method: str, url: str, retries=3, **kwargs) -> str:
    """Esegue una richiesta custom ad un url, utilizzando il metodo request
    Se ci sono errori nell'API, vengono fatti dei retry (default 3)

    Args:
        method (str): metodo (POST, GET, etc...)
        url (str): url da interrogare
        retries (int): default a 3, numero di retry da fare

    Raises:
        ConnectionError: Errore di rete
        HTTPError: Errore di protocollo HTTP (401, 404, 500, etc...)
        TimeoutError: Errore di timeout
        RequestException: Errore generale

    Returns:
        str: contenuto della risposta
    """
    retries = retries
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=0.3,
        method_whitelist=False,
        raise_on_status=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    try:
        r = session.request(method, url, proxies=proxies, **kwargs)
        r.raise_for_status()
        logging.info("API called")
        return r.text
    except ConnectionError as exc:
        error_type = str(exc)
        logging.error(
            f"Netowork error (DNS, refused connection, etc) - {method} {url} {kwargs}"
        )
        raise Exception("Netowork error (DNS, refused connection, etc)")
    except HTTPError as exc:
        error_type = str(exc)
        logging.error(f"{r.status_code} {r.reason} - {method} {url} {kwargs}")
        raise Exception(f"{r.status_code} {r.reason}")
    except TimeoutError as exc:
        error_type = str(exc)
        logging.error(f"Timeout error from API - {method} {url} {kwargs}")
        raise Exception("Timeout error from API")
    except RequestException as exc:
        error_type = str(exc)
        logging.error(
            f"General error in getting data from API - {method} {url} {kwargs}"
        )
        raise Exception("General error in getting data from API")


def create_directory(directory_name: str) -> WorkingDir:
    """Crea la directory richiesta nella cartella di lavoro dello script

    Args:
        directory_name (str): Il nome della directory da creare

    Returns:
        path: Il path della directory creata
    """
    if directory_name is None or not directory_name:
        logging.error("Attempted to create directory with no name")
        raise SyntaxError("Attempted to create directory with no name")
    path = Path(rf"{directory_name}")
    logging.info(f"Trying to create {path}")
    os.mkdir(path)
    logging.info(f"Created {path}")
    return WorkingDir(directory_name)


def delete_directory(directory: WorkingDir) -> bool:
    """Cancella una directory precedentemente creata ed il suo contenuto

    Args:
        directory (WorkingDir): La directory di lavoro precedentemente creata
    """
    if not isinstance(directory, WorkingDir):
        logging.error(
            f"Trying to delete a directory that is NOT a previosly created working directory"
        )
        raise ValueError("Can't delete not WorkingDir directory")
    logging.info(f"Trying to delete {directory.path}")
    shutil.rmtree(directory.path, ignore_errors=True)
    logging.info(f"Deleted {directory.path}")
    return True


def __create_sql_query(table_name, data: List[Dict[str, Any]]) -> str:
    """Metodo private, che crea una query sql del tipo 'INSERT INTO [table_name] (col1, col2, etc...) VALUES (%(col1)s, %(col2)s, etc..)

    Args:
        table_name (str): nome della tabella in cui inserire i dati
        data (List[Dict[str,Any]]): dizionario contenente i dati da inserire in tabella

    Returns:
        str: query
    """
    if not isinstance(table_name, str):
        logging.error(
            f"The name of the table must be a string, and {table_name} is a {type(table_name)}"
        )
        raise ValueError(
            f"The name of the table must be a string, and {table_name} is a {type(table_name)}"
        )
    columns = ",".join(data[0].keys())
    return f"INSERT INTO {table_name} ({columns}) VALUES %s"


def insert_on_db(
    user: str,
    password: str,
    host: str,
    port: str,
    database: str,
    table_name: str,
    data: List[Dict[str, Any]],
    truncate=False,
) -> None:
    """Genera la connessione al db PGSQL specificato ed esegue la query.
    Lancia un'eccezione in caso di errori lato db.

    Args:
        user (str): username
        password (str): password
        host (str): hostname
        port (str): porta
        database (str): database
        table_name (str): nome della tabella in cui inserire i dati
        data (List[Dict[str,Any]]): lista di dizionari contenente i dati da inserire in tabella (un dizionario per riga)
        truncate (bool): default a False, parametro opzionale per decidere se fare la truncate o no della tabella

    Returns:
        None
    """
    connection = None
    try:
        connection = psycopg2.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        logging.info(f"Connected to {database} on {host}")
        cursor = connection.cursor()
        if truncate:
            cursor.execute(f"TRUNCATE {table_name}")
        values = [[value for value in row.values()] for row in data]
        execute_values(cursor, __create_sql_query(table_name, data), values)
        connection.commit()
        logging.info(f"Queries executed")
    except Exception as error:
        logging.error(error)
        raise error
    finally:
        if connection is not None:
            connection.close()


def send_email(
    subject: str, sender: str, receivers: List[str], text: str, **kwargs
) -> Any:
    """Manda una mail utilizzando il server mail interno

    Args:
        subject (str): oggetto della mail
        sender (str): mittente
        receivers (List[str]): lista di destinatari
        text (str): testo della mail
        **kwargs: argomenti opzionali, vedi https://pypi.org/project/redmail/

    Returns:
        EmailMessage: [description]
    """
    email = EmailSender(host="mailint.comune.intranet", port=25)
    return email.send(
        subject=subject, sender=sender, receivers=receivers, text=text, **kwargs
    )
