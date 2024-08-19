num_threads = 10
num_inscritos = 6393
num_inscritos_por_thread = num_inscritos // num_threads
threads = []

for i in range(num_threads):
    print(num_inscritos_por_thread * i, num_inscritos_por_thread * (i + 1))

print(num_inscritos_por_thread * num_threads, num_inscritos)
