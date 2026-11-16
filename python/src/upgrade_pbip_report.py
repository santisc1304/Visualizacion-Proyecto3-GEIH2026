"""
Actualizador estructural del proyecto Power BI (.pbip / PBIR + TMDL)
==================================================================
Conecta `Equipo_Sandoval_Ramos_Proyecto3.pbip` a la base completa procesada
(`data/processed/base_geih_ciudadana_analisis.csv`, 183.911 registros con INGLABO y FEX_C18)
e implementa medidas DAX ponderadas por FEX_C18, tema personalizado pergamino/roble
y 3 páginas de reporte PBIR 1920x1080.
"""

from __future__ import annotations

import json
import os
import shutil
import uuid

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE_PBI_DIR = os.path.join(ROOT_DIR, "powerbi")
REPORT_DIR = os.path.join(BASE_PBI_DIR, "Equipo_Sandoval_Ramos_Proyecto3.Report")
SEMANTIC_DIR = os.path.join(
    BASE_PBI_DIR, "Equipo_Sandoval_Ramos_Proyecto3.SemanticModel"
)
CSV_DATA_PATH = os.path.join(
    ROOT_DIR, "data", "processed", "base_geih_ciudadana_analisis.csv"
)

SCHEMA_REPORT = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json"
SCHEMA_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"
SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_VISUAL = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"

PAGE_PANORAMA_ID = "aa3ec3b05a03397a538b"
PAGE_CICLO_ID = "07a5b96d475378c08910"
PAGE_SIMULADOR_ID = "c8a4f21d9e0731b64210"

THEME_FILENAME = "Cartografia_Ejecutiva_GEIH2026.json"


def det_uuid(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"uec.proyecto3.{seed}"))


def lit(val: str) -> dict:
    return {"expr": {"Literal": {"Value": val}}}


def solid_hex(hex_color: str) -> dict:
    return {"solid": {"color": lit(f"'{hex_color}'")}}


def field_col(prop: str, entity: str = "Base_Analisis") -> dict:
    return {
        "Column": {
            "Expression": {"SourceRef": {"Entity": entity}},
            "Property": prop,
        }
    }


def field_measure(prop: str, entity: str = "Base_Analisis") -> dict:
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Entity": entity}},
            "Property": prop,
        }
    }


def proj_col(prop: str, entity: str = "Base_Analisis", active: bool = False) -> dict:
    p = {
        "field": field_col(prop, entity),
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }
    if active:
        p["active"] = True
    return p


def proj_measure(prop: str, entity: str = "Base_Analisis", fmt: str | None = None) -> dict:
    p = {
        "field": field_measure(prop, entity),
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }
    if fmt:
        p["format"] = fmt
    return p


def container_chrome(
    title_text: str | None = None,
    bg_hex: str = "#FFFDF7",
    border_hex: str = "#D4B483",
    accent_title_hex: str = "#2A1808",
    radius: int = 8,
    show_title: bool = True,
) -> dict:
    objs = {
        "background": [
            {
                "properties": {
                    "show": lit("true"),
                    "color": solid_hex(bg_hex),
                    "transparency": lit("0D"),
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": lit("true"),
                    "color": solid_hex(border_hex),
                    "radius": lit(f"{radius}D"),
                }
            }
        ],
    }
    if title_text is not None:
        objs["title"] = [
            {
                "properties": {
                    "show": lit("true" if show_title else "false"),
                    "text": lit(f"'{title_text}'"),
                    "fontColor": solid_hex(accent_title_hex),
                    "fontSize": lit("12D"),
                    "bold": lit("true"),
                }
            }
        ]
    return objs


def make_header_banner(vid: str, page_subtitle: str, tab_order: int = 9000) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {
            "x": 0,
            "y": 0,
            "z": 9000,
            "height": 88,
            "width": 1920,
            "tabOrder": tab_order,
        },
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [
                                        {
                                            "value": "POWER BI  |  MONITOR EJECUTIVO: ESTABILIDAD DEL TRABAJO INDEPENDIENTE EN COLOMBIA (GEIH 2026)",
                                            "textStyle": {
                                                "fontWeight": "bold",
                                                "fontSize": "18pt",
                                                "fontFamily": "Georgia",
                                                "color": "#FFFDF7",
                                            },
                                        }
                                    ],
                                    "horizontalTextAlignment": "left",
                                },
                                {
                                    "textRuns": [
                                        {
                                            "value": page_subtitle,
                                            "textStyle": {
                                                "fontSize": "10.5pt",
                                                "fontFamily": "Segoe UI",
                                                "color": "#FCD34D",
                                            },
                                        }
                                    ],
                                    "horizontalTextAlignment": "left",
                                },
                            ]
                        }
                    }
                ]
            },
            "visualContainerObjects": {
                "background": [
                    {
                        "properties": {
                            "show": lit("true"),
                            "color": solid_hex("#2A1808"),
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": lit("true"),
                            "color": solid_hex("#B45309"),
                        }
                    }
                ],
            },
            "drillFilterOtherVisuals": True,
        },
    }


