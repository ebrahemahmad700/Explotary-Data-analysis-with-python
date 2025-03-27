from sqlalchemy import MetaData, Column, Table, Float, String, create_engine


def sqlite_store_deviation_result(outcome):
    """
  This function saves the results of a classification calculation to a SQLite database while adhering to the assignment requirements.
:param result: A list containing a dictionary that details the test results of a classification evaluation.
  """
    # This function utilizes a native SQLAlchemy method instead of using SQL syntax.
    # It uses MetaData to define the table and its columns instead, which is then used by SQLAlchemy to generate the table.

    sqt_eng = create_engine('sqlite:///{}.db'.format("mapping"), echo=False)
    sqt_metadata = MetaData(sqt_eng)

    exc_mapping = Table('mapping', sqt_metadata,
                            Column('X (test func)', Float, primary_key=False),
                            Column('Y (test func)', Float),
                            Column('Delta Y (test func)', Float),
                            Column('No. of ideal func', String(50))
                            )

    sqt_metadata.create_all()
    

    # To enhance performance, this code avoids inserting values one by one and instead utilizes SQLAlchemy's batch processing capabilities.
    # Utilizes the execute method with a dictionary that holds all the required values.
    # This dictionary is created by transforming the internal data structures to match the required format for the assignment.

    run_the_mapping = []
    for compontents in outcome:
        mark = compontents["point"]
        classifications = compontents["classification"]
        y_dlt = compontents["delta_y"]

      

        classification_name = None
        if classifications is not None:
            classification_name = classifications.name.replace("y", "N")
        else:
            # When there is no classification available, the distance cannot be computed
            classification_name = "_____"
            y_delta = -1

        run_the_mapping.append(
            {"X (test func)": mark["x"], "Y (test func)": mark["y"], "Delta Y (test func)": y_dlt,
             "Number of ideal functions ": classification_name})

    # insert data.
    da_ent = exc_mapping.insert()
    da_ent.execute(run_the_mapping)
