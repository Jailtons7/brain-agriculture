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
    {
      "arable_area": "50.26",
      "vegetation_area": "200.00",
      "state": "Minas Gerais",
      "total": "0.00"
    },
    {
      "arable_area": "100.00",
      "vegetation_area": "120.00",
      "state": "Bahia",
      "total": "220.00"
    }
  ],
  "properties_by_state": [
    {"state": "Paraná", "total": 4},
    {"state": "Bahia", "total": 6}
  ],
  "total_areas_by_land_usage": {
    "arable_area": 800.0,
    "vegetation_area": 430.5
  },
  "top_cultivated_crops": [
    {"name": "Trigo", "total_farms": 5},
    {"name": "Arroz", "total_farms": 2}
  ]
}
"""