def make_page_navigator(vid: str) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {
            "x": 1248,
            "y": 14,
            "z": 9500,
            "height": 60,
            "width": 648,
            "tabOrder": 9500,
        },
        "visual": {
            "visualType": "pageNavigator",
            "objects": {
                "shape": [
                    {
                        "properties": {
                            "tileShape": lit("'rectangle'"),
                            "roundEdge": lit("6L"),
                        },
                        "selector": {"id": "default"},
                    }
                ],
                "text": [
                    {
                        "properties": {
                            "fontColor": solid_hex("#FDE68A"),
                            "fontSize": lit("10D"),
                            "bold": lit("true"),
                        },
                        "selector": {"id": "default"},
                    },
                    {
                        "properties": {
                            "fontColor": solid_hex("#2A1808"),
                            "fontSize": lit("10D"),
                            "bold": lit("true"),
                        },
                        "selector": {"id": "selected"},
                    },
                ],
                "fill": [
                    {
                        "properties": {
                            "show": lit("true"),
                            "fillColor": solid_hex("#4A2B11"),
                        },
                        "selector": {"id": "default"},
                    },
                    {
                        "properties": {
                            "show": lit("true"),
                            "fillColor": solid_hex("#F59E0B"),
                        },
                        "selector": {"id": "selected"},
                    },
                ],
                "outline": [
                    {
                        "properties": {"lineColor": solid_hex("#B45309")},
                        "selector": {"id": "default"},
                    }
                ],
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": lit("false")}}],
                "border": [{"properties": {"show": lit("false")}}],
                "title": [{"properties": {"show": lit("false")}}],
            },
            "drillFilterOtherVisuals": True,
        },
    }


def make_slicer(vid: str, prop: str, label: str, x: float, w: float, tab_order: int) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {
            "x": x,
            "y": 98,
            "z": 7000 + tab_order,
            "height": 70,
            "width": w,
            "tabOrder": tab_order,
        },
        "visual": {
            "visualType": "slicer",
            "query": {
                "queryState": {
                    "Values": {"projections": [proj_col(prop, active=True)]}
                }
            },
            "objects": {
                "data": [{"properties": {"mode": lit("'Dropdown'")}}],
                "header": [
                    {
                        "properties": {
                            "show": lit("true"),
                            "text": lit(f"'{label}'"),
                            "fontColor": solid_hex("#784B16"),
                            "fontSize": lit("10D"),
                        }
                    }
                ],
                "items": [
                    {
                        "properties": {
                            "fontColor": solid_hex("#2A1808"),
                            "background": solid_hex("#FFFDF7"),
                        }
                    }
                ],
            },
            "visualContainerObjects": container_chrome(
                title_text=None,
                bg_hex="#FFFDF7",
                border_hex="#D4B483",
                radius=6,
                show_title=False,
            ),
            "syncGroup": {
                "groupName": prop,
                "fieldChanges": True,
                "filterChanges": True,
            },
            "drillFilterOtherVisuals": True,
        },
    }


def make_slicers_row(prefix: str) -> list[dict]:
    specs = [
        ("SectorEconomico", "Sector Económico", 24, 452, 100),
        ("GrupoEdad", "Grupo de Edad", 496, 452, 200),
        ("DPTO_Nombre", "Departamento", 968, 452, 300),
        ("Sexo", "Sexo", 1440, 456, 400),
    ]
    return [
        make_slicer(f"{prefix}sl{i+1:02d}", prop, lbl, x, w, tab)
        for i, (prop, lbl, x, w, tab) in enumerate(specs)
    ]


