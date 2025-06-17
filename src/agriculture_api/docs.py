DASHBOARD_VIEW_DESCRIPTION = """
Retorna estatísticas consolidadas sobre as fazendas, áreas e culturas cadastradas no sistema.
O retorno inclui:

- **Total de fazendas cadastradas**
- **Área total (em hectares)**
- **Distribuição de área total por estado**
- **Quantidade de fazendas por estado**
- **Áreas totais por tipo de uso do solo (Agricultável e Vegetação)**
- **Top culturas plantadas com maior número de propriedades (ex.: Soja, Milho, etc)**

Exemplo de resposta:

```json
{
  "total_farms": 10,
  "total_area": 1230.5,
  "areas_by_state": [
    {"state": "Paraná", "total_area": 600.0},
    {"state": "Bahia", "total_area": 630.5}
  ],
  "properties_by_state": [
    {"state": "Paraná", "properties": 4},
    {"state": "Bahia", "properties": 6}
  ],
  "total_areas_by_land_usage": {
    "total_arable_area": 800.0,
    "total_vegetation_area": 430.5
  },
  "top_cultivated_crops": [
    {"crop_name": "Soja", "properties": 5},
    {"crop_name": "Milho", "properties": 3}
  ]
}
"""
