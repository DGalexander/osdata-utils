from pyproj import Transformer
import geopandas as gpd

def transform_bounding_box(bbox, from_crs, to_crs):
    """
    Transforms a bounding box from one CRS to another.

    Parameters:
    - bbox: Tuple of (xmin, ymin, xmax, ymax) in the source CRS.
    - from_crs: Source CRS.
    - to_crs: Target CRS.

    Returns:
    - Transformed bounding box as (xmin, ymin, xmax, ymax).
    """
    transformer = Transformer.from_crs(from_crs, to_crs, always_xy=True)
    xmin, ymin = transformer.transform(bbox[0], bbox[1])
    xmax, ymax = transformer.transform(bbox[2], bbox[3])
    return xmin, ymin, xmax, ymax

def filter_gdf_by_column(gdf, column_name, value):
    """
    Filters a GeoDataFrame by a specific column value.

    Parameters:
    - gdf: Input GeoDataFrame.
    - column_name: The column to filter on.
    - value: The value to filter by.

    Returns:
    - Filtered GeoDataFrame.
    """
    if column_name not in gdf.columns:
        raise ValueError(f"Column '{column_name}' not found in GeoDataFrame.")
    return gdf[gdf[column_name] == value]

def merge_geodataframes(gdf_list):
    """
    Merges a list of GeoDataFrames into one.

    Parameters:
    - gdf_list: List of GeoDataFrames to merge.

    Returns:
    - Merged GeoDataFrame.
    """
    return gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))

def validate_crs(gdf, expected_crs):
    """
    Validates and optionally reprojects a GeoDataFrame to the expected CRS.

    Parameters:
    - gdf: Input GeoDataFrame.
    - expected_crs: The expected CRS.

    Returns:
    - GeoDataFrame reprojected to the expected CRS if necessary.
    """
    if gdf.crs is None:
        raise ValueError("GeoDataFrame has no CRS defined.")
    if not gdf.crs.equals(expected_crs):
        gdf = gdf.to_crs(expected_crs)
    return gdf