from enum import Enum


class ChartScale(Enum):
    ChartMinute = 'm'   # grouping data on 1 minute
    ChartHour = 'h'     # grouping data on 1 hour
    ChartDay = 'd'      # grouping data on 1 day
