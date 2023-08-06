import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Props:
    """
    Class name: Props
    Pupose: Visualization of simple proportional charts

    Description:
        Class that holds lot of simple propositional chart functions to help developer(Data Analyst) on
        his data analyzation for proportional values

    Private Methods
    ----------
    __axes_parameter(ax=None)
        Sets the major axes parameters

    __description_row_calculator(dataset=None, column=None, max_char=None)
        Calculating the maximum rows needed fot the description to fit in


    """
    def __init__(self):
        """
        Variables
        ----------
        location_aspects : list[strings]
            four side location aspects denoting top, bottom, left and right

        title_locations : dict{loc: tuple(x, y, horizontal alignment)}
            locations of title text based on the input location
            tl - top left
            tr - top right
            bl - bottom left
            br - bottom right
        """
        self.location_aspects = ["top", "bottom", "left", "right"]
        self.title_locations = {
            "tl": (0, 1.1, "left"),
            "tr": (1, 1.1, "right"),
            "bl": (0, -0.1, "left"),
            "br": (1, -0.1, "right"),
        }

    def __axes_parameter(self, ax):
        """
        Sets the major axes parameters
        Basic parameters

        which includes,
        | aspect ratio
        | spines visibility
        | ticks visibility
        | axes limit setting
        :parameter ax: Axis of current chart
        :return: None
        """
        ax.set(adjustable='box', aspect='equal')
        for s in self.location_aspects:
            ax.spines[s].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    def __description_row_calculator(self, dataset, column, max_char):
        """
        Calculating the maximum rows needed for the description to fit right in
        This value is used in determining the locations of the title and description for the charts

        Update:
            Maximum character could be more dynamic, working on updates in that part to make it more effective
            Apologies in advance, If you can't find the right graph description

        :parameter dataset: Dataset (Major Component)
        :parameter column: String name (column name) of description colummn
        :parameter max_char: Maximum number of characters could fit in the sentance (Currently under development)
        :return max_row: Minimum number of rows
        """
        max_row = 0
        for index, row in dataset.iterrows():
            if len(row[column]) > max_char:
                temp = math.ceil(len(row[column]) / max_char)
                if temp > max_row:
                    max_row = temp
        return max_row

    def __get_title_location(self, loc, max_rows):
        """
        Location of title text in prop charts
        Individualized for different locations
        Based on the location given, the function returns the locations of title

        :parameter loc: location of the title text
                    "tl" - top left
                    "tr" - top right
        :parameter max_rows: Rows determined for description
                         Calculated from the private method "__description_row_calculator()"
        :return: list of location and alignment properties
                 [x, y, horizontal_alignment]
        """
        if loc == "tl":
            return [self.title_locations[loc][0], self.title_locations[loc][1] + max_rows / 10 + 0.05, "left"]
        elif loc == "tr":
            return [self.title_locations[loc][0], self.title_locations[loc][1] + max_rows / 10 + 0.05, "right"]

    def __get_description_location(self, loc, max_rows):
        """
        Location of description text in prop charts
        Individualized for different locations
        Based on the location given, the function returns the locations of description

        :parameter loc: location of the description text
                    "tl" - "top left"
                    "tr" - "top right"
                    "bl" - "bottom left"
                    "br" - "bottom right",
        :parameter max_rows: Rows determined for description
                         Calculated from the private method "__description_row_calculator()"
        :return: list of location and alignment properties
                 [x, y, horizontal_alignment]
        """
        if loc == "tl":
            return [self.title_locations[loc][0], self.title_locations[loc][1] + max_rows / 10 - 0.1 + 0.05, "left"]
        elif loc == "tr":
            return [self.title_locations[loc][0], self.title_locations[loc][1] + max_rows / 10 - 0.1 + 0.05, "right"]
        elif loc == "bl":
            return [self.title_locations[loc][0], self.title_locations[loc][1] - 0.1 + 0.05, "left"]
        elif loc == "bl":
            return [self.title_locations[loc][0], self.title_locations[loc][1] - 0.1 + 0.05, "right"]


    def __get_label_location(self, label, loc):
        """
        Location of prop labels in prop charts
        Individualized for different locations
        Based on the location given, the function returns the locations of labels

        :parameter label: Number to be shown (possibly integer, float)
        :parameter loc: location of the label text
                    "inc" - inner center
                    "inbl" - inner bottom left
                    "inbr" - inner bottom right
                    "intl" - inner top left
                    "intr" - inner top right
                    "outc" - outer center
                    "outtl" - outer top left
                    "outtr" - outer top right
        :return: list of location and alignment properties
                 [x, y, horizontal_alignment, vertical_alignment]
        """
        if loc == "inc":
            return [label / 2, label / 2, "center", "center"]
        if loc == "inbl":
            return [0, 0, "left", "bottom"]
        if loc == "inbr":
            return [label, 0, "right", "bottom"]
        if loc == "intl":
            return [0 + 0.02, label - 0.02, "left", "top"]
        if loc == "intr":
            return [label - 0.02, label - 0.02, "right", "top"]
        if loc=="outc":
            return [row[col]+0.05, row[col]+0.05, "left", "top"]
        if loc == "outtl":
            return [label - 0.05, label + 0.05, "right", "bottom"]
        if loc == "outtr":
            return [label + 0.05, label - 0.1, "left", "bottom"]

    def AreaProp(self, dataset, col, cols=8, labels=True, label_loc="inc", labelcolor="white", title=None, title_loc="tl", facecolor="black", bgcolor="#707070", description=None):
        """
        Square area proportional chart
        This function is used to create and customize almost everything in basic square area proportional chart
        Supports only for the percentages(proportions)
        The values of the columns should be between 0 and 1, which is considered as normal percentile.

        :parameter dataset: (pandas dataframe)
                        May hold a larger number of columns
                        including title, description and proportions
        :parameter col: (str)
                    Column name for which the proportions to be visualized
        :param cols: (int, default=8)
                     Number of proportion square columns for a single row
        :param labels: (bool, default=True)
                       Bool value denoting the labels visibility
                       True: Visible
                       False: Invisible
        :param label_loc: (str, default="inc" - inner center)
                          String deciding the location of labels in individual props

                          Valid locations,
                          "inc" - inner center
                          "inbl" - inner bottom left
                          "inbr" - inner bottom right
                          "intl" - inner top left
                          "intr" - inner top right
                          "outc" - outer center
                          "outtl" - outer top left
                          "outtr" - outer top right
        :param labelcolor: (str, default="white")
                            Color of the label
                            All hex values, and default color code in matplotlib are supported
        :param title: (str, default=None)
                      Column name of the dataset denoting the title of each prop
                      Each row should be associated with the proportions directly
        :param title_loc: (str, default="tl")
                          String deciding the location of labels in individual props

                          Valid locations,
                          "tl" - top left
                          "tr" - top right
        :param facecolor: (str, default="black")
                          Color of the square prop
                          All hex values, and default color code in matplotlib are supported
        :param bgcolor: (str, default="black")
                        Background color of the props
                        All hex values, and default color code in matplotlib are supported
        :param description: (str, default=None)
                            Column name of the dataset denoting the description of each prop
                            Each row should be associated with the proportions directly
        :return: A square area proportional chart
        """
        if len(dataset) > cols:
            rows = math.ceil(len(dataset) / cols)
        else:
            rows = 1
        fig = plt.figure(figsize=(18, 2 * rows))
        for index, row in dataset.iterrows():
            ax = fig.add_subplot(rows, cols, index + 1)
            ax.axvspan(0, 1, ymax=1, fc=bgcolor, alpha=0.2)
            ax.axvspan(0, row[col], ymax=row[col], fc=facecolor)
            if labels:
                label_locations_reset = self.__get_label_location(row[col], label_loc)
                ax.text(label_x, label_y, str(row[col] * 100) + "%", c=labelcolor, fontsize=8, ha=label_h_alignment, va=label_v_alignment)
            if description is None:
                if title is not None:
                    ax.text(title_locations[title_loc][0], title_locations[title_loc][1], row[title], fontweight="bold", ha=title_locations[title_loc][2])
            else:
                if title is None:
                    warnings.warn("Provide label column to get a better chart")
                else:
                    max_char = 10
                    max_des_rows = self.__description_row_calculator(dataset, description, max_char=max_char)
                    if title_loc == "tl" or title_loc == "tr":
                        title_locations_reset = self.__get_title_location(title_loc, max_des_rows)
                    else:
                        title_locations_reset = [title_locations[title_loc][0], title_locations[title_loc][1], title_locations[title_loc][2]]
                    ax.text(title_locations_reset[0], title_locations_reset[1], row[title], fontweight="bold", ha=title_locations_reset[2])
                    description_locations_reset = self.__get_description_location(title_loc, max_des_rows)
                    out_desc_list = [(row[description][i:i + max_char]) for i in range(0, len(row[description]), max_char)]
                    for i in out_desc_list:
                        ax.text(description_locations_reset[0], description_locations_reset[1], i, fontweight="normal", ha=description_locations_reset[2])
                        description_locations_reset = [description_locations_reset[0], description_locations_reset[1] - 0.1 + 0.05, description_locations_reset[2]]
            self.__axes_parameter(ax)
        plt.show();
