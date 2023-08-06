import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer
import yfinance as yf

app = typer.Typer()


def make_data_and_image_folder(download):
    cwd = os.getcwd()
    image_folder = os.path.join(cwd, "images")
    data_folder = os.path.join(cwd, "data")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    if download and not os.path.exists(data_folder):
        os.makedirs(data_folder)


ERROR = typer.style("ERROR:", fg=typer.colors.WHITE, bg=typer.colors.RED)
SUCCESS = typer.style("SUCCESS:", fg=typer.colors.WHITE, bg=typer.colors.GREEN)


@app.command()
def get_stock_data(
    stock: str = typer.Option(..., help="Stock to get from YF API"),
    period: str = typer.Option("1y", help="Time period"),
    download: bool = typer.Option(False, help="Option to download dataset as csv"),
):

    make_data_and_image_folder(download=download)
    df = yf.download(stock, group_by="Ticker", period=period)
    typer.echo(f'{SUCCESS}: "Download SUCCESSful..."')
    df = df.reset_index(level=0)

    plot_df = df.plot(x="Date", y="Close")
    fig = plot_df.get_figure()
    fig.savefig(f"{os.path.join(image_folder, stock)}.png")

    typer.echo(
        f"{SUCCESS}: Plot for {stock} created successfully. Please check: {os.path.join(image_folder, stock)}.png"
    )

    if download:
        df.to_csv(f"{os.path.join(data_folder, stock)}.csv", sep=";", decimal=",")
        typer.echo(
            f"{SUCCESS}: Stock data for {stock} downloaded successfully.\n Please check: {os.path.join(data_folder, stock)}.csv"
        )


@app.command()
def get_dividends(
    stock: str = typer.Option(..., help="Stock to get from YF API"),
    download: bool = typer.Option(
        False, help="Option to download dividend dataset as csv"
    ),
):
    make_data_and_image_folder(download=download)

    df = yf.Ticker(stock)
    cwd = os.getcwd()
    image_folder = os.path.join(cwd, "images")
    dividends = df.dividends

    if isinstance(dividends, list):

        typer.echo(f"{ERROR} No dividend data available for {stock}")
        raise typer.Exit()

    plot_df = dividends.plot(x="Date", y="Dividends")
    fig = plot_df.get_figure()
    fig.savefig(f"{os.path.join(image_folder, stock + '_dividends')}.png")

    if download:
        dividends.to_csv(
            f"{os.path.join(data_folder, stock)}.csv", sep=";", decimal=","
        )
        typer.echo(
            f"{SUCCESS}: Dividend data for {stock} downloaded successfully.\nPlease check: {os.path.join(data_folder, stock)}.csv"
        )
