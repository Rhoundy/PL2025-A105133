import re
import sys

def read_csv(file):
    with open(file, "r", encoding="utf-8") as f:
        header = f.readline()  # Read and discard the first line (header)
        content = f.read()  # Read the remaining conten

    headers = re.findall(r'[^;]+', header.strip())
    data = re.findall(r"(?s)([^;]+);(\".*?\");([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)\n", content)

    for piece in data:
        piece = list(piece)
        for value in piece:
            value = value.strip()

    return headers, data



def process_data(file):
    header, data = read_csv(file)
    
    try:
        idx_composer = header.index("compositor")
        idx_period = header.index("periodo")
        idx_title = header.index("nome")
    except ValueError:
        print("Error: Missing headers in csv.")
        return
    
    composers = sorted(set(line[idx_composer] for line in data if line[idx_composer]))
    
    period_dist = {}
    pieces_by_period = {}

    for line in data:
        if len(line) <= max(idx_composer, idx_period, idx_title):
            continue
        
        period = line[idx_period]
        title = line[idx_title]
        
        if period:
            period_dist[period] = period_dist.get(period, 0) + 1
            
            if period not in pieces_by_period:
                pieces_by_period[period] = []
            pieces_by_period[period].append(title)
    
    for period in pieces_by_period:
        pieces_by_period[period].sort()
    
    return composers, period_dist, pieces_by_period

if __name__ == '__main__':
    file = sys.argv[1]
    processed_data = process_data(file)
    if processed_data:
        composers, period_dist, pieces_by_period = processed_data
    
        print("Lista de Compositores:")
        print(composers)
        
        print("\nDistribuição de Obras por Período:")
        print(period_dist)
        
        print("\nDicionário de Obras por Período:")
        for periodo, obras in pieces_by_period.items():
            print(f"{periodo}: {obras}")
