import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt


class BaseBuilder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @property
    @abstractmethod
    def weather(self) -> None:
        pass

    @abstractmethod
    def change_dtypes(self, col_name: str, to_col_dtype: str) -> None:
        pass

    @abstractmethod
    def remove_duplicated(self) -> None:
        pass

    @abstractmethod
    def drop_columns(self, cols=None) -> None:
        pass

    @abstractmethod
    def convert_multilabel_encoding(self, col: str) -> None:
        pass

    @abstractmethod
    def convert_categorical_ohe(self, cols=None) -> None:
        pass

    @abstractmethod
    def convert_categorical_le(self, cols=None) -> None:
        pass

    @abstractmethod
    def convert_numerical_encoding(self, enc, cols=None) -> None:
        pass

    @abstractmethod
    def convert_cat2num_infer(self, enc, cols=None) -> None:
        pass

    @abstractmethod
    def check_missing_values(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def remove_col_white_space_l(self, col: str) -> None:
        pass

    @abstractmethod
    def remove_col_white_space_r(self, col: str) -> None:
        pass

    @abstractmethod
    def remove_col_white_space_all(self, col: str) -> None:
        pass

    @abstractmethod
    def convert_to_datetime(self, col: str) -> None:
        pass

    @abstractmethod
    def add_year_month_day_feats(self, col: str) -> None:
        pass

    @abstractmethod
    def add_hour_feat(self, col: str) -> None:
        pass

    @abstractmethod
    def add_day_of_week_feat(self, col: str) -> None:
        pass

    @abstractmethod
    def convert_string_to_set(self, col: str) -> None:
        pass

    @abstractmethod
    def add_season_feat(self, col: str) -> None:
        pass


class WeatherData:
    def __init__(self, df: pd.DataFrame = None):
        self.df = df
        # self.win_size = kwargs.get('win_size') if kwargs.get('win_size') else None

    @staticmethod
    def display_corr(df: pd.DataFrame = None, win_size: tuple[float, float] = (20, 16)) -> None:
        """
        display the corr of dataset
        Args:
            df: DataFrame
            win_size: tuple, display size of window
        Returns:

        """
        plt.figure(figsize=win_size)
        # plotting correlation heatmap
        sns.heatmap(df.corr(), cmap="coolwarm", annot=True)

        # displaying heatmap
        plt.show()


class ConcreteBuilderWeather(BaseBuilder, ABC):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self, df: pd.DataFrame = None) -> None:
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self._weather = WeatherData(df)
        # self.reset()

    # def reset(self) -> None:
    #     self._weather = WeatherData(self._df)

    @property
    def weather(self) -> WeatherData:
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different products that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another product.
        That's why it's a usual practice to call the reset method at the end of
        the `getProduct` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        return self._weather

    def change_dtypes(self, col_name: str, to_col_dtype: str) -> None:
        """
        Change column dtype to target dtype
        Args:
            col_name: str, col name that its dtype will be changed
            to_col_dtype: str, target dtype
        Return:
            df: pd.DataFrame
        """
        self.weather.df[col_name] = self.weather.df[col_name].astype(to_col_dtype)

    def remove_duplicated(self) -> None:
        """
        remove duplicated rows
        """
        if self.weather.df.duplicated().sum() > 0:
            self.weather.df = self.weather.df.drop_duplicates()

    def drop_columns(self, cols=None) -> None:
        """
        drop columns that we don't need
        Args:
            cols: list, columns that need be dropped

        Returns:

        """
        if cols and isinstance(cols, list):
            self.weather.df.drop(columns=cols, inplace=True)

    def convert_multilabel_encoding(self, col: str) -> list:
        """
        convert categorical column into numerical column
        Args:
            col: str, encoding column name
        """
        mlb = MultiLabelBinarizer()
        self.convert_string_to_set(col)
        self.weather.df = self.weather.df.join(
            pd.DataFrame(mlb.fit_transform(self.weather.df[col]),
                         columns=mlb.classes_,
                         )
        )
        if col in self.weather.df.columns:
            self.weather.df.drop(columns=[col], inplace=True)

        return mlb.classes_

    def convert_categorical_ohe(self, cols=None) -> None:
        """
        categorical one hot encoding of columns
        Args:
            cols: list, columns applying one hot encoding

        Returns:

        """
        if not cols or not isinstance(cols, list):
            return None
        # outputs array instead of dataframe
        ohe = OneHotEncoder()
        array_hot_encoded = ohe.fit_transform(self.weather.df[cols]).toarray()
        feature_labels = ohe.categories_
        feature_labels = '_' + np.array(feature_labels).ravel()
        data_hot_encoded = pd.DataFrame(array_hot_encoded, columns=feature_labels)
        data_other_cols = self.weather.df.drop(columns=cols)
        self.weather.df = pd.concat([data_hot_encoded, data_other_cols], axis=1)

    def convert_categorical_le(self, cols=None) -> None:
        """
        categorical label encoding of columns
        Args:
            cols: list, columns applying label encoding

        Returns:

        """
        le = LabelEncoder()
        self.weather.df[cols] = self.weather.df[cols].apply(lambda col: le.fit_transform(col))

    def convert_cat2num_infer(self, enc, cols=None) -> None:
        """
        convert categorical column into numerical column
        Args:
            enc: type of encoding used to convert
            cols: list of columns need to be converted
        """
        pass

    def convert_numerical_encoding(self, enc, cols=None) -> None:
        """
        convert numerical columns into normalization or standardization form
        Args:
            enc: function, encoding method
            cols: list, columns get encoded

        Returns:

        """

    def check_missing_values(self) -> pd.DataFrame:
        """

        Returns:
            df: DataFrame with missing values
        """
        return (self.weather.df.isnull().sum()
                .sort_values(ascending=False))

    def remove_col_white_space_l(self, col: str) -> None:
        """
        remove white space at the beginning of string
        Args:
            col: str, column name

        Returns:

        """
        self.weather.df[col] = self.weather.df[col].str.lstrip()

    def remove_col_white_space_r(self, col: str) -> None:
        """
        remove white space at the end of string
        Args:
            col: str, column name

        Returns:

        """
        self.weather.df[col] = self.weather.df[col].str.strip()

    def remove_col_white_space_all(self, col: str) -> None:
        """
        remove all white space
        Args:
            col: str, column name

        Returns:

        """
        self.weather.df[col] = self.weather.df[col].str.replace(' ', '')

    def convert_to_datetime(self, col: str = 'datetime') -> None:
        """
        Convert column to pandas datetime for further processing
        Args:
            col: str, date column in object or string format

        Returns:

        """
        self.weather.df[col] = pd.to_datetime(self.weather.df[col])

    def add_year_month_day_feats(self, col: str = 'datetime') -> None:
        """
        Add year, month, and day features to dataset
        Args:
            col: str, create day features based on this column

        Returns:

        """
        if not pd.api.types.is_datetime64_dtype(self.weather.df.datetime):
            self.convert_to_datetime(col)
        self.weather.df['day'] = self.weather.df[col].dt.day
        self.weather.df['month'] = self.weather.df[col].dt.month
        self.weather.df['year'] = self.weather.df[col].dt.year

    def add_hour_feat(self, col: str = 'datetime') -> None:
        """
        Add hour feature to dataset
        Args:
            col: str, create day features based on this column

        Returns:

        """
        self.weather.df['hour'] = self.weather.df[col].dt.hour

    def add_day_of_week_feat(self, col: str = 'datetime') -> None:
        """
        Add a feature column: day of week
        Args:
            col: str, create day of week based on this column
        Returns:

        """
        self.weather.df['dayofweek'] = self.weather.df[col].dt.dayofweek

    def convert_string_to_set(self, col: str) -> None:
        """
        Convert str column into set by splitting ','
        Args:
            col: str, column name to be proceeded

        Returns:

        """
        self.remove_col_white_space_all(col)
        self.weather.df[col] = self.weather.df[col].apply(lambda x: set(x.split(',')))

    def add_season_feat(self, col: str = 'datetime') -> None:
        """
        Add season feature into dataframe
        Args:
            col: str, column name. create season column based on this column

        Returns:

        """
        # Toronto Seasons format from (month, day) to (month, day)
        spring_s, spring_e = (3, 20), (6, 20)
        summer_s, summer_e = (6, 21), (9, 21)
        fall_s, fall_e = (9, 22), (12, 20)
        # winter_s, winter_e = (12, 21), (3, 19)

        def get_season(dt) -> int:
            # spring = 0, summer = 1, fall = 2, winter = 3
            season, month, day = 0, dt.month, dt.day
            curr_day = (month, day)
            if spring_e <= curr_day <= spring_e:
                season = 0
            elif summer_s <= curr_day <= summer_e:
                season = 1
            elif fall_s <= curr_day <= fall_e:
                season = 2
            else:
                season = 3

            return season

        if not pd.api.types.is_datetime64_dtype(self.weather.df.datetime):
            self.convert_to_datetime(col)
        self.weather.df['season'] = self.weather.df[col].apply(get_season)


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> BaseBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: BaseBuilder) -> None:
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    def build_weather_dataset(self) -> None:
        # 1. remove duplicated
        self.builder.remove_duplicated()
        # 2. handling missing data in preciptype
        # because it is quite similar with conditions
        # just drop this column, 'stations' and 'name' column
        self.builder.drop_columns(['preciptype', 'name', 'stations'])
        # 3. change datetime column dtypes
        self.builder.convert_to_datetime('datetime')
        # 4. Convert categorical variable to numerical variable
        self.builder.convert_multilabel_encoding('conditions')
        self.builder.convert_categorical_ohe(['icon'])
        # 5. create time series features based on datetime
        self.builder.add_year_month_day_feats('datetime')
        self.builder.add_day_of_week_feat('datetime')
        self.builder.add_hour_feat('datetime')
        self.builder.add_season_feat('datetime')
