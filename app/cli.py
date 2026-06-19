import typer
import uvicorn
from app.config import settings

app = typer.Typer()

@app.command()
def run(host: str = settings.APP_HOST, port: int = settings.APP_PORT):
    """Run the web server."""
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

@app.command()
def add_product():
    """Add a product via CLI (placeholder)."""
    typer.echo("Add product command - not implemented yet.")

@app.command()
def update_stock():
    """Update stock via CLI (placeholder)."""
    typer.echo("Update stock command - not implemented yet.")

@app.command()
def export_data():
    """Export data via CLI (placeholder)."""
    typer.echo("Export data command - not implemented yet.")

@app.command()
def backup_db():
    """Backup database (placeholder)."""
    typer.echo("Backup DB command - not implemented yet.")

@app.command()
def restore_db():
    """Restore database (placeholder)."""
    typer.echo("Restore DB command - not implemented yet.")

if __name__ == "__main__":
    app()
