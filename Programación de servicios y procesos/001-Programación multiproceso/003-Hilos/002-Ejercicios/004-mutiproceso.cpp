// build (Windows MinGW/LLVM o MSVC):
//   g++ -O2 -std=c++17 -march=native -o paralelo paralelo.cpp
// build (Linux):
//   g++ -O2 -std=c++17 -march=native -pthread -o paralelo paralelo.cpp
// run:
//   ./paralelo  (o paralelo.exe)

#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <cstdint>
#include <chrono>

#if defined(_WIN32)
  #include <windows.h>
#elif defined(__linux__)
  #include <pthread.h>
  #include <sched.h>
#endif

static volatile double g_sink; // evita que el compilador elimine el cálculo

// Afinidad opcional por core (no pasa nada si falla)
static void set_affinity(unsigned core_index) {
#if defined(_WIN32)
    DWORD_PTR mask = (DWORD_PTR)1 << (core_index % (8*sizeof(DWORD_PTR)));
    HANDLE h = GetCurrentThread();
    // Ignorar errores
    SetThreadAffinityMask(h, mask);
#elif defined(__linux__)
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(core_index, &set);
    pthread_setaffinity_np(pthread_self(), sizeof(set), &set);
#else
    (void)core_index;
#endif
}

int main() {
    constexpr int PROCESOS = 16;                       // nº de hilos
    constexpr uint64_t ITERACIONES = 1'000'000'000ULL;    // OJO: 10^10 tardará muchísimo
    constexpr double FACTOR   = 1.0000000000654;
    constexpr double INICIAL  = 1.00000098;

    const unsigned hw = std::max(1u, std::thread::hardware_concurrency());

    auto t0 = std::chrono::steady_clock::now();

    std::vector<std::thread> ths;
    ths.reserve(PROCESOS);

    for (int k = 0; k < PROCESOS; ++k) {
        ths.emplace_back([k, hw]() {
            set_affinity((unsigned)k % hw); // opcional

            std::cout << "empiezo\n";
            double numero = INICIAL;
            for (uint64_t i = 0; i < ITERACIONES; ++i) {
                numero *= FACTOR;
            }
            g_sink = numero; // evitar eliminación por el optimizador
        });
    }

    for (auto& th : ths) th.join();

    auto t1 = std::chrono::steady_clock::now();
    auto secs = std::chrono::duration_cast<std::chrono::seconds>(t1 - t0).count();
    std::cout << "he tardado " << secs << " segundos\n";
    return 0;
}
