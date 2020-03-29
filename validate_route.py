#!/usr/bin/env python3
from argparse import ArgumentParser
import logging

from gps import GpsRoute


def main():
    # Define and parse script arguments
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file", dest="source_data",
        help="source data point file", default="data/data_points.csv"
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose_mode",
        help="set verbose logging", default=False
    )
    parser.add_argument(
        "-o", "--output", dest="output_file",
        help="data point output path", default="data/pruned_data_points.csv"
    )
    args = parser.parse_args()
    source_data = args.source_data
    output_path = args.output_file
    if args.verbose_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Process source data
    route = GpsRoute()
    route.read_nodes_from_csv(source_data)
    logging.info(f"Parsed {len(route.node_list)} data points from file {source_data}")

    # Prune outlier data points
    removal_count = route.prune_outlier_nodes()
    logging.info(f"Removed {removal_count} invalid gps nodes")

    # Write new pruned Gps data points to disk
    route.write_to_csv(output_path)
    logging.info(f"Wrote pruned GPS data to {output_path}")


if __name__ == '__main__':
    main()
