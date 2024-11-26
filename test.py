import os
import glob
import time
import sys
import requests
import random
import subprocess
from datetime import datetime

import numpy as np

SET = "FullTest"
LOCALE_CHEACK_FILE = "./vol/RUNNING.txt"#RESTART 완료되었는지 확인하기 위함 
LOCALE_COMPLETE_FILE = "./vol/Complete.txt"
LOCALE_SAVE = "./vol/"
LOCALE_RDF = "./vol/_RDF"
LOCALE_BACK = "./vol/_BACK"
HOSTNAME = "http://localhost:8080"
TEST_ROUTE_REPEAT = 10

RDF_ORI_LIST = [
    '2_2.rdf',
    '2_4.rdf',
    '2_8.rdf',
    '2_16.rdf',
    '2_32.rdf',
    '2_64.rdf',
    '2_128.rdf',
    '2_256.rdf',
    '4_2.rdf',
    '4_4.rdf',
    '4_8.rdf',
    '4_16.rdf',
    '4_32.rdf',
    '4_64.rdf',
    '4_128.rdf',
    '4_256.rdf',
    '8_2.rdf',
    '8_4.rdf',
    '8_8.rdf',
    '8_16.rdf',
    '8_32.rdf',
    '8_64.rdf',
    '8_128.rdf',
    '8_256.rdf',
    '16_2.rdf',
    '16_4.rdf',
    '16_8.rdf',
    '16_16.rdf',
    '16_32.rdf',
    '16_64.rdf',
    '16_128.rdf',
    '16_256.rdf',
    '32_2.rdf',
    '32_4.rdf',
    '32_8.rdf',
    '32_16.rdf',
    '32_32.rdf',
    '32_64.rdf',
    '32_128.rdf',
    '32_256.rdf',
    '64_2.rdf',
    '64_4.rdf',
    '64_8.rdf',
    '64_16.rdf',
    '64_32.rdf',
    '64_64.rdf',
    '64_128.rdf',
    '64_256.rdf',
    '128_2.rdf',
    '128_4.rdf',
    '128_8.rdf',
    '128_16.rdf',
    '128_32.rdf',
    '128_64.rdf',
    '128_128.rdf',
    '128_256.rdf',
    '256_2.rdf',
    '256_4.rdf',
    '256_8.rdf',
    '256_16.rdf',
    '256_32.rdf',
    '256_64.rdf',
    '256_128.rdf',
    '256_256.rdf'
]

RDF_EDIT_LIST = [
    '2_2a.rdf',
    '2_4a.rdf',
    '2_8a.rdf',
    '2_16a.rdf',
    '2_32a.rdf',
    '2_64a.rdf',
    '2_128a.rdf',
    '2_256a.rdf',
    '4_2a.rdf',
    '4_4a.rdf',
    '4_8a.rdf',
    '4_16a.rdf',
    '4_32a.rdf',
    '4_64a.rdf',
    '4_128a.rdf',
    '4_256a.rdf',
    '8_2a.rdf',
    '8_4a.rdf',
    '8_8a.rdf',
    '8_16a.rdf',
    '8_32a.rdf',
    '8_64a.rdf',
    '8_128a.rdf',
    '8_256a.rdf',
    '16_2a.rdf',
    '16_4a.rdf',
    '16_8a.rdf',
    '16_16a.rdf',
    '16_32a.rdf',
    '16_64a.rdf',
    '16_128a.rdf',
    '16_256a.rdf',
    '32_2a.rdf',
    '32_4a.rdf',
    '32_8a.rdf',
    '32_16a.rdf',
    '32_32a.rdf',
    '32_64a.rdf',
    '32_128a.rdf',
    '32_256a.rdf',
    '64_2a.rdf',
    '64_4a.rdf',
    '64_8a.rdf',
    '64_16a.rdf',
    '64_32a.rdf',
    '64_64a.rdf',
    '64_128a.rdf',
    '64_256a.rdf',
    '128_2a.rdf',
    '128_4a.rdf',
    '128_8a.rdf',
    '128_16a.rdf',
    '128_32a.rdf',
    '128_64a.rdf',
    '128_128a.rdf',
    '128_256a.rdf',
    '256_2a.rdf',
    '256_4a.rdf',
    '256_8a.rdf',
    '256_16a.rdf',
    '256_32a.rdf',
    '256_64a.rdf',
    '256_128a.rdf',
    '256_256a.rdf'
]

TEST_ROUTE = [
    "/category/selectTempMax0", "/category/selectTempMax1",
    "/category/updateLevel0", "/category/updateLevel1",
    "/category/selectPMAvgMax0", "/category/selectPMAvgMax1",
    "/category/selectLLToLight0", "/category/selectLLToLight1"
]


