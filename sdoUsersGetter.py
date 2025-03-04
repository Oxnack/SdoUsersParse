from bs4 import BeautifulSoup
import re
import requests
from config import *
import csv
import os



def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    
    try:
        full_name = soup.find('h1', class_='h2 mb-0').get_text(strip=True)
    except AttributeError:
        print("no attribute")
        full_name = "error"

   
    try:
        email_link = soup.find('a', href=re.compile(r'mailto:'))
        if email_link:
            email = email_link.get_text(strip=True)
        else:
            raise AttributeError
    except AttributeError:
        print("no attribute for email")
        email = "error"

    return full_name, email




def fetch_html(course_id: int) -> str:
    url = f"https://sdo24.1580.ru/user/profile.php?id={course_id}"
    headers = {
        "Cookie": cookie
    }
    
    response = requests.get(url, headers=headers)
    
    try:
        if response.status_code == 200:
            return response.text
        else: 
            return "error"
    except Exception as e:
        return "error"





def save_to_csv(full_name: str, email: str, filename: str = 'data.csv'):
   
    file_exists = os.path.isfile(filename)

    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

       
        if not file_exists:
            writer.writerow(['Full Name', 'Email'])

       
        writer.writerow([full_name, email])


if __name__ == "__main__":
    course_number = 0 
    try:
        for i in range(6489, 1000000):
            course_number = i
            print(i, ". ")

            html_content = fetch_html(course_number)

            if(html_content == "error"):
                print("er Line")
            else:

                fio, email = extract_info(html_content)
                if (fio == "error" or fio == "Пользователь"):
                    print("fio err")
                    if (email == "error"):
                        print("all err")
                    else:
                        print(f"ФИО, gmail: \"{fio}\" , " + email + "---------------------[+]")

                        save_to_csv(fio, email)
                else:
                    print(f"ФИО, gmail: \"{fio}\" , " + email + "---------------------[+]")

                    save_to_csv(fio, email)
        
    except Exception as e:
        print(e)
#print(extract_info(fetch_html(8)))
