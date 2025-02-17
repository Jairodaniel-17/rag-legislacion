import os
import shutil
import time
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
name_vectorstore = "legislacion_COSINE"
vectorstore = VectorStoreManager(name=name_vectorstore, path=path)
llm_manager = LLMManager()


def interact_with_vectorstore(files_to_add: List[str], add_files: bool) -> None:
    """Interact with the vectorstore."""
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
            console.print("[bold purple]Contexto:[/bold purple]\n")
            console.print(context)
            respuesta_llm = llm_manager.generate_response_with_context(query, context)
            console.print("[bold purple]Respuesta:[/bold purple]\n")
            # Simular respuesta en vivo con velocidad constante de 128 caracteres*s
            respuesta = respuesta_llm
            chars_per_second = 128
            sleep_time = 1 / chars_per_second
            for char in respuesta:
                console.print(char, end="", style="bold green")
                time.sleep(sleep_time)
            console.print("\n")
        except Exception as e:
            logger.error(f"Error al realizar la consulta: {e}")
            console.print(f"[bold red]Error:[/bold red] {str(e)}")


def main() -> None:
    """Initialize and manage vector store operations.

    Initialize and manage a vector store for legal documents. It performs the
    following operations:
    1. Checks if vector store exists, creates it if not
    2. Compares existing files in the path with those in vector store
    3. Creates a table showing status of each file
    4. Initiates interaction with vector store for any new files

    The function runs in a loop until the vector store is properly initialized,
    then processes any new files found in the specified path.
    """
    while True:
        # limpiar la consola
        console.clear()
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

    table = Table(
        title="Estado de Archivos en el Vectorstore",
        caption=f"En total hay {len(lista_path)} archivos en el vectorstore '{name_vectorstore}'.",  # noqa: E501
    )
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
            fuente_sin_guion_bajo = os.path.splitext(fuente)[0].replace("_", " ").lower()
            fuente_sin_guion_bajo = (
                fuente_sin_guion_bajo[:100] + "..."
                if len(fuente_sin_guion_bajo) > 100
                else fuente_sin_guion_bajo
            )
            fuente_sin_guion_bajo = fuente_sin_guion_bajo.capitalize()
            table.add_row(
                fuente_sin_guion_bajo, "[green]Ya está en el vectorstore[/green]"
            )

    console.print(table)
    interact_with_vectorstore(files_to_add, bool(files_to_add))


if __name__ == "__main__":
    # limpar la ventana de la consola
    os.system("cls" if os.name == "nt" else "clear")
    if not os.path.exists(path):
        console.print(f"[bold yellow]Carpeta '{path}' no encontrada.[/bold yellow]")
        console.print(
            f"Coloque archivos en '{path}' [bold yellow](*.pdf, *.txt, *.docx, max 100MB)[/bold yellow]"  # noqa: E501
        )
        # se crea la carpeta para los archivos
        os.makedirs(path, exist_ok=True)
        os._exit(0)
    main()
