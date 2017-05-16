""" Some functions for parsing simple attribute/value cfg files """

COMMENT = '#'

def tokenize_file(file_name, delimiter=None):
    """tokenize file_name. returns a dict of key/value pairs."""
    values = {}
    try:
        infile = open(file_name)
        try:
            i = 0
            for line in infile:
                i = i + 1
                #print "read line %d: %s" % (i, line[:-1])
                # check for comment
                if line[0:1] == COMMENT:
                    #print "skipping comment on line %d" % i
                    continue
                # split the line
                words = line.split(delimiter)
                #print "got words: %s" % str(words)
                # make sure the amount of items on the line is valid
                if len(words) != 2:
                    #print "in tokenize_file: got wrong number of items in line %d, skipping" % i
                    continue
                # convert every second word to an int or float if possible
                final_val = convert_str(words[1])
                # add string and value to our lists if we made it through the previous mine field
                #attributes.append(words[0])
                values[words[0]] = final_val
        finally:
            infile.close()
            # print("after tokenizeFile:")
            # print("values = %s" % str(values))
            # print("attributes = %s" % str(attributes))
    except IOError:
        print("in tokenize_file: Can't open %s" % file_name)
        raise

    return values


def parse(cfg_file, delimiter=None):
    """ Parse the lines of a cfg file
    Returns a dictionary of all the values found"""
    try:
        values = tokenize_file(cfg_file, delimiter)
    except IOError:
        raise

    return values


def parse_and_apply(cfg_file, target_object, typesafe=False, delimiter=None):
    """Parse cfg_file and try to assign its key/value pairs to an object dynamically."""
    try:
        values = parse(cfg_file, delimiter)
    except IOError:
        raise
    #print "starting parse_and_apply:"
    #print "values = %s" % str(values)
    #print "attributes = %s" % str(attributes)
    for target_attr_name in list(values.keys()):
        val = values[target_attr_name]
        #print "val = %s" % str(val)
        val_type = type(val)
        try:
            target_type = type(getattr(target_object, target_attr_name))
        except AttributeError:
            #print "in parse_and_apply: member not found, attempting to create"
            setattr(target_object, target_attr_name, val)
            target_type = None
        # skip the attribute if the variable type from file doesn't match variable type in object
        if typesafe is True and target_type != val_type and target_type is not None:
            print("in parse_and_apply: failed to set %s to %s due to typesafe" % \
             (target_attr_name, str(val)))
            continue
        setattr(target_object, target_attr_name, val)
        #print "in parse_and_apply: set %s to %s" % \
        #     (targetAttributeName, str(getattr(targetObject, targetAttributeName)))


def convert_str(input_str):
    """Try to convert string to either int or float, returning the original string if this fails."""
    try:
        ret = int(input_str)
    except ValueError:
        # try float.
        try:
            ret = float(input_str)
        except ValueError:
            ret = input_str
    return ret


def test():
    """Test the parse_and_apply function."""
    #print __doc__
    test_file_name = "testfile.cfg"
    #import settings
    class TestClass:
        """test class"""
        int_var_1 = 0
        string_var_1 = "foo"
        float_var_1 = 0.0

    print("testing parse_and_apply on TestClass with %s" % test_file_name)
    parse_and_apply(test_file_name, TestClass, True)
    #print "int_var_1 = %s" % str(TestClass.int_var_1)
    #print "string_var_1 = %s" % str(TestClass.string_var_1)
    #print "float_var_1 = %s" % str(TestClass.float_var_1)
    #print "wild = %s" % str(TestClass.wild)


if __name__ == "__main__":
    test()


