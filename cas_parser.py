import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import time
from io import BytesIO, StringIO
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("cas_parser.log"),
        logging.StreamHandler()
    ]
)

class CASParser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.delay = 2

    def normalize_cas(self, cas):
        """Приведение CAS номеров к стандартному формату"""
        try:
            if pd.isna(cas):
                return None
                
            cas = str(cas).strip()
            cas = re.sub(r'[^0-9\-]', '', cas)
            
            if not re.match(r'^\d{1,7}-\d{2}-\d$', cas):
                nums = re.findall(r'\d', cas)
                if len(nums) < 4:
                    return None
                    
                part1 = ''.join(nums[:-3])
                part2 = ''.join(nums[-3:-1])
                check = nums[-1]
                cas = f"{part1}-{part2}-{check}"
                
            return cas
        except Exception as e:
            logging.error(f"Ошибка нормализации CAS {cas}: {str(e)}")
            return None

    def download_file(self, url):
        """Загрузка файлов"""
        try:
            time.sleep(self.delay)
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return BytesIO(response.content)
        except Exception as e:
            logging.error(f"Ошибка загрузки файла {url}: {str(e)}")
            return None

    def parse_cdc(self):
        """Парсинг CDC NIOSH"""
        url = "https://www.cdc.gov/niosh/nmam/method-cas1.html"
        try:
            logging.info("Парсинг CDC NIOSH...")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            
            if not table:
                raise ValueError("Таблица не найдена")
                
            # Исправленное чтение таблицы
            df = pd.read_html(StringIO(str(table)))[0]
            
            # Автоматический поиск колонки с CAS
            cas_col = None
            for col in df.columns:
                if 'cas' in str(col).lower():
                    cas_col = col
                    break
                    
            if not cas_col:
                raise ValueError("Колонка с CAS не найдена")
                
            df = df[[cas_col]].rename(columns={cas_col: "CAS"})
            df["Source"] = "CDC NIOSH"
            return df
            
        except Exception as e:
            logging.error(f"Ошибка парсинга CDC: {str(e)}")
            return pd.DataFrame()

    def parse_wikipedia(self):
        """Парсинг Википедии"""
        url = "https://en.wikipedia.org/wiki/List_of_CAS_numbers_by_chemical_compound"
        try:
            logging.info("Парсинг Wikipedia...")
            # Исправление для html5lib
            tables = pd.read_html(url, flavor='html5lib')
            
            for table in tables:
                if "CAS Number" in table.columns:
                    df = table[["Compound", "CAS Number"]]
                    df["Source"] = "Wikipedia"
                    return df.rename(columns={"CAS Number": "CAS"})
                    
            raise ValueError("Таблица с CAS не найдена")
            
        except Exception as e:
            logging.error(f"Ошибка парсинга Wikipedia: {str(e)}")
            return pd.DataFrame()

    def parse_nih(self):
        """Парсинг NIEHS Excel"""
        url = "https://ntp.niehs.nih.gov/sites/default/files/ntp/roc/content/roc15_casrn_index.xlsx"
        try:
            logging.info("Парсинг NIEHS Excel...")
            file = self.download_file(url)
            if not file:
                return pd.DataFrame()
                
            # Автоматическое определение листа
            df = pd.read_excel(file, sheet_name=None)
            sheet_name = list(df.keys())[0]
            df = pd.read_excel(file, sheet_name=sheet_name)
            
            # Поиск колонки с CAS
            cas_col = next((col for col in df.columns if 'cas' in str(col).lower()), None)
            if not cas_col:
                raise ValueError("Колонка CAS не найдена")
                
            df = df[[cas_col]].rename(columns={cas_col: "CAS"})
            df["Source"] = "NIEHS"
            return df
            
        except Exception as e:
            logging.error(f"Ошибка парсинга NIEHS: {str(e)}")
            return pd.DataFrame()

    def parse_epa(self):
        """Парсинг EPA Excel"""
        url = "https://www.epa.gov/system/files/documents/2022-12/"\
              "Microsoft%20Excel%20Version%20of%20EPCRA%20CERCLA%20CAA%20112%28r%29%20"\
              "Consolidated%20List%20of%20Lists_December%202022.xlsx"
        try:
            logging.info("Парсинг EPA Excel...")
            file = self.download_file(url)
            if not file:
                return pd.DataFrame()
                
            # Чтение первого листа
            df = pd.read_excel(file, sheet_name=0)
            
            # Поиск колонки с CAS
            cas_col = next((col for col in df.columns if 'cas' in str(col).lower()), None)
            if not cas_col:
                raise ValueError("Колонка CAS не найдена")
                
            df = df[[cas_col]].rename(columns={cas_col: "CAS"})
            df["Source"] = "EPA"
            return df
            
        except Exception as e:
            logging.error(f"Ошибка парсинга EPA: {str(e)}")
            return pd.DataFrame()

    def run(self):
        """Основной метод"""
        sources = [
            self.parse_cdc(),
            self.parse_wikipedia(),
            self.parse_nih(),
            self.parse_epa()
        ]
        
        combined = pd.concat(sources, ignore_index=True)
        
        if not combined.empty:
            combined["CAS"] = combined["CAS"].apply(self.normalize_cas)
            combined = combined.dropna(subset=["CAS"])
            combined = combined.drop_duplicates(subset=["CAS"])
            combined["IsValid"] = combined["CAS"].apply(self.validate_cas)
            combined.to_csv("cas_database.csv", index=False)
            logging.info(f"Найдено {len(combined)} CAS номеров.")
        else:
            logging.error("Не удалось получить данные ни из одного источника")

    def validate_cas(self, cas):
        """Проверка контрольной суммы"""
        try:
            parts = cas.split("-")
            if len(parts) != 3:
                return False
                
            digits = list(parts[0] + parts[1])
            check_digit = int(parts[2])
            
            total = sum(int(d) * (i + 1) for i, d in enumerate(reversed(digits)))
            return total % 10 == check_digit
            
        except:
            return False

if __name__ == "__main__":
    parser = CASParser()
    parser.run()