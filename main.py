import os
import shutil
from typing import List

from loguru import logger
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from llm.llm_manager import LLMManager
from vectorstore.vectorstore_manager import VectorStoreManager

logger.add("warnings.log", level="WARNING", format="{time} - {level} - {message}")
console = Console()

path = "derecho_files"
name_vectorstore = "legislacion"
vectorstore = VectorStoreManager(name=name_vectorstore, path=path)
llm_manager = LLMManager()


def interact_with_vectorstore(files_to_add: List[str], add_files: bool) -> None:
    if add_files:
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Añadiendo archivos al vectorstore...", total=len(files_to_add)
            )
            os.makedirs("temp", exist_ok=True)
            for file in files_to_add:
                shutil.copy(file, "temp")
            if vectorstore.add_list_files_vectorstore(path_files="temp"):
                progress.update(task, advance=len(files_to_add))
        console.print(
            "[bold green]Archivos añadidos correctamente al vectorstore.[/bold green]"
        )
        shutil.rmtree("temp")

    console.print("\n[bold cyan]Interacción con la base de datos vectorial[/bold cyan]")
    console.print("[bold green]Escribe tu consulta o 'exit' para salir.[/bold green]\n")

    while True:
        try:
            query = console.input("[bold yellow]Consulta > [/bold yellow]").strip()
            if query.lower() == "exit":
                console.print("[bold red]Saliendo de la interacción...[/bold red]")
                break
        except KeyboardInterrupt:
            console.print("[bold red]Saliendo de la interacción...[/bold red]")
            break

        try:
            context = vectorstore.search_similarity(query=query)
            respuesta_llm = llm_manager.generate_response_with_context(query, context)
            console.print(f"[bold green]Respuesta:[/bold green] {respuesta_llm}\n")
        except Exception as e:
            logger.error(f"Error al realizar la consulta: {e}")
            console.print(f"[bold red]Error:[/bold red] {str(e)}")


def main() -> None:
    while True:
        os.system("cls")
        console.print("[bold green]Hello from rag-legislacion![/bold green]")
        if not vectorstore.exist_vectorstore():
            console.print(
                f"[bold yellow]No se encontró el vectorstore '{name_vectorstore}'.[/bold yellow]"  # noqa: E501
            )
            console.print(
                f"Se procede a crear el vectorstore con los archivos en '{path}'."
            )
            vectorstore.create_vectorstore()
            console.print(
                f"[bold green]Vectorstore '{name_vectorstore}' creado correctamente.[/bold green]"  # noqa: E501
            )
        else:
            break

    lista_fuentes = {os.path.basename(fuente) for fuente in vectorstore.list_sources()}
    lista_path = os.listdir(path)

    table = Table(title="Estado de Archivos en el Vectorstore")
    table.add_column("Archivo", justify="left")
    table.add_column("Estado", justify="center")

    files_to_add = []
    for fuente in lista_path:
        if fuente not in lista_fuentes:
            table.add_row(fuente, "[yellow]Se añadirá[/yellow]")
            logger.warning(
                f"El archivo '{fuente}' no está en el vectorstore. Se procede a añadir."
            )
            files_to_add.append(os.path.join(path, fuente))
        else:
            table.add_row(fuente, "[green]Ya está en el vectorstore[/green]")

    console.print(table)
    interact_with_vectorstore(files_to_add, bool(files_to_add))


if __name__ == "__main__":
    if not os.path.exists(path):
        console.print(f"[bold yellow]Carpeta '{path}' no encontrada.[/bold yellow]")
        console.print(f"Coloque archivos en '{path}' [bold yellow](*.pdf, *.txt, *.docx, max 100MB)[/bold yellow]")  # noqa: E501
        os._exit(0)
    main()
