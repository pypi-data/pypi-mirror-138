import os
from turtle import title

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prompt_toolkit import prompt
import typer
import yfinance as yf
from enum import Enum


app = typer.Typer()

ERROR = typer.style("ERROR:", fg=typer.colors.WHITE, bg=typer.colors.RED)
SUCCESS = typer.style("SUCCESS:", fg=typer.colors.WHITE, bg=typer.colors.GREEN)
VALID_PERIODS = ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]

@app.command()
def get_stock_data(
    stock: str = typer.Option(..., help="Stock to get from YF API", prompt="Please provide the ticker symbol here"),
    period: str = typer.Option("1y", help="Time period"),
    download: bool = typer.Option(False, help="Option to download dataset as csv"),
):

    if period not in VALID_PERIODS:
        typer.echo(f'{ERROR} Period is not valid!\nPlease select one of these: "1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"')
        raise typer.Exit()

    cwd = os.getcwd()
    image_folder = os.path.join(cwd, "images")
    data_folder = os.path.join(cwd, "data")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    if download and not os.path.exists(data_folder):
        os.makedirs(data_folder)

    df = yf.download(stock, group_by="Ticker", period=period)


    if df.empty:

        typer.echo(f"{ERROR} {stock} not found!")
        raise typer.Exit()

    typer.echo(f'{SUCCESS}: "Download SUCCESSful..."')
    df = df.reset_index(level=0)

    plot_df = df.plot(x="Date", y="Close", title=f"{stock} for {period}")
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
    stock: str = typer.Option(..., help="Stock to get from YF API", prompt="Please provide the ticker symbol here"),
    download: bool = typer.Option(
        False, help="Option to download dividend dataset as csv"
    ),
):

    cwd = os.getcwd()
    image_folder = os.path.join(cwd, "images")
    data_folder = os.path.join(cwd, "data")
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    if download and not os.path.exists(data_folder):
        os.makedirs(data_folder)

    df = yf.Ticker(stock)
    cwd = os.getcwd()
    image_folder = os.path.join(cwd, "images")
    dividends = df.dividends

    if isinstance(dividends, list):

        typer.echo(f"{ERROR} No dividend data available for {stock}")
        raise typer.Exit()

    plot_df = dividends.plot(x="Date", y="Dividends", title=f"Dividends for {stock}")
    fig = plot_df.get_figure()
    fig.savefig(f"{os.path.join(image_folder, stock + '_dividends')}.png")

    if download:
        dividends.to_csv(
            f"{os.path.join(data_folder, stock)}.csv", sep=";", decimal=","
        )
        typer.echo(
            f"{SUCCESS}: Dividend data for {stock} downloaded successfully.\nPlease check: {os.path.join(data_folder, stock)}.csv"
        )
