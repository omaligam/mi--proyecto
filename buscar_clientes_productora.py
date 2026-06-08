"""
Busca empresas/marcas que necesitan servicios de produccion audiovisual
(video, fotografia, eventos, contenido) y extrae datos de contacto en
formato estructurado, usando Scrapegraph-ai.

Requisitos:
    pip install -e Scrapegraph-ai
    export OPENAI_APIKEY=sk-...

Uso:
    python buscar_clientes_productora.py
"""

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from scrapegraphai.graphs import SearchGraph
from scrapegraphai.utils import convert_to_csv, convert_to_json, prettify_exec_info

load_dotenv()


class Lead(BaseModel):
    empresa: str = Field(description="Nombre de la empresa o marca que busca el servicio")
    necesidad: str = Field(
        description="Que tipo de servicio audiovisual busca (video, fotografia, eventos, etc.)"
    )
    contacto: Optional[str] = Field(
        description="Email, telefono o persona de contacto si esta disponible", default=None
    )
    fuente: str = Field(description="URL de la pagina donde se encontro la oportunidad")


class Leads(BaseModel):
    leads: List[Lead]


openai_key = os.getenv("OPENAI_APIKEY")

graph_config = {
    "llm": {
        "api_key": openai_key,
        "model": "openai/gpt-4o-mini",
    },
    "max_results": 5,
    "verbose": True,
}

PROMPT = (
    "Encontra empresas, marcas o agencias que actualmente estan buscando "
    "contratar una productora audiovisual (para video, fotografia, cobertura "
    "de eventos o creacion de contenido). Para cada una indica el nombre de "
    "la empresa, que tipo de servicio audiovisual necesita, datos de contacto "
    "si estan disponibles, y la URL donde se publico la busqueda."
)

search_graph = SearchGraph(prompt=PROMPT, config=graph_config, schema=Leads)

result = search_graph.run()
print(result)

print(prettify_exec_info(search_graph.get_execution_info()))

convert_to_csv(result, "leads_productora")
convert_to_json(result, "leads_productora")
