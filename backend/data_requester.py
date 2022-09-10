from time import sleep
from sqlalchemy.orm import Session
import httplib2
import apiclient.discovery
import datetime
import requests
from oauth2client.service_account import ServiceAccountCredentials
from data.db import SessionLocal
from data.models import Order
import xml.etree.ElementTree as ET


def request_for_ruble_cource():
    session = requests.Session()
    link = "http://www.cbr.ru/scripts/XML_daily.asp"
    with session.get(link) as response:
        root = ET.fromstring(response.content)
        for valute in root.iter('Valute'):
            if valute.find('CharCode').text == 'USD':
                cource = valute.find('Value').text
                return float(cource.replace(',', '.'))
    return None


def main():
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'credentials.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = '1wsX3FEh_Ae50aJhrHH39x9RaPYpbCJ9epZRHjcWnSyc'

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    # чтение файла
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:E',
        majorDimension='ROWS'
    ).execute()
    
    db: Session = SessionLocal()
    all_orders = db.query(Order).all()
    orders_ids = [order.order_id for order in all_orders]
    
    '''Request for CBRF'''
    ruble_cource = request_for_ruble_cource()
    for value in values["values"][1:]:
        order_db = db.query(Order).filter(Order.order_id == value[1]).first()
        delivery_date = datetime.datetime.strptime(value[3], '%d.%m.%Y')
        if order_db is not None:
            '''Update'''
            order_db.number = value[0]
            order_db.price_usd = value[2]
            order_db.delivery_time = delivery_date
            try:
                orders_ids.remove(int(value[1]))
            except ValueError:
                pass
        else:
            '''Create'''
            order_db = Order(
                number = value[0],
                order_id = value[1],
                price_usd = value[2],
                delivery_time = delivery_date,
            )
            db.add(order_db)
        if ruble_cource is not None:
            order_db.price_rub = int(float(order_db.price_usd) * ruble_cource)
    if len(orders_ids)>0:
        for order in orders_ids:
            order_db = db.query(Order).filter(Order.order_id == order).first()
            if order_db is not None:
                db.delete(order_db)
    db.commit()
    db.close()
            
if __name__ == '__main__':
    while True:
        main()
        sleep(5)