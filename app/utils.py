def splitter(str_line, sep=","):
    return str_line.strip().split(sep)


def get_probability(favourable_outcomes, total_possible_outcomes):
    if type(favourable_outcomes) is int or float and type(
            total_possible_outcomes) is int or float and favourable_outcomes > -1 and total_possible_outcomes > 0 and favourable_outcomes <= total_possible_outcomes:
        return float(favourable_outcomes) / float(total_possible_outcomes)
    else:
        raise ValueError("Probability outcomes are always positive integers.Please Check input.")

def csv_to_generator(csv_file_path):
    with open(csv_file_path,"r") as csv:
        for line in csv:
            yield line
        return



if __name__ == "__main__":
    print(splitter("foo:bar:voo:doo", ":"))
    print(get_probability(2, 11))

