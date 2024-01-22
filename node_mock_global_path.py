"""Node that publishes the mock global path, represented by the `MockGlobalPath` class."""

import csv
import os
from datetime import datetime

import numpy as np
from _path import Path
from _helper_lat_lon import HelperLatLon
from coord_systems import GEODESIC, meters_to_km


def generate_path(
    dest: HelperLatLon,
    interval_spacing: float,
    pos: HelperLatLon,
    write: bool = False,
    file_path: str = "",
) -> Path:
    """Returns a path from the current GPS location to the destination point.
    Waypoints are evenly spaced along the path according to the interval_spacing parameter.
    Path does not include pos, but does include dest as the final element.

    If write is True, the path is written to a new csv file in the same directory as file_path,
    with the name of the original file, appended with a timestamp.

    Args:
        dest (list[HelperLatLon]): The destination point or partial path
        interval_spacing (float): The desired distance between waypoints on the path
        pos (HelperLatLon): The current GPS location
        write (bool, optional): Whether to write the path to a new csv file, default False
        file_path (str, optional): The filepath to the global path csv file, default empty

    Returns:
        Path: The generated path
    """
    global_path = Path()

    lat1 = pos.latitude
    lon1 = pos.longitude

    lat2 = dest.latitude
    lon2 = dest.longitude

    distance = meters_to_km(GEODESIC.inv(lats1=lat1, lons1=lon1, lats2=lat2, lons2=lon2)[2])

    # minimum number of waypoints to not exceed interval_spacing
    n = np.floor(distance / interval_spacing)
    n = max(1, n)

    # npts returns a path with neither pos nor dest included
    global_path_tuples = GEODESIC.npts(lon1=lon1, lat1=lat1, lon2=lon2, lat2=lat2, npts=n)
    
    # npts returns (lon,lat) tuples, its backwards for some reason
    for lon, lat in global_path_tuples:
        global_path.waypoints.append(HelperLatLon(latitude=lat, longitude=lon))

    # append the destination point
    global_path.waypoints.append(HelperLatLon(latitude=lat2, longitude=lon2))

    if write:
        write_to_file(file_path=file_path, global_path=global_path)
    print(len(global_path.waypoints))
    return global_path


def _interpolate_path(
    global_path: Path,
    interval_spacing: float,
    pos: HelperLatLon,
    path_spacing: list[float],
    write: bool = False,
    file_path: str = "",
) -> Path:
    """Interpolates and inserts subpaths between any waypoints which are spaced too far apart.

    Args:
        global_path (Path): The path to interpolate between
        interval_spacing (float): The desired spacing between waypoints
        pos (HelperLatLon): The current GPS location
        path_spacing (list[float]): The distances between pairs of points in global_path
        write (bool, optional): Whether to write the path to a new csv file, default False
        file_path (str, optional): The filepath to the global path csv file, default empty

    Returns:
        Path: The interpolated path
    """

    waypoints = [pos] + global_path.waypoints

    i, j = 0, 0
    while i < len(path_spacing):
        if path_spacing[i] > interval_spacing:
            # interpolate a new sub path between the two waypoints
            pos = waypoints[j]
            dest = waypoints[j + 1]

            sub_path = generate_path(
                dest=dest,
                interval_spacing=interval_spacing,
                pos=pos,
            )
            # insert sub path into path
            waypoints[j + 1 : j + 1] = sub_path.waypoints[:-1]
            # shift indices to account for path insertion
            j += len(sub_path.waypoints) - 1

        i += 1
        j += 1
    # remove pos from waypoints again
    waypoints.pop(0)

    global_path.waypoints = waypoints

    if write:
        write_to_file(file_path=file_path, global_path=global_path)

    return global_path


def calculate_interval_spacing(pos: HelperLatLon, waypoints: list[HelperLatLon]) -> list[float]:
    """Returns the distances between pairs of points in a list of latitudes and longitudes,
    including pos as the first point.

    Args:
        pos (HelperLatLon): The gps position of the boat
        waypoints (list[HelperLatLon]): The list of waypoints

    Returns:
        list[float]: The distances between pairs of points in waypoints [km]
    """
    all_coords = [(pos.latitude, pos.longitude)] + [
        (waypoint.latitude, waypoint.longitude) for waypoint in waypoints
    ]

    coords_array = np.array(all_coords)

    lats1, lons1 = coords_array[:-1].T
    lats2, lons2 = coords_array[1:].T

    distances = GEODESIC.inv(lats1=lats1, lons1=lons1, lats2=lats2, lons2=lons2)[2]

    distances = [meters_to_km(distance) for distance in distances]

    return distances


def write_to_file(file_path: str, global_path: Path, tmstmp: bool = True) -> Path:
    """Writes the global path to a new, timestamped csv file.

    Args
        file_path (str): The filepath to the global path csv file
        global_path (Path): The global path to write to file
        tmstmp (bool, optional): Whether to append a timestamp to the file name, default True

    Raises:
        ValueError: If file_path is not to an existing `global_paths` directory
    """

    # check if file_path is a valid file path
    if not os.path.isdir(os.path.dirname(file_path)):
        raise ValueError(f"Invalid file path: {file_path}")

    if tmstmp:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dst_file_path = file_path.removesuffix(".csv") + f"_{timestamp}.csv"
    else:
        dst_file_path = file_path

    with open(dst_file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["latitude", "longitude"])
        for waypoint in global_path.waypoints:
            writer.writerow([waypoint.latitude, waypoint.longitude])


def path_to_dict(path: Path, num_decimals: int = 4) -> dict[int, str]:
    """Converts a Path msg to a dictionary suitable for printing.

    Args:
        path (Path): The Path msg to be converted.
        num_decimals (int, optional): The number of decimal places to round to, default 4.

    Returns:
        dict[int, str]: Keys are the indices of the formatted latlon waypoints.
    """
    return {
        i: f"({waypoint.latitude:.{num_decimals}f}, {waypoint.longitude:.{num_decimals}f})"
        for i, waypoint in enumerate(path.waypoints)
    }