def make_kpi_card(
    vid: str,
    measure: str,
    label: str,
    accent_hex: str,
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
    fmt: str | None = None,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {
            "x": x,
            "y": y,
            "z": 4000 + tab_order,
            "height": h,
            "width": w,
            "tabOrder": tab_order,
        },
        "visual": {
            "visualType": "cardVisual",
            "query": {
                "queryState": {
                    "Data": {"projections": [proj_measure(measure, fmt=fmt)]}
                },
                "sortDefinition": {
                    "sort": [{"field": field_measure(measure), "direction": "Descending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "label": [
                    {
                        "properties": {
                            "fontColor": solid_hex("#784B16"),
                            "fontSize": lit("10.5D"),
                            "bold": lit("true"),
                        },
                        "selector": {"id": "default"},
                    }
                ],
                "value": [
                    {
                        "properties": {
                            "fontColor": solid_hex("#2A1808"),
                            "fontSize": lit("22D"),
                            "bold": lit("true"),
                        },
                        "selector": {"id": "default"},
                    }
                ],
                "outline": [
                    {
                        "properties": {
                            "show": lit("true"),
                            "lineColor": solid_hex(accent_hex),
                        },
                        "selector": {"id": "default"},
                    }
                ],
            },
            "visualContainerObjects": container_chrome(
                title_text=label,
                bg_hex="#FFFDF7",
                border_hex=accent_hex,
                accent_title_hex=accent_hex,
                radius=8,
                show_title=True,
            ),
            "drillFilterOtherVisuals": True,
        },
    }


def make_clustered_bar(
    vid: str,
    title: str,
    cat_prop: str,
    measures: list[tuple[str, str]],
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "clusteredBarChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "Y": {"projections": [proj_measure(m) for m, _ in measures]},
                },
                "sortDefinition": {
                    "sort": [{"field": field_measure(measures[0][0]), "direction": "Descending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "legend": [{"properties": {"show": lit("true"), "position": lit("'Top'")}}],
                "labels": [{"properties": {"show": lit("true"), "fontSize": lit("9D")}}],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_clustered_column(
    vid: str,
    title: str,
    cat_prop: str,
    measures: list[tuple[str, str]],
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "clusteredColumnChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "Y": {"projections": [proj_measure(m) for m, _ in measures]},
                },
                "sortDefinition": {
                    "sort": [{"field": field_col(cat_prop), "direction": "Ascending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "legend": [{"properties": {"show": lit("true"), "position": lit("'Top'")}}],
                "labels": [{"properties": {"show": lit("true"), "fontSize": lit("9D")}}],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_line_chart_measures(
    vid: str,
    title: str,
    cat_prop: str,
    measures: list[tuple[str, str]],
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "lineChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "Y": {"projections": [proj_measure(m) for m, _ in measures]},
                },
                "sortDefinition": {
                    "sort": [{"field": field_col(cat_prop), "direction": "Ascending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "legend": [{"properties": {"show": lit("true"), "position": lit("'Top'")}}],
                "lineStyles": [
                    {
                        "properties": {
                            "lineStyle": lit("'solid'"),
                            "strokeWidth": lit("3D"),
                        }
                    }
                ],
                "labels": [{"properties": {"show": lit("true"), "fontSize": lit("9D")}}],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_line_chart_series(
    vid: str,
    title: str,
    cat_prop: str,
    series_prop: str,
    measure_name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "lineChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "Series": {"projections": [proj_col(series_prop)]},
                    "Y": {"projections": [proj_measure(measure_name)]},
                },
                "sortDefinition": {
                    "sort": [{"field": field_col(cat_prop), "direction": "Ascending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "legend": [{"properties": {"show": lit("true"), "position": lit("'Top'")}}],
                "lineStyles": [
                    {
                        "properties": {
                            "lineStyle": lit("'solid'"),
                            "strokeWidth": lit("3D"),
                        }
                    }
                ],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_bar_chart(
    vid: str,
    title: str,
    cat_prop: str,
    measure_name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "barChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "Y": {"projections": [proj_measure(measure_name)]},
                },
                "sortDefinition": {
                    "sort": [{"field": field_measure(measure_name), "direction": "Descending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {
                                "solid": {
                                    "color": {
                                        "expr": {
                                            "ThemeDataColor": {
                                                "ColorId": 6,
                                                "Percent": 0,
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                ],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_scatter(
    vid: str,
    title: str,
    cat_prop: str,
    x_measure: str,
    y_measure: str,
    size_measure: str,
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "scatterChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "X": {"projections": [proj_measure(x_measure)]},
                    "Y": {"projections": [proj_measure(y_measure)]},
                    "Size": {"projections": [proj_measure(size_measure)]},
                }
            },
            "objects": {
                "bubbles": [{"properties": {"markerShape": lit("'circle'")}}],
                "dataPoint": [
                    {
                        "properties": {
                            "fill": {
                                "solid": {
                                    "color": {
                                        "expr": {
                                            "ThemeDataColor": {
                                                "ColorId": 4,
                                                "Percent": 0,
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                ],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_donut(
    vid: str,
    title: str,
    cat_prop: str,
    measure_name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "donutChart",
            "query": {
                "queryState": {
                    "Category": {"projections": [proj_col(cat_prop, active=True)]},
                    "Y": {"projections": [proj_measure(measure_name)]},
                }
            },
            "objects": {
                "legend": [{"properties": {"show": lit("true"), "position": lit("'Right'")}}],
                "labels": [{"properties": {"show": lit("true")}}],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_pivot(
    vid: str,
    title: str,
    row_prop: str,
    col_prop: str,
    measures: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "pivotTable",
            "query": {
                "queryState": {
                    "Rows": {"projections": [proj_col(row_prop, active=True)]},
                    "Columns": {"projections": [proj_col(col_prop, active=True)]},
                    "Values": {"projections": [proj_measure(m) for m in measures]},
                }
            },
            "objects": {
                "grid": [
                    {
                        "properties": {
                            "gridHorizontal": lit("true"),
                            "gridVertical": lit("true"),
                            "gridHorizontalColor": solid_hex("#E2CBA2"),
                            "gridVerticalColor": solid_hex("#E2CBA2"),
                        }
                    }
                ],
                "columnHeaders": [
                    {
                        "properties": {
                            "fontColor": solid_hex("#FFFDF7"),
                            "backColor": solid_hex("#2A1808"),
                        }
                    }
                ],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def make_table(
    vid: str,
    title: str,
    cols: list[str],
    measures: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    tab_order: int,
) -> dict:
    projections = [proj_col(c) for c in cols] + [proj_measure(m) for m in measures]
    return {
        "$schema": SCHEMA_VISUAL,
        "name": vid,
        "position": {"x": x, "y": y, "z": 2000 + tab_order, "height": h, "width": w, "tabOrder": tab_order},
        "visual": {
            "visualType": "tableEx",
            "query": {
                "queryState": {"Values": {"projections": projections}},
                "sortDefinition": {
                    "sort": [{"field": field_measure(measures[0]), "direction": "Descending"}]
                },
            },
            "objects": {
                "grid": [
                    {
                        "properties": {
                            "gridHorizontal": lit("true"),
                            "gridHorizontalColor": solid_hex("#E2CBA2"),
                        }
                    }
                ],
                "columnHeaders": [
                    {
                        "properties": {
                            "fontColor": solid_hex("#FFFDF7"),
                            "backColor": solid_hex("#2A1808"),
                        }
                    }
                ],
            },
            "visualContainerObjects": container_chrome(title_text=title),
            "drillFilterOtherVisuals": True,
        },
    }


def write_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def update_semantic_model() -> None:
    # 1. Limpiar expressions.tmdl (sin consultas rotas a C:\Users\sebas\...)
    expr_path = os.path.join(SEMANTIC_DIR, "definition", "expressions.tmdl")
    with open(expr_path, "wb") as f:
        f.write(b"")

    # 2. Actualizar model.tmdl para dejar solo Base_Analisis en PBI_QueryOrder
    model_path = os.path.join(SEMANTIC_DIR, "definition", "model.tmdl")
    model_tmdl = (
        "model Model\r\n"
        "\tculture: es-CO\r\n"
        "\tdefaultPowerBIDataSourceVersion: powerBI_V3\r\n"
        "\tsourceQueryCulture: es-CO\r\n"
        "\tvalueFilterBehavior: independent\r\n"
        "\tdataAccessOptions\r\n"
        "\t\tlegacyRedirects\r\n"
        "\t\treturnErrorValuesAsNull\r\n"
        "\r\n"
        "annotation __PBI_TimeIntelligenceEnabled = 1\r\n"
        "\r\n"
        'annotation PBI_QueryOrder = ["Base_Analisis"]\r\n'
        "\r\n"
        'annotation PBI_ProTooling = ["DevMode"]\r\n'
        "\r\n"
        "ref table Base_Analisis\r\n"
        "ref table Calendario\r\n"
        "ref table DateTableTemplate_4d387154-6386-4bdf-8f6f-2a4c135d912e\r\n"
        "ref table LocalDateTable_d778b86c-da1e-4316-a668-e807fe72e22c\r\n"
        "\r\n"
        "ref cultureInfo es-CO\r\n"
    )
    with open(model_path, "wb") as f:
        f.write(model_tmdl.encode("utf-8"))

    # 3. Actualizar Base_Analisis.tmdl conectado a base_geih_ciudadana_analisis.csv (183.911 filas, INGLABO + FEX_C18)
    csv_escaped = CSV_DATA_PATH.replace('"', '""')
    tmdl_content = (
        "table Base_Analisis\r\n"
        "\tlineageTag: 1c9d1ee0-4022-4236-b6ba-ae4e68353f6d\r\n"
        "\r\n"
        "\tmeasure 'Poblacion Representada' = SUM(Base_Analisis[FEX_C18])\r\n"
        "\t\tformatString: #,##0\r\n"
        f"\t\tlineageTag: {det_uuid('Poblacion Representada')}\r\n"
        "\r\n"
        "\tmeasure 'Mediana de Ingreso' = MEDIAN(Base_Analisis[INGLABO])\r\n"
        "\t\tformatString: $ #,##0\r\n"
        "\t\tlineageTag: 291df1c1-7ce9-4e22-853e-a46a1209a124\r\n"
        "\r\n"
        "\tmeasure 'Ingreso Promedio' =\r\n"
        "\t\t\tDIVIDE(\r\n"
        "\t\t\t\tSUMX(Base_Analisis, Base_Analisis[INGLABO] * Base_Analisis[FEX_C18]),\r\n"
        "\t\t\t\tSUM(Base_Analisis[FEX_C18]),\r\n"
        "\t\t\t\tBLANK()\r\n"
        "\t\t\t)\r\n"
        "\t\tformatString: $ #,##0\r\n"
        "\t\tlineageTag: f7467549-b7c0-468a-82ae-c6fd0255e079\r\n"
        "\r\n"
        "\tmeasure 'Coef Variacion Ingreso' =\r\n"
        "\t\t\tVAR Media = [Ingreso Promedio]\r\n"
        "\t\t\tVAR Numerador = SUMX(Base_Analisis, Base_Analisis[FEX_C18] * ((Base_Analisis[INGLABO] - Media)^2))\r\n"
        "\t\t\tVAR Denominador = SUM(Base_Analisis[FEX_C18])\r\n"
        "\t\t\tRETURN DIVIDE(SQRT(DIVIDE(Numerador, Denominador, BLANK())), Media, BLANK())\r\n"
        "\t\tformatString: 0.00\r\n"
        "\t\tlineageTag: 05a87573-79c8-4ddf-942e-ffffa467e2d3\r\n"
        "\r\n"
        "\tmeasure 'Personas Analizadas' = COUNTROWS(Base_Analisis)\r\n"
        "\t\tformatString: #,##0\r\n"
        "\t\tlineageTag: 6be7fabd-d4a6-4465-8f0c-51aaca0df4c7\r\n"
        "\r\n"
        "\tmeasure 'Mediana Cuenta Propia' = CALCULATE(MEDIAN(Base_Analisis[INGLABO]), Base_Analisis[TipoTrabajador] = \"Cuenta propia\")\r\n"
        "\t\tformatString: $ #,##0\r\n"
        f"\t\tlineageTag: {det_uuid('Mediana Cuenta Propia')}\r\n"
        "\r\n"
        "\tmeasure 'Mediana Asalariado' = CALCULATE(MEDIAN(Base_Analisis[INGLABO]), Base_Analisis[TipoTrabajador] = \"Asalariado\")\r\n"
        "\t\tformatString: $ #,##0\r\n"
        f"\t\tlineageTag: {det_uuid('Mediana Asalariado')}\r\n"
        "\r\n"
        "\tmeasure 'Ingreso Medio Cuenta Propia' = CALCULATE([Ingreso Promedio], Base_Analisis[TipoTrabajador] = \"Cuenta propia\")\r\n"
        "\t\tformatString: $ #,##0\r\n"
        f"\t\tlineageTag: {det_uuid('Ingreso Medio Cuenta Propia')}\r\n"
        "\r\n"
        "\tmeasure 'Ingreso Medio Asalariado' = CALCULATE([Ingreso Promedio], Base_Analisis[TipoTrabajador] = \"Asalariado\")\r\n"
        "\t\tformatString: $ #,##0\r\n"
        f"\t\tlineageTag: {det_uuid('Ingreso Medio Asalariado')}\r\n"
        "\r\n"
        "\tmeasure 'CV Cuenta Propia' = CALCULATE([Coef Variacion Ingreso], Base_Analisis[TipoTrabajador] = \"Cuenta propia\")\r\n"
        "\t\tformatString: 0.00\r\n"
        f"\t\tlineageTag: {det_uuid('CV Cuenta Propia')}\r\n"
        "\r\n"
        "\tmeasure 'CV Asalariado' = CALCULATE([Coef Variacion Ingreso], Base_Analisis[TipoTrabajador] = \"Asalariado\")\r\n"
        "\t\tformatString: 0.00\r\n"
        f"\t\tlineageTag: {det_uuid('CV Asalariado')}\r\n"
        "\r\n"
        "\tmeasure 'Brecha Cuenta Propia vs Asalariado' = DIVIDE([Ingreso Medio Cuenta Propia] - [Ingreso Medio Asalariado], [Ingreso Medio Asalariado])\r\n"
        "\t\tformatString: +0.0%;-0.0%;0.0%\r\n"
        "\t\tlineageTag: 725f4b16-e51f-4164-a90c-f65e44d1267e\r\n"
        "\r\n"
        "\tmeasure 'Brecha Mediana Indep vs Asal' = DIVIDE([Mediana Cuenta Propia] - [Mediana Asalariado], [Mediana Asalariado])\r\n"
        "\t\tformatString: +0.0%;-0.0%;0.0%\r\n"
        f"\t\tlineageTag: {det_uuid('Brecha Mediana Indep vs Asal')}\r\n"
        "\r\n"
        "\tmeasure 'Delta CV Indep vs Asal' = [CV Cuenta Propia] - [CV Asalariado]\r\n"
        "\t\tformatString: +0.00;-0.00;0.00\r\n"
        f"\t\tlineageTag: {det_uuid('Delta CV Indep vs Asal')}\r\n"
        "\r\n"
        "\tmeasure 'Mediana Corredor Dorado' = CALCULATE([Mediana Cuenta Propia], Base_Analisis[GrupoEdad] = \"35 a 54 años\")\r\n"
        "\t\tformatString: $ #,##0\r\n"
        f"\t\tlineageTag: {det_uuid('Mediana Corredor Dorado')}\r\n"
        "\r\n"
        "\tmeasure 'Dptos Indep Mas Estable' =\r\n"
        "\t\t\tCOUNTROWS(\r\n"
        "\t\t\t\tFILTER(\r\n"
        "\t\t\t\t\tVALUES(Base_Analisis[DPTO_Nombre]),\r\n"
        "\t\t\t\t\tNOT(ISBLANK([CV Cuenta Propia])) && NOT(ISBLANK([CV Asalariado])) && [CV Cuenta Propia] <= [CV Asalariado]\r\n"
        "\t\t\t\t)\r\n"
        "\t\t\t)\r\n"
        "\t\tformatString: 0\r\n"
        f"\t\tlineageTag: {det_uuid('Dptos Indep Mas Estable')}\r\n"
        "\r\n"
        "\tmeasure 'Variacion Mensual Ingreso %' =\r\n"
        "\t\t\tVAR IngresoActual = [Ingreso Promedio]\r\n"
        "\t\t\tVAR IngresoMesAnterior = CALCULATE([Ingreso Promedio], DATEADD(Calendario[Date], -1, MONTH))\r\n"
        "\t\t\tRETURN DIVIDE(IngresoActual - IngresoMesAnterior, IngresoMesAnterior)\r\n"
        "\t\tformatString: +0.0%;-0.0%;0.0%\r\n"
        "\t\tlineageTag: ca762f2f-085c-4d4b-9a94-27885b88a4f6\r\n"
        "\r\n"
        "\tmeasure 'Semaforo Predictibilidad' =\r\n"
        "\t\t\tVAR cv = [CV Cuenta Propia]\r\n"
        "\t\t\tRETURN SWITCH(\r\n"
        "\t\t\t\tTRUE(),\r\n"
        "\t\t\t\tISBLANK(cv), \"Sin datos suficientes\",\r\n"
        "\t\t\t\tcv <= 0.75, \"Alta Predictibilidad (Estable)\",\r\n"
        "\t\t\t\tcv <= 1.05, \"Estabilidad Moderada\",\r\n"
        "\t\t\t\t\"Alta Volatilidad (Estacional)\"\r\n"
        "\t\t\t)\r\n"
        f"\t\tlineageTag: {det_uuid('Semaforo Predictibilidad')}\r\n"
        "\r\n"
        "\tmeasure 'Colchon Emergencia Sugerido' =\r\n"
        "\t\t\tVAR cv = [CV Cuenta Propia]\r\n"
        "\t\t\tRETURN SWITCH(\r\n"
        "\t\t\t\tTRUE(),\r\n"
        "\t\t\t\tISBLANK(cv), \"Evaluar perfil\",\r\n"
        "\t\t\t\tcv <= 0.75, \"2 a 3 meses de reserva\",\r\n"
        "\t\t\t\tcv <= 1.05, \"3 a 5 meses de reserva\",\r\n"
        "\t\t\t\t\"6+ meses (ingreso variable)\"\r\n"
        "\t\t\t)\r\n"
        f"\t\tlineageTag: {det_uuid('Colchon Emergencia Sugerido')}\r\n"
        "\r\n"
        "\tmeasure 'Nombre Departamento' = COALESCE(SELECTEDVALUE(Base_Analisis[DPTO_Nombre]), \"Nacional (33 Dptos.)\")\r\n"
        f"\t\tlineageTag: {det_uuid('Nombre Departamento')}\r\n"
        "\r\n"
        "\tcolumn MES\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        "\t\tlineageTag: 4cf439a5-83c5-4532-a383-7c3013ef723a\r\n"
        "\t\tsummarizeBy: sum\r\n"
        "\t\tsourceColumn: MES\r\n"
        "\r\n"
        "\tcolumn DIRECTORIO\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        "\t\tlineageTag: edd3109f-4db7-4212-ac5e-b5fc1852a5af\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: DIRECTORIO\r\n"
        "\r\n"
        "\tcolumn SECUENCIA_P\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        "\t\tlineageTag: c2436131-5fde-4889-8a38-bc1cc4b2ed7b\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: SECUENCIA_P\r\n"
        "\r\n"
        "\tcolumn ORDEN\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        "\t\tlineageTag: 407195c7-43b4-4c0b-aac4-cd3822c65833\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: ORDEN\r\n"
        "\r\n"
        "\tcolumn HOGAR\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        "\t\tlineageTag: 78f33600-dc99-41a8-9059-014317c80bcf\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: HOGAR\r\n"
        "\r\n"
        "\tcolumn FEX_C18\r\n"
        "\t\tdataType: double\r\n"
        f"\t\tlineageTag: {det_uuid('col_FEX_C18')}\r\n"
        "\t\tsummarizeBy: sum\r\n"
        "\t\tsourceColumn: FEX_C18\r\n"
        "\r\n"
        "\tcolumn DPTO\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: 8580229c-2aaf-434a-b214-170b1bffcc88\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: DPTO\r\n"
        "\r\n"
        "\tcolumn P6430\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        "\t\tlineageTag: 11438280-2d76-4cb7-9374-4f2cbfe4d57e\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: P6430\r\n"
        "\r\n"
        "\tcolumn P6500\r\n"
        "\t\tdataType: double\r\n"
        "\t\tlineageTag: 3ef5e0db-fcec-4e3a-bfc8-b606098d03fd\r\n"
        "\t\tsummarizeBy: sum\r\n"
        "\t\tsourceColumn: P6500\r\n"
        "\r\n"
        "\tcolumn INGLABO\r\n"
        "\t\tdataType: double\r\n"
        f"\t\tlineageTag: {det_uuid('col_INGLABO')}\r\n"
        "\t\tsummarizeBy: sum\r\n"
        "\t\tsourceColumn: INGLABO\r\n"
        "\r\n"
        "\tcolumn RAMA2D_R4\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: 6a88abd0-7ed8-4aa4-898b-8a5e9b07f79a\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: RAMA2D_R4\r\n"
        "\r\n"
        "\tcolumn P3271\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        f"\t\tlineageTag: {det_uuid('col_P3271')}\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: P3271\r\n"
        "\r\n"
        "\tcolumn P6040\r\n"
        "\t\tdataType: int64\r\n"
        "\t\tformatString: 0\r\n"
        f"\t\tlineageTag: {det_uuid('col_P6040')}\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: P6040\r\n"
        "\r\n"
        "\tcolumn DPTO_Nombre\r\n"
        "\t\tdataType: string\r\n"
        f"\t\tlineageTag: {det_uuid('col_DPTO_Nombre')}\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: DPTO_Nombre\r\n"
        "\r\n"
        "\tcolumn SectorEconomico\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: 25dc9430-4b7f-41e2-bc64-23b5822e3af0\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: SectorEconomico\r\n"
        "\r\n"
        "\tcolumn GrupoEdad\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: e64773fb-6920-462b-a5fc-0d4ed15fd5ef\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: GrupoEdad\r\n"
        "\r\n"
        "\tcolumn Sexo\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: 106abf0c-27ad-47c6-992b-e7feb671a663\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: Sexo\r\n"
        "\r\n"
        "\tcolumn TipoTrabajador\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: f4b410d4-ee88-4e16-bc6f-c881bdf48c9b\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: TipoTrabajador\r\n"
        "\r\n"
        "\tcolumn ID_Persona\r\n"
        "\t\tdataType: string\r\n"
        "\t\tlineageTag: 10e41194-f889-4da9-972d-6472f2f72ffd\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\t\tsourceColumn: ID_Persona\r\n"
        "\r\n"
        "\tcolumn Fecha = DATE(2026, Base_Analisis[MES], 1)\r\n"
        "\t\tformatString: General Date\r\n"
        "\t\tlineageTag: 7ac1043d-9e65-4661-a694-410da72171fc\r\n"
        "\t\tsummarizeBy: none\r\n"
        "\r\n"
        "\tpartition Base_Analisis = m\r\n"
        "\t\tmode: import\r\n"
        "\t\tsource =\r\n"
        "\t\t\t\tlet\r\n"
        f'\t\t\t\t    Origen = Csv.Document(File.Contents("{csv_escaped}"), [Delimiter=",", Columns=19, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\r\n'
        "\t\t\t\t    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),\r\n"
        "\t\t\t\t    Tipos = Table.TransformColumnTypes(Encabezados, {\r\n"
        '\t\t\t\t        {"MES", Int64.Type}, {"DIRECTORIO", Int64.Type}, {"SECUENCIA_P", Int64.Type},\r\n'
        '\t\t\t\t        {"ORDEN", Int64.Type}, {"HOGAR", Int64.Type}, {"FEX_C18", type number},\r\n'
        '\t\t\t\t        {"DPTO", type text}, {"P6430", Int64.Type}, {"P6500", type number},\r\n'
        '\t\t\t\t        {"INGLABO", type number}, {"RAMA2D_R4", type text}, {"P3271", Int64.Type},\r\n'
        '\t\t\t\t        {"P6040", Int64.Type}, {"DPTO_Nombre", type text}, {"SectorEconomico", type text},\r\n'
        '\t\t\t\t        {"GrupoEdad", type text}, {"Sexo", type text}, {"TipoTrabajador", type text},\r\n'
        '\t\t\t\t        {"ID_Persona", type text}\r\n'
        '\t\t\t\t    }, "en-US")\r\n'
        "\t\t\t\tin\r\n"
        "\t\t\t\t    Tipos\r\n"
        "\r\n"
        "\tannotation PBI_NavigationStepName = Navegación\r\n"
    )
    tmdl_path = os.path.join(SEMANTIC_DIR, "definition", "tables", "Base_Analisis.tmdl")
    with open(tmdl_path, "wb") as f:
        f.write(tmdl_content.encode("utf-8"))


def write_custom_theme_and_report_json() -> None:
    theme = {
        "name": "Cartografia_Ejecutiva_GEIH2026",
        "dataColors": [
            "#D97706",
            "#0F3D5E",
            "#DC2626",
            "#15803D",
            "#B45309",
            "#784B16",
            "#0284C7",
            "#991B1B",
        ],
        "foreground": "#2A1808",
        "foregroundNeutralSecondary": "#784B16",
        "foregroundNeutralTertiary": "#A17C4C",
        "background": "#FFFDF7",
        "backgroundLight": "#F4E1B8",
        "backgroundNeutral": "#E2CBA2",
        "backgroundDark": "#2A1808",
        "tableAccent": "#B45309",
        "shapeStroke": "#D4B483",
        "good": "#15803D",
        "neutral": "#D97706",
        "bad": "#DC2626",
        "maximum": "#15803D",
        "center": "#FBF4E3",
        "minimum": "#DC2626",
        "textClasses": {
            "callout": {"fontSize": 22, "fontFace": "Segoe UI Semibold", "color": "#2A1808"},
            "title": {"fontSize": 12, "fontFace": "Georgia", "color": "#2A1808"},
            "header": {"fontSize": 11, "fontFace": "Segoe UI Semibold", "color": "#2A1808"},
            "label": {"fontSize": 10, "fontFace": "Segoe UI", "color": "#5C3A1B"},
        },
        "visualStyles": {
            "*": {
                "*": {
                    "background": [{"show": True, "color": {"solid": {"color": "#FFFDF7"}}}],
                    "border": [{"show": True, "color": {"solid": {"color": "#D4B483"}}, "radius": 8}],
                    "title": [{"fontColor": {"solid": {"color": "#2A1808"}}, "fontFamily": "Georgia", "fontSize": 12}],
                }
            },
            "page": {
                "*": {
                    "background": [{"color": {"solid": {"color": "#FBF4E3"}}, "transparency": 0}]
                }
            },
        },
    }
    theme_path = os.path.join(
        REPORT_DIR, "StaticResources", "RegisteredResources", THEME_FILENAME
    )
    write_json(theme_path, theme)

    report_json = {
        "$schema": SCHEMA_REPORT,
        "themeCollection": {
            "baseTheme": {
                "name": "Fluent2-CY26SU10",
                "reportVersionAtImport": {
                    "visual": "2.14.0",
                    "report": "3.4.0",
                    "page": "2.3.1",
                },
                "type": "SharedResources",
            },
            "customTheme": {
                "name": THEME_FILENAME,
                "reportVersionAtImport": {
                    "visual": "2.14.0",
                    "report": "3.4.0",
                    "page": "2.3.1",
                },
                "type": "RegisteredResources",
            },
        },
        "objects": {
            "section": [{"properties": {"verticalAlignment": lit("'Top'")}}],
            "outspacePane": [{"properties": {"expanded": lit("false")}}],
        },
        "resourcePackages": [
            {
                "name": "SharedResources",
                "type": "SharedResources",
                "items": [
                    {
                        "name": "Fluent2-CY26SU10",
                        "path": "BaseThemes/Fluent2-CY26SU10.json",
                        "type": "BaseTheme",
                    }
                ],
            },
            {
                "name": "RegisteredResources",
                "type": "RegisteredResources",
                "items": [
                    {
                        "name": THEME_FILENAME,
                        "path": THEME_FILENAME,
                        "type": "CustomTheme",
                    }
                ],
            },
        ],
        "settings": {
            "useStylableVisualContainerHeader": True,
            "exportDataMode": "AllowSummarized",
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True,
        },
    }
    write_json(os.path.join(REPORT_DIR, "definition", "report.json"), report_json)


def build_page(page_id: str, display_name: str, visuals: list[dict]) -> None:
    page_dir = os.path.join(REPORT_DIR, "definition", "pages", page_id)
    visuals_dir = os.path.join(page_dir, "visuals")
    if os.path.isdir(visuals_dir):
        shutil.rmtree(visuals_dir)

    page_meta = {
        "$schema": SCHEMA_PAGE,
        "name": page_id,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
        "objects": {
            "background": [
                {
                    "properties": {
                        "color": solid_hex("#FBF4E3"),
                        "transparency": lit("0D"),
                    }
                }
            ]
        },
    }
    write_json(os.path.join(page_dir, "page.json"), page_meta)

    for v in visuals:
        v_path = os.path.join(visuals_dir, v["name"], "visual.json")
        write_json(v_path, v)


def build_all_pages() -> None:
    pages_meta = {
        "$schema": SCHEMA_PAGES,
        "pageOrder": [PAGE_PANORAMA_ID, PAGE_CICLO_ID, PAGE_SIMULADOR_ID],
        "activePageName": PAGE_PANORAMA_ID,
    }
    write_json(
        os.path.join(REPORT_DIR, "definition", "pages", "pages.json"), pages_meta
    )

    # PÁGINA 1: Panorama Ejecutivo
    p1_visuals = [
        make_header_banner(
            "p1hdr000000000000001",
            "Corte: Enero – Julio 2026 • Muestra: 183.911 adultos ponderados por FEX_C18 • Santiago Sandoval & Sebastián Ramos",
        ),
        make_page_navigator("p1nav000000000000002"),
        *make_slicers_row("p1"),
        make_kpi_card("p1kpi010000000000001", "Mediana Cuenta Propia", "MEDIANA CUENTA PROPIA", "#D97706", 24, 182, 359, 124, 1000),
        make_kpi_card("p1kpi020000000000002", "CV Cuenta Propia", "VOLATILIDAD INDEPENDIENTE (CV)", "#DC2626", 403, 182, 359, 124, 1010, fmt="0.00"),
        make_kpi_card("p1kpi030000000000003", "Brecha Mediana Indep vs Asal", "BRECHA MEDIANA VS. ASALARIADO", "#0F3D5E", 782, 182, 359, 124, 1020, fmt="+0.0%;-0.0%;0.0%"),
        make_kpi_card("p1kpi040000000000004", "Mediana Corredor Dorado", "CORREDOR DORADO (35–54 AÑOS)", "#15803D", 1161, 182, 359, 124, 1030),
        make_kpi_card("p1kpi050000000000005", "Dptos Indep Mas Estable", "DPTOS DONDE INDEP. ES MÁS ESTABLE", "#B45309", 1540, 182, 356, 124, 1040, fmt="0"),
        make_clustered_bar(
            "p1viz010000000000001",
            "1. Mediana de Ingreso por Sector Económico: Cuenta Propia vs. Asalariado",
            "SectorEconomico",
            [("Mediana Cuenta Propia", "#D97706"), ("Mediana Asalariado", "#0F3D5E")],
            24, 322, 926, 358, 2000,
        ),
        make_line_chart_measures(
            "p1viz020000000000002",
            "2. Trayectoria por Ciclo de Vida (Grupo de Edad): Cuenta Propia vs. Asalariado",
            "GrupoEdad",
            [("Mediana Cuenta Propia", "#D97706"), ("Mediana Asalariado", "#0F3D5E")],
            970, 322, 926, 358, 2010,
        ),
        make_bar_chart(
            "p1viz030000000000003",
            "3. Extremos Territoriales: Volatilidad Independiente (CV) por Departamento",
            "DPTO_Nombre",
            "CV Cuenta Propia",
            24, 696, 926, 362, 2020,
        ),
        make_scatter(
            "p1viz040000000000004",
            "4. Mapa Retorno vs. Riesgo por Sector (Mediana Cuenta Propia vs. CV)",
            "SectorEconomico",
            "CV Cuenta Propia",
            "Mediana Cuenta Propia",
            "Personas Analizadas",
            970, 696, 926, 362, 2030,
        ),
    ]
    build_page(PAGE_PANORAMA_ID, "1. Panorama Ejecutivo", p1_visuals)

    # PÁGINA 2: Ciclo de Vida, Estacionalidad y Brechas
    p2_visuals = [
        make_header_banner(
            "p2hdr000000000000001",
            "Corte: Enero – Julio 2026 • Diagnóstico Profundo: Matriz Sector × Edad, Serie Mensual y Composición Laboral",
        ),
        make_page_navigator("p2nav000000000000002"),
        *make_slicers_row("p2"),
        make_pivot(
            "p2viz010000000000001",
            "1. Matriz de Volatilidad Independiente (CV) y Mediana: Sector × Grupo de Edad",
            "SectorEconomico",
            "GrupoEdad",
            ["CV Cuenta Propia", "Mediana Cuenta Propia"],
            24, 184, 926, 430, 2000,
        ),
        make_line_chart_series(
            "p2viz020000000000002",
            "2. Dinámica Mensual (Enero – Julio 2026): Coeficiente de Variación por Modalidad",
            "MES",
            "TipoTrabajador",
            "Coef Variacion Ingreso",
            970, 184, 926, 430, 2010,
        ),
        make_clustered_column(
            "p2viz030000000000003",
            "3. Ingreso Medio Ponderado (FEX_C18) por Grupo de Edad: Independiente vs. Asalariado",
            "GrupoEdad",
            [("Ingreso Medio Cuenta Propia", "#D97706"), ("Ingreso Medio Asalariado", "#0F3D5E")],
            24, 630, 926, 428, 2020,
        ),
        make_donut(
            "p2viz040000000000004",
            "4. Distribución Poblacional Ponderada (FEX_C18): Independientes vs. Asalariados",
            "TipoTrabajador",
            "Poblacion Representada",
            970, 630, 926, 428, 2030,
        ),
    ]
    build_page(PAGE_CICLO_ID, "2. Ciclo de Vida y Brechas", p2_visuals)

    # PÁGINA 3: Simulador Ciudadano y Territorio
    p3_visuals = [
        make_header_banner(
            "p3hdr000000000000001",
            "Corte: Enero – Julio 2026 • Simulador de Bolsillo Ciudadano: Semáforo de Estabilidad y Colchón de Reserva",
        ),
        make_page_navigator("p3nav000000000000002"),
        *make_slicers_row("p3"),
        make_kpi_card("p3kpi010000000000001", "Semaforo Predictibilidad", "SEMÁFORO DE PREDICTIBILIDAD", "#15803D", 24, 182, 453, 124, 1000),
        make_kpi_card("p3kpi020000000000002", "Colchon Emergencia Sugerido", "COLCHÓN DE EMERGENCIA SUGERIDO", "#D97706", 497, 182, 453, 124, 1010),
        make_kpi_card("p3kpi030000000000003", "Nombre Departamento", "TERRITORIO ACTIVO", "#0F3D5E", 970, 182, 453, 124, 1020),
        make_kpi_card("p3kpi040000000000004", "Delta CV Indep vs Asal", "DIFERENCIAL DE VOLATILIDAD (ΔCV)", "#DC2626", 1443, 182, 453, 124, 1030, fmt="+0.00;-0.00;0.00"),
        make_clustered_bar(
            "p3viz010000000000001",
            "Comparativo Sectorial de Volatilidad (CV): Cuenta Propia vs. Asalariado",
            "SectorEconomico",
            [("CV Cuenta Propia", "#D97706"), ("CV Asalariado", "#0F3D5E")],
            24, 322, 680, 736, 2000,
        ),
        make_table(
            "p3viz020000000000002",
            "Simulador de Bolsillo Ciudadano: Perfiles por Sector, Edad y Departamento",
            ["SectorEconomico", "GrupoEdad", "DPTO_Nombre"],
            [
                "Mediana Cuenta Propia",
                "Mediana Asalariado",
                "CV Cuenta Propia",
                "Semaforo Predictibilidad",
                "Colchon Emergencia Sugerido",
            ],
            724, 322, 1172, 736, 2010,
        ),
    ]
    build_page(PAGE_SIMULADOR_ID, "3. Simulador Ciudadano", p3_visuals)


def main() -> None:
    update_semantic_model()
    write_custom_theme_and_report_json()
    build_all_pages()
    print("PBIP actualizado con exito: Base_Analisis.tmdl (183.911 filas + FEX_C18) + Tema + 3 Paginas PBIR.")


if __name__ == "__main__":
    main()
