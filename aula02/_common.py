from __future__ import annotations

from pathlib import Path

import duckdb


def encontrar_raiz_projeto(start: Path | None = None) -> Path:
    """Encontra a raiz do projeto a partir do diretorio atual."""
    start = (start or Path.cwd()).resolve()
    for candidato in [start, *start.parents]:
        if (candidato / "aula02" / "_common.py").exists():
            return candidato
        if (candidato / "_common.py").exists() and candidato.name == "aula02":
            return candidato.parent
        if (candidato / "TODO.MD").exists() and (candidato / "exercicios").exists():
            return candidato
        filho = candidato / "sessao-02-data-architecture"
        if (filho / "TODO.MD").exists() and (filho / "exercicios").exists():
            return filho

    fallback = Path(
        "/Users/Vinicius_Ribeiro/repositories/bootcamp-delas-2026/sessao-02-data-architecture"
    )
    return fallback if fallback.exists() else start


def configurar_paths(project_root: str | None = None) -> dict[str, Path]:
    project = (
        Path(project_root).expanduser().resolve()
        if project_root
        else encontrar_raiz_projeto()
    )
    data_dir = project / "data"
    charts_dir = data_dir / "charts"
    runs_dir = data_dir / "runs"

    data_dir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)
    runs_dir.mkdir(parents=True, exist_ok=True)

    return {
        "PROJECT_ROOT": project,
        "DATA_DIR": data_dir,
        "CHARTS_DIR": charts_dir,
        "RUNS_DIR": runs_dir,
        "DB_PATH": data_dir / "hackerone.duckdb",
        "BRONZE_PARQUET": data_dir / "bronze_hackerone_reports.parquet",
        "RAW_CSV": data_dir / "raw_data.csv",
    }


def conectar_duckdb(db_path: Path) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(str(db_path))
    for ext in ["parquet", "json"]:
        try:
            con.execute(f"INSTALL {ext}; LOAD {ext};")
        except Exception:
            try:
                con.execute(f"LOAD {ext};")
            except Exception as exc:
                print(f"Extensao {ext} nao carregada: {exc}")
    return con
