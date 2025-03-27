from functionalities import IdealFunction


def loss_minimisation(trn_func, competitor_functions_list, func_loss):

#This function generates an IdealFunction object using a training function, an ideal function input, and a list of candidate functions.


    minimum_error = None
    idl_func = None
    for function in competitor_functions_list:
        minimized_errors = func_loss(trn_func, function)
        if minimum_error is None or minimized_errors < minimum_error:
            minimum_error = minimized_errors
            idl_func = IdealFunction(function=function, trn_func=trn_func, error=minimized_errors)

    return idl_func


def classification_search(point, idl_funcs):
 
    minimum_classification = None
    minimum_gap = None

    for idl_func in idl_funcs:
        try:
            classification_locates_y = idl_func.find_y_by_x(point["x"])
        except IndexError:
            print("This point is not included in the function of the classification.")
            raise IndexError

        # In this section, please note the use of absolute distance.
        gap = abs(classification_locates_y - point["y"])

        if (abs(gap < idl_func.tolerance)):
            # The following method ensures proper handling in case multiple classifications are possible
            # returns the one with the lowest distance.
            if ((minimum_classification == None) or (gap < minimum_gap)):
                minimum_classification = idl_func
                minimum_gap = gap

    return minimum_classification, minimum_gap



 # calculating square error and deviations
def calculate_mean_squarederror(region1, region2):
## compute the squared error using independent function
    differences = region2 - region1
    differences["y"] = differences["y"] ** 2
    dev = sum(differences["y"])
    return dev
