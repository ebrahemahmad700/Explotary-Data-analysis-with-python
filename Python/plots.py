from bokeh.layouts import column
from bokeh.models import Band, ColumnDataSource
from bokeh.plotting import figure, show, output_file
import operator


def ideal_plots(ideal_functions, file_name):

#ploting all of the ideal plot and showing it in html file
  

    # sort the Ideal Fucntions list based on the 'training_function.name' attribute
    ideal_functions.sort(key=operator.attrgetter('training_function.name'), reverse=False)
    # empty array to all of the plot inside 
    all_plts = []
    for idl_func in ideal_functions:
        plts = plot_train_Ideal(function_line=idl_func, function_sctr=idl_func.training_function,
                                            Squrate_error_result=idl_func.error)
#appending all of the plot to the empty array the we made
        all_plts.append(plts)
    output_file(" {}.html".format(file_name))
    # Notice how the unpacking technique is utilized here to supply arguments.
    show(column(*all_plts))


def plot_point(classification_points, file_name):
    
   # every point which equvallent to classification should be determine

    plts = [classification_plot(component["point"], component["classification"]) for component in classification_points
            if component["classification"] is not None]
    output_file(f"{file_name}.html")
    show(column(*plts))


def plot_train_Ideal(function_sctr,function_line,Squrate_error_result):
    
  #For the Train Function, the code makes a scatter plot and for the Ideal Fucntion, it makes a line plot.
  
    func1_dataframe = function_sctr.dataframe
    func1_name = function_sctr.name

    func2_dataframe = function_line.dataframe
    func2_name = function_line.name

    Squrate_error_result = round(Squrate_error_result, 2)
    plts = figure(
        title="The train model: exemplary {} vs. ideal {}. Sum of Squared Error = {}.".format(func1_name, func2_name,
                                                                                         Squrate_error_result),
        x_axis_label='x', y_axis_label='y')
    plts.scatter(func1_dataframe["x"], func1_dataframe["y"], fill_color="#D3544D", legend_label="Train",
                 line_color="#eb3b5a")
    plts.line(func2_dataframe["x"], func2_dataframe["y"], legend_label="Ideal", line_color="#12A8A2", line_width=2)

    return plts


def classification_plot(marks, ideal_function):
    """
 This code generates a visualization that shows both the function of the classification and a point overlaid on top.
This code generates a visualization that displays the classification function along with an overlaid point.
Additionally, it indicates the tolerance.
Parameters:
marks: A dictionary with the keys "x" and "y".
  """
    if ideal_function is not None:
        classification_function_framedata = ideal_function.dataframe

        string_mark = "({},{})".format(marks["x"], round(marks["y"], 2))
        header_name = "points {}  with classifications: {}".format(string_mark, ideal_function.name)

        plt = figure(title=header_name, x_axis_label='x', y_axis_label='y')

        # show one ideal function
        plt.line(classification_function_framedata["x"], classification_function_framedata["y"],
                 legend_label="Function of Classification", line_width=2, line_color='black')

        # Develop a method to display the tolerance range within the graph.
        view_tolerance_on_graph = ideal_function.tolerance
        classification_function_framedata['upper'] = classification_function_framedata['y'] + view_tolerance_on_graph
        classification_function_framedata['lower'] = classification_function_framedata['y'] - view_tolerance_on_graph

        src = ColumnDataSource(classification_function_framedata.reset_index())

        line = Band(level='underlay', upper='upper', lower='lower', source=src, base='x',
                    fill_alpha=0.5, line_width=1, line_color='#26A65B', fill_color="#29B765")

        plt.add_layout(line)

        # Implement a function to plot the point.
        plt.scatter([marks["x"]], [round(marks["y"], 4)], legend_label="Test point", fill_color="red", size=8)

        return plt
