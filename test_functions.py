import FindMaxDate


def test_find_max_date():
    table = r"C:\DiskTemp\Innspill\Innspill.gdb\Innspill"
    field = "CreationDate"
    return FindMaxDate.find_newest_date(table, field)


print(test_find_max_date())

