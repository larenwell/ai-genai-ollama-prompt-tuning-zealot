# Zealot Asistente CallCenter


## Estructura del proyecto
```
zealot-callcenter/
├── api.py                # FastAPI backend (En progreso. NO CORRER)
├── display.py            # Streamlit dashboard
├── prompt_tuning.py      # Prompt evaluation script
├── requirements.txt      # Python dependencies
└── utils/
    ├── analysis/         # Data processing and analysis
    ├── llms/            # Language model handling
    └── metrics/         # Performance evaluation
└── results/              # Resultados de las evaluaciones
└── data/                 # Datos para las evaluaciones (De referencia solo algunos)
```


## Instalación

```bash
pip install -r requirements.txt
```

## Uso

- Para generar el procesamiento de prompts y evaluacion:
```bash
python prompt_tuning.py
```

* Los reultados serán guardados en el archivo `results/all_results.csv`
* Los mejores resultados serán guardados en el archivo `results/best_combinations.csv`

- Para generar el dashboard: 
```bash
streamlit run display.py
```


## Notas
- Los modelos utilizados son: Llama 3.1 y Mistral (ambos disponibles en Ollama y AWS Bedrock)
- Para cambiar de modelo o proveedor, modificar el archivo `utils/llms/llm_handling.py`
- Para verificar las metricas de evaluacion, ver el archivo `utils/metrics/info.md` y el archivo `utils/metrics/response_metrics.py`
