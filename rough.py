# {'itemname': 'Acer Aspire 7 (2023) Intel Core i5 12th Gen 12450H - (16 GB/512 GB SSD/Windows 11 Home/4 GB Graphics/NVIDIA GeForce RTX 3050/144 Hz) A715-76G Gaming Laptop', 'quantity': 1, 'price': 50990.0}







from slider_value import get_value




def decide(str1, str2):
    val1 = None
    x1 = None
    x2 = None
    val2 = None

    # Extract item name
    start = str1.find("'itemname': '") + len("'itemname': '")
    end = str1.find("', 'quantity'")
    item = str1[start:end]

    # Extract bought price
    for x in str1.split(" "):
        if x == "'price':":
            var = (str1.split(" ")[str1.split(" ").index(x) + 1])
            val1 = float(var[0:(len(var) - 1)])

    # Extract market min/max
    for x in str2.split(" "):
        if x == "'min':":
            var = (str2.split(" ")[str2.split(" ").index(x) + 1])
            x1 = float(var[0:(len(var) - 1)])
        if x == "'max':":
            var = (str2.split(" ")[str2.split(" ").index(x) + 1])
            x2 = float(var[0:(len(var))])

    # Average market price
    val2 = (x1 + x2) / 2
    result = None

    # print(item)
    # print(val1, val2)

    if val1 <= val2:
        result = "The products are decently priced"
    else:
        chg = val1 - val2
        calc = int((chg / val2) * 100)
        result = f"The products are {calc}% more expensive than the average price"

        if (get_value() != None and calc <= get_value()):
            result = "The products are priced within the accepted range"
        else:
            result = "The products are priced outside the accepted range, extremely overpriced!!! 🤷‍♂️"

    return(item+result)


if __name__ == "__main__":

    str1="{'itemname': 'Acer Aspire 7 (2023) Intel Core i5 12th Gen 12450H - (16 GB/512 GB SSD/Windows 11 Home/4 GB Graphics/NVIDIA GeForce RTX 3050/144 Hz) A715-76G Gaming Laptop', 'quantity': 1, 'price': 150990.0}"
    str2="'min': 70427, 'max': 70990"

    decide(str1, str2)