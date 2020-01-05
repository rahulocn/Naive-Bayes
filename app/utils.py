def splitter(str_line, sep=","):
    return str_line.strip().split(sep)


def get_probability(favourable_outcomes, total_possible_outcomes):
    if type(favourable_outcomes) is int and type(
            total_possible_outcomes) is int and favourable_outcomes > -1 and total_possible_outcomes > 0 and favourable_outcomes <= total_possible_outcomes:
        return float(favourable_outcomes) / float(total_possible_outcomes)
    else:
        raise ValueError("Probability outcomes are always positive integers.Please Check input.")


def get_probability_percentage(probability):
    if type(probability) is float and probability >= 0:
        return probability * 100
    else:
        raise ValueError("Probabilities are always non-negative floats")


def read_csv_to_list(csv_file_path):
    pass


if __name__ == "__main__":
    splitter("foo:bar:voo:doo", ":")
    p = get_probability(2, 11)
    get_probability_percentage(p)
