# Como correr la busqueda de clientes en tu computadora (gratis, con Ollama)

Esta guia te permite ejecutar `buscar_clientes_productora.py` en tu propia
maquina usando un modelo de lenguaje **local y gratuito** (Ollama), sin
necesitar una API key paga de OpenAI.

## 1. Instalar Ollama

- **Mac / Linux**:
  ```
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Windows**: descargar el instalador desde https://ollama.com/download

## 2. Descargar un modelo

Se recomienda un modelo liviano para que corra bien en una compu normal:

```
ollama pull llama3.1
```

(Si tu maquina tiene poca RAM, probar con `ollama pull llama3.2:3b`)

## 3. Clonar este repositorio e instalar dependencias

```
git clone <URL-de-tu-repo>
cd mi--proyecto
git submodule update --init --recursive

python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

pip install -e Scrapegraph-ai
pip install reportlab
```

## 4. Ajustar el script para usar Ollama en vez de OpenAI

Editar `buscar_clientes_productora.py` y reemplazar el bloque `graph_config`
por esto:

```python
graph_config = {
    "llm": {
        "model": "ollama/llama3.1",
        "temperature": 0,
        "base_url": "http://localhost:11434",
    },
    "max_results": 5,
    "verbose": True,
}
```

(Y se puede borrar la linea `openai_key = os.getenv("OPENAI_APIKEY")`, ya
no se usa)

## 5. Asegurarse de que Ollama este corriendo

```
ollama serve
```

(En Mac/Windows con la app de Ollama instalada, ya queda corriendo solo)

## 6. Ejecutar la busqueda

En otra terminal, dentro de la carpeta del proyecto:

```
python buscar_clientes_productora.py
```

Esto va a generar:
- `leads_productora.csv`
- `leads_productora.json`

con la lista real de empresas, PYMES y licitaciones de gobierno encontradas,
incluyendo presupuesto (cuando este disponible), necesidad y contacto.

## 7. Pasar los resultados al PDF

Una vez que tengas `leads_productora.csv`, se puede adaptar
`generar_plantilla_leads_pdf.py` para que lea ese archivo y vuelque los
datos reales en las filas de la tabla del PDF (en vez de filas vacias).

> Nota: los modelos locales son mas lentos y, dependiendo del modelo, pueden
> dar resultados de menor calidad que GPT-4o. Si en algun momento conseguis
> una API key de OpenAI, Anthropic, Groq, etc., el script original
> (`graph_config` con `"api_key"` y `"model": "openai/gpt-4o-mini"`) va a dar
> mejores resultados.
