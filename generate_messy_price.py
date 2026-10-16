import csv
import random
from datetime import datetime, timedelta

random.seed(42)
base_date = datetime(2020, 1, 1)
wrong_date = ["2020-14-50", "2020-02-30", "2020-13-01", "2020-00-10", "2020-01-32"]
markets=["Mukono","Bwaise","Nakasero","Kalerwe","Kireka","Kampala",None]
Commodities= ["Maize","MAIZE","Beans","BEANS","Rice","RICE","Wheat","WHEAT","Sorghum","SORGHUM"]

rows=[]

for i in range(1000):
    row= {
       "id": f'fd-{i}' if random.random()>0.02 else f'fd-{i}-1',
       "date": (base_date + timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d") if random.random() > 0.03 else random.choice(wrong_date),
       "market" : random.choice(markets),
       "Commodity" : random.choice(Commodities),
       "price" : random.randint(500, 25000) if random.random()> 0.05 else random.randint(-5000, -1000)  
}
    if random.random() > 0.075:
        rows.append(row)
    else:
        rows.append(row)
        

rows += rows[20:30]

with open("data/raw/prices.csv", "w") as f:
    writer= csv.DictWriter(f, fieldnames=["id","date","market","Commodity", "price"])
    writer.writeheader()
    writer.writerows(rows)
