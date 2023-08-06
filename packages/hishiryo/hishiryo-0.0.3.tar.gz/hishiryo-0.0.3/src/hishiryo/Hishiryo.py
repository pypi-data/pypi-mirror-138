import math
import numpy as np
from typing import Any, Tuple, Union


import pandas as pd

import cv2

from hishiryo import _toolbox


class Hishiryo(_toolbox.Mixin):
    def __init__(self):
        """Constructor, setup of default parameters"""

        # color of the output picture background
        self.config_background_color = (0, 0, 0)
        # radius of the rendered circle (in pixels)
        self.radial_render_radius = 2000
        # define the padding size outside the circle
        self.radial_render_outer_padding = int(self.radial_render_radius * 0.05)
        # define the padding size inside the circle
        self.radial_render_inner_padding = int(self.radial_render_radius * 0.4)

    def convertCSVToBitmap(self, input_dataset_path, output_image_path, separator):
        """
        Convert an input csv file into a simple bitmap and save it on disk
        """
        #  load the dataset
        dataset_df = pd.read_csv(input_dataset_path, sep=separator,low_memory=True)

        #  convert it to bitmap
        current_bitmap = Hishiryo.processDataFrame2Bitmap(self, dataset_df)

        # write bitmap on disk
        cv2.imwrite(output_image_path, current_bitmap)

        return True

    def convertCSVToRadialBitmap(
        self,
        input_dataset_path,
        separator,
        output_image_radial_opencv_render_path,
        radius=None,
        sort_by=None,
        glyph_type="Polygon",
    ):
        """
        Convert an input csv file into a radial bitmap and save it on disk
        """

        #  load the dataset
        dataset_df = pd.read_csv(input_dataset_path, sep=separator)

        #  check if a radius is defined by the user
        if radius:
            self.radial_render_radius = radius
            self.radial_render_outer_padding = int(self.radial_render_radius * 0.05)
            self.radial_render_inner_padding = int(self.radial_render_radius * 0.4)
            self.radial_render_circle_radius = 0.2

        #  check if a sort is required by user
        if sort_by:
            dataset_df.sort_values(
                by=sort_by, ascending=False, na_position="first", inplace=True
            )

        #  convert it to bitmap and keep it in memory
        print(dataset_df.shape)
        current_bitmap = Hishiryo.processDataFrame2Bitmap(self, dataset_df)

        bitmap_width = dataset_df.shape[1]
        bitmap_height = dataset_df.shape[0]

        #  render the radial bitmap

        #  compute origin coordinates / center of the disk
        radial_render_width = (
            self.radial_render_radius * 2
            + self.radial_render_outer_padding * 2
            + self.radial_render_inner_padding * 2
        )
        radial_render_height = (
            self.radial_render_radius * 2
            + self.radial_render_outer_padding * 2
            + self.radial_render_inner_padding * 2
        )
        radial_render_origin_coordinates = (
            int(round(radial_render_width / 2)),
            int(round(radial_render_height / 2)),
        )

        #  initialize the rendered opencv bitmap
        opencv_image = np.zeros(
            (radial_render_width, radial_render_height, 3), np.uint8
        )
        opencv_image[:, :, 0] = self.config_background_color[0]
        opencv_image[:, :, 1] = self.config_background_color[1]
        opencv_image[:, :, 2] = self.config_background_color[2]

        #  start open cv rendering
        #  parse all the pixels of the bitmap in memory and map them to the radial svg image

        #  transpose to manage more easily the bitmap data
        # (a dataset often have less column than rows, the radial representation
        # should put columnar data as contour of a circle
        for current_pixel_row in range(0, bitmap_width):

            print("Render CSV Column:", current_pixel_row)

            # compute glyph radius if we use dot glyph
            if glyph_type == "Dot":
                # compute the perimeter of the circle, check how many datapoint on the circle, divide to obtain de diameter, divide by two for the radius of the glyph
                radial_render_circle_radius = Hishiryo.computeDotGlyphRadius(
                    self,
                    current_pixel_row,
                    bitmap_width,
                    bitmap_height,
                    self.radial_render_radius,
                    self.radial_render_inner_padding,
                )
                print("Glyph Estimated:", radial_render_circle_radius)

            # compute glyph size (witdh & weight) if we use dot Square
            if glyph_type == "Square":
                glyph_size = Hishiryo.computeSquareGlyphSize(
                    self,
                    current_pixel_row,
                    bitmap_width,
                    bitmap_height,
                    self.radial_render_radius,
                    self.radial_render_inner_padding,
                )
                print("Glyph Size:", glyph_size)

            # compute glyph size (witdh & weight) if we use dot Square
            if glyph_type == "Polygon":
                glyph_shape = Hishiryo.computePolygonGlyphShape(
                    self,
                    current_pixel_row,
                    bitmap_width,
                    bitmap_height,
                    self.radial_render_radius,
                    self.radial_render_inner_padding,
                )
                print("Glyph Size:", glyph_shape)

            for current_pixel_column in range(0, bitmap_height):

                if glyph_type == "Dot":

                    current_radial_coordinates = Hishiryo.get_radial_coordinates(
                        self,
                        radial_render_origin_coordinates[0],
                        radial_render_origin_coordinates[1],
                        self.radial_render_inner_padding,
                        bitmap_width,
                        bitmap_height,
                        current_pixel_row,
                        current_pixel_column,
                        self.radial_render_radius,
                    )
                    #  get pixel color
                    pixel_color = current_bitmap[
                        current_pixel_column, current_pixel_row
                    ]

                    #  create a disc for each pixel.
                    cv2.circle(
                        opencv_image,
                        (
                            int(current_radial_coordinates[0]),
                            int(current_radial_coordinates[1]),
                        ),
                        int(radial_render_circle_radius),
                        (int(pixel_color[2]), int(pixel_color[1]), int(pixel_color[0])),
                        thickness=-1,
                        lineType=8,
                        shift=0,
                    )

                if glyph_type == "Square":

                    radial_render_circle_radius = 1
                    current_square_radial_coordinates = (
                        Hishiryo.get_square_radial_coordinates(
                            self,
                            radial_render_origin_coordinates[0],
                            radial_render_origin_coordinates[1],
                            self.radial_render_inner_padding,
                            bitmap_width,
                            bitmap_height,
                            current_pixel_row,
                            current_pixel_column,
                            self.radial_render_radius,
                            glyph_size,
                        )
                    )

                    # get pixel color
                    pixel_color = current_bitmap[
                        current_pixel_column, current_pixel_row
                    ]
                    # print(pixel_color)

                    current_square_radial_coordinates = np.array(
                        current_square_radial_coordinates, np.int32
                    )
                    cv2.fillPoly(
                        opencv_image,
                        [current_square_radial_coordinates],
                        (int(pixel_color[2]), int(pixel_color[1]), int(pixel_color[0])),
                        lineType=0,
                        shift=0,
                    )

                if glyph_type == "Polygon":

                    radial_render_circle_radius = 1
                    current_square_radial_coordinates = (
                        Hishiryo.get_polygon_radial_coordinates(
                            self,
                            radial_render_origin_coordinates[0],
                            radial_render_origin_coordinates[1],
                            self.radial_render_inner_padding,
                            bitmap_width,
                            bitmap_height,
                            current_pixel_row,
                            current_pixel_column,
                            self.radial_render_radius,
                            glyph_shape,
                        )
                    )
                    # get pixel color
                    pixel_color = current_bitmap[
                        current_pixel_column, current_pixel_row
                    ]

                    current_square_radial_coordinates = np.array(
                        current_square_radial_coordinates, np.int32
                    )
                    cv2.fillPoly(
                        opencv_image,
                        [current_square_radial_coordinates],
                        (int(pixel_color[2]), int(pixel_color[1]), int(pixel_color[0])),
                        lineType=0,
                        shift=0,
                    )

        #  write images to disk
        print("write radial opencv image")
        #  out_resized = cv2.resize(opencv_image,None, fx=0.5, fy=0.5,interpolation = cv2.INTER_AREA)
        cv2.imwrite(output_image_radial_opencv_render_path, opencv_image)

        return True
