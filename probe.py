import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl

    df = pl.read_parquet("data/verkehrszaehlungen_werte_fussgaenger_velo_alle_jahre.parquet")
    print(df.columns)
    print(df.height, "rows")
    df.head()
    return df, pl


@app.cell
def _(df, pl):
    # FK_STANDORT is the site id. Does a site keep its coordinates (OST/NORD)?
    coords_per_site = (
        df.group_by("FK_STANDORT")
        .agg(pl.struct("OST", "NORD").n_unique().alias("n_coords"))
        .sort("n_coords", descending=True)
    )
    print(df["FK_STANDORT"].n_unique(), "sites")
    print((coords_per_site["n_coords"] > 1).sum(), "sites with more than one coordinate pair")
    coords_per_site
    return


@app.cell
def _(df, pl):
    # bike site = row has a VELO_IN or VELO_OUT value; year from DATUM
    bike = df.filter(pl.col("VELO_IN").is_not_null() | pl.col("VELO_OUT").is_not_null()).with_columns(
        pl.col("DATUM").str.slice(0, 4).cast(pl.Int32).alias("year")
    )
    sites_per_year = bike.group_by("year").agg(pl.col("FK_STANDORT").n_unique().alias("bike_sites")).sort("year")
    n_years = sites_per_year.height
    years_per_site = bike.group_by("FK_STANDORT").agg(pl.col("year").n_unique().alias("n_years"))
    n_all = years_per_site.height
    n_every = (years_per_site["n_years"] == n_years).sum()
    print(n_all, "bike sites in total,", n_every, "in every one of", n_years, "years:", round(100 * n_every / n_all, 1), "%")
    sites_per_year
    return (bike,)


@app.cell
def _(bike, pl):
    # per bike site: first year, last year, number of years it reports
    site_span = (
        bike.group_by("FK_STANDORT")
        .agg(
            pl.col("year").min().alias("first_year"),
            pl.col("year").max().alias("last_year"),
            pl.col("year").n_unique().alias("n_years"),
        )
        .with_columns((pl.col("last_year") - pl.col("first_year") + 1).alias("span"))
        .sort("first_year", "FK_STANDORT")
    )
    site_span
    return


@app.cell
def _(bike, pl):
    # coordinate pairs of the bike sites, and pairs shared by more than one site id
    bike_coords = bike.select("FK_STANDORT", "OST", "NORD").unique()
    print(bike_coords.select("OST", "NORD").unique().height, "distinct coordinate pairs for", bike_coords["FK_STANDORT"].n_unique(), "bike sites")
    shared_coords = (
        bike_coords.group_by("OST", "NORD")
        .agg(pl.col("FK_STANDORT").sort().alias("site_ids"), pl.len().alias("n_sites"))
        .filter(pl.col("n_sites") > 1)
        .sort("n_sites", descending=True)
    )
    shared_coords
    return


@app.cell
def _(bike, pl):
    # place = coordinate pair (OST, NORD), taken as is; complete years 2010-2025
    years_per_place = (
        bike.filter(pl.col("year").is_between(2010, 2025))
        .group_by("OST", "NORD")
        .agg(pl.col("year").n_unique().alias("n_years"))
        .sort("n_years", descending=True)
    )
    n_places = bike.select("OST", "NORD").unique().height
    n_places_every = (years_per_place["n_years"] == 16).sum()
    print(n_places_every, "of", n_places, "places report bikes in every year 2010-2025")
    years_per_place
    return


if __name__ == "__main__":
    app.run()
