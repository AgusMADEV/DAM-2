from datetime import datetime
import multiprocessing as mp

def trabajo(_):
    numero = 1.00000098
    # evita imprimir en cada proceso: el I/O frena el paralelismo
    for _ in range(0, 100_000_000):
        numero *= 1.0000000000654
    return int(datetime.now().timestamp())

if __name__ == "__main__":
    # usa tantos procesos como cores tengas (o 16, lo que sea menor)
    NUM_PROCESOS = min(16, mp.cpu_count())

    inicio = int(datetime.now().timestamp())
    with mp.get_context("fork").Pool(processes=NUM_PROCESOS) as pool:
        finales = pool.map(trabajo, range(0, 16))
    final = max(finales)

    print("He tardado " + str(final - inicio) + " segundos")
