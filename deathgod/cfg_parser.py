""" Some functions for parsing simple attribute/value cfg files """

COMMENT = '#'

def tokenize_file(fileName, delimiter=None):
    values = {}
    try:
        infile = open(fileName)
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
                finalVal = convert_str(words[1])
                # add string and value to our lists if we made it through the previous mine field
                #attributes.append(words[0])
                values[words[0]] = finalVal
        finally:
            infile.close()
            # print("after tokenizeFile:")
            # print("values = %s" % str(values))
            # print("attributes = %s" % str(attributes))
    except IOError:
        print("in tokenize_file: Can't open %s" % fileName)
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

def parse_and_apply(cfg_file, targetObject, typesafe=False, delimiter=None):
    try:
        values = parse(cfg_file, delimiter)
    except IOError:
        raise
    #print "starting parse_and_apply:"
    #print "values = %s" % str(values)
    #print "attributes = %s" % str(attributes)
    for targetAttributeName in list(values.keys()):
        val = values[targetAttributeName]
        #print "val = %s" % str(val)
        valType = type(val)
        try:
            targetType = type(getattr(targetObject, targetAttributeName))
        except AttributeError:
            #print "in parse_and_apply: member not found, attempting to create"
            setattr(targetObject, targetAttributeName, val)
            targetType = None
        # skip the attribute if the variable type from file doesn't match variable type in object
        if typesafe == True and targetType != valType and targetType is not None:
            print("in parse_and_apply: failed to set %s to %s due to typesafe" % \
             (targetAttributeName, str(val)))
            continue
        setattr(targetObject, targetAttributeName, val)
        #print "in parse_and_apply: set %s to %s" % \
        #     (targetAttributeName, str(getattr(targetObject, targetAttributeName)))

def convert_str(s):
    """Convert string to either int or float or string."""
    try:
        ret = int(s)
    except ValueError:
        # try float.
        try:
            ret = float(s)
        except ValueError:
            ret = s
    return ret

if __name__ == "__main__":
    #print __doc__
    testFileName = "testfile.cfg"
    #import settings
    class TestClass:
        intVar1 = 0
        stringVar1 = "foo"
        floatVar1 = 0.0
    print("testing parse_and_apply on TestClass with %s" % testFileName)
    try:
        parse_and_apply(testFileName, TestClass, True)
        #print "intVar1 = %s" % str(TestClass.intVar1)
        #print "stringVar1 = %s" % str(TestClass.stringVar1)
        #print "floatVar1 = %s" % str(TestClass.floatVar1)
        #print "wild = %s" % str(TestClass.wild)
    except IOError:
        "whoo screwed up"


