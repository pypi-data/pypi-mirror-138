import math
import numpy as np
from collections import defaultdict
import random
import pandas as pd

class Mixin:
    def get_radial_coordinates(
        self,
        x_center,
        y_center,
        inner_padding,
        dataset_column_count,
        dataset_row_count,
        current_column,
        current_row,
        disc_radius,
    ):
        """
        Compute target position coordinates of a datapoint on the
        radial representation

        :return: tuple containing the target position of the datapoint
        on the radial representation.
        """

        #  define the elevation of the pixel based on it's column in the dataset 
        # (if first column, the outer it will be)
        elevation = (
            (current_column / dataset_column_count) * disc_radius
        ) + inner_padding
        initial_coordinates = (0, elevation)

        #  define the rotation of the coordinates based 
        # on the location of the datapoint in the rows
        rotation_angle = (current_row / dataset_row_count) * (math.pi * 2)

        #  preform rotation of coordinates with an angle = to rotation angle
        new_coordinates = (
            initial_coordinates[0] * math.cos(rotation_angle)
            - initial_coordinates[1] * math.sin(rotation_angle),
            initial_coordinates[0] * math.sin(rotation_angle)
            + initial_coordinates[1] * math.cos(rotation_angle),
        )

        # x' = x*cos(angle) - y*sin(angle)
        # y' = x*sin(angle) + y*cos(angle)

        radial_coordinates = (
            new_coordinates[0] + x_center,
            new_coordinates[1] + y_center,
        )

        return radial_coordinates

    def get_square_radial_coordinates(
        self,
        x_center,
        y_center,
        inner_padding,
        dataset_column_count,
        dataset_row_count,
        current_column,
        current_row,
        disc_radius,
        glyph_size,
    ):
        """
        Compute target position coordinates of each square point on the
        radial representation

        return: array of tuples containing the target position of each point in the square
        """

        # Properties of the square
        square_height = glyph_size[0]
        square_width = glyph_size[1]

        #  define the elevation of the glyph based on it's column 
        # in the dataset (if first column, the outer it will be
        elevation = (
            (current_column / dataset_column_count) * disc_radius
        ) + inner_padding
        initial_coordinates = (0, elevation)

        #  the square has 4 points , 1,2,3,4
        initial_coordinates = []
        initial_coordinates.append((square_width / 2, elevation + (square_height / 2)))
        initial_coordinates.append((-square_width / 2, elevation + (square_height / 2)))
        initial_coordinates.append((-square_width / 2, elevation - (square_height / 2)))
        initial_coordinates.append((square_width / 2, elevation - (square_height / 2)))

        # these square points are rotated depending on the location of the datapoint.

        #  define the rotation of the coordinates based on the location of the datapoint in the rows
        rotation_angle = (current_row / dataset_row_count) * (math.pi * 2)

        #  preform rotation of coordinates with an angle = to rotation angle
        new_coordinates = []
        for current_coordinates in initial_coordinates:
            new_coordinates.append(
                (
                    current_coordinates[0] * math.cos(rotation_angle)
                    - current_coordinates[1] * math.sin(rotation_angle),
                    current_coordinates[0] * math.sin(rotation_angle)
                    + current_coordinates[1] * math.cos(rotation_angle),
                )
            )

        # x' = x*cos(angle) - y*sin(angle)
        # y' = x*sin(angle) + y*cos(angle)

        radial_coordinates = []
        for current_radial_coordinates in new_coordinates:
            radial_coordinates.append(
                (
                    current_radial_coordinates[0] + x_center,
                    current_radial_coordinates[1] + y_center,
                )
            )

        return radial_coordinates

    def get_polygon_radial_coordinates(
        self,
        x_center,
        y_center,
        inner_padding,
        dataset_column_count,
        dataset_row_count,
        current_column,
        current_row,
        disc_radius,
        glyph_size,
    ):
        """
        Compute target position coordinates of each polygon point on the
        radial representation

        :return: array of tuples containing the target position of each point in the polygon
        """

        bitmap_width = dataset_column_count
        bitmap_height = dataset_row_count

        #  define the distance between two rows on the disc
        interrow_distance = (disc_radius - inner_padding) / (bitmap_width)

        #  the polygon will be made of 4 points.
        #  compute the distance between the two higher points
        #  radius @ height + 1/2 interrow distance.
        circle_radius = (
            ((current_column / bitmap_width) * disc_radius) + inner_padding
        ) + (0.5 * interrow_distance)
        current_row_perimeter = 2 * math.pi * circle_radius
        inter_glyph_distance_top = current_row_perimeter / bitmap_height

        #  compute the distance between the two lower points
        #  radius @ height - 1/2 interrow distance.
        circle_radius = (
            ((current_column / bitmap_width) * disc_radius) + inner_padding
        ) - (0.5 * interrow_distance)
        current_row_perimeter = 2 * math.pi * circle_radius
        inter_glyph_distance_bottom = current_row_perimeter / bitmap_height

        #  properties of the square
        square_height = interrow_distance
        square_width_top = inter_glyph_distance_top
        square_width_bottom = inter_glyph_distance_bottom

        #  define the elevation of the glyph based on it's column in the dataset (if first column, the outer it will be
        elevation = (
            (current_column / dataset_column_count) * disc_radius
        ) + inner_padding
        initial_coordinates = (0, elevation)

        #  the square has 4 points , 1,2,3,4
        initial_coordinates = []
        initial_coordinates.append(
            (square_width_top / 2, elevation + (square_height / 2))
        )
        initial_coordinates.append(
            (-square_width_top / 2, elevation + (square_height / 2))
        )
        initial_coordinates.append(
            (-square_width_bottom / 2, elevation - (square_height / 2))
        )
        initial_coordinates.append(
            (square_width_bottom / 2, elevation - (square_height / 2))
        )

        # these square points are rotated depending on the location of the datapoint.

        #  define the rotation of the coordinates based on the location of the datapoint in the rows
        rotation_angle = (current_row / dataset_row_count) * (math.pi * 2)

        #  perform rotation of coordinates with an angle = to rotation angle
        new_coordinates = []
        for current_coordinates in initial_coordinates:
            new_coordinates.append(
                (
                    current_coordinates[0] * math.cos(rotation_angle)
                    - current_coordinates[1] * math.sin(rotation_angle),
                    current_coordinates[0] * math.sin(rotation_angle)
                    + current_coordinates[1] * math.cos(rotation_angle),
                )
            )

        # x' = x*cos(angle) - y*sin(angle)
        # y' = x*sin(angle) + y*cos(angle)

        radial_coordinates = []
        for current_radial_coordinates in new_coordinates:
            radial_coordinates.append(
                (
                    current_radial_coordinates[0] + x_center,
                    current_radial_coordinates[1] + y_center,
                )
            )

        return radial_coordinates

    def processDataFrame2Bitmap(self, dataset_df):
        """
        Convert a dataframe into a bitmap with the same shape.

        :return: an opencv rgb bitmap
        """

        #  2 Read the dataset specs
        print("Number of rows", dataset_df.shape[0])
        print("Number of columns", dataset_df.shape[1])

        #  3 define the size of the bitmap
        bitmap_width = dataset_df.shape[1]
        bitmap_height = dataset_df.shape[0]
        datapoint_count = bitmap_height * bitmap_width

        print("Datapoints to display:", datapoint_count)

        #  4 initialize the image in memory
        print("create image")
        current_bitmap_opencv = np.zeros((bitmap_height, bitmap_width, 3), np.uint8)

        #  5 process each column data, and fill the bitmap with dynamic colors

        #  for each dataset column, detect the id and the type. if float, then populate the corresponding pixels on the bitmap applying a simple normalisation.
        for id, current_column in enumerate(dataset_df.columns):

            print(id, current_column)

            # if column is empty, fill it with 0
            if len(dataset_df[current_column].value_counts()) == 0:
                print("empty column")
                dataset_df[current_column] = 0

            if (
                dataset_df[current_column].dtypes == "float64"
                or dataset_df[current_column].dtypes == "int64"
            ):

                if dataset_df[current_column].dtypes == "float64":
                    colorTint = (0.5, 0.5, 1.0)  # red for floats
                if dataset_df[current_column].dtypes == "int64":
                    colorTint = (1.0, 0.5, 0.5)  # blue for integers

                #  get the min, max
                column_min = dataset_df[current_column].min()
                column_max = dataset_df[current_column].max()

                if dataset_df[current_column].dtypes == "float64":
                    dataset_df[current_column].fillna(0.0, inplace=True)
                if dataset_df[current_column].dtypes == "int64":
                    dataset_df[current_column].fillna(0, inplace=True)

                #  get the dataseries

                if (column_max - column_min) == 0:
                    column_data = dataset_df[current_column]
                else:
                    column_data = (dataset_df[current_column] - column_min) / (
                        column_max - column_min
                    )

                # coerce column data to integer in rare cases of ValueError
                try:
                    column_data_rgb = [
                        (
                            int(round(x * 255 * colorTint[0])),
                            int(round(x * 255 * colorTint[1])),
                            int(round(x * 255 * colorTint[2])),
                        )
                        for x in column_data
                    ]

                except ValueError:
                    column_data = pd.to_numeric(column_data, errors="coerce")
                    column_data.fillna(value=0, inplace=True)

                    column_data_rgb = [
                        (
                            int(round(x * 255 * colorTint[0])),
                            int(round(x * 255 * colorTint[1])),
                            int(round(x * 255 * colorTint[2])),
                        )
                        for x in column_data
                    ]

                # write the pixels
                for current_pixel in range(0, bitmap_height):
                    current_bitmap_opencv[current_pixel, id] = [
                        column_data_rgb[current_pixel][2],
                        column_data_rgb[current_pixel][1],
                        column_data_rgb[current_pixel][0],
                    ]

            elif dataset_df[current_column].dtypes == "object":

                colorTint = (0.5, 1.0, 0.5)

                #  remove the nan and replace it with zero. (it's not an object for sure..)
                dataset_df[current_column].fillna(0, inplace=True)
                #  get the modalities.
                column_labels = set(dataset_df[current_column].values.tolist())

                # attribute colors to each modality
                modalities_color_dict = defaultdict()
                for current_label in column_labels:
                    modalities_color_dict[current_label] = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )

                #  get the dataseries
                dataset_df[current_column].fillna(0, inplace=True)
                column_data = dataset_df[current_column].values.tolist()
                column_data_rgb = [
                    (
                        modalities_color_dict[x][0],
                        modalities_color_dict[x][1],
                        modalities_color_dict[x][2],
                    )
                    for x in column_data
                ]

                # write the pixels
                for current_pixel in range(0, bitmap_height):
                    current_bitmap_opencv[current_pixel, id] = [
                        column_data_rgb[current_pixel][2],
                        column_data_rgb[current_pixel][1],
                        column_data_rgb[current_pixel][0],
                    ]
            else:
                print("Column type unknown")

        return current_bitmap_opencv

    def computeDotGlyphRadius(
        self,
        current_pixel_row,
        bitmap_width,
        bitmap_height,
        radial_render_radius,
        radial_render_inner_padding,
    ):
        """
        Compute the expected radius of a dot based on it's position in the circle
        """

        #  compute the radius of a datapoint
        circle_radius = (
            (current_pixel_row / bitmap_width) * radial_render_radius
        ) + radial_render_inner_padding
        current_row_perimeter = 2 * math.pi * circle_radius
        radial_render_circle_radius = (current_row_perimeter / bitmap_height) / 2

        #  compute the distance between two circles
        interrow_distance = (radial_render_radius - radial_render_inner_padding) / (
            bitmap_width
        )
        interrow_distance = (
            interrow_distance / 2
        )  # divide by two as two datapoint circles share the distance

        #  if the radius must not be superior to the distance to prevent overlap
        if radial_render_circle_radius > interrow_distance:
            radial_render_circle_radius = interrow_distance

        return radial_render_circle_radius

    def computeSquareGlyphSize(
        self,
        current_pixel_row,
        bitmap_width,
        bitmap_height,
        radial_render_radius,
        radial_render_inner_padding,
    ):
        """
        Compute the expected size of a square based on it's position in the circle
        """

        circle_radius = (
            (current_pixel_row / bitmap_width) * radial_render_radius
        ) + radial_render_inner_padding
        current_row_perimeter = 2 * math.pi * circle_radius
        inter_glyph_distance = (current_row_perimeter / bitmap_height) / 2
        glyph_width = inter_glyph_distance
        glyph_height = glyph_width

        glyph_size = [glyph_width, glyph_height]

        interrow_distance = (
            (radial_render_radius - radial_render_inner_padding) / (bitmap_width) / 2
        )
        print(interrow_distance)

        #  the height must not be superior to the distance to prevent overlap
        if glyph_height > interrow_distance:
            glyph_size[0] = interrow_distance
            glyph_size[1] = interrow_distance

        return glyph_size

    def computePolygonGlyphShape(
        self,
        current_pixel_row,
        bitmap_width,
        bitmap_height,
        radial_render_radius,
        radial_render_inner_padding,
    ):
        """
        Compute the expected size of a 4 vertex polygon based on  it's position in the circle
        """
        #  define the distance between two rows on the disc
        interrow_distance = (radial_render_radius - radial_render_inner_padding) / (
            bitmap_width
        )

        circle_radius = (
            (current_pixel_row / bitmap_width) * radial_render_radius
        ) + radial_render_inner_padding
        current_row_perimeter = 2 * math.pi * circle_radius
        inter_glyph_distance = current_row_perimeter / bitmap_height
        glyph_width = inter_glyph_distance
        glyph_height = glyph_width

        glyph_size = [glyph_width, glyph_height]

        #  the height must not be superior to the distance to prevent overlap
        if glyph_height > interrow_distance:
            glyph_size[0] = interrow_distance
            glyph_size[1] = interrow_distance

        return glyph_size
