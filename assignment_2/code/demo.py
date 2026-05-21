
# The main Bayesian Network
from pgmpy.models import DiscreteBayesianNetwork
# The Conditional Probability Tables
from pgmpy.factors.discrete import TabularCPD
# Inference
from pgmpy.inference import VariableElimination

def main():
    # Implementation of the burglary/earthquake/alarm network example

    # Defining the Network, with connections as tuples of the form:
    # (Independent, Dependent)
    # model = DiscreteBayesianNetwork([
    #     ("Burglary", "Alarm"),
    #     ("Earthquake", "Alarm"),
    #     ("Alarm", "JohnCalls"),
    #     ("Alarm", "MaryCalls"),
    # ])

    model = DiscreteBayesianNetwork([
        ("veggie", "burger"),
        ("bread", "burger"),
        ("late-work", "late-dinner"),
        ("burger", "pizza-for-dinner"),
        ("late-dinner", "pizza-for-dinner"),
    ])

    # The Conditional Probability Distributions for the Independent Variables
    # These simply have two cases each: [Prob. False, Prob. True]
    # cpd_burglary = TabularCPD("Burglary", 2, [[0.999], [0.001]])
    # cpd_earthquake = TabularCPD("Earthquake", 2, [[0.998], [0.002]])

    cpd_veggie= TabularCPD("veggie", 2, [[0.7], [0.3]])
    cpd_bread = TabularCPD("bread", 2, [[0.5], [0.5]])
    cpd_late_work = TabularCPD("late-work", 2, [[0.65], [0.35]])

    # Alarm conditionally depends on two variables: Burglary and Earthquake
    # The ordering of evidence is given by the line:
    #      evidence = ["Burglary", "Earthquake"]
    # So, that determines the order used to read the values
    # Then, values[0] is :
    #   P( NOT burger | NOT veggie and NOT bread) = 0.999
    #   P( NOT burger | NOT veggie and bread) = 0.71
    #   P( NOT burger | veggie and NOT bread) = 0.06
    #   P( NOT burger | veggie and bread) = 0.05
    cpd_burger = TabularCPD(
        "burger", 2,
        values=[
            [0.95, 0.55, 0.8, 0.2],  # P(burder=False | B,E)
            [0.05, 0.45, 0.2, 0.8],  # P(burder=True  | B,E)
        ],
        evidence=["veggie", "bread"],
        evidence_card=[2, 2],
    )

    cpd_late_dinner = TabularCPD(
        "late-dinner", 2,
        values=[
            [0.88, 0.05],   # P(late-dinner=False | A )
            [0.12, 0.95],   # P(late-dinner=True | A ) false , true
        ],
        evidence=["late-work"],
        evidence_card=[2],
    )

    cpd_pizza_for_dinner = TabularCPD(
        "pizza-for-dinner", 2,
        values=[
            [0.96, 0.03, 0.99, 0.94],  # P(burder=False | B,E)
            [0.04, 0.97, 0.01, 0.06],  # P(burder=True  | B,E)
        ],
        evidence=["burger", "late-dinner"],
        evidence_card=[2, 2],
    )


    # add the CDPs to the model
    model.add_cpds(
        cpd_veggie,
        cpd_bread,
    cpd_late_work,
    cpd_burger,
    cpd_late_dinner,
    cpd_pizza_for_dinner
    )

    # Validate the model ...
    print(model.check_model())

    # create the object that can do probabilistic inference
    infer = VariableElimination(model)

    # run a query:
    #     P( Burglary | JohnCalls=True, MaryCalls=True)
    # Note that unlike the simple examples seen in class, this one requires marginalization
    # over the unobserved variables: Earthquake and Alarm.
    # result = infer.query(
    #     variables=["Burglary"],
    #     evidence={"JohnCalls": 1, "MaryCalls": 1}
    # )

    # P( pizza-for-dinner | burger)
    result_1 = infer.query(
        variables=["pizza-for-dinner"],
        evidence={"burger": 1, }
    )

    print(result_1)

    # P( burger | pizza-for-dinner)
    result_2 = infer.query(
        variables=["burger"],
        evidence={"pizza-for-dinner": 1, }
    )

    print(result_2)

    # P( work-late | not pizza-for-dinner)
    result_3 = infer.query(
        variables=["late-work"],
        evidence={"pizza-for-dinner": 0, }
    )

    print(result_3)

    # P( Veggies | Late dinner.)
    result_4 = infer.query(
        variables=["veggie"],
        evidence={"late-dinner": 1}
    )

    print(result_4)


if __name__ == "__main__":
    main()