def makeList(type: str) -> list:
    ret = []
    random.shuffle(RDF_ORI_LIST)
    if type == 'debugUpdate':
        for i in RDF_ORI_LIST:
            ret.append(f"CMD::mv {os.path.join(LOCALE_BACK, i)} {os.path.join(LOCALE_RDF, i)}")
            ret.append("RESTART")
            for j in UPDATE_ROUTE:
                ret.append(j)
            ret.append("/save")
            ret.append(f'CMD::find {LOCALE_SAVE} -maxdepth 1 -type f -name "*.rdf" -exec mv {{}} {os.path.join(LOCALE_BACK, i.split(".")[0] + "a.rdf")} \\;')
            ret.append(f'CMD::find {LOCALE_RDF} -maxdepth 1 -type f -name "*.rdf" -exec mv {{}} {LOCALE_BACK} \\;')

    if type == 'emmUpdate':
        for i in RDF_EDIT_LIST_0:
            ret.append(f"CMD::mv {os.path.join(LOCALE_BACK, i)} {os.path.join(LOCALE_RDF, i)}")
            ret.append("RESTART")
            ret.append("/category/addPro")
            ret.append("/save")
            ret.append(f'CMD::find {LOCALE_SAVE} -maxdepth 1 -type f -name "*.rdf" -exec mv {{}} {os.path.join(LOCALE_BACK, i.split(".")[0] + "a.rdf")} \\;')
            ret.append(f'CMD::find {LOCALE_RDF} -maxdepth 1 -type f -name "*.rdf" -exec mv {{}} {LOCALE_BACK} \\;')

    elif type == 'FullTest':
        random.shuffle(RDF_EDIT_LIST)
        for i in RDF_EDIT_LIST:
            ret.append(f"CMD::mv {os.path.join(LOCALE_BACK, i)} {os.path.join(LOCALE_RDF, i)}")
            ret.append("RESTART")
            REAL_TEST_ROUTE = []
            for j in range(TEST_ROUTE_REPEAT):
                REAL_TEST_ROUTE += TEST_ROUTE
            random.shuffle(REAL_TEST_ROUTE)
            for j in REAL_TEST_ROUTE:
                ret.append(j)
                ret.append("RESTART")
            ret.append("/traceComplite")
            ret.append("END")
            ret.append(f'CMD::find {LOCALE_RDF} -maxdepth 1 -type f -name "*.rdf" -exec mv {{}} {LOCALE_BACK} \\;')

            
    else:
        print("Unknown List Type")
    
    return ret

def req(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def restartWait():
    try:
        subprocess.run(["docker", "restart", "Onto"], check=True)
        print("Docker container 'Onto' restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting Docker container 'Onto': {e}")

    while True:
        if os.path.isfile(LOCALE_CHEACK_FILE):
            try:
                if os.path.isfile(LOCALE_CHEACK_FILE):
                    os.remove(LOCALE_CHEACK_FILE)
                    print(f"Deleted file: {LOCALE_CHEACK_FILE}")
                else:
                    print(f"File not found: {LOCALE_CHEACK_FILE}")
            except Exception as e:
                print(f"Error deleting file {LOCALE_CHEACK_FILE}: {e}")
            break
        else:
            time.sleep(2)


def getName(dir, ext):
    files = glob.glob(os.path.join(dir, f'*.{ext}'))
    if len(files) == 1:
        return os.path.basename(files[0])
    else:
        print(f"{dir}에 {ext}파일이 없거나 두 개 이상임")
        return None

def main():
    i = 0
    lines = makeList(SET)
    for line in lines:
        print(f"{i} : {line}")
        i += 1

    i = 0
    print("======================================================================")
    print(f"TEST START : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("======================================================================")
    for line in lines:
        print(f"{i} / {len(lines) - 1} -- {line}")
        time.sleep(2)
        if line == "RESTART":   
            restartWait()
            time.sleep(5)
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

        elif line == "END":
            with open(LOCALE_COMPLETE_FILE, 'r+', encoding='utf-8') as file:
                data = file.readlines()
                categories = {}
                for line in data:
                    key, value = line.strip().split(': ')
                    if key not in categories:
                        categories[key] = []
                    categories[key].append(int(value))

                averages = {key: round(np.mean(values), 2) for key, values in categories.items()}
                std_devs = {key: round(np.std(values), 2) for key, values in categories.items()}
                coeff_vars = {key: round((std_devs[key] / averages[key]) if averages[key] != 0 else 0, 2) for key in categories}

                file.write("\n\n--- Averages, Standard Deviations, and Coefficients of Variation ---\n")
                for key in averages:
                    avg = averages[key]
                    std_dev = std_devs[key]
                    coeff_var = coeff_vars[key]
                    file.write(f"{key} - Average: {avg}, Standard Deviation: {std_dev}, Coefficient of Variation: {coeff_var}\n")
        
            save_name = f"./{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}--{getName(LOCALE_RDF, 'rdf')}.txt"
            subprocess.run(["mv", LOCALE_COMPLETE_FILE, save_name], check=True)

        elif "CMD::" in line:
            cmd = line.split('::')[1]
            subprocess.run(cmd, shell=True, check=True)
            print("")

        else:
            url = HOSTNAME + line
            result = req(url)
            if result:
                time.sleep(5)
            else:
                print(f"Failed to fetch {url}")
                time.sleep(5)



        i += 1
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
    print("======================================================================")
    print(f"TEST END : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
if __name__ == "__main__":
    main()