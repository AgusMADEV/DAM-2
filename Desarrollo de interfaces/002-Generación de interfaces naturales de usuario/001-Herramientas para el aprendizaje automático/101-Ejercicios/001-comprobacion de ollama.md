ollama --version

ollama version is 0.11.10

ollama list
josevicente@josevicenteportatil:~$ ollama list
NAME                         ID              SIZE      MODIFIED    
llama3.1:8b-instruct-q4_0    42182419e950    4.7 GB    2 days ago     
qwen2.5-coder:7b             dae161e27b0e    4.7 GB    2 weeks ago    
gpt-oss:20b                  f2b8351c629c    13 GB     6 weeks ago    
josevicente@josevicenteportatil:~$ 

Instalar un nuevo modelo:

ollama pull llama3.1:8b-instruct-q4_0

ollama run llama3.1:8b-instruct-q4_0 "¿Cual es la capital de España?"



