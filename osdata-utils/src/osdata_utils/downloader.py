import os
import geopandas as gpd
import rasterio
from shapely.geometry import Polygon
from osdatahub import FeaturesAPI, Extent
from pyproj import Transformer

class OSDataDownloader:
    def __init__(self, api_key):
        """
        Initialize the OSDataDownloader class.

        Parameters:
        - api_key: Your OS Data Hub API key.
        """
        self.api_key = api_key

    def get_tiff_metadata(self, tiff_path):
        """
        Extract metadata directly from a TIFF file.

        Parameters:
        - tiff_path: Path to the TIFF file.

        Returns:
        - metadata: Dictionary containing bounding box and CRS metadata.
        """
        with rasterio.open(tiff_path) as src:
            if src.crs is None:
                raise ValueError(f"The TIFF file {tiff_path} has no CRS information.")

            # Extract bounding box and CRS
            bounds = src.bounds
            crs = src.crs.to_string()

            return {
                "bounding_box": (bounds.left, bounds.bottom, bounds.right, bounds.top),
                "crs": crs,
                "image_name": os.path.basename(tiff_path),
            }

    def transform_bounding_box(self, bbox, from_crs, to_crs="EPSG:27700"):
        """
        Transforms a bounding box from one CRS to another.

        Parameters:
        - bbox: Tuple of (xmin, ymin, xmax, ymax) in the source CRS.
        - from_crs: Source CRS.
        - to_crs: Target CRS (default is EPSG:27700).

        Returns:
        - Transformed bounding box as (xmin, ymin, xmax, ymax).
        """
        transformer = Transformer.from_crs(from_crs, to_crs, always_xy=True)
        xmin, ymin = transformer.transform(bbox[0], bbox[1])
        xmax, ymax = transformer.transform(bbox[2], bbox[3])
        return (xmin, ymin, xmax, ymax)

    def initialize_features_api(self, product_name, extent="GB", crs="EPSG:27700"):
        """
        Initialize the Ordnance Survey FeaturesAPI client for the specified product.

        Parameters:
        - product_name: The open data product to access.
        - extent: The spatial extent to use (default is "GB" for Great Britain).
        - crs: The CRS for the extent (default is "EPSG:27700").

        Returns:
        - features_api: An initialized FeaturesAPI client.
        """
        if extent == "GB":
            extent_obj = Extent.from_predefined("GB")
        else:
            xmin, ymin, xmax, ymax = extent
            polygon = Polygon(
                [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)]
            )
            extent_obj = Extent(polygon, crs)

        features_api = FeaturesAPI(
            key=self.api_key, product_name=product_name, extent=extent_obj
        )
        return features_api

    def query_os_data(self, features_api, product_filter=None, type_filter=None):
        """
        Query Ordnance Survey open data using the FeaturesAPI client and filter by product name.

        Parameters:
        - features_api: An initialized FeaturesAPI client.
        - product_filter: The name of the OS open data product to filter.

        Returns:
        - gdf: GeoDataFrame with the queried data or None if no data is found.
        """
        response = features_api.query()
        if "features" not in response or not response["features"]:
            print("No data found for this bounding box.")
            return None

        gdf = gpd.GeoDataFrame.from_features(response["features"])
        if "geometry" not in gdf.columns:
            print("The API response does not include a 'geometry' column.")
            return None

        gdf = gdf.set_geometry("geometry")
        gdf.crs = "EPSG:27700"

        if product_filter:
            gdf = gdf[gdf["product"] == product_filter]
            if gdf.empty:
                print(
                    f"No data found for product '{product_filter}' within the extent."
                )
                return None

        if type_filter:
            gdf = gdf[gdf["Type"] == type_filter]
            if gdf.empty:
                print(f"No data found for Type '{type_filter}'.")
                return None

        return gdf

    def download_os_data(
        self,
        tiff_path,
        product_name,
        output_file=None,
        product_filter=None,
        type_filter=None,
    ):
        """
        Download Ordnance Survey open data for the specified TIFF and product.

        Parameters:
        - tiff_path: Path to the TIFF file.
        - product_name: The OS open data product to query.
        - output_file: Optional path to save the queried data.
        - product_filter: The name of the OS open data product to filter.
        - type_filter: Optional filter for the 'Type' column in the GeoDataFrame.

        Returns:
        - gdf: GeoDataFrame with the queried data or None if no data is found.
        """
        metadata = self.get_tiff_metadata(tiff_path)
        bbox_27700 = self.transform_bounding_box(
            metadata["bounding_box"], from_crs=metadata["crs"], to_crs="EPSG:27700"
        )

        features_api = self.initialize_features_api(
            product_name, extent=bbox_27700, crs="EPSG:27700"
        )
        gdf = self.query_os_data(features_api, product_filter, type_filter=type_filter)

        if gdf is not None and output_file:
            gdf.to_file(
                output_file,
                driver="GeoJSON"
                if output_file.endswith(".geojson")
                else "ESRI Shapefile",
            )

        return gdf