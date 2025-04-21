import argparse
import csv
import logging
import requests
import sys
import time
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cas_processor.log"), logging.StreamHandler()]
)

def compute_check_digit(part1: int, part2: int) -> int:
    try:
        combined = f"{part1}{part2:02d}"
        digits = list(map(int, combined))
        total = sum(d * (i + 1) for i, d in enumerate(reversed(digits)))
        return total % 10
    except Exception as e:
        logging.error(f"Error computing check digit for {part1}-{part2}: {str(e)}")
        raise

def generate_cas_numbers(start: int, end: int, output_file: str):
    try:
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["CAS Number"])
            
            for part1 in tqdm(range(start, end + 1), desc="Generating CAS"):
                for part2 in range(0, 100):
                    try:
                        check_digit = compute_check_digit(part1, part2)
                        cas_number = f"{part1}-{part2:02d}-{check_digit}"
                        writer.writerow([cas_number])
                    except:
                        continue
        logging.info(f"Generated CAS numbers from {start} to {end} in {output_file}")
    except Exception as e:
        logging.error(f"Generation failed: {str(e)}")
        sys.exit(1)

def verify_cas_numbers(input_file: str, output_file: str, delay: float, batch_size: int):
    def check_single(cas):
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cas/{cas}/cids/JSON"
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "CAS Validator/1.0"},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logging.warning(f"Error checking {cas}: {str(e)}")
            return False

    def check_batch(batch):
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cas/cids/JSON"
        try:
            response = requests.post(
                url,
                data={"cas": "\n".join(batch)},
                headers={"User-Agent": "CAS Validator/1.0"},
                timeout=15
            )
            if response.status_code == 200:
                return set(response.json()["IdentifierList"]["CID"])
            return set()
        except Exception as e:
            logging.warning(f"Batch error: {str(e)}")
            return set()

    try:
        with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            next(reader)  # Skip header
            writer.writerow(["CAS Number", "IsValid", "Timestamp"])
            
            cas_list = [row[0] for row in reader]
            total = len(cas_list)
            
            with tqdm(total=total, desc="Verifying CAS") as pbar:
                if batch_size > 1:
                    for i in range(0, total, batch_size):
                        batch = cas_list[i:i + batch_size]
                        valid_cids = check_batch(batch)
                        
                        for cas in batch:
                            writer.writerow([cas, cas in valid_cids, time.strftime("%Y-%m-%d %H:%M:%S")])
                        
                        pbar.update(len(batch))
                        time.sleep(delay)
                else:
                    for cas in cas_list:
                        isValid = check_single(cas)
                        writer.writerow([cas, isValid, time.strftime("%Y-%m-%d %H:%M:%S")])
                        pbar.update(1)
                        time.sleep(delay)
                        
        logging.info(f"Verification completed. Results saved to {output_file}")
    
    except Exception as e:
        logging.error(f"Verification failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CAS Number Processor")
    subparsers = parser.add_subparsers(dest="command")
    
    # Парсер для генерации
    gen_parser = subparsers.add_parser("generate", help="Generate CAS numbers")
    gen_parser.add_argument("-s", "--start", type=int, default=1, help="Start range")
    gen_parser.add_argument("-e", "--end", type=int, required=True, help="End range")
    gen_parser.add_argument("-o", "--output", default="cas_db.csv", help="Output file")
    
    # Парсер для проверки
    verify_parser = subparsers.add_parser("verify", help="Verify CAS numbers")
    verify_parser.add_argument("-i", "--input", required=True, help="Input file")
    verify_parser.add_argument("-o", "--output", default="verified_cas.csv", help="Output file")
    verify_parser.add_argument("-d", "--delay", type=float, default=0.2, 
                             help="Delay between requests (seconds)")
    verify_parser.add_argument("-b", "--batch", type=int, default=1,
                             help="Batch size for POST requests (1-100)")
    
    args = parser.parse_args()
    
    try:
        if args.command == "generate":
            if args.start < 1 or args.end < args.start:
                raise ValueError("Invalid range parameters")
            generate_cas_numbers(args.start, args.end, args.output)
            
        elif args.command == "verify":
            if args.batch < 1 or args.batch > 100:
                raise ValueError("Batch size must be between 1 and 100")
            verify_cas_numbers(args.input, args.output, args.delay, args.batch)
            
        else:
            parser.print_help()
            
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)