from tqdm import tqdm
from time import sleep

for _ in tqdm(range(1000)):
    sleep(0.001)
print('concluido')