from rich.console import Console
from sha256 import encode
from typing import List


def main() -> None:
    console: Console = Console()
    
    while True:
        inp: str = console.input("[bold][green]SHA256[/green][cyan]:$[/cyan][/bold] ")
        
        if inp.isspace() or not inp:
            return
        
        encoded: str = encode(inp)
        spaced_hex: List[str] = map("".join, zip(*[iter(encoded.hex())] * 8))
        
        for index, value in enumerate(spaced_hex):
            if index % 2 == 0:
                console.print(f"[bold blue]{value}[/bold blue]", end="")
            else:
                console.print(f"[blue]{value}[/blue]", end="")
        
        console.print("")

if __name__ == "__main__":
    main()