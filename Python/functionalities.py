import pandas as pd
from sqlalchemy import create_engine


class FunctionAdministrator:

    def __init__(self, csv_source):
      
        self._functions = []

        try:
            self._data_of_function = pd.read_csv(csv_source)
        except FileNotFoundError:
            print("error when reading the file")
            raise

    # X is independent var
        x_s = self._data_of_function["x"]

      
        for column_name, column_data in self._data_of_function.items():
            if "x" in column_name:
                continue
            # With the x column already stored, we can now use the concat function to combine it with the y column.
            sub_group = pd.concat([x_s, column_data], axis=1)
            combine_function = Function.within_framedata(column_name, sub_group)
            self._functions.append(combine_function)

    def to_sql(self, name_of_file, suffix):
         #Local Sqlite required
      
        enginedb = create_engine('sqlite:///{}.db'.format(name_of_file), echo=False)

        # To conform with the given suffix, the columns are renamed, and the first column is set as the index.
        func_copy_data = self._data_of_function.copy()
        func_copy_data.columns = [name.capitalize() + suffix for name in func_copy_data.columns]
        func_copy_data.set_index(func_copy_data.columns[0], inplace=True)

         
        func_copy_data.to_sql(name=name_of_file, con=enginedb, if_exists="replace", index=True)

    @property
    def functions(self):
   
        return self._functions

    def __iter__(self):
        # This enables the object to be iterated.
        return FunctionAdministratorRepeater(self)

    def __repr__(self):
        return "here are {} alot of functionalities ".format(len(self.functions))


class FunctionAdministratorRepeater():

    def __init__(self, func_mngr):
    
        # This has been used for the iteration of a FunctionAdministrator.
        self._index = 0
        self._func_mngr = func_mngr

    def __next__(self):
    
        try:
            ordered_value = self._func_mngr.functions[self._index]
            self._index += 1
        except IndexError:
            raise StopIteration
        else:
            return ordered_value


class Function:

    def __init__(self, name):
        self._name, self.dataframe = name, pd.DataFrame()

    def find_y_by_x(self, x):
      
      
        try:
            return self.dataframe.loc[self.dataframe["x"] == x].iat[0, 1]
        except IndexError:
            raise IndexError

    @property
    def name(self):
        return self._name

    def __iter__(self):
        return FunctionRepeater(self)

    def __sub__(self, other):
 
        return self.dataframe.sub(other.dataframe)

    @classmethod
    def within_framedata(cls, names, framedata):
        """
        During the creation process of a function, the original column names are replaced with "x" and "y",
        and it is initiated by providing a dataframe.
        :rtype: returns function
        """
        df_func = cls(names)
        df_func.dataframe = framedata
        df_func.dataframe.columns = ["x", "y"]
        return df_func

    def __repr__(self):
        return "functions for the {}".format(self.name)


class IdealFunction(Function):
    def __init__(self, function, trn_func, error):
        super().__init__(function.name)
        self.dataframe = function.dataframe

        self.training_function = trn_func
        self.error = error
        self._tolerance_value = 1
        self._tolerance = 1

    def _determining_biggest_dev(self, ideal_fuction, trn_func):
        # This function takes two input functions and returns a new function which is the subtraction of the two input functions.
        # It searches for the largest value from the resulting dataframe.
       #A is stand for area
        a = trn_func - ideal_fuction
        a["y"] = a["y"].abs()
        biggest_dev = max(a["y"])
        return biggest_dev

    @property
    def tolerance(self):

        self._tolerance = self.tolerance_factor * self.biggest_dev
        return self._tolerance

    @tolerance.setter
    def tolerance(self, values):
        self._tolerance = values

    @property
    def tolerance_factor(self):

        return self._tolerance_value

    @tolerance_factor.setter
    def tolerance_factor(self, value):
        self._tolerance_value = value

    @property
    def biggest_dev(self):
 
        biggest_dev = self._determining_biggest_dev(self, self.training_function)
        return biggest_dev


class FunctionRepeater:

    def __init__(self, func):
        # If a function is iterated over, a dictionary is returned that provides a description of the point..
        self._function = func
        self._index = 0

    def __next__(self):
        # It returns a dictionary that describes the point when iterating over a function.
        if self._index < len(self._function.dataframe):
            ordered_chain_values = (self._function.dataframe.iloc[self._index])
            mark = {"x": ordered_chain_values.x, "y": ordered_chain_values.y}
            self._index += 1
            return mark
        raise StopIteration
